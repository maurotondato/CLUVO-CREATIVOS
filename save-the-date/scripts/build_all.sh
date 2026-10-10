#!/usr/bin/env bash
# Regenera todo el video a partir de invitation.config.json.
# Requiere: node 20+, npm, ffmpeg, python 3.12 (uv o venv) y tesseract para el QA.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d node_modules ] || npm ci --no-fund --no-audit
if [ ! -x .venv/bin/python ]; then
  uv venv -q --python 3.12 .venv 2>/dev/null || python3 -m venv .venv
  .venv/bin/python -m pip install -q numpy opencv-python-headless librosa pytesseract pillow scipy soundfile
fi

# 1. análisis del original (frames, tiempos, beats)
mkdir -p analysis/frames
if [ ! -f analysis/frame_times.txt ]; then
  ffmpeg -v error -i input/original.mp4 -vsync 0 analysis/frames/f%04d.png
  ffprobe -v error -select_streams v -show_entries frame=pts_time -of csv=p=0 input/original.mp4 | tr -d ',' > analysis/frame_times.txt
fi

# 2. fondos sin texto, cristales, fuentes y logo
.venv/bin/python scripts/plates_edl.py
.venv/bin/python scripts/build_plates.py
node scripts/fetch_fonts.mjs
.venv/bin/python scripts/make_grain.py
.venv/bin/python scripts/prepare_logo.py

# 3. render de Remotion (textos, animaciones, efectos) y audio
rm -rf output/frames
npx remotion render src/index.ts SaveTheDate --sequence --image-format=png output/frames --concurrency=4
.venv/bin/python scripts/make_audio.py

# 4. export y QA
scripts/export.sh
SLUG=$(ls output/save_the_date_*_1080x1920.mp4 | head -1)
.venv/bin/python scripts/qa.py "$SLUG"
