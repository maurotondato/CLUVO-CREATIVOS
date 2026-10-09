"""Genera música original + efectos sincronizados para el reel de CLUVO (20 s, 48 kHz, estéreo).
Salida: build/music.wav, build/sfx.wav, build/vo.wav"""
import numpy as np, scipy.signal as sg, subprocess, json, os

SR = 48000
T = 20.0
N = int(SR * T)
rng = np.random.default_rng(7)
os.makedirs("build", exist_ok=True)


def tt(d):
    return np.arange(int(SR * d)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, fc, o=2):
    return sg.sosfilt(sg.butter(o, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, o=2):
    return sg.sosfilt(sg.butter(o, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, o=2):
    return sg.sosfilt(sg.butter(o, [lo, hi], "band", fs=SR, output="sos"), x)


def noise(d):
    return rng.standard_normal(int(SR * d))


class Bus:
    def __init__(self):
        self.L = np.zeros(N + SR * 3)
        self.R = np.zeros(N + SR * 3)

    def add(self, x, t, g=1.0, pan=0.0):
        i = int(t * SR)
        if i < 0:
            x = x[-i:]; i = 0
        gl, gr = g * np.cos((pan + 1) * np.pi / 4) * 1.414, g * np.sin((pan + 1) * np.pi / 4) * 1.414
        if x.ndim == 2:
            self.L[i:i + len(x)] += x[:, 0] * gl
            self.R[i:i + len(x)] += x[:, 1] * gr
        else:
            self.L[i:i + len(x)] += x * gl
            self.R[i:i + len(x)] += x * gr

    def out(self):
        return np.stack([self.L[:N], self.R[:N]], 1)


# reverb IR (estéreo, decaimiento suave)
def make_ir(dur=1.6, decay=0.45, tone=5000):
    t = tt(dur)
    irs = []
    for s in (1, 2):
        n = rng.standard_normal(len(t)) * np.exp(-t / decay)
        irs.append(lp(n, tone))
    ir = np.stack(irs, 1)
    return ir / np.abs(ir).sum(0).max() * 6


IR = make_ir()


def reverb(x, mix=0.25):
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    w = np.stack([sg.fftconvolve(x[:, c], IR[:, c])[: len(x) + len(IR) - 1] for c in (0, 1)], 1)
    d = np.zeros_like(w); d[: len(x)] = x
    return d * (1 - mix) + w * mix


# ---------------------------------------------------------------- instrumentos
def kick(g=1.0):
    t = tt(0.5)
    f = 42 + 120 * np.exp(-t / 0.035)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.2)
    y += hp(noise(0.5), 3000) * np.exp(-t / 0.004) * 0.25
    return np.tanh(y * 1.6) * g


def clap():
    t = tt(0.35)
    e = np.zeros_like(t)
    for o in (0, 0.011, 0.022):
        e += (t >= o) * np.exp(-np.clip(t - o, 0, None) / (0.012 if o < 0.02 else 0.11))
    return bp(noise(0.35), 900, 2600) * e * 0.8


def hat(open_=False):
    d = 0.25 if open_ else 0.06
    t = tt(d)
    return hp(noise(d), 7500, 4) * np.exp(-t / (0.09 if open_ else 0.018))


def bass(m, d):
    t = tt(d)
    f = mtof(m)
    y = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9))
    y = lp(y, 700)
    y += np.sin(2 * np.pi * f / 2 * t) * 0.9
    env = np.minimum(1, t / 0.005) * np.minimum(1, (d - t) / 0.03) * np.exp(-t / 0.5)
    return np.tanh(y * env * 1.2) * 0.6


def pad(notes, d, bright=2400):
    t = tt(d)
    L = np.zeros_like(t); R = np.zeros_like(t)
    for m in notes:
        for det, side in ((-9, 0), (0, 2), (9, 1)):
            f = mtof(m) * 2 ** (det / 1200)
            ph = rng.uniform(0, 6.28)
            y = sum(np.sin(2 * np.pi * f * k * t + ph * k) / k for k in range(1, 10))
            if side in (0, 2): L += y
            if side in (1, 2): R += y
    env = np.minimum(1, t / 0.35) * np.minimum(1, (d - t) / 0.4)
    L = lp(L * env, bright); R = lp(R * env, bright)
    return np.stack([L, R], 1) * 0.05


def pluck(m, d=0.7, damp=0.994):
    f = mtof(m)
    p = int(SR / f)
    n = int(SR * d)
    buf = rng.uniform(-1, 1, p)
    y = np.zeros(n)
    for i in range(n):
        y[i] = buf[i % p]
        buf[i % p] = damp * 0.5 * (buf[i % p] + buf[(i + 1) % p])
    return lp(y, 5000) * 0.5


