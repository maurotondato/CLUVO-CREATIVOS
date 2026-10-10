# CLUVO · Creativos

## Reel de ventas (9:16 · 20 s · 1080×1920 · 60 fps)

Archivo final: `entregables/CLUVO_reel_ventas_9x16.mp4`

### Guion

| Tiempo | Escena | Voz en off (es-AR-TomasNeural) |
|---|---|---|
| 0–3 s | Hook: "¿Tu club todavía se maneja con planillas y mensajes?" con una planilla con errores y mensajes de WhatsApp que se acumulan | ¿Tu club todavía se maneja con planillas y mensajes? |
| 3–6 s | Revelación de CLUVO. En la app del jugador se elige el día, se toca un turno y llega la confirmación | Con Cluvo, tus socios reservan canchas en segundos, |
| 6–8 s | Inscripción a una clase y a un torneo, con confeti | se anotan a clases y a torneos. |
| 8–12 s | Panel del dueño: caja, stock, pagos online, reportes y más módulos | Y vos controlás todo: caja, stock, pagos y reportes. |
| 12–16.5 s | Tenis → pádel → fútbol → hockey → básquet → vóley. Cada club con su logo, sus colores y su foto | Tenis, pádel, fútbol... se adapta a tu deporte. |
| 16.5–20 s | Cierre: CLUVO, "La gestión de tu club, en un solo lugar.", logo de moctLab y moctlab.com.ar | Cluvo. By Mok Lab. |

### Cómo regenerarlo

```bash
pip install edge-tts numpy scipy pillow
cd audio/vo && python3 ../../video/tts.py           # locución por frase + tiempos por palabra
cd video
python3 audio.py                                    # música original + SFX + pista de voz -> build/
node render.js full 60 build/video_60.mp4           # animación (Playwright) -> frames -> H.264
# mezcla y muxeo: ver video/mix.sh
```

- `video/reel.html` tiene toda la animación. `render(t)` dibuja el fotograma del segundo `t`, así que cada render da exactamente el mismo resultado. Para revisar un instante puntual se puede abrir con `?t=5.4`.
- Las pantallas de la app están recreadas con el diseño real de CLUVO y cargadas con datos de ejemplo.
- La foto de cancha de tenis pertenece al club demo "Hipódromo Tenis". Cada club carga la suya desde Personalización.

## Open Edit (VEED)

El skill [`open-edit`](https://github.com/veedstudio/open-edit) está instalado en `.claude/skills/open-edit/` (y `.agents/skills/` para Codex/Gemini), con el CLI `@veedstudio/openedit-cli` fijado en `package.json`.

```bash
npm install                       # instala el CLI fijado
npx openedit --help               # lista de comandos (render, transcribe, mix-audio, etc.)
```

Cada pieza que se haga con el skill queda en `runs/<key>/` (ignorado en git).

## Wan 2.2 (video con IA)

Hay scripts para generar clips con [Wan2.2](https://github.com/Wan-Video/Wan2.2), ya sea pagando en fal (`wan/fal.sh`) o gratis en una PC con GPU NVIDIA de 24 GB (`wan/instalar-local.sh` y `wan/generar-local.sh`). Ver [`wan/README.md`](wan/README.md).
