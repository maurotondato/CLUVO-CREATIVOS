"""OCR de todos los frames de una carpeta, buscando palabras prohibidas.

uso: python scripts/ocr_scan.py <frames_dir> <salida.json> [--fps 30 | --times frame_times.txt]

Cada frame se pasa a tesseract dos veces (normal e invertido, ampliado 2x) en modo
texto disperso. El JSON guarda el texto leído por frame y las coincidencias.
"""
import json
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import os

os.environ.setdefault("OMP_THREAD_LIMIT", "1")  # sin esto los procesos en paralelo se pisan y tesseract tarda minutos

import cv2
import numpy as np
import pytesseract

FORBIDDEN = ["ONA", "28", "MADERO", "TANGO", "LOMBARDI", "OL"]
# variantes que tesseract suele devolver para texto estilizado
PATTERNS = {
    "ONA": r"\b[O0Q]NA\b",
    "28": r"28[\.\s,]?0?3|28\.|\b28\b",
    "MADERO": r"MAD[E3]R|ADERO|MADER",
    "TANGO": r"TANG[O0]|ANGO\b",
    "LOMBARDI": r"L[O0]MBAR|OMBARD|Lombardi",
    "OL": r"\bOL\b",
}


def read(path):
    g = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    # a 576 px de ancho alcanza con 1,5x; el render final (1080) se reduce a la misma escala
    scale = 864 / g.shape[1]
    g = cv2.resize(g, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC)
    out = []
    for img in (g, 255 - g):
        out.append(pytesseract.image_to_string(img, config="--psm 11"))
    return " | ".join(" ".join(t.split()) for t in out)


def main():
    frames_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    files = sorted(frames_dir.glob("*.png")) + sorted(frames_dir.glob("*.jpg"))
    if "--times" in sys.argv:
        times = [float(x) for x in Path(sys.argv[sys.argv.index("--times") + 1]).read_text().split()]
    else:
        fps = float(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 30.0
        times = [i / fps for i in range(len(files))]
    with ProcessPoolExecutor() as ex:
        texts = list(ex.map(read, files, chunksize=4))
    rows, hits = [], []
    for f, t, txt in zip(files, times, texts):
        found = [k for k, p in PATTERNS.items() if re.search(p, txt, re.IGNORECASE if k != "OL" else 0)]
        rows.append({"file": f.name, "t": round(t, 3), "frame": round(t * 30), "text": txt, "hits": found})
        if found:
            hits.append((round(t * 30), round(t, 2), found))
    json.dump({"forbidden": FORBIDDEN, "frames": rows}, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"{len(hits)} frames con coincidencias de {len(files)}")
    for h in hits:
        print(*h)


if __name__ == "__main__":
    main()