def sine_bell(f, d=0.8, partials=((1, 1), (2.76, 0.25), (5.4, 0.08)), dec=0.35):
    t = tt(d)
    return sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (dec / r ** 0.5)) for r, a in partials) * np.minimum(1, t / 0.002)


# ---------------------------------------------------------------- SFX
def tvfilter(x, f0, f1, q=1.2, curve=1.0):
    """bandpass con centro que barre de f0 a f1 (procesado por bloques)"""
    out = np.zeros_like(x)
    B = 256
    zi = None
    nb = len(x) // B + 1
    for b in range(nb):
        k = (b / max(1, nb - 1)) ** curve
        fc = f0 * (f1 / f0) ** k
        lo, hi = fc / (1 + 1 / q), min(fc * (1 + 1 / q), SR / 2 - 100)
        sos = sg.butter(2, [lo, hi], "band", fs=SR, output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        seg = x[b * B:(b + 1) * B]
        if len(seg) == 0: break
        out[b * B:b * B + len(seg)], zi = sg.sosfilt(sos, seg, zi=zi)
    return out


def whoosh(d=0.5, f0=300, f1=3000, peak=0.6):
    t = tt(d)
    x = tvfilter(noise(d), f0, f1, q=1.5)
    env = np.where(t < d * peak, (t / (d * peak)) ** 2, ((d - t) / (d * (1 - peak))) ** 1.5)
    y = x * env
    pan = np.linspace(-0.7, 0.7, len(t))
    return np.stack([y * (1 - pan) * 0.7, y * (1 + pan) * 0.7], 1)


def riser(d=1.2):
    t = tt(d)
    x = tvfilter(noise(d), 400, 6000, q=2, curve=1.6) * (t / d) ** 2
    s = np.sin(2 * np.pi * np.cumsum(200 * (6 ** (t / d))) / SR) * (t / d) ** 3 * 0.15
    return x * 0.8 + s


def impact(g=1.0, sub=48):
    t = tt(1.6)
    f = sub * (1 + 0.6 * np.exp(-t / 0.05))
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.5)
    y += lp(noise(1.6), 1200) * np.exp(-t / 0.12) * 0.6
    y += hp(noise(1.6), 4000) * np.exp(-t / 0.02) * 0.3
    return reverb(np.tanh(y * 1.4) * g, 0.3)


def thud(g=1.0):
    t = tt(0.4)
    f = 70 + 90 * np.exp(-t / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.09)
    y += bp(noise(0.4), 800, 3000) * np.exp(-t / 0.03) * 0.35
    return y * g


def pop(f0=500, g=1.0):
    t = tt(0.12)
    f = f0 * (1 + 0.9 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035) * g


def notif(f=1046.5, g=1.0):
    a = sine_bell(f, 0.35, ((1, 1), (3, 0.15)), 0.08)
    b = sine_bell(f * 1.5, 0.45, ((1, 1), (3, 0.15)), 0.12)
    y = np.zeros(int(SR * 0.6)); y[:len(a)] += a; i = int(0.07 * SR); y[i:i + len(b)] += b
    return y * g


def tap(g=1.0):
    t = tt(0.05)
    return (hp(noise(0.05), 2500) * np.exp(-t / 0.003) * 0.6 + np.sin(2 * np.pi * 1700 * t) * np.exp(-t / 0.008) * 0.5) * g


def tick(f=2600, g=1.0):
    t = tt(0.04)
    return np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) * g


def chime(base=1318.5, g=1.0):
    a = sine_bell(base, 1.0, dec=0.4); b = sine_bell(base * 1.4983, 1.2, dec=0.5)
    y = np.zeros(int(SR * 1.4)); y[:len(a)] += a; i = int(0.09 * SR); y[i:i + len(b)] += b
    return reverb(y * g, 0.35)


def coin(g=1.0):
    p = ((1, 1), (1.52, 0.6), (2.31, 0.35), (3.07, 0.2))
    a = sine_bell(2637, 0.5, p, 0.12); b = sine_bell(3136, 0.8, p, 0.25)
    y = np.zeros(int(SR * 1.0)); y[:len(a)] += a; i = int(0.075 * SR); y[i:i + len(b)] += b
    return reverb(y * g, 0.3)


def shimmer(d=0.6, n=14, g=1.0, seed=1):
    r = np.random.default_rng(seed)
    y = np.zeros((int(SR * (d + 0.6)), 2))
    for k in range(n):
        f = r.uniform(2800, 7500); o = r.uniform(0, d)
        s = sine_bell(f, 0.5, ((1, 1),), 0.09) * r.uniform(.3, 1)
        pn = r.uniform(-1, 1); i = int(o * SR)
        y[i:i + len(s), 0] += s * (1 - pn) / 2; y[i:i + len(s), 1] += s * (1 + pn) / 2
    return reverb(y * g, 0.4)


