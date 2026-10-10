"""Renderiza los fondos (public/plates.mp4) y la capa de cristales (public/crystals.mp4).

Lee src/data/plates.json (generado por scripts/plates_edl.py). Cada frame de salida sale
de los frames del original: espejado, zoom/rotación/punch-in, cámara lenta con mezcla de
frames, escalado 576x1024 -> 1080x1920 con lanczos, unsharp y el look B/N unificado.

uso: python scripts/build_plates.py [--only plates|crystals] [--frames a:b --png dir]
"""
import json
import math
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
W, H = 1080, 1920
SW, SH = 576, 1024
BASE = W / SW  # 1.875, igual en alto

EDL = json.loads((ROOT / "src/data/plates.json").read_text())
FPS, TOTAL = EDL["fps"], EDL["total"]


def frame_map():
    times = [float(x) for x in (ROOT / "analysis/frame_times.txt").read_text().split()]
    m = {round(t * FPS): i + 1 for i, t in enumerate(times)}
    for n in range(657):
        if n not in m:
            m[n] = m[n - 1]
    return m


FMAP = frame_map()


@lru_cache(maxsize=96)
def src_frame(n):
    n = int(min(max(n, 0), 656))
    return cv2.imread(str(ROOT / f"analysis/frames/f{FMAP[n]:04d}.png"), cv2.IMREAD_GRAYSCALE)


