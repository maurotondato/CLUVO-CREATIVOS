"""Inventario de planos limpios (clean pool) y EDL de fondos.

Escribe analysis/clean_pool.json y src/data/plates.json. Los números son frames del
original a 30 fps constantes (frame n = n/30 s; el original no trae el frame 25 y se
repite el 24).

uso: python scripts/plates_edl.py
"""
import json
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FPS = 30
TOTAL = 708  # 23,6 s: 21,9 s del original + 1,7 s de placa M·DATOS

# ---------------------------------------------------------------- clean pool
# id, primer frame, último frame (inclusive), tipo, descripción, notas
POOL = [
    ("crystals", 1, 16, "cristales", "Cristales/diamantes 3D facetados cayendo sobre negro", ""),
    ("street", 17, 20, "ciudad", "Calle de noche con faros (antes de que entre el texto)", "solo 4 frames limpios"),
    ("dj", 114, 126, "fiesta", "Bandeja de DJ / vinilo", ""),
    ("stage", 127, 140, "luces", "Siluetas de multitud con escenario blanco", ""),
    ("flash", 141, 155, "luces", "Flash blanco que quema, copa a contraluz", "trazo chico tipo '4' abajo a la derecha en 150-151"),
    ("bokeh", 156, 169, "luces", "Bokeh", "167 casi negro"),
    ("hands", 170, 182, "fiesta", "Manos arriba con confeti y destellos", ""),
    ("handwriting", 183, 201, "doodle", "Frases manuscritas stop motion (we were, Sunshine & Rainbows...)", "texto manuscrito del template, no es texto de la invitación"),
    ("vhs", 202, 209, "doodle", "Collage de paneles con ruido VHS e íconos", ""),
    ("neon", 210, 218, "luces", "Cartel de neón", "desde 219 asoman caracteres de la fecha vieja"),
    ("sparklers", 306, 318, "fiesta", "Multitud con bengalas", ""),
    ("sparklers_close", 319, 326, "fiesta", "Bengalas en primer plano", "carita malvada quemada desde 323"),
    ("scratches", 327, 328, "doodle", "Rayas blancas sobre bengalas", "desde 329 fantasmas tenues de MADERO TANGO a la izquierda"),
    ("car_smoke", 417, 428, "humo", "Auto con humo en la calle", ""),
    ("radio_city", 429, 439, "ciudad", "Radio City, cartel vertical", "carita malvada quemada desde 440"),
    ("zoom_city", 442, 458, "ciudad", "Zoom blur, ciudad con doodles (carita, calavera, sonrisa, scanlines)", "doodles quemados del original"),
    ("chrysler", 459, 463, "ciudad", "Chrysler de noche", "464-467 con garabato y corazón quemados"),
    ("chrysler_b", 468, 470, "ciudad", "Chrysler de noche (después del corazón)", ""),
    ("flatiron", 471, 485, "ciudad", "Flatiron con bus y estelas de luz", ""),
    ("metlife", 486, 493, "aerea", "Aérea MetLife", "desde 494 entra la O cromada"),
]