def crackle(d=0.5, g=1.0):
    y = np.zeros(int(SR * d))
    for k in range(40):
        i = rng.integers(0, len(y) - 300)
        y[i:i + 200] += hp(noise(200 / SR), 3000) * np.exp(-np.arange(200) / 30) * rng.uniform(.2, 1)
    return y * g * np.linspace(1, 0.2, len(y))


# ================================================================ MÚSICA
music = Bus()
BEAT = 0.5
# --- intro (0-3 s): pulso grave tenso + reloj + riser
for i in range(12):
    t0 = i * 0.25
    music.add(lp(bass(36, 0.22), 400), t0, 0.35 + 0.25 * (i / 12))
for i in range(6):
    music.add(tick(1800 if i % 2 else 2400, 0.25), i * 0.5)
music.add(pad([48, 55, 63], 3.0, 900), 0, 0.9)  # Cm tenso, oscuro
music.add(riser(1.25), 1.75, 0.55)

# --- groove (3-16.5 s)
CH = [(3, [60, 64, 67, 72], 48), (5, [59, 62, 67, 71], 43), (7, [57, 60, 64, 69], 45), (9, [57, 60, 65, 69], 41),
      (11, [60, 64, 67, 72], 48), (13, [59, 62, 67, 71], 43), (15, [57, 60, 65, 69], 41)]