def ghost_clean(g, strong):
    """Borra los contornos tenues del texto viejo (MADERO TANGO) del lado izquierdo.

    Mediana fuerte solo en la zona de los fantasmas y fuera de los trazos blancos de los
    doodles, mezclada con máscara suave.
    """
    h, w = g.shape
    reg = np.zeros((h, w), np.float32)
    reg[int(0.25 * h) : int(0.82 * h), : int(0.66 * w)] = 1
    reg = cv2.GaussianBlur(reg, (0, 0), 12)
    bright = cv2.dilate((g > 200).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    bright = cv2.GaussianBlur(bright.astype(np.float32), (0, 0), 2)
    med = cv2.medianBlur(g, 13 if strong else 9)
    med = cv2.GaussianBlur(med, (0, 0), 1.5)
    wgt = reg * (1 - bright)
    return (g * (1 - wgt) + med * wgt).astype(np.uint8)


def sample(pos, ghosts=False, ghost_strong=False):
    """Frame de la fuente en una posición fraccionaria (mezcla lineal entre vecinos)."""
    a = math.floor(pos + 1e-6)
    f = pos - a
    fa = src_frame(a)
    if ghosts:
        fa = ghost_clean(fa, ghost_strong)
    if f < 0.02:
        return fa.astype(np.float32)
    fb = src_frame(a + 1)
    if ghosts:
        fb = ghost_clean(fb, ghost_strong)
    return fa.astype(np.float32) * (1 - f) + fb.astype(np.float32) * f


def ease_out(x):
    return 1 - (1 - x) ** 3


def warp(img, zoom, center, rotate, mirror):
    if mirror:
        img = img[:, ::-1]
    s = BASE * zoom
    cx, cy = center[0] * SW, center[1] * SH
    # que la ventana visible no se salga de la fuente
    hw, hh = (W / 2) / s, (H / 2) / s
    cx = min(max(cx, hw), SW - hw)
    cy = min(max(cy, hh), SH - hh)
    th = math.radians(rotate)
    c, sn = math.cos(th) * s, math.sin(th) * s
    m = np.array([[c, -sn, W / 2 - (c * cx - sn * cy)], [sn, c, H / 2 - (sn * cx + c * cy)]], np.float32)
    return cv2.warpAffine(np.ascontiguousarray(img), m, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)


# Look: B/N, contraste alto, negros aplastados, blancos que queman.
_x = np.linspace(0, 1, 256)
_x = np.clip((_x - 0.035) / (0.95 - 0.035), 0, 1)
_g = 1.3
LUT = (_x**_g / (_x**_g + (1 - _x) ** _g) * 255).astype(np.float32)


def grade(img):
    img = np.clip(img, 0, 255)
    blur = cv2.GaussianBlur(img, (0, 0), 1.3)
    img = np.clip(img * 1.55 - blur * 0.55, 0, 255)  # unsharp suave
    return LUT[img.astype(np.uint8)]


def plate_frame(n):
    seg = next(s for s in EDL["segments"] if s["out"][0] <= n < s["out"][1])
    shot = seg["shot"]
    if shot == "black":
        return np.zeros((H, W), np.float32)
    o0, o1 = seg["out"]
    k = n - o0
    L = o1 - o0
    speed = seg.get("speed", 1.0)
    if seg.get("path") == "pingpong":
        x = k * 0.5
        span = 3
        pos = seg["src"] + (span - abs(span - (x % (2 * span))))
    else:
        pos = seg["src"] + k * speed
    strong = n >= 344
    img = sample(pos, seg.get("ghosts", False), strong)
    z0, z1 = seg.get("zoom", [1.0, 1.0])
    u = k / max(1, L - 1)
    zoom = z0 + (z1 - z0) * u
    if seg.get("punch"):
        zoom *= 1 + 0.06 * ease_out(min(1.0, k / 4))
    out = warp(img, zoom, seg.get("center", [0.5, 0.5]), seg.get("rotate", 0), seg.get("mirror", False))
    out = grade(out * seg.get("gain", 1.0))
    if seg.get("smear"):
        ln = 90 if k == 0 else 220
        ker = np.ones((ln, 1), np.float32) / ln
        out = cv2.filter2D(out, -1, ker, borderType=cv2.BORDER_REFLECT)
        out = cv2.addWeighted(out, 0.85, np.full_like(out, 255), 0.15 * k, 0)
    return out


# ---------------------------------------------------------------- cristales
def crystal_frame(n):
    cl = EDL["crystalsClear"]
    if cl["out"][0] <= n < cl["out"][1]:
        u = (n - cl["out"][0] + 1) / (cl["out"][1] - cl["out"][0])
        base = crystal_frame(cl["hold"])
        dy = int(cl["drop"] * H * ease_out(u) ** 1.0)
        out = np.zeros_like(base)
        out[dy:] = base[: H - dy]
        return out * (1 - u) ** 1.5
    acc = np.zeros((H, W), np.float32)
    for inst in EDL["crystals"]:
        o0, o1 = inst["out"]
        if not (o0 <= n < o1):
            continue
        k = n - o0
        pos = inst["src"] + k * inst["speed"]
        if pos > 16:
            continue
        img = sample(min(pos, 16))
        img = np.clip((img - 6) * 1.1, 0, 255)  # negro limpio alrededor
        z0, z1 = inst.get("zoom", [1, 1])
        zoom = z0 + (z1 - z0) * (k / max(1, o1 - o0 - 1))
        c = inst.get("center", [0.5, 0.5])
        dy = inst.get("dy", [0, 0])
        ddy = dy[0] + (dy[1] - dy[0]) * (k / max(1, o1 - o0 - 1))
        layer = warp_free(img, zoom, c, inst.get("mirror", False), ddy)
        op = inst.get("opacity", 1.0)
        fade = inst.get("fadeOut")
        if fade and n >= o1 - fade:
            op *= (o1 - n) / fade
        layer = layer * op / 255
        acc = 1 - (1 - acc) * (1 - layer)  # screen
    return acc * 255


def warp_free(img, zoom, center, mirror, dy):
    """Como warp, pero sin forzar a cubrir el cuadro (borde negro) y con desplazamiento vertical."""
    if mirror:
        img = img[:, ::-1]
    s = BASE * zoom
    cx, cy = center[0] * SW, center[1] * SH
    m = np.array([[s, 0, W / 2 - s * cx], [0, s, H / 2 - s * cy + dy * H]], np.float32)
    return cv2.warpAffine(np.ascontiguousarray(img), m, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


def encode(path, gen, frames):
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "10", "-g", "15", "-bf", "0", "-pix_fmt", "yuv420p",
           "-color_range", "tv", "-movflags", "+faststart", str(path)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in frames:
        p.stdin.write(np.clip(gen(n), 0, 255).astype(np.uint8).tobytes())
        if n % 100 == 0:
            print(path.name, n, flush=True)
    p.stdin.close()
    if p.wait():
        sys.exit(f"ffmpeg falló con {path}")


def main():
    args = sys.argv[1:]
    only = args[args.index("--only") + 1] if "--only" in args else None
    if "--frames" in args:  # previsualizar frames sueltos a PNG
        a, b = map(int, args[args.index("--frames") + 1].split(":"))
        d = Path(args[args.index("--png") + 1])
        d.mkdir(parents=True, exist_ok=True)
        gen = crystal_frame if only == "crystals" else plate_frame
        for n in range(a, b):
            cv2.imwrite(str(d / f"p{n:04d}.png"), np.clip(gen(n), 0, 255).astype(np.uint8))
        return
    pub = ROOT / "public"
    pub.mkdir(exist_ok=True)
    if only in (None, "plates"):
        encode(pub / "plates.mp4", plate_frame, range(TOTAL))
    if only in (None, "crystals"):
        encode(pub / "crystals.mp4", crystal_frame, range(TOTAL))


if __name__ == "__main__":
    main()
