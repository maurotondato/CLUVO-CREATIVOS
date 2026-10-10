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
| crystals | 1-16 | 0,03–0,57 | cristales | 14,1 | Cristales/diamantes 3D facetados cayendo sobre negro |  |
| street | 17-20 | 0,57–0,70 | ciudad | 13,8 | Calle de noche con faros (antes de que entre el texto) | solo 4 frames limpios |
| dj | 114-126 | 3,80–4,23 | fiesta | 35,5 | Bandeja de DJ / vinilo |  |
| stage | 127-140 | 4,23–4,70 | luces | 130,1 | Siluetas de multitud con escenario blanco |  |
| flash | 141-155 | 4,70–5,20 | luces | 195,1 | Flash blanco que quema, copa a contraluz | trazo chico tipo '4' abajo a la derecha en 150-151 |
| bokeh | 156-169 | 5,20–5,67 | luces | 41,1 | Bokeh | 167 casi negro |
| hands | 170-182 | 5,67–6,10 | fiesta | 41,5 | Manos arriba con confeti y destellos |  |
| handwriting | 183-201 | 6,10–6,73 | doodle | 52,1 | Frases manuscritas stop motion (we were, Sunshine & Rainbows...) | texto manuscrito del template, no es texto de la invitación |
| vhs | 202-209 | 6,73–7,00 | doodle | 29,8 | Collage de paneles con ruido VHS e íconos |  |
| neon | 210-218 | 7,00–7,30 | luces | 38,6 | Cartel de neón | desde 219 asoman caracteres de la fecha vieja |
| sparklers | 306-318 | 10,20–10,63 | fiesta | 36,3 | Multitud con bengalas |  |
| sparklers_close | 319-326 | 10,63–10,90 | fiesta | 66,2 | Bengalas en primer plano | carita malvada quemada desde 323 |
| scratches | 327-328 | 10,90–10,97 | doodle | 71,1 | Rayas blancas sobre bengalas | desde 329 fantasmas tenues de MADERO TANGO a la izquierda |
| car_smoke | 417-428 | 13,90–14,30 | humo | 48,9 | Auto con humo en la calle |  |
| radio_city | 429-439 | 14,30–14,67 | ciudad | 34,1 | Radio City, cartel vertical | carita malvada quemada desde 440 |
| zoom_city | 442-458 | 14,73–15,30 | ciudad | 52,3 | Zoom blur, ciudad con doodles (carita, calavera, sonrisa, scanlines) | doodles quemados del original |
| chrysler | 459-463 | 15,30–15,47 | ciudad | 24,6 | Chrysler de noche | 464-467 con garabato y corazón quemados |
| chrysler_b | 468-470 | 15,60–15,70 | ciudad | 13,4 | Chrysler de noche (después del corazón) |  |
| flatiron | 471-485 | 15,70–16,20 | ciudad | 91,1 | Flatiron con bus y estelas de luz |  |
| metlife | 486-493 | 16,20–16,47 | aerea | 53,1 | Aérea MetLife | desde 494 entra la O cromada |

## 3. Fondos de los tramos con texto viejo

Se usa el mismo tipo de plano que en el original cuando existe limpio: humo por humo, marquesina por Radio City, DJ por el mismo DJ, cenital y aérea por MetLife. Para variar: espejado, punch-in, Ken Burns, cámara lenta y distintos puntos de entrada. Ningún plano reutilizado cae en dos cortes seguidos (control de repetición del QA).

