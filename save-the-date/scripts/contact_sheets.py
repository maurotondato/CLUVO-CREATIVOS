"""Contact sheets con timestamp de una carpeta de frames.

uso: python scripts/contact_sheets.py <frames_dir> <frame_times.txt|fps> <out_dir> [por_hoja] [ancho_thumb]
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

frames_dir, times_arg, out_dir = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
per_sheet = int(sys.argv[4]) if len(sys.argv) > 4 else 60
tw = int(sys.argv[5]) if len(sys.argv) > 5 else 144
cols = 10

files = sorted(frames_dir.glob("*.png")) + sorted(frames_dir.glob("*.jpg"))
if Path(times_arg).exists():
    times = [float(x) for x in Path(times_arg).read_text().split()]
else:
    fps = float(times_arg)
    times = [i / fps for i in range(len(files))]

out_dir.mkdir(parents=True, exist_ok=True)
first = Image.open(files[0])
th = round(tw * first.height / first.width)
lab = 16
for s in range(0, len(files), per_sheet):
    chunk = files[s : s + per_sheet]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + lab)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        im = Image.open(f).convert("RGB").resize((tw, th))
        x, y = (i % cols) * tw, (i // cols) * (th + lab)
        sheet.paste(im, (x, y + lab))
        t = times[s + i]
        d.text((x + 3, y + 2), f"{t:5.2f}s  #{round(t * 30)}", fill=(255, 255, 0))
    t0, t1 = times[s], times[s + len(chunk) - 1]
    sheet.save(out_dir / f"sheet_{t0:05.2f}-{t1:05.2f}.jpg", quality=88)
    print(out_dir / f"sheet_{t0:05.2f}-{t1:05.2f}.jpg")
