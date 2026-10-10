import React from 'react';
import {AbsoluteFill, OffthreadVideo, random, staticFile, useCurrentFrame} from 'remotion';
import {FLASHES, GLITCHES, H, W} from '../timeline';

export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const easeOut = (x: number) => 1 - Math.pow(1 - clamp01(x), 3);
export const easeOutBack = (x: number) => {
	const c1 = 1.9;
	const c3 = c1 + 1;
	const t = clamp01(x);
	return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
};

// Métrica de Montserrat (unitsPerEm 1000, ascender 968, descender -251, capHeight 700):
// con line-height 1, el centro de las mayúsculas queda a 0,5085 em del borde superior de la caja.
export const MONT_CAP_CENTER = 0.5085;
export const MONT_CAP = 0.7;

export const Plates: React.FC = () => (
	<AbsoluteFill>
		<OffthreadVideo src={staticFile('plates.mp4')} muted style={{width: W, height: H}} />
	</AbsoluteFill>
);

export const Crystals: React.FC = () => (
	<AbsoluteFill style={{mixBlendMode: 'screen'}}>
		<OffthreadVideo src={staticFile('crystals.mp4')} muted style={{width: W, height: H}} />
	</AbsoluteFill>
);

/** Rebanadas horizontales desplazadas: el mismo contenido repetido y recortado por bandas. */
export const Slices: React.FC<{
	seed: string;
	bands: number;
	maxShift: number;
	minShift?: number;
	dropout?: number; // probabilidad de que una banda desaparezca
	children: React.ReactNode;
}> = ({seed, bands, maxShift, minShift = 0, dropout = 0, children}) => {
	const cuts = [0];
	for (let i = 1; i < bands; i++) cuts.push(random(`${seed}-c${i}`));
	cuts.push(1);
	cuts.sort((a, b) => a - b);
	return (
		<>
			{cuts.slice(0, -1).map((top, i) => {
				const bottom = cuts[i + 1];
				if (random(`${seed}-d${i}`) < dropout) return null;
				const r = random(`${seed}-s${i}`) * 2 - 1;
				const shift = Math.sign(r) * (minShift + Math.abs(r) * (maxShift - minShift));
				const moved = random(`${seed}-m${i}`) < 0.65;
				return (
					<AbsoluteFill
						key={i}
						style={{
							clipPath: `inset(${(top * 100).toFixed(3)}% -20% ${((1 - bottom) * 100).toFixed(3)}% -20%)`,
							transform: `translateX(${moved ? shift : 0}px)`,
						}}
					>
						{children}
					</AbsoluteFill>
				);
			})}
		</>
	);
};

/** Glitches globales de 1-2 frames (rebanadas, bloques de ruido o scanlines blancas). */
export const GlitchFrame: React.FC<{children: React.ReactNode}> = ({children}) => {
	const frame = useCurrentFrame();
	const g = GLITCHES.find((x) => frame >= x.frame && frame < x.frame + x.len);
	if (!g) return <AbsoluteFill>{children}</AbsoluteFill>;
	const seed = `glitch-${frame}`;
	if (g.kind === 'slices') {
		return (
			<AbsoluteFill>
				<Slices seed={seed} bands={9} maxShift={70} minShift={12}>
					{children}
				</Slices>
			</AbsoluteFill>
		);
	}
	if (g.kind === 'blocks') {
		const blocks = Array.from({length: 14}, (_, i) => {
			const w = 60 + random(`${seed}-w${i}`) * 260;
			const h = 14 + random(`${seed}-h${i}`) * 70;
			return {
				x: random(`${seed}-x${i}`) * (W - w),
				y: random(`${seed}-y${i}`) * (H - h),
				w,
				h,
				v: Math.round(random(`${seed}-v${i}`) * 255),
			};
		});
		return (
			<AbsoluteFill>
				{children}
				{blocks.map((b, i) => (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: b.x,
							top: b.y,
							width: b.w,
							height: b.h,
							background: `rgb(${b.v},${b.v},${b.v})`,
							mixBlendMode: i % 2 ? 'difference' : 'normal',
							opacity: 0.85,
						}}
					/>
				))}
			</AbsoluteFill>
		);
	}
	// scanlines: líneas blancas finas que cruzan el cuadro
	return (
		<AbsoluteFill>
			{children}
			{Array.from({length: 11}, (_, i) => (
				<div
					key={i}
					style={{
						position: 'absolute',
						left: 0,
						width: W,
						top: random(`${seed}-l${i}`) * H,
						height: 2 + random(`${seed}-t${i}`) * 4,
						background: 'rgba(255,255,255,0.85)',
						transform: `translateX(${(random(`${seed}-o${i}`) - 0.5) * 120}px)`,
					}}
				/>
			))}
		</AbsoluteFill>
	);
};

