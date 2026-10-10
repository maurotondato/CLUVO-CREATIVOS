# Save the Date XV · PÍA: reporte

Réplica de la invitación original ("Save the Date" de XV, 21,9 s, 9:16, B/N nocturno) con los textos nuevos y una placa final de M·DATOS. Mismo ritmo, mismos cortes y mismo audio que el original. Cambian los textos y el cierre.

| Archivo | Qué es |
|---|---|
| `output/save_the_date_PIA_1080x1920.mp4` | 1080×1920, H.264 High, yuv420p, 30 fps, CRF 16, preset slow, AAC 192 kbps 44,1 kHz, faststart, 23,6 s |
| `output/save_the_date_PIA_whatsapp.mp4` | 720×1280, menos de 16 MB |
| `output/poster.jpg` | monograma a los 20,5 s |
| `qa/side_by_side.mp4` | original (izquierda) contra nuevo (derecha), los dos a 1080×1920 |
| `qa/sheets/*.jpg` | comparativas cada 0,125 s por bloque |
| `qa/tilde.jpg` | la Í en el bloque A, en cada paso del flip, en la franja y en la portada |
| `qa/qa_report.json` | procedencia de los fondos, cortes contra el original y los beats, repetición de planos, OCR |

## 1. Análisis del original

- `ffprobe`: 576×1024, 30 fps, 21,9 s, AAC 44,1 kHz estéreo. Trae 656 frames en vez de 657: falta el frame de 0,833 s (n.º 25). Para trabajar a 30 fps constantes se repite el 24.
- **El frame 0 es una portada**, distinta del video: "ONA" cromado con la franja SAVE THE DATE sobre bokeh. Es la miniatura que muestra WhatsApp antes de reproducir. Se reconstruyó con PÍA (sección 4).
- Frames y hojas de contacto: `analysis/frames/` (no se versiona, se regenera) y `analysis/sheets/`.
- Beats (`analysis/beats.json`): librosa da 132,5 BPM, con un beat cada 0,4535 s. Los cortes del original siguen una grilla de unos 131 BPM, con una fase unos 4 frames antes de los beats que marca librosa. Ese desfase es del original y se conserva tal cual, porque se respetan sus cortes cuadro por cuadro.
- Cortes medidos por diferencia entre frames: `analysis/framediff.json`.
- OCR del original: `analysis/ocr_original.json`.

### Timeline maestro medido (frames a 30 fps)

Donde mi medición difiere del brief, manda el original. Las diferencias son de 1 a 6 frames.

| # | Tiempo (s) | Frames | Qué pasa |
|---|---|---|---|
| 0 | 0,00 | 0 | Portada (miniatura) |
| 1 | 0,03–0,57 | 1–16 | Cristales cayendo, limpio |
| 2 · A | 0,57–3,80 | 17–113 | La calle entra en 0,57 (el brief decía 0,70). El texto entra en 0,70 con glitch y queda fijo en 0,90. Cortes: 17, 33 (1,10), 45 (1,50), 60 (2,00), 74 (2,47), 88 (2,93), 100 (3,33) |
| 3–4 | 3,80–7,00 | 114–209 | DJ, multitud, flash, bokeh, manos, manuscritos, VHS. Limpio |
| 5 | 7,00–7,53 | 210–225 | Neón (empieza en 7,00, no en 6,90). Desde 7,30 asoman los primeros caracteres de la fecha |
| 6 · B | 7,53–10,20 | 226–305 | Cortes: 226 (bola), 238 (LED que quema), 251 (bokeh), 264 (doodles), 278 (VHS), 295 (LED). Doodles: < X X > en 8,80, lamparita en 8,90, negro en 9,03, dibujito en 9,07, mancha en 9,13 y garabato en 9,23 |
| 7 | 10,20–11,67 | 306–349 | Bengalas y doodles quemados (carita 10,77, calavera 11,03, sonrisa 11,13, scanlines 11,27, tacos 11,40, garabato 11,57, corazón 11,63). Desde 10,97 hay fantasmas de MADERO TANGO a la izquierda |
| 8 · C | 11,67–13,90 | 350–416 | Grand Central en 11,67. El texto sólido entra en 12,03 (no 11,95). Ventanas en 12,47, cristales en 12,90, calle en 13,40 |
| 9 | 13,90–16,20 | 417–485 | Limpio, con doodles quemados del original |
| 10 · D | 16,20–19,37 | 486–580 | Letras en 16,47, 16,83 y 17,20 (cada 11 frames, no una por beat). Franja de 18,17 a 18,50, abriéndose **desde el centro** |
| 11 | 19,37–19,53 | 581–585 | Smear en 581 y flash con light leak de 582 a 585 |
| 12 · E | 19,53–21,90 | 586–656 | El monograma aparece en 19,53 sobre el resto cálido del leak. Puntos en 587, estiramiento de 588 a 590, nítido desde 591. Cristales desde 19,93 |
| 13 · F | 21,90–23,60 | 657–707 | Placa M·DATOS (nueva) |

