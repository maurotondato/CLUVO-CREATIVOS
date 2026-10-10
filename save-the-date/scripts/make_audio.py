"""Pista de audio final: el audio original sin tocar + silencio hasta el final de la placa,
con un shimmer muy sutil (-24 dBFS de pico) sintetizado cuando entra el logo de M·DATOS.

uso: python scripts/make_audio.py
"""
import json
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parent.parent
SR = 44100
EDL = json.loads((ROOT / "src/data/plates.json").read_text())
TOTAL_S = EDL["total"] / EDL["fps"]
LOGO_S = 663 / 30  # F.logo en src/timeline.ts

wav = ROOT / "analysis/original_stereo.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ROOT / "input/original.mp4"), "-vn", "-ac", "2", "-ar", str(SR),
                "-c:a", "pcm_f32le", str(wav)], check=True)
orig, sr = sf.read(wav, dtype="float32")
assert sr == SR

n = int(round(TOTAL_S * SR))
out = np.zeros((n, 2), np.float32)
out[: min(n, len(orig))] = orig[:n]

# shimmer: parciales agudos con vibrato y envolvente suave, más un soplo de ruido filtrado
t = np.arange(int(1.1 * SR)) / SR
env = np.minimum(1, t / 0.08) * np.exp(-t / 0.35)
rng = np.random.default_rng(7)
sh = np.zeros_like(t)
for f, a in [(2637, 1.0), (3520, 0.7), (4699, 0.5), (5274, 0.35), (7040, 0.2)]:
    sh += a * np.sin(2 * np.pi * f * t + 2.5 * np.sin(2 * np.pi * 6.5 * t) + rng.uniform(0, 6.28))
noise = rng.standard_normal(len(t))
noise = np.convolve(noise, np.ones(8) / 8, mode="same") - np.convolve(noise, np.ones(64) / 64, mode="same")
sh = (sh / 2.75 + 0.35 * noise) * env
sh = sh / np.max(np.abs(sh)) * 10 ** (-24 / 20)
start = int(LOGO_S * SR)
end = min(n, start + len(sh))
pan = np.stack([sh[: end - start] * 0.9, sh[: end - start]], axis=1)
out[start:end] += pan

dst = ROOT / "output/audio_final.wav"
sf.write(dst, out, SR, subtype="FLOAT")
print(dst, f"{n / SR:.3f} s", "pico original", float(np.abs(orig).max()))