for (t0, notes, root) in CH:
    d = 2.0 if t0 < 15 else 1.5
    music.add(pad(notes, d + 0.3), t0, 0.8)
    # bajo en corcheas con bombeo
    for k in range(int(d / 0.25)):
        if k % 2 == 1 or k == 0:
            music.add(bass(root + (12 if k % 4 == 3 else 0), 0.22), t0 + k * 0.25, 0.55)
    # arpegio pluck
    arp = [notes[0] + 12, notes[2] + 12, notes[1] + 12, notes[3] + 12]
    for k in range(int(d / 0.25)):
        m = arp[k % 4] + (12 if (k // 4) % 2 and t0 >= 11 else 0)
        music.add(pluck(m, 0.5), t0 + k * 0.25, 0.32, pan=(-0.5 if k % 2 else 0.5))

beat_t = np.arange(3.0, 16.0, BEAT)
for i, b in enumerate(beat_t):
    music.add(kick(), b, 0.9)
    if i % 2 == 1:
        music.add(reverb(clap(), 0.2), b, 0.45)
    music.add(hat(True), b + 0.25, 0.10, pan=0.3)
    for s in (0, 0.125, 0.375):
        music.add(hat(), b + s, 0.07 if s else 0.05, pan=-0.3)
# energía extra en el montaje de deportes: shaker 16avos
for b in np.arange(12.25, 16.0, 0.125):
    music.add(hat(), b, 0.05, pan=0.6)
# build final: redoble que acelera 15.5-16.4
for k, b in enumerate(np.concatenate([np.arange(15.5, 16.0, 0.125), np.arange(16.0, 16.45, 0.0625)])):
    music.add(clap(), b, 0.12 + 0.25 * k / 16)
music.add(riser(0.9), 15.6, 0.45)
# golpe final + acorde C abierto que se sostiene
music.add(kick(1.2), 16.5, 1.0)
music.add(pad([48, 55, 60, 64, 67, 72], 3.5, 3000), 16.5, 1.1)
music.add(bass(36, 1.6), 16.5, 0.6)
for k, m in enumerate([72, 76, 79, 84, 79, 76, 72, 67]):
    music.add(pluck(m, 0.9), 16.5 + k * 0.25, 0.22 * (1 - k / 10), pan=(-0.4 if k % 2 else 0.4))

M = music.out()
M = np.stack([lp(M[:, 0], 14000), lp(M[:, 1], 14000)], 1)
fade = np.ones(N); fi = int(19.2 * SR); fade[fi:] = np.linspace(1, 0, N - fi) ** 2
M *= fade[:, None]
M /= np.abs(M).max() * 1.12

# ================================================================ SFX
fx = Bus()
# S1 hook
for t0 in [0.25, 0.42, 0.66, 1.04, 1.18, 1.57]:
    fx.add(pop(320, 0.35), t0)
fx.add(thud(0.9), 1.75)
for r in range(6):
    fx.add(tick(3000 - r * 120, 0.25), 1.78 + r * 0.06, pan=-0.3)
fx.add(thud(0.7), 2.22)
for i, t0 in enumerate([2.3, 2.42, 2.54, 2.66, 2.78]):
    fx.add(notif(880 * 2 ** (i * 2 / 12), 0.32), t0, pan=(-0.5 if i % 2 == 0 else 0.5))
fx.add(pop(900, 0.5), 2.86, pan=0.5)
fx.add(whoosh(0.4, 400, 4000, 0.85), 2.72, 0.7)
fx.add(impact(0.9), 3.0)
# S2 reservas
fx.add(whoosh(0.7, 200, 2500, 0.5), 3.05, 0.6)
fx.add(shimmer(0.5, 12, 0.7, seed=2), 3.36)
fx.add(whoosh(0.35, 800, 3000), 4.12, 0.3)
fx.add(tap(0.7), 4.5)
for k in range(15):
    fx.add(tick(2200 + (k % 5) * 180, 0.12), 4.58 + k * 0.022, pan=(k % 3 - 1) * 0.5)
fx.add(tap(0.8), 5.0); fx.add(pop(700, 0.45), 5.06)
fx.add(chime(1318.5, 0.5), 5.24)
# S3 clases/torneos
fx.add(whoosh(0.35, 600, 4000), 6.03, 0.45)
fx.add(tap(0.7), 6.72); fx.add(pop(820, 0.45), 6.8)
fx.add(whoosh(0.35, 600, 4000), 7.03, 0.45)
fx.add(tap(0.7), 7.54)
fx.add(chime(1568, 0.5), 7.62); fx.add(crackle(0.55, 0.35), 7.62)
# S4 admin
fx.add(whoosh(0.6, 3000, 250, 0.4), 7.85, 0.7)
fx.add(thud(0.5), 8.1)
for t0 in [9.48, 10.06, 10.68, 11.14]:
    fx.add(pop(420, 0.55), t0); fx.add(thud(0.35), t0)
for k in range(16):
    fx.add(tick(3200, 0.13), 9.6 + 0.9 * (k / 16) ** 1.3, pan=-0.2)
fx.add(coin(0.45), 10.45)
fx.add(notif(660, 0.22), 10.5, pan=0.4)
for k in range(4):
    fx.add(tick(2400 + k * 200, 0.3), 10.82 + k * 0.13, pan=-0.4)
for k, m in enumerate([72, 74, 76, 79, 81, 84, 86]):
    fx.add(sine_bell(mtof(m), 0.3, ((1, 1), (2, 0.2)), 0.07) * 0.18, 11.24 + k * 0.05, pan=0.4)
fx.add(whoosh(0.8, 300, 1500, 0.3), 11.45, 0.3)
# S5 deportes
fx.add(whoosh(0.5, 250, 3500, 0.7), 12.05, 0.7)
fx.add(thud(0.7), 12.4)
fx.add(whoosh(0.3, 700, 5000, 0.7), 12.94, 0.55); fx.add(thud(0.5), 13.14)
fx.add(whoosh(0.3, 700, 5000, 0.7), 13.46, 0.55); fx.add(thud(0.5), 13.66)
for t0 in [14.02, 14.17, 14.31]:
    fx.add(whoosh(0.12, 1500, 6000, 0.6), t0 - 0.06, 0.4); fx.add(tick(1800, 0.3), t0)
fx.add(impact(0.5, 60), 14.45)
for i in range(6):
    fx.add(pop(500 + i * 60, 0.35), 14.48 + i * 0.07, pan=(-0.5 if i % 2 == 0 else 0.5))
fx.add(shimmer(0.4, 8, 0.5, seed=3), 15.45)
# S6 cierre
fx.add(whoosh(0.6, 5000, 300, 0.35), 16.0, 0.5)
fx.add(impact(1.0, 42), 16.5)
fx.add(shimmer(0.8, 18, 0.8, seed=4), 16.55)
fx.add(whoosh(0.6, 1500, 6000, 0.5), 16.98, 0.25)
fx.add(pop(600, 0.35), 17.9)
fx.add(pop(760, 0.5), 18.45); fx.add(tap(0.5), 18.5)
fx.add(shimmer(0.4, 6, 0.4, seed=5), 19.0)
F = fx.out()
F /= np.abs(F).max() * 1.05

# ================================================================ VOZ
vo = Bus()
PLACE = {"f1": 0.15, "f2": 3.05, "f3": 6.05, "f4": 8.10, "f5": 12.35, "f6": 16.60}
for k, t0 in PLACE.items():
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", f"../audio/vo/{k}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.float32).astype(np.float64)
    vo.add(x, t0, 1.0)
V = vo.out()


def wav(name, x):
    import wave
    x = np.clip(x, -1, 1)
    with wave.open(name, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


wav("build/music.wav", M)
wav("build/sfx.wav", F)
wav("build/vo.wav", V / np.abs(V).max() * 0.9)
print("ok")