# ---------------------------------------------------------------- EDL
# Cada segmento cubre los frames de salida [out0, out1). Fuente: src0 + (n - out0) * speed.
# zoom: [inicio, fin] (Ken Burns), center: punto de la fuente que queda en el centro,
# punch: punch-in 1,00 -> 1,06 en 4 frames al entrar el corte.
SEGMENTS = [
    # 0: portada (miniatura de WhatsApp). Fondo bokeh fijo; el texto lo pone Remotion.
    dict(out=[0, 1], shot="bokeh", src=161, speed=0, zoom=[1.15, 1.15], status="nuevo", note="portada: bokeh fijo"),
    dict(out=[1, 17], shot="crystals", src=1, status="limpio"),
    # Tramo 2 (Bloque A)
    dict(out=[17, 33], shot="street", src=17, path="pingpong", zoom=[1.0, 1.06], status="reconstruido",
         note="calle: 4 frames limpios en ida y vuelta a 0,5x"),
    dict(out=[33, 45], shot="metlife", src=486, speed=8 / 12, mirror=True, rotate=-8, zoom=[1.32, 1.4], punch=True,
         status="reconstruido", note="avenida aérea en diagonal -> MetLife espejada y rotada"),
    dict(out=[45, 60], shot="car_smoke", src=417, speed=12 / 15, mirror=True, zoom=[1.12, 1.18], status="reconstruido",
         note="vapor -> humo del auto, espejado"),
    dict(out=[60, 74], shot="flatiron", src=471, speed=1.0, mirror=True, zoom=[1.12, 1.2], punch=True,
         status="reconstruido", note="avenida con skyline -> Flatiron espejado"),
    dict(out=[74, 88], shot="radio_city", src=429, speed=11 / 14, zoom=[1.08, 1.14], status="reconstruido",
         note="marquesina con cartel vertical -> Radio City"),
    dict(out=[88, 100], shot="bokeh", src=158, speed=9 / 12, zoom=[1.2, 1.28], punch=True, status="reconstruido",
         note="bola de espejos -> bokeh"),
    dict(out=[100, 114], shot="chrysler", src=459, speed=4 / 13, zoom=[1.05, 1.22], center=[0.5, 0.42],
         status="reconstruido", note="vista cenital -> Chrysler con push-in lento"),
    # Tramo 3-5: limpio
    dict(out=[114, 210], shot="orig", src=114, status="limpio", note="DJ, multitud, flash, bokeh, manos, manuscritos, VHS"),
    # Tramo 6 (Bloque B)
    dict(out=[210, 226], shot="neon", src=210, speed=9 / 16, status="reconstruido",
         note="neón: los 9 frames limpios estirados a 16"),
    dict(out=[226, 238], shot="hands", src=171, speed=11 / 12, mirror=True, zoom=[1.15, 1.2], punch=True,
         status="reconstruido", note="bola de espejos -> destellos sobre la multitud (oscuro, como la bola), espejado"),
    dict(out=[238, 251], shot="flash", src=141, speed=1.0, mirror=True, zoom=[1.1, 1.14], status="reconstruido",
         note="panel LED que se quema -> flash que quema, espejado"),
    dict(out=[251, 264], shot="bokeh", src=159, speed=4 / 12, mirror=True, zoom=[1.3, 1.36], punch=True,
         status="reconstruido", note="bokeh con cartel -> bokeh espejado"),
    dict(out=[264, 278], shot="black", status="reconstruido", note="doodles sobre negro (doodles recreados en Remotion)"),
    dict(out=[278, 295], shot="vhs", src=202, speed=8 / 17, mirror=True, zoom=[1.05, 1.1], status="reconstruido",
         note="collage VHS -> collage de 6,73 espejado a 0,47x"),
    dict(out=[295, 306], shot="stage", src=128, speed=1.0, mirror=True, zoom=[1.25, 1.3], center=[0.5, 0.66],
         status="reconstruido", note="panel de luces -> luces del escenario arriba, siluetas detrás de la fecha"),
    # Tramo 7: limpio, con fantasmas de MADERO TANGO a la izquierda desde 329
    dict(out=[306, 329], shot="orig", src=306, status="limpio"),
    dict(out=[329, 350], shot="orig", src=329, ghosts=True, status="limpio+fantasmas",
         note="doodles originales; se rellenan los contornos tenues de MADERO TANGO"),
    # Tramo 8 (Bloque C)
    dict(out=[350, 374], shot="flatiron", src=471, speed=15 / 24, zoom=[1.3, 1.45], center=[0.5, 0.62], punch=True,
         status="reconstruido", note="Grand Central con estelas -> estelas del Flatiron"),
    dict(out=[374, 387], shot="radio_city", src=429, speed=11 / 13, mirror=True, zoom=[1.5, 1.56], center=[0.5, 0.42],
         status="reconstruido", note="edificio con ventanas -> ventanas de Radio City, espejado"),
    dict(out=[387, 402], shot="black", status="reconstruido", note="cristales sobre negro (cristales en la capa de overlay)"),
    dict(out=[402, 417], shot="street", src=17, path="pingpong", mirror=True, zoom=[1.06, 1.0], status="reconstruido",
         note="calle con faros: 4 frames limpios en ida y vuelta, espejada"),
    # Tramo 9: limpio
    dict(out=[417, 486], shot="orig", src=417, status="limpio"),
    # Tramo 10 (Bloque D)
    dict(out=[486, 497], shot="metlife", src=486, speed=8 / 11, status="reconstruido",
         note="aérea MetLife: los 8 frames limpios estirados a 11 (la O vieja asoma desde 494)"),
    dict(out=[497, 512], shot="car_smoke", src=417, speed=12 / 15, zoom=[1.25, 1.3], center=[0.42, 0.5], punch=True,
         status="reconstruido", note="humo -> humo del auto"),
    dict(out=[512, 526], shot="chrysler", src=459, speed=4 / 13, mirror=True, zoom=[1.0, 1.08], center=[0.5, 0.55],
         status="reconstruido", note="avenida con skyline y Chrysler -> Chrysler espejado"),
    dict(out=[526, 540], shot="radio_city", src=429, speed=11 / 14, mirror=True, zoom=[1.18, 1.24], center=[0.5, 0.6],
         status="reconstruido", note="marquesina -> Radio City espejado"),
    dict(out=[540, 554], shot="metlife", src=486, speed=8 / 14, mirror=True, zoom=[1.3, 1.42], center=[0.5, 0.6], punch=True,
         status="reconstruido", note="cenital -> MetLife espejada"),
    dict(out=[554, 567], shot="dj", src=114, speed=1.0, zoom=[1.06, 1.08], status="reconstruido",
         note="bandeja de DJ: el mismo plano que en 3,80"),
    dict(out=[567, 581], shot="flash", src=141, speed=1.0, zoom=[1.6, 1.68], center=[0.72, 0.28], punch=True, gain=0.85, status="reconstruido",
         note="brindis a contraluz -> flash con copa a contraluz"),
    dict(out=[581, 583], shot="flash", src=154, speed=0, zoom=[1.68, 1.68], center=[0.72, 0.28], smear=True, gain=0.85, status="reconstruido",
         note="smear vertical de salida"),
    # Tramo 11-13: negro (flash, light leak, monograma, cristales y placa en Remotion)
    dict(out=[583, TOTAL], shot="black", status="nuevo"),
]


