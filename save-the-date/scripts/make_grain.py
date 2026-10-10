"""Texturas de grano (12 variantes) para el overlay animado de Remotion: public/grain/g00.png..."""
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
d = ROOT / "public/grain"
d.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(11)
for k in range(12):
    n = rng.normal(0, 1, (960, 540)).astype(np.float32)
    n = cv2.GaussianBlur(n, (0, 0), 0.6)
    n = n / n.std()
    img = np.clip(128 + n * 52, 0, 255).astype(np.uint8)
    cv2.imwrite(str(d / f"g{k:02d}.png"), img)
print("grano:", len(list(d.glob('*.png'))))