| Frames | Tiempo (s) | Estado | Fuente | Tratamiento | Nota |
|---|---|---|---|---|---|
| 0-0 | 0,00–0,03 | nuevo | bokeh (161-161) | cuadro fijo, zoom 1.15 | portada: bokeh fijo |
| 1-16 | 0,03–0,57 | limpio | crystals (1-16) |  |  |
| 17-32 | 0,57–1,10 | reconstruido | street (17-20, ida y vuelta) | zoom 1.00→1.06 | calle: 4 frames limpios en ida y vuelta a 0,5x |
| 33-44 | 1,10–1,50 | reconstruido | metlife (486-493) | espejado, 0.67x, zoom 1.32→1.40, rot -8°, punch-in | avenida aérea en diagonal -> MetLife espejada y rotada |
| 45-59 | 1,50–2,00 | reconstruido | car_smoke (417-428) | espejado, 0.80x, zoom 1.12→1.18 | vapor -> humo del auto, espejado |
| 60-73 | 2,00–2,47 | reconstruido | flatiron (471-484) | espejado, zoom 1.12→1.20, punch-in | avenida con skyline -> Flatiron espejado |
| 74-87 | 2,47–2,93 | reconstruido | radio_city (429-439) | 0.79x, zoom 1.08→1.14 | marquesina con cartel vertical -> Radio City |
| 88-99 | 2,93–3,33 | reconstruido | bokeh (158-166) | 0.75x, zoom 1.20→1.28, punch-in | bola de espejos -> bokeh |
| 100-113 | 3,33–3,80 | reconstruido | chrysler (459-463) | 0.31x, zoom 1.05→1.22 | vista cenital -> Chrysler con push-in lento |
| 114-209 | 3,80–7,00 | limpio | original 114-209 |  | DJ, multitud, flash, bokeh, manos, manuscritos, VHS |
| 210-225 | 7,00–7,53 | reconstruido | neon (210-218) | 0.56x | neón: los 9 frames limpios estirados a 16 |
| 226-237 | 7,53–7,93 | reconstruido | hands (171-181) | espejado, 0.92x, zoom 1.15→1.20, punch-in | bola de espejos -> destellos sobre la multitud (oscuro, como la bola), espejado |
| 238-250 | 7,93–8,37 | reconstruido | flash (141-153) | espejado, zoom 1.10→1.14 | panel LED que se quema -> flash que quema, espejado |
| 251-263 | 8,37–8,80 | reconstruido | bokeh (159-163) | espejado, 0.33x, zoom 1.30→1.36, punch-in | bokeh con cartel -> bokeh espejado |
| 264-277 | 8,80–9,27 | reconstruido | negro |  | doodles sobre negro (doodles recreados en Remotion) |
| 278-294 | 9,27–9,83 | reconstruido | vhs (202-209) | espejado, 0.47x, zoom 1.05→1.10 | collage VHS -> collage de 6,73 espejado a 0,47x |
| 295-305 | 9,83–10,20 | reconstruido | stage (128-138) | espejado, zoom 1.25→1.30 | panel de luces -> luces del escenario arriba, siluetas detrás de la fecha |
| 306-328 | 10,20–10,97 | limpio | original 306-328 |  |  |
| 329-349 | 10,97–11,67 | limpio+fantasmas | original 329-349 | borrado de fantasmas | doodles originales; se rellenan los contornos tenues de MADERO TANGO |
| 350-373 | 11,67–12,47 | reconstruido | flatiron (471-485) | 0.62x, zoom 1.30→1.45, punch-in | Grand Central con estelas -> estelas del Flatiron |
| 374-386 | 12,47–12,90 | reconstruido | radio_city (429-439) | espejado, 0.85x, zoom 1.50→1.56 | edificio con ventanas -> ventanas de Radio City, espejado |
| 387-401 | 12,90–13,40 | reconstruido | negro |  | cristales sobre negro (cristales en la capa de overlay) |
| 402-416 | 13,40–13,90 | reconstruido | street (17-20, ida y vuelta) | espejado, zoom 1.06→1.00 | calle con faros: 4 frames limpios en ida y vuelta, espejada |
| 417-485 | 13,90–16,20 | limpio | original 417-485 |  |  |
| 486-496 | 16,20–16,57 | reconstruido | metlife (486-493) | 0.73x | aérea MetLife: los 8 frames limpios estirados a 11 (la O vieja asoma desde 494) |
| 497-511 | 16,57–17,07 | reconstruido | car_smoke (417-428) | 0.80x, zoom 1.25→1.30, punch-in | humo -> humo del auto |
| 512-525 | 17,07–17,53 | reconstruido | chrysler (459-463) | espejado, 0.31x, zoom 1.00→1.08 | avenida con skyline y Chrysler -> Chrysler espejado |
| 526-539 | 17,53–18,00 | reconstruido | radio_city (429-439) | espejado, 0.79x, zoom 1.18→1.24 | marquesina -> Radio City espejado |
| 540-553 | 18,00–18,47 | reconstruido | metlife (486-493) | espejado, 0.57x, zoom 1.30→1.42, punch-in | cenital -> MetLife espejada |
| 554-566 | 18,47–18,90 | reconstruido | dj (114-126) | zoom 1.06→1.08 | bandeja de DJ: el mismo plano que en 3,80 |
| 567-580 | 18,90–19,37 | reconstruido | flash (141-154) | zoom 1.60→1.68, punch-in, ganancia 0.85 | brindis a contraluz -> flash con copa a contraluz |
| 581-582 | 19,37–19,43 | reconstruido | flash (154-154) | cuadro fijo, zoom 1.68, smear vertical, ganancia 0.85 | smear vertical de salida |
| 583-707 | 19,43–23,60 | nuevo | negro |  |  |

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

Corrido con `python scripts/qa.py output/save_the_date_PIA_1080x1920.mp4` sobre el render final (708 frames). Los detalles están en `qa/qa_report.json`.

