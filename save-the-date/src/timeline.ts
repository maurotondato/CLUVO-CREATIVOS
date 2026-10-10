// Tiempos maestros en frames @30 fps, medidos sobre el original (analysis/).
// Frame n = n/30 s. El original dura 657 frames (21,9 s); la placa M·DATOS suma hasta 708.

export const FPS = 30;
export const W = 1080;
export const H = 1920;
export const TOTAL = 708;

export const COVER = 0; // portada (miniatura de WhatsApp)

// Bloque A: SAVE THE DATE + PÍA
export const A = {
	in: 21, // entra con glitch
	stable: 27, // queda fijo
	out: 114, // corte seco al DJ
	cuts: [33, 45, 60, 74, 88, 100],
	cutGlitches: [45, 74, 100], // glitch de 1-2 frames en 3 cortes
};

// Bloque B: fecha en 3 filas
export const B = {
	firstChar: 219, // primeros caracteres tenues sobre el neón
	ballCut: 226, // con la bola de espejos entra el resto
	built: 237,
	out: 306,
	cuts: [226, 238, 251, 264, 278, 295],
	burn: [238, 251], // panel que quema a blanco
	doodles: {
		arrows: [264, 267],
		bulb: [267, 271],
		sketch: [272, 274],
		blob: [274, 277],
		scribble: [277, 278],
	},
};

// Bloque C: JANOS COSTANERA II x5
export const C = {
	preroll: [329, 361],
	main: 361,
	echoUntil: 374,
	crystals: [387, 402],
	out: 417,
	cuts: [350, 374, 387, 402],
};

// Bloque D: PÍA cromado + franja SAVE THE DATE
export const D = {
	letters: [494, 505, 516], // P, Í, A: cada una entra con flip 3D
	flip: 10,
	band: [545, 555], // la franja se abre desde el centro
	smear: [581, 583],
	out: 581,
};

// Transición: flash + light leak (el único color del video)
export const LEAK = {flash: 582, until: 586};

// Bloque E: monograma
export const E = {
	in: 586, // aparece sobre el final del leak
	dots: 587,
	stretch: [588, 591],
	stable: 591,
	out: 657,
};

// Bloque F: placa M·DATOS
export const F = {
	in: 657,
	crystalsClear: [657, 664],
	logo: 663,
	logoDur: 12,
	url: 669,
	fadeOut: 699,
	out: TOTAL,
};

// Efectos globales
// Glitch de 1-2 frames en corcheas acentuadas (onsets fuertes de analysis/beats.json), máx. 1 por segundo.
export const GLITCHES: {frame: number; len: number; kind: 'slices' | 'blocks' | 'scanlines'}[] = [
	{frame: 45, len: 2, kind: 'slices'},
	{frame: 74, len: 1, kind: 'scanlines'},
	{frame: 100, len: 2, kind: 'slices'},
	{frame: 139, len: 1, kind: 'blocks'},
	{frame: 193, len: 2, kind: 'slices'},
	{frame: 255, len: 1, kind: 'scanlines'},
	{frame: 324, len: 2, kind: 'slices'},
	{frame: 433, len: 1, kind: 'blocks'},
	{frame: 467, len: 2, kind: 'slices'},
	{frame: 542, len: 1, kind: 'scanlines'},
	{frame: 569, len: 2, kind: 'blocks'},
];

// Flash blanco de 1 frame en cortes clave
export const FLASHES = [127, 238, 417];
