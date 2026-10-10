import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {fitText} from '@remotion/layout-utils';
import {MONTSERRAT} from '../fonts';
import {C, H, W} from '../timeline';
import {MONT_CAP_CENTER, clamp01} from './fx';
import type {InvitationConfig} from '../config';

const CENTER_Y = 0.49 * H;
const LINES = 5;

// Alternancia relleno/contorno por plano, como en el original.
const patternFor = (frame: number) => {
	if (frame >= 374 && frame < 387) return [0, 1, 0, 1, 0];
	if (frame >= 402) return [0, 1, 0, 1, 0];
	return [1, 0, 1, 0, 1];
};

const Lines: React.FC<{
	text: string;
	size: number;
	pattern: number[];
	opacity?: (i: number) => number;
}> = ({text, size, pattern, opacity}) => {
	const gap = size * 1.45;
	const top0 = CENTER_Y - ((LINES - 1) / 2) * gap;
	return (
		<>
			{Array.from({length: LINES}, (_, i) => {
				const filled = pattern[i] === 1;
				return (
					<div
						key={i}
						style={{
							position: 'absolute',
							left: 0,
							width: W,
							top: top0 + i * gap - MONT_CAP_CENTER * size,
							textAlign: 'center',
							fontFamily: MONTSERRAT,
							fontWeight: 800,
							fontSize: size,
							lineHeight: 1,
							whiteSpace: 'nowrap',
							opacity: opacity ? opacity(i) : 1,
							...(filled
								? {
										backgroundImage: 'linear-gradient(180deg, #ffffff 0%, #ffffff 50%, #c4c4c4 100%)',
										WebkitBackgroundClip: 'text',
										backgroundClip: 'text',
										color: 'transparent',
										// extrusión corta hacia abajo a la derecha, como las letras 3D del original
										filter:
											'url(#bevel-thin) drop-shadow(1px 1px 0 #a8a8a8) drop-shadow(1px 1px 0 #7c7c7c) drop-shadow(1px 1px 0 #555) drop-shadow(1px 2px 0 #333)',
									}
								: {color: '#fff', filter: 'url(#outline-venue)'}),
						}}
					>
						{text}
					</div>
				);
			})}
		</>
	);
};

export const BlockC: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame < C.preroll[0] || frame >= C.out) return null;
	const {fontSize} = fitText({text: cfg.venue, withinWidth: W * 0.9, fontFamily: MONTSERRAT, fontWeight: '800'});
	const size = Math.min(fontSize, 132);
	// plano inclinado con temblor constante (cambia cada 2 frames)
	const step = Math.floor(frame / 2);
	const sx = (random(`c-sx-${step}`) - 0.5) * 4;
	const sy = (random(`c-sy-${step}`) - 0.5) * 4;
	const sr = (random(`c-sr-${step}`) - 0.5) * 0.8;
	const plane = (extraX = 0) =>
		`translate(${sx + extraX}px, ${sy}px) perspective(1700px) rotateY(-10deg) rotateZ(${-3 + sr}deg)`;

	if (frame < C.main) {
		// pre-roll: líneas tenues que se deslizan desde la izquierda, medio cortadas por el borde
		const p = clamp01((frame - C.preroll[0]) / (C.preroll[1] - C.preroll[0]));
		const x = -W * (0.34 - 0.16 * p);
		return (
			<AbsoluteFill style={{transform: plane(x), filter: 'blur(2px)'}}>
				<Lines
					text={cfg.venue}
					size={size}
					pattern={[0, 1, 0, 1, 0]}
					opacity={(i) => 0.1 + 0.1 * random(`c-pre-${i}-${Math.floor(frame / 3)}`)}
				/>
			</AbsoluteFill>
		);
	}
	const pattern = patternFor(frame);
	if (frame < C.echoUntil) {
		// eco/fantasma: copias desplazadas que se van enfocando
		const p = clamp01((frame - C.main) / (C.echoUntil - C.main - 1));
		const blur = 5 * (1 - p);
		const off = 20 - 12 * p;
		return (
			<AbsoluteFill style={{transform: plane()}}>
				<AbsoluteFill style={{transform: `translateX(${off}px)`, opacity: 0.32 * (1 - p * 0.5), filter: 'blur(1.5px)'}}>
					<Lines text={cfg.venue} size={size} pattern={pattern} />
				</AbsoluteFill>
				<AbsoluteFill style={{transform: `translateX(${-off * 0.6}px)`, opacity: 0.22 * (1 - p * 0.5), filter: 'blur(1.5px)'}}>
					<Lines text={cfg.venue} size={size} pattern={pattern} />
				</AbsoluteFill>
				<AbsoluteFill style={{filter: `blur(${blur.toFixed(2)}px)`}}>
					<Lines text={cfg.venue} size={size} pattern={pattern} />
				</AbsoluteFill>
			</AbsoluteFill>
		);
	}
	return (
		<AbsoluteFill style={{transform: plane(), filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.5))'}}>
			<Lines text={cfg.venue} size={size} pattern={pattern} />
		</AbsoluteFill>
	);
};