# Capa de cristales (screen sobre todo): instancias del clip de cristales de la intro.
CRYSTALS = [
    # Bloque C, 12,90-13,37: cristales que pasan por delante del texto
    dict(out=[387, 402], src=1, speed=1.0, mirror=True, zoom=[1.1, 1.18], center=[0.5, 0.48]),
    # Bloque E, 20,0-21,9: cada vez más densos hasta tapar casi todo
    dict(out=[598, 657], src=1, speed=15 / 58, zoom=[1.0, 1.1], center=[0.5, 0.5]),
    dict(out=[615, 657], src=1, speed=15 / 41, mirror=True, zoom=[1.5, 1.65], center=[0.46, 0.45], opacity=0.95),
    dict(out=[630, 657], src=3, speed=13 / 26, zoom=[2.2, 2.45], center=[0.56, 0.56], opacity=0.7),
    dict(out=[642, 657], src=7, speed=9 / 14, mirror=True, zoom=[3.0, 3.3], center=[0.5, 0.58], opacity=0.6),
]
# Bloque F, 21,90-22,13: los últimos cristales se despejan hacia abajo
CRYSTALS_CLEAR = dict(out=[657, 664], hold=656, drop=0.9)


def frame_map():
    times = [float(x) for x in (ROOT / "analysis/frame_times.txt").read_text().split()]
    m = {round(t * FPS): i + 1 for i, t in enumerate(times)}
    for n in range(657):
        if n not in m:
            m[n] = m[n - 1]
    return m


def main():
    fm = frame_map()
    pool = []
    for sid, a, b, typ, desc, note in POOL:
        lum = [cv2.imread(str(ROOT / f"analysis/frames/f{fm[n]:04d}.png"), 0).mean() for n in range(a, b + 1)]
        pool.append(dict(id=sid, start=a, end=b, t0=round(a / FPS, 3), t1=round((b + 1) / FPS, 3), frames=b - a + 1,
                         type=typ, description=desc, notes=note, meanLuma=round(float(np.mean(lum)), 1)))
    (ROOT / "analysis/clean_pool.json").write_text(json.dumps(pool, ensure_ascii=False, indent=1))

    # cada segmento lee solo dentro de su plano limpio (la cámara lenta mezcla frames vecinos)
    ranges = {sid: (a, b) for sid, a, b, *_ in POOL}
    for s in SEGMENTS:
        if s["shot"] in ranges:
            s["srcMax"] = ranges[s["shot"]][1]
        elif s["shot"] == "orig":
            s["srcMax"] = s["src"] + (s["out"][1] - s["out"][0]) - 1
    # validar cobertura continua
    pos = 0
    for s in SEGMENTS:
        assert s["out"][0] == pos, (pos, s)
        pos = s["out"][1]
    assert pos == TOTAL
    out = ROOT / "src/data"
    out.mkdir(parents=True, exist_ok=True)
    (out / "plates.json").write_text(json.dumps({"fps": FPS, "total": TOTAL, "segments": SEGMENTS, "crystals": CRYSTALS, "crystalsClear": CRYSTALS_CLEAR}, ensure_ascii=False, indent=1))
    print("pool", len(pool), "segmentos", len(SEGMENTS))


if __name__ == "__main__":
    main()
