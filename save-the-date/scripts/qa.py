"""QA del render final.

uso: python scripts/qa.py <video_final.mp4>

Genera en qa/:
  side_by_side.mp4         original | nuevo, ambos a 1080x1920
  sheets/<bloque>.jpg      comparativas cada 0,125 s por bloque
  tilde.jpg                recortes de la Í en los bloques A y D (cada paso del flip) y en la franja
  ocr_final.json           OCR de todos los frames del render
  qa_report.json           procedencia de los fondos, cortes vs. original y beats, repetición de planos
"""
import json
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
QA = ROOT / "qa"
VIDEO = Path(sys.argv[1])
EDL = json.loads((ROOT / "src/data/plates.json").read_text())
FPS = EDL["fps"]


def run(cmd):
    subprocess.run(cmd, check=True)


def side_by_side():
    out = QA / "side_by_side.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "input/original.mp4"), "-i", str(VIDEO), "-filter_complex",
         "[0:v]fps=30,scale=1080:1920:flags=lanczos,setsar=1,tpad=stop_mode=add:stop_duration=2:color=black[a];"
         "[1:v]setsar=1[b];[a][b]hstack=inputs=2,trim=duration=23.6[v]",
         "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "160k", "-shortest", str(out)])
    return str(out)


def extract_frames():
    d = QA / "final_frames"
    d.mkdir(parents=True, exist_ok=True)
    for f in d.glob("*.jpg"):
        f.unlink()
    run(["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO), "-vsync", "0", "-q:v", "2", str(d / "n%04d.jpg")])
    return sorted(d.glob("*.jpg"))


BLOCKS = {
    "1_intro": (0.0, 0.7), "A_save_the_date": (0.7, 3.8), "3-5_limpio": (3.8, 7.2), "B_fecha": (7.2, 10.2),
    "7_doodles_preroll": (10.2, 11.95), "C_salon": (11.95, 13.9), "9_limpio": (13.9, 16.43),
    "D_cromado": (16.43, 19.37), "11_leak": (19.37, 19.75), "E_monograma": (19.75, 21.9), "F_placa": (21.9, 23.6),
}


def sheets():
    d = QA / "sheets"
    d.mkdir(exist_ok=True)
    out = []
    for name, (a, b) in BLOCKS.items():
        frames = sorted({min(707, round(t * FPS)) for t in np.arange(a, b, 0.125)})
        p = d / f"{name}.jpg"
        run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/compare.py"), str(QA / "final_frames_png"), str(p),
             *map(str, frames), "--w", "160", "--cols", "6"])
        out.append(str(p))
    return out


