import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {MONTSERRAT} from '../fonts';
import {B, H, W} from '../timeline';
import {MONT_CAP_CENTER, clamp01} from './fx';
import type {InvitationConfig} from '../config';
import {Doodles} from './Doodles';

// Medido en el original (#250): tres filas centradas en y = 40,5 %, 49 % y 57,5 %;
// la del medio rellena y un poco más grande, las otras dos solo contorno.
const ROWS = [
	{y: 0.405 * H, size: 150, filled: false},
	{y: 0.49 * H, size: 162, filled: true},
	{y: 0.575 * H, size: 150, filled: false},
];

const charTimes = (date: string) => {
	// cada carácter de cada fila aparece en un frame propio, en orden aleatorio (determinístico)
	const n = date.length * ROWS.length;
	const order = Array.from({length: n}, (_, i) => i).sort((a, b) => random(`bo-${a}`) - random(`bo-${b}`));
	const times: number[] = new Array(n);
	order.forEach((idx, k) => {
		if (k < 4) {
			// los primeros asoman tenues sobre el neón
			times[idx] = B.firstChar + Math.round((k / 4) * (B.ballCut - B.firstChar - 1));
		} else {
			times[idx] = B.ballCut + Math.round(((k - 4) / (n - 5)) * (B.built - B.ballCut));
		}
	});
	return times;
};

export const BlockB: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame < B.firstChar || frame >= B.out) return null;
	const times = charTimes(cfg.date);
	// micro-jitter de ±1 px en los cortes
	const jitter = B.cuts.includes(frame)
		? {x: Math.round(random(`bj-x-${frame}`) * 2 - 1) || 1, y: Math.round(random(`bj-y-${frame}`) * 2 - 1)}
		: {x: 0, y: 0};
	return (
		<AbsoluteFill style={{transform: `translate(${jitter.x}px, ${jitter.y}px)`}}>
			{ROWS.map((row, r) => (
				<div
					key={r}
					style={{
						position: 'absolute',
						left: 0,
						width: W,
						top: row.y - MONT_CAP_CENTER * row.size,
						display: 'flex',
						justifyContent: 'center',
						fontFamily: MONTSERRAT,
						fontWeight: 700,
						fontSize: row.size,
						lineHeight: 1,
						fontVariantNumeric: 'tabular-nums',
						letterSpacing: '0.035em',
						whiteSpace: 'nowrap',
					}}
				>
					{cfg.date.split('').map((ch, i) => {
						const t = times[r * cfg.date.length + i];
						if (frame < t) {
							return (
								<span key={i} style={{opacity: 0}}>
									{ch}
								</span>
							);
						}
						const p = clamp01((frame - t + 1) / 2); // pop de 2 frames
						const faint = t < B.ballCut && frame < B.ballCut ? 0.4 : 1;
						const style: React.CSSProperties = row.filled
							? {
									backgroundImage: 'linear-gradient(180deg, #ffffff 0%, #f1f1f1 48%, #bdbdbd 100%)',
									WebkitBackgroundClip: 'text',
									backgroundClip: 'text',
									color: 'transparent',
									filter: 'url(#bevel-thin) drop-shadow(0 0 2px rgba(0,0,0,0.85)) drop-shadow(0 3px 6px rgba(0,0,0,0.6))',
								}
							: {
									color: '#fff',
									filter: 'url(#outline-date) drop-shadow(0 0 1.5px rgba(0,0,0,1)) drop-shadow(0 0 4px rgba(0,0,0,0.75))',
								};
						return (
							<span
								key={i}
								style={{
									display: 'inline-block',
									opacity: p * faint,
									transform: `scale(${1.15 - 0.15 * p})`,
									...style,
								}}
							>
								{ch}
							</span>
						);
					})}
				</div>
			))}
			<Doodles />
		</AbsoluteFill>
	);
};
