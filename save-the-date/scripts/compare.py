"""Comparativa original | nuevo para una lista de frames.

uso: python scripts/compare.py <stills_dir|video.mp4> <salida.jpg> <frame> [frame...] [--w 270] [--cols 4]

Si la fuente nueva es una carpeta, toma <dir>/sNNNN.png; si es un video, extrae los frames.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
args = sys.argv[1:]
opt = {}
for k in ("--w", "--cols"):
    if k in args:
        i = args.index(k)
        opt[k] = int(args[i + 1])
        del args[i : i + 2]
src, out, frames = args[0], args[1], [int(x) for x in args[2:]]
tw = opt.get("--w", 270)
cols = opt.get("--cols", 4)
th = round(tw * 16 / 9)

times = [float(x) for x in (ROOT / "analysis/frame_times.txt").read_text().split()]
fm = {round(t * 30): i + 1 for i, t in enumerate(times)}
for n in range(657):
    fm.setdefault(n, fm.get(n - 1))


def new_frame(n):
    p = Path(src)
    if p.is_dir():
        return Image.open(p / f"s{n:04d}.png").convert("RGB")
    cap = cv2.VideoCapture(str(p))
    cap.set(cv2.CAP_PROP_POS_FRAMES, n)
    ok, f = cap.read()
    return Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB))


def orig_frame(n):
    if n > 656:
        return Image.new("RGB", (576, 1024), (0, 0, 0))
    return Image.open(ROOT / f"analysis/frames/f{fm[n]:04d}.png").convert("RGB")


rows = (len(frames) + cols - 1) // cols
lab = 18
sheet = Image.new("RGB", (cols * (2 * tw + 10), rows * (th + lab)), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for i, n in enumerate(frames):
    x, y = (i % cols) * (2 * tw + 10), (i // cols) * (th + lab)
    sheet.paste(orig_frame(n).resize((tw, th), Image.LANCZOS), (x, y + lab))
    sheet.paste(new_frame(n).resize((tw, th), Image.LANCZOS), (x + tw, y + lab))
    d.text((x + 4, y + 3), f"#{n}  {n / 30:.2f}s   original | nuevo", fill=(255, 255, 0))
sheet.save(out, quality=90)
print(out, sheet.size)
