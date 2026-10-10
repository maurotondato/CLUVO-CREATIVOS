#!/usr/bin/env bash
# Exporta el render maestro de Remotion con el audio final.
# uso: scripts/export.sh  (después de render + make_audio)
set -euo pipefail
cd "$(dirname "$0")/.."
SLUG=$(.venv/bin/python -c "import json,unicodedata;n=json.load(open('invitation.config.json'))['name'];print(''.join(c for c in unicodedata.normalize('NFD',n) if unicodedata.category(c)!='Mn').upper().replace(' ','_'))")
# master: la secuencia PNG del render de Remotion (sin pérdida)
MASTER_IN=(-framerate 30 -start_number 0 -i output/frames/element-%03d.png)
AUDIO=output/audio_final.wav
FULL=output/save_the_date_${SLUG}_1080x1920.mp4
WA=output/save_the_date_${SLUG}_whatsapp.mp4

# 1080x1920: H.264 High, yuv420p, 30 fps, CRF 16, preset slow, AAC 192 kbps 44,1 kHz, faststart
ffmpeg -v error -y "${MASTER_IN[@]}" -i "$AUDIO" -map 0:v -map 1:a \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -crf 16 -preset slow \
  -c:a aac -b:a 192k -ar 44100 -movflags +faststart -shortest "$FULL"

# WhatsApp: 720x1280, menos de 16 MB (dos pasadas a 4 Mbps de video)
ffmpeg -v error -y "${MASTER_IN[@]}" -vf scale=720:1280:flags=lanczos -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 \
  -b:v 4000k -maxrate 5000k -bufsize 8000k -preset slow -pass 1 -passlogfile output/x264wa -an -f mp4 /dev/null
ffmpeg -v error -y "${MASTER_IN[@]}" -i "$AUDIO" -map 0:v -map 1:a -vf scale=720:1280:flags=lanczos \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -r 30 -b:v 4000k -maxrate 5000k -bufsize 8000k -preset slow \
  -pass 2 -passlogfile output/x264wa -c:a aac -b:a 128k -ar 44100 -movflags +faststart -shortest "$WA"
rm -f output/x264wa*

# Póster: el monograma a los 20,5 s
ffmpeg -v error -y -ss 20.5 -i "$FULL" -frames:v 1 -q:v 2 output/poster.jpg

ls -la "$FULL" "$WA" output/poster.jpg
