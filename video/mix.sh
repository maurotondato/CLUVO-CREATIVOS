#!/bin/sh
# Mezcla final (voz procesada + música con ducking + SFX, -14 LUFS) y muxeo con el video.
set -e
cd "$(dirname "$0")/build"
ffmpeg -y -loglevel error -i vo.wav -i music.wav -i sfx.wav -filter_complex "
[0:a]highpass=f=75,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=3,equalizer=f=7000:t=q:w=2:g=-2,acompressor=threshold=-20dB:ratio=3.5:attack=5:release=120:makeup=4,alimiter=limit=0.9,asplit=2[vo][key];
[1:a]volume=0.9[mu];
[mu][key]sidechaincompress=threshold=0.04:ratio=4:attack=15:release=280:makeup=1[mud];
[2:a]volume=0.65[fx];
[vo][mud][fx]amix=inputs=3:normalize=0:weights=1 1 1,alimiter=limit=0.95,loudnorm=I=-14:TP=-1.0:LRA=9[out]" -map "[out]" -ar 48000 -c:a pcm_s16le mix.wav
mkdir -p ../../entregables
ffmpeg -y -loglevel error -i video_60.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart -shortest ../../entregables/CLUVO_reel_ventas_9x16.mp4