def tilde(frames):
    """Recortes del nombre: bloque A, cada paso del flip de la Í, la franja y la portada."""
    picks = [0, 27, 50, 80, 110] + list(range(505, 517)) + [530, 548, 552, 560, 578]
    tiles = []
    for n in picks:
        im = cv2.imread(str(frames[n]))
        y0, y1 = (820, 1180) if 0 < n < 120 else (560, 1240)
        crop = im[y0:y1, 140:940]
        crop = cv2.resize(crop, (400, round(400 * crop.shape[0] / crop.shape[1])))
        crop = cv2.copyMakeBorder(crop, 22, 0, 0, 0, cv2.BORDER_CONSTANT, value=(40, 40, 40))
        cv2.putText(crop, f"#{n} {n / FPS:.2f}s", (6, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        tiles.append(crop)
    h = max(t.shape[0] for t in tiles)
    tiles = [cv2.copyMakeBorder(t, 0, h - t.shape[0], 0, 4, cv2.BORDER_CONSTANT, value=(40, 40, 40)) for t in tiles]
    rows = [np.hstack(tiles[i : i + 6]) for i in range(0, len(tiles), 6)]
    w = max(r.shape[1] for r in rows)
    rows = [cv2.copyMakeBorder(r, 0, 4, 0, w - r.shape[1], cv2.BORDER_CONSTANT, value=(40, 40, 40)) for r in rows]
    cv2.imwrite(str(QA / "tilde.jpg"), np.vstack(rows))
    return str(QA / "tilde.jpg")


def provenance():
    """Qué frames del original alimentan cada frame del fondo, contra los frames con texto viejo."""
    dirty = set([0]) | set(range(21, 114)) | set(range(219, 306)) | set(range(329, 417)) | set(range(494, 657))
    ghost_ok = set(range(329, 350))  # doodles originales con los contornos tenues borrados
    used = {}
    for s in EDL["segments"]:
        o0, o1 = s["out"]
        if s["shot"] == "black":
            continue
        for n in range(o0, o1):
            k = n - o0
            if s.get("path") == "pingpong":
                x = k * 0.5
                pos = s["src"] + (3 - abs(3 - (x % 6)))
            else:
                pos = s["src"] + k * s.get("speed", 1.0)
            if "srcMax" in s:
                pos = min(pos, s["srcMax"])
            srcs = {int(np.floor(pos + 1e-6)), int(np.ceil(pos - 1e-6))}
            used[n] = sorted(srcs)
    for c in EDL["crystals"]:
        for n in range(*c["out"]):
            pos = c["src"] + (n - c["out"][0]) * c["speed"]
            used.setdefault(n, [])
            used[n] = sorted(set(used[n]) | {int(np.floor(pos)), min(16, int(np.ceil(pos)))})
    bad = {n: [x for x in v if x in dirty and x not in ghost_ok] for n, v in used.items()}
    bad = {n: v for n, v in bad.items() if v}
    ghosts = sorted(n for n, v in used.items() if set(v) & ghost_ok)
    return {"frames_con_fuente_sucia": bad, "frames_con_fantasmas_borrados": [min(ghosts), max(ghosts)] if ghosts else []}


def cut_list(frames_iter, thr_mean=18, thr_hist=0.45):
    prev = hp = None
    cuts = []
    for n, g in frames_iter:
        g = cv2.resize(g, (144, 256), interpolation=cv2.INTER_AREA).astype(np.float32)
        h = cv2.calcHist([g.astype(np.uint8)], [0], None, [32], [0, 256]).ravel()
        h /= h.sum()
        if prev is not None:
            dm = float(np.abs(g - prev).mean())
            dh = float(np.abs(h - hp).sum())
            if dm > thr_mean or dh > thr_hist:
                cuts.append(n)
        prev, hp = g, h
    return cuts


def plate_cuts():
    """Cortes del fondo nuevo (sin texto encima, para no confundir animaciones con cortes)."""
    cap = cv2.VideoCapture(str(ROOT / "public/plates.mp4"))
    def it():
        n = 0
        while True:
            ok, f = cap.read()
            if not ok:
                return
            yield n, cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
            n += 1
    return cut_list(it())


def sync():
    edl_cuts = [s["out"][0] for s in EDL["segments"]][1:]
    orig_major = [17, 33, 45, 60, 74, 88, 100, 114, 127, 141, 156, 170, 183, 210, 226, 238, 251, 264, 278, 295, 306,
                  319, 350, 374, 387, 402, 417, 429, 442, 471, 486, 497, 512, 526, 540, 554, 567, 582, 586, 592]
    new = plate_cuts()
    rows = []
    beats = json.loads((ROOT / "analysis/beats.json").read_text())["beats"]
    period = float(np.median(np.diff(beats)))
    # grilla de cortes del original: misma fase que los cortes medidos
    phase = float(np.median([(c / FPS) % period for c in orig_major]))
    for c in orig_major:
        if c in (582, 586, 592):
            continue  # flash, monograma y negro: los resuelve Remotion, no el fondo
        near = min(new, key=lambda x: abs(x - c)) if new else None
        fuente = "detectado en el fondo"
        if (near is None or abs(near - c) > 1) and c in edl_cuts:
            near, fuente = c, "EDL (corte entre planos casi negros: el detector no lo ve)"
        g = phase + round((c / FPS - phase) / period * 2) / 2 * period  # beat o medio beat más cercano
        rows.append({"corte_original": c, "corte_nuevo": near, "fuente": fuente, "dif_frames": None if near is None else near - c,
                     "t": round(c / FPS, 3), "grilla_beat_s": round(g, 3), "dif_grilla_frames": round((c / FPS - g) * FPS, 2)})
    ok = all(r["dif_frames"] is not None and abs(r["dif_frames"]) <= 1 for r in rows)
    return {"cortes": rows, "todos_dentro_de_1_frame": ok, "periodo_beat_s": round(period, 4),
            "fase_grilla_s": round(phase, 4), "cortes_del_edl": edl_cuts}


def repetition():
    segs = [s for s in EDL["segments"] if s["shot"] not in ("black",)]
    issues = []
    for a, b in zip(segs, segs[1:]):
        if a["out"][1] != b["out"][0]:
            continue
        same_shot = a["shot"] == b["shot"] and a["shot"] != "orig"
        same_frame = same_shot and a.get("mirror", False) == b.get("mirror", False) and a.get("zoom") == b.get("zoom")
        if same_shot and not b.get("smear"):
            issues.append({"cortes": [a["out"], b["out"]], "plano": a["shot"], "mismo_encuadre": same_frame})
    # también: plano reconstruido igual al plano original vecino
    for a, b in zip(EDL["segments"], EDL["segments"][1:]):
        if a["shot"] == "orig" and b["shot"] != "orig" and b.get("src") is not None:
            pass
    usage = {}
    for s in EDL["segments"]:
        if s["shot"] not in ("orig", "black"):
            usage.setdefault(s["shot"], []).append({"out": s["out"], "espejado": s.get("mirror", False), "zoom": s.get("zoom")})
    return {"consecutivos": issues, "uso_por_plano": usage}


def ocr(frames):
    d = QA / "final_frames_png"
    out = QA / "ocr_final.json"
    run([str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/ocr_scan.py"), str(d), str(out), "--fps", "30"])
    data = json.loads(out.read_text())
    return [(r["frame"], r["hits"]) for r in data["frames"] if r["hits"]]


def main():
    QA.mkdir(exist_ok=True)
    frames = extract_frames()
    # PNG reducidos para OCR y comparativas
    d = QA / "final_frames_png"
    d.mkdir(exist_ok=True)
    for i, f in enumerate(frames):
        im = cv2.imread(str(f))
        cv2.imwrite(str(d / f"s{i:04d}.png"), cv2.resize(im, (576, 1024), interpolation=cv2.INTER_AREA))
    report = {"video": str(VIDEO), "frames": len(frames)}
    report["side_by_side"] = side_by_side()
    report["sheets"] = sheets()
    report["tilde"] = tilde(frames)
    report["procedencia"] = provenance()
    report["sincronia"] = sync()
    report["repeticion"] = repetition()
    report["ocr_coincidencias"] = ocr(frames)
    (QA / "qa_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    print(json.dumps({k: report[k] for k in ("frames", "ocr_coincidencias")}, ensure_ascii=False))
    print("procedencia:", report["procedencia"])
    print("sincronía ok:", report["sincronia"]["todos_dentro_de_1_frame"])
    print("repetición:", report["repeticion"]["consecutivos"])


if __name__ == "__main__":
    main()
