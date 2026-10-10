import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {B, H, W} from '../timeline';

// Doodles de pincel/marcador recreados (los originales quedaban sobre la fecha vieja).
// Borde irregular con turbulencia y animación "boil": el trazo se redibuja cada 2 frames.

type Pt = [number, number];

const jitterPath = (pts: Pt[], seed: string, amp: number) =>
	pts.map(([x, y], i) => [x + (random(`${seed}-x${i}`) - 0.5) * 2 * amp, y + (random(`${seed}-y${i}`) - 0.5) * 2 * amp] as Pt);

const smooth = (pts: Pt[], closed = false) => {
	// curva Catmull-Rom -> Bézier
	const p = closed ? [pts[pts.length - 1], ...pts, pts[0], pts[1]] : [pts[0], ...pts, pts[pts.length - 1]];
	let d = `M ${p[1][0].toFixed(1)} ${p[1][1].toFixed(1)}`;
	for (let i = 1; i < p.length - 2; i++) {
		const [p0, p1, p2, p3] = [p[i - 1], p[i], p[i + 1], p[i + 2]];
		const c1: Pt = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
		const c2: Pt = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
		d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
	}
	return closed ? d + ' Z' : d;
};

const Stroke: React.FC<{d: string; w: number; fill?: boolean}> = ({d, w, fill}) => (
	<path
		d={d}
		fill={fill ? '#fff' : 'none'}
		stroke="#fff"
		strokeWidth={w}
		strokeLinecap="round"
		strokeLinejoin="round"
	/>
);

const CY = 0.49 * H; // centro de la fecha

export const Doodles: React.FC = () => {
	const frame = useCurrentFrame();
	const d = B.doodles;
	const inR = (r: number[]) => frame >= r[0] && frame < r[1];
	const boil = Math.floor(frame / 2);
	const seed = `boil-${boil}`;
	const J = (pts: Pt[], amp: number, k: string) => jitterPath(pts, `${seed}-${k}`, amp);

	let content: React.ReactNode = null;
	let rough = 7;
	if (inR(d.arrows)) {
		// "<  X  X  >" de pincel grueso a los lados y sobre la fecha
		const h = 170;
		content = (
			<g>
				<Stroke d={smooth(J([[150, CY - h], [55, CY], [150, CY + h]], 6, 'lt'))} w={44} />
				<Stroke d={smooth(J([[930, CY - h], [1025, CY], [930, CY + h]], 6, 'gt'))} w={44} />
				<Stroke d={smooth(J([[250, CY - h + 10], [370, CY], [490, CY + h - 10]], 6, 'x1a'))} w={48} />
				<Stroke d={smooth(J([[490, CY - h + 10], [370, CY], [250, CY + h - 10]], 6, 'x1b'))} w={48} />
				<Stroke d={smooth(J([[590, CY - h + 10], [710, CY], [830, CY + h - 10]], 6, 'x2a'))} w={48} />
				<Stroke d={smooth(J([[830, CY - h + 10], [710, CY], [590, CY + h - 10]], 6, 'x2b'))} w={48} />
			</g>
		);
		rough = 12;
	} else if (inR(d.bulb)) {
		// lamparita de línea fina
		const cx = W / 2;
		const top = CY - 150;
		content = (
			<g>
				<Stroke
					d={smooth(
						J(
							[
								[cx - 62, top + 205],
								[cx - 92, top + 120],
								[cx - 78, top + 40],
								[cx, top],
								[cx + 78, top + 40],
								[cx + 92, top + 120],
								[cx + 62, top + 205],
							],
							3,
							'glass',
						),
					)}
					w={7}
				/>
				<Stroke d={smooth(J([[cx - 62, top + 205], [cx - 58, top + 240]], 2, 'n1'))} w={7} />
				<Stroke d={smooth(J([[cx + 62, top + 205], [cx + 58, top + 240]], 2, 'n2'))} w={7} />
				<Stroke d={smooth(J([[cx - 62, top + 245], [cx + 62, top + 245]], 2, 'b1'))} w={7} />
				<Stroke d={smooth(J([[cx - 56, top + 268], [cx + 56, top + 268]], 2, 'b2'))} w={7} />
				<Stroke d={smooth(J([[cx - 44, top + 290], [cx + 44, top + 290]], 2, 'b3'))} w={7} />
				<Stroke d={smooth(J([[cx - 22, top + 312], [cx + 22, top + 312]], 2, 'b4'))} w={7} />
				<Stroke
					d={smooth(J([[cx - 30, top + 205], [cx - 18, top + 120], [cx - 6, top + 150], [cx + 6, top + 120], [cx + 18, top + 150], [cx + 30, top + 205]], 3, 'fil'))}
					w={5}
				/>
			</g>
		);
		rough = 3;
	} else if (inR(d.sketch)) {
		// dibujito chico debajo de la fecha (una tacita)
		const cx = W / 2;
		const y = CY + 150;
		content = (
			<g>
				<Stroke d={smooth(J([[cx - 70, y], [cx - 60, y + 110], [cx + 60, y + 110], [cx + 70, y]], 3, 'cup'))} w={7} />
				<Stroke d={smooth(J([[cx - 74, y], [cx, y - 14], [cx + 74, y], [cx, y + 12]], 3, 'rim'), true)} w={7} />
				<Stroke d={smooth(J([[cx + 66, y + 25], [cx + 112, y + 40], [cx + 104, y + 82], [cx + 62, y + 88]], 3, 'handle'))} w={7} />
				<Stroke d={smooth(J([[cx - 40, y + 45], [cx + 30, y + 75]], 3, 'h1'))} w={6} />
				<Stroke d={smooth(J([[cx - 30, y + 80], [cx + 40, y + 50]], 3, 'h2'))} w={6} />
			</g>
		);
		rough = 3;
	} else if (inR(d.blob)) {
		// mancha blanca chica sobre la fecha
		const cx = W / 2 - 20;
		content = (
			<Stroke
				d={smooth(
					J(
						[
							[cx - 70, CY - 20],
							[cx - 30, CY - 52],
							[cx + 40, CY - 46],
							[cx + 78, CY - 8],
							[cx + 50, CY + 36],
							[cx - 20, CY + 44],
							[cx - 66, CY + 22],
						],
						5,
						'blob',
					),
					true,
				)}
				w={10}
				fill
			/>
		);
		rough = 6;
	} else if (inR(d.scribble)) {
		// garabato circular enorme que tapa la fecha
		const pts: Pt[] = [];
		const cx = 430;
		for (let i = 0; i < 46; i++) {
			const a = i * 0.62;
			const rx = 300 + (random(`scr-rx-${i}`) - 0.5) * 120;
			const ry = 190 + (random(`scr-ry-${i}`) - 0.5) * 90;
			pts.push([cx + Math.cos(a) * rx + (random(`scr-ox-${i}`) - 0.5) * 80, CY + Math.sin(a) * ry]);
		}
		content = <Stroke d={smooth(J(pts, 6, 'scr'))} w={26} />;
		rough = 8;
	}
	if (!content) return null;
	return (
		<AbsoluteFill>
			<svg width={W} height={H}>
				<filter id={`rough-${boil}`} x="-10%" y="-10%" width="120%" height="120%">
					<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves={2} seed={boil} />
					<feDisplacementMap in="SourceGraphic" scale={rough} xChannelSelector="R" yChannelSelector="G" />
				</filter>
				<g filter={`url(#rough-${boil})`}>{content}</g>
			</svg>
		</AbsoluteFill>
	);
};