1. **Comparativa lado a lado:** `qa/side_by_side.mp4` y `qa/sheets/` (cada 0,125 s, por bloque). Las revisé una por una e iteré sobre estos puntos: los contornos con las curvas internas de la fuente variable (pasaron a filtros SVG sobre el alfa), la legibilidad de la fecha sobre el blanco que quema, la perspectiva y el interlineado del bloque C, la velocidad de los flips y de la apertura de la franja, el tamaño del monograma y el light leak.
2. **Cero texto viejo:**
   - **Por construcción:** ningún frame del fondo lee frames del original con texto viejo. El control de procedencia recorre el EDL, incluida la mezcla entre frames vecinos de la cámara lenta, y da `frames_con_fuente_sucia = {}`. La única excepción son los frames 329–349, con los fantasmas borrados (sección 3).
   - **OCR:** 2 coincidencias en 708 frames, las dos falsos positivos que revisé a ojo: un "28" leído en la textura de ventanas de MetLife (frame 35) y otro en un destello de las manos con confeti (frame 175, que es un frame original limpio). Cero lecturas de ONA, MADERO, TANGO, Lombardi u OL.
   - **A ojo:** sin restos en los tramos rojos ni en 10,97–11,67.
3. **Tilde de PÍA:** `qa/tilde.jpg` muestra la portada, el bloque A, los frames 505 a 516 (el flip de la Í y de la A) y la franja. La tilde entra con la letra y nunca se recorta ni queda tapada por la franja.
4. **Sincronía:** los 37 cortes del fondo caen en el mismo frame que en el original (diferencia 0). 36 se detectaron en el render; el de 402 es entre dos planos casi negros y se verificó contra el EDL. Contra la grilla de beats ajustada a los cortes (período 0.4528 s), el original ya se desvía hasta ±3,4 frames; esa desviación se conserva tal cual.

| Corte original (frame) | t (s) | Corte nuevo | Diferencia (frames) | Desvío del original respecto de la grilla de beats (frames) |
|---|---|---|---|---|
| 17 | 0,57 | 17 | +0 | +3,2 |
| 33 | 1,10 | 33 | +0 | -1,2 |
| 45 | 1,50 | 45 | +0 | -2,8 |
| 60 | 2,00 | 60 | +0 | -1,4 |
| 74 | 2,47 | 74 | +0 | -1,0 |
| 88 | 2,93 | 88 | +0 | -0,5 |
| 100 | 3,33 | 100 | +0 | -2,1 |
| 114 | 3,80 | 114 | +0 | -1,7 |
| 127 | 4,23 | 127 | +0 | -2,3 |
| 141 | 4,70 | 141 | +0 | -1,9 |
| 156 | 5,20 | 156 | +0 | -0,5 |
| 170 | 5,67 | 170 | +0 | -0,0 |
| 183 | 6,10 | 183 | +0 | -0,6 |
| 210 | 7,00 | 210 | +0 | -0,8 |
| 226 | 7,53 | 226 | +0 | +1,6 |
| 238 | 7,93 | 238 | +0 | +0,0 |
| 251 | 8,37 | 251 | +0 | -0,5 |
| 264 | 8,80 | 264 | +0 | -1,1 |
| 278 | 9,27 | 278 | +0 | -0,7 |
| 295 | 9,83 | 295 | +0 | +2,7 |
| 306 | 10,20 | 306 | +0 | +0,1 |
| 319 | 10,63 | 319 | +0 | -0,5 |
| 350 | 11,67 | 350 | +0 | +3,4 |
| 374 | 12,47 | 374 | +0 | +0,2 |
| 387 | 12,90 | 387 | +0 | -0,4 |
| 402 | 13,40 | 402 | +0 | +1,0 |
| 417 | 13,90 | 417 | +0 | +2,5 |
| 429 | 14,30 | 429 | +0 | +0,9 |
| 442 | 14,73 | 442 | +0 | +0,3 |
| 471 | 15,70 | 471 | +0 | +2,1 |
| 486 | 16,20 | 486 | +0 | -3,3 |
| 497 | 16,57 | 497 | +0 | +0,9 |
| 512 | 17,07 | 512 | +0 | +2,4 |
| 526 | 17,53 | 526 | +0 | +2,8 |
| 540 | 18,00 | 540 | +0 | +3,2 |
| 554 | 18,47 | 554 | +0 | -3,2 |
| 567 | 18,90 | 567 | +0 | +3,0 |

5. **Repetición de planos:** ningún plano reutilizado aparece en dos cortes consecutivos. Usos de cada plano del pool en los tramos reconstruidos (siempre con encuadre distinto: espejado, zoom, centro o velocidad): bokeh ×3, crystals ×1, street ×2, metlife ×3, car_smoke ×2, flatiron ×2, radio_city ×3, chrysler ×2, neon ×1, hands ×1, flash ×3, vhs ×1, stage ×1, dj ×1.
6. **Exports:**
   - 1080×1920: H.264 High, yuv420p, 30 fps, CRF 16, AAC 192 kbps 44,1 kHz, 23,6 s, 47,6 MB.
   - WhatsApp: 720×1280, 12,2 MB.
   - Póster en 20,5 s.
   - Audio: el original sin tocar (comparado muestra por muestra contra el decodificado del original: diferencia 0), silencio después de los 21,9 s y un shimmer a −24 dBFS en 22,1 s.

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