## 2. Clean pool (`analysis/clean_pool.json`)

Rangos sin texto viejo, validados con OCR (sin coincidencias en ninguno, salvo un falso positivo "28" en la textura de MetLife, frame 491) y con hojas de contacto.

| Plano | Frames | Tiempo (s) | Tipo | Luma media | Descripción | Notas |
|---|---|---|---|---|---|---|
POOL_TABLE

## 3. Fondos de los tramos con texto viejo

Se usa el mismo tipo de plano que en el original cuando existe limpio: humo por humo, marquesina por Radio City, DJ por el mismo DJ, cenital y aérea por MetLife. Para variar: espejado, punch-in, Ken Burns, cámara lenta y distintos puntos de entrada. Ningún plano reutilizado cae en dos cortes seguidos (control de repetición del QA).

| Frames | Tiempo (s) | Estado | Fuente | Tratamiento | Nota |
|---|---|---|---|---|---|
EDL_TABLE

Todos los fondos pasan por el mismo look: escala de grises, curva de contraste en S con negros aplastados y blancos que queman, escalado 576→1080 con lanczos y unsharp suave. El grano animado (cada frame) y la viñeta los suma Remotion arriba de todo.

### Último recurso

- **Fantasmas de MADERO TANGO, 10,97–11,63 (frames 329–349):** los contornos tenues del pre-roll viejo se borran con una mediana fuerte, aplicada solo en la zona de los fantasmas (66 % izquierdo, 25–82 % del alto) y fuera de los trazos blancos de los doodles, con máscara suave. Así se conservan la calavera, la sonrisa, las scanlines, los tacos, el garabato y el corazón originales. Encima va el pre-roll nuevo de JANOS COSTANERA II, tenue y desenfocado, como en el original.
- **Planos muy cortos estirados en cámara lenta:** calle (4 frames en ida y vuelta a 0,5x), neón (9 frames llevados a 16), Chrysler (0,31x), collage VHS (0,47x) y bokeh (0,33x). Los frames intermedios salen de mezclar vecinos. Cada plano lee solo dentro de su rango limpio (`srcMax`).
- **No se usó recorte de banda ni `delogo`** en ningún tramo.

## 4. Bloques de texto

| Bloque | Implementación | Diferencias con el brief y motivo |
|---|---|---|
| Portada (frame 0) | PÍA cromado con la franja SAVE THE DATE sobre bokeh, igual a la miniatura original | El brief no la menciona; el original la tiene |
| A | Montserrat 800, SAVE THE DATE ajustado de borde a borde (fitText), centro en y = 46,8 %. PÍA en contorno (anillo de alfa con filtro SVG) en y = 53,4 %. Entrada con glitch de 6 a 14 rebanadas (21–26), glitch en los cortes 45, 74 y 100 | Separación entre líneas medida en el original (≈0,55× la altura de mayúscula, no 0,3×) |
| B | 3 filas de 06.03.27 en y = 40,5 / 49 / 57,5 %, con números tabulares. La del medio va rellena con bisel; las otras dos en contorno con halo oscuro, para que se lean cuando el fondo quema a blanco. Cada carácter aparece en orden aleatorio con un pop de 2 frames; los 4 primeros, tenues sobre el neón. Micro-jitter de 1 px en los cortes. Doodles recreados en SVG con borde de pincel (turbulencia) y boil cada 2 frames | Tamaño medido: la cifra mide ≈6 % del alto (el brief decía 4,5 %). Doodles en los tiempos del original |
| C | 5 líneas de JANOS COSTANERA II, Montserrat 800, con perspectiva rotateY(−10°) rotateZ(−3°) y temblor de ±2 px y ±0,4° cada 2 frames. Alternancia relleno/contorno por plano. Las rellenas tienen una extrusión corta como el original. Pre-roll tenue desde 10,97, eco que se enfoca de 12,03 a 12,47 y cristales en screen por delante de 12,90 a 13,37 | El texto es 50 % más largo que MADERO TANGO: ocupa ≈88 % del ancho con mayúsculas de ≈3 % del alto (el original tenía ≈4 %). Interlineado de 1,45 veces el tamaño de fuente, para cubrir la misma altura que el bloque original |
| D | PÍA en Montserrat 900 con escala horizontal ×1,1 y mayúscula de ≈14,5 % del alto. Cromado con gradiente y banda oscura de horizonte, bisel interno (filtro SVG), sombra proyectada y brillo especular cada 1,5 s. Flip 3D desde la base: arranque lento, final rápido y un rebote leve de 11 frames. La Í entra con su tilde. Franja oscura con SAVE THE DATE en Montserrat 600 y tracking 0,25 em | La franja se abre **desde el centro** (primero asoma "THE"), como el original, no como máquina de escribir. Los tiempos de las letras son los medidos |
| Salida D + leak | Smear vertical de 2 frames (desenfoque SVG direccional). Flash blanco con arcoíris espectral en multiply y resto cálido | Duración del leak medida: 582–585 |
| E | P en Cormorant Garamond 500 (≈19 % del alto), Pía en Allura cruzando el tercio medio en diagonal ascendente, FIFTEEN en Montserrat 500 con tracking 0,45 em. Fondo cálido en 586, puntos tenues desde 587, estiramiento horizontal con motion blur (588–590). Cristales: el clip de la intro en 4 capas (velocidades de 0,26x a 0,64x, espejadas y a distintas escalas) en screen, cada vez más densas | El conjunto ocupa ≈50 % del ancho |
| F | Logo M·DATOS recortado a su caja (62 % del ancho, y = 46 %), "Invitación digital creada por" arriba, www.mdatos.com.ar abajo con glitch de 2 frames al entrar. Los cristales se despejan hacia abajo (21,90–22,13). Fundido a negro en los últimos 9 frames. Shimmer sintetizado a −24 dBFS cuando entra el logo | El logo mantiene sus colores de marca: es el único color además del leak |

