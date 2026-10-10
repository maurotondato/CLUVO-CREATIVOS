"""Tablas para REPORT.md a partir de src/data/plates.json y analysis/clean_pool.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDL = json.loads((ROOT / "src/data/plates.json").read_text())
POOL = {p["id"]: p for p in json.loads((ROOT / "analysis/clean_pool.json").read_text())}


def t(f):
    return f"{f / 30:.2f}".replace(".", ",")


print("| Frames | Tiempo (s) | Estado | Fuente | Tratamiento | Nota |")
print("|---|---|---|---|---|---|")
for s in EDL["segments"]:
    o0, o1 = s["out"]
    shot = s["shot"]
    if shot == "black":
        src = "negro"
    elif shot == "orig":
        src = f"original {o0}-{o1 - 1}"
    else:
        p = POOL[shot]
        sp = s.get("speed", 1.0)
        if s.get("path") == "pingpong":
            src = f"{shot} ({p['start']}-{p['end']}, ida y vuelta)"
        else:
            last = min(s["src"] + (o1 - o0 - 1) * sp, s.get("srcMax", 1e9))
            src = f"{shot} ({s['src']}-{last:.0f})"
    tr = []
    if s.get("mirror"):
        tr.append("espejado")
    if s.get("speed") not in (None, 1.0, 0) and shot not in ("orig", "black"):
        tr.append(f"{s['speed']:.2f}x")
    if s.get("speed") == 0:
        tr.append("cuadro fijo")
    if s.get("zoom"):
        z = s["zoom"]
        tr.append(f"zoom {z[0]:.2f}" + (f"→{z[1]:.2f}" if z[1] != z[0] else ""))
    if s.get("rotate"):
        tr.append(f"rot {s['rotate']}°")
    if s.get("punch"):
        tr.append("punch-in")
    if s.get("ghosts"):
        tr.append("borrado de fantasmas")
    if s.get("smear"):
        tr.append("smear vertical")
    if s.get("gain"):
        tr.append(f"ganancia {s['gain']}")
    print(f"| {o0}-{o1 - 1} | {t(o0)}–{t(o1)} | {s.get('status', '')} | {src} | {', '.join(tr)} | {s.get('note', '')} |")