export const Flashes: React.FC = () => {
	const frame = useCurrentFrame();
	if (!FLASHES.includes(frame)) return null;
	return <AbsoluteFill style={{background: '#fff', opacity: 0.82}} />;
};

/** Grano fino animado (cambia en cada frame) y viñeta leve. */
export const GrainAndVignette: React.FC = () => {
	const frame = useCurrentFrame();
	const k = Math.floor(random(`grain-k-${frame}`) * 12);
	const ox = Math.round(random(`grain-x-${frame}`) * 400);
	const oy = Math.round(random(`grain-y-${frame}`) * 400);
	return (
		<>
			<AbsoluteFill
				style={{
					mixBlendMode: 'overlay',
					opacity: 0.32,
					backgroundImage: `url(${staticFile(`grain/g${String(k).padStart(2, '0')}.png`)})`,
					backgroundSize: `${W}px ${H}px`,
					backgroundPosition: `${ox}px ${oy}px`,
					backgroundRepeat: 'repeat',
				}}
			/>
			<AbsoluteFill
				style={{
					background: 'radial-gradient(ellipse 75% 62% at 50% 50%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.42) 100%)',
				}}
			/>
		</>
	);
};

const OUTLINES = [
	{id: 'outline-name', r: 1.6, ring: 0.66, fill: 0.09},
	{id: 'outline-date', r: 1.4, ring: 0.62, fill: 0.05},
	{id: 'outline-venue', r: 1.5, ring: 0.85, fill: 0.06},
];
const BEVELS = [
	{id: 'bevel-chrome', r: 3, op: 0.85},
	{id: 'bevel-thin', r: 1.6, op: 0.75},
];

/** Filtros SVG compartidos: smear vertical, motion blur horizontal, contornos y biseles. */
export const SvgFilters: React.FC = () => (
	<svg width={0} height={0} style={{position: 'absolute'}}>
		<defs>
			<filter id="vsmear1" x="-10%" y="-60%" width="120%" height="220%">
				<feGaussianBlur stdDeviation="0 45" />
			</filter>
			<filter id="vsmear2" x="-10%" y="-80%" width="120%" height="260%">
				<feGaussianBlur stdDeviation="0 110" />
			</filter>
			<filter id="hblur1" x="-60%" y="-10%" width="220%" height="120%">
				<feGaussianBlur stdDeviation="16 0" />
			</filter>
			<filter id="hblur2" x="-60%" y="-10%" width="220%" height="120%">
				<feGaussianBlur stdDeviation="34 0" />
			</filter>
			<filter id="hblur3" x="-60%" y="-10%" width="220%" height="120%">
				<feGaussianBlur stdDeviation="8 0" />
			</filter>
			{/* contorno limpio a partir del alfa del texto (sin las curvas superpuestas de la fuente variable) */}
			{OUTLINES.map((o) => (
				<filter key={o.id} id={o.id} x="-5%" y="-20%" width="110%" height="140%">
					<feMorphology in="SourceAlpha" operator="dilate" radius={o.r} result="outer" />
					<feMorphology in="SourceAlpha" operator="erode" radius={o.r} result="inner" />
					<feComposite in="outer" in2="inner" operator="out" result="ring" />
					<feFlood floodColor="#fff" floodOpacity={o.ring} />
					<feComposite in2="ring" operator="in" result="ringC" />
					<feFlood floodColor="#fff" floodOpacity={o.fill} />
					<feComposite in2="SourceAlpha" operator="in" result="fillC" />
					<feMerge>
						<feMergeNode in="fillC" />
						<feMergeNode in="ringC" />
					</feMerge>
				</filter>
			))}
			{/* bisel: borde interno oscuro fino */}
			{BEVELS.map((b) => (
				<filter key={b.id} id={b.id} x="-5%" y="-20%" width="110%" height="140%">
					<feMorphology in="SourceAlpha" operator="erode" radius={b.r} result="er" />
					<feComposite in="SourceAlpha" in2="er" operator="out" result="edge" />
					<feFlood floodColor="#1e1e1e" floodOpacity={b.op} />
					<feComposite in2="edge" operator="in" result="edgeC" />
					<feMerge>
						<feMergeNode in="SourceGraphic" />
						<feMergeNode in="edgeC" />
					</feMerge>
				</filter>
			))}
		</defs>
	</svg>
);