Efectos globales: punch-in de 1,00 a 1,06 en 4 frames en los cortes marcados (en el fondo); glitches de 1 a 2 frames en corcheas acentuadas (onsets fuertes, como máximo uno por segundo) alternando rebanadas, bloques y scanlines; flash blanco de 1 frame en 4,23, 7,93 y 13,90.

### Fuentes

Montserrat, Cormorant Garamond y Allura de Google Fonts. Son exactamente los woff2 que carga `@remotion/google-fonts` (mismas URLs y versiones). `scripts/fetch_fonts.mjs` los baja a `public/fonts/` y se cargan locales con `@remotion/fonts`: el Chrome headless de Remotion no confía en la CA del proxy de este entorno, y así además el render no depende de la red. La Í (U+00CD) y la í (U+00ED) están en el subset latin de las tres fuentes.

### Lo que no se hizo

- *Nice to have* del bloque A: que el cartel vertical de la marquesina pase por delante del texto con máscara por luma. En la reconstrucción la marquesina es Radio City, cuyo cartel queda a los costados del texto.

## 5. QA

QA_SECTION

## 6. Cómo hacer otra invitación

1. Editar `invitation.config.json`: nombre, fecha (formato DD.MM.AA), salón, inicial y script del monograma, logo y URL.
2. `npm run build` (corre `scripts/build_all.sh`). Necesita Node 20+, ffmpeg, Python 3.12 (con `uv` o venv) y tesseract para el QA. El render tarda unos 25 minutos con 4 núcleos.
3. Los videos quedan en `output/` con el nombre en mayúsculas sin tildes (por ejemplo `save_the_date_PIA_1080x1920.mp4`).

Notas para reutilizar:

- SAVE THE DATE y el salón se ajustan solos al ancho (`fitText`). Un salón muy largo achica la letra.
- El nombre cromado anima una letra cada 11 frames. Con más de 3 letras, las siguientes siguen el mismo ritmo. Un nombre de más de 5 o 6 letras conviene probarlo con `node scripts/stills.mjs qa/stills 530 575`.
- Los fondos sin texto no dependen de la config: solo se regeneran si cambia el video original.
- Para revisar frames sueltos: `node scripts/stills.mjs <carpeta> <frame> [...]` y `python scripts/compare.py <carpeta> salida.jpg <frames...>`.

| Script | Qué hace |
|---|---|
| `scripts/plates_edl.py` | Clean pool y EDL de fondos y cristales |
| `scripts/build_plates.py` | Renderiza `public/plates.mp4` y `public/crystals.mp4` |
| `scripts/fetch_fonts.mjs`, `scripts/make_grain.py`, `scripts/prepare_logo.py` | Fuentes locales, texturas de grano, recorte del logo |
| `src/` | Composición de Remotion (`timeline.ts` tiene todos los tiempos) |
| `scripts/make_audio.py` | Audio original sin tocar, silencio y shimmer |
| `scripts/export.sh` | Exports y póster |
| `scripts/qa.py`, `scripts/ocr_scan.py`, `scripts/compare.py` | QA |
