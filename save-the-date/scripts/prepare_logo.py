"""Recorta el logo de la placa final a su bounding box sobre fondo negro.

Lee creditLogo de invitation.config.json y escribe public/credit_logo.png y
src/data/logo.json (tamaño, para mantener la proporción en Remotion).

uso: python scripts/prepare_logo.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
cfg = json.loads((ROOT / "invitation.config.json").read_text())
im = Image.open(ROOT / cfg["creditLogo"]).convert("RGBA")
bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
bg.alpha_composite(im)  # el fondo transparente pasa a ser negro, igual que la placa
rgb = bg.convert("RGB")
a = np.asarray(rgb).max(axis=2)
ys, xs = np.where(a > 12)
box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
crop = rgb.crop(box)
crop.save(ROOT / "public/credit_logo.png")
(ROOT / "src/data").mkdir(parents=True, exist_ok=True)
(ROOT / "src/data/logo.json").write_text(json.dumps({"width": crop.width, "height": crop.height, "bbox": box}))
print("logo", box, crop.size)
