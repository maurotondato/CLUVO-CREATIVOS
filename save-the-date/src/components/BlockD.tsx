import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {fitText} from '@remotion/layout-utils';
import {MONTSERRAT} from '../fonts';
import {COVER, D, H, W} from '../timeline';
import {MONT_CAP, MONT_CAP_CENTER, clamp01} from './fx';
import type {InvitationConfig} from '../config';

// Medido en el original (#558): letras cromadas con mayúsculas de ~14,5 % del alto,
// centradas en y = 50 %; franja oscura de ~20 % del alto de letra cruzando el centro.
const CENTER_Y = 0.5 * H;
const SIZE = 400;
const SCALE_X = 1.1;
const CAP = SIZE * MONT_CAP;

const CHROME =
	'linear-gradient(180deg, #ffffff 0%, #f6f6f6 22%, #d9d9d9 40%, #8a8a8a 47%, #2e2e2e 51%, #5a5a5a 55%, #a9a9a9 64%, #e9e9e9 82%, #ffffff 100%)';

const Letter: React.FC<{ch: string; angle: number; visible: boolean; sweep: number}> = ({ch, angle, visible, sweep}) => {
	const base: React.CSSProperties = {
		display: 'inline-block',
		fontFamily: MONTSERRAT,
		fontWeight: 900,
		fontSize: SIZE,
		lineHeight: 1,
		whiteSpace: 'pre',
	};
	return (
		<span
			style={{
				display: 'inline-block',
				position: 'relative',
				opacity: visible ? 1 : 0,
				transformOrigin: '50% 82%',
				transform: `perspective(1000px) rotateX(${angle}deg)`,
			}}
		>
			{/* sombra proyectada suave */}
			<span style={{...base, position: 'absolute', left: 0, top: 0, color: 'rgba(0,0,0,0.55)', transform: 'translate(6px, 14px)', filter: 'blur(9px)'}}>
				{ch}
			</span>
			{/* cuerpo cromado con bisel fino oscuro */}
			<span
				style={{
					...base,
					position: 'relative',
					backgroundImage: CHROME,
					WebkitBackgroundClip: 'text',
					backgroundClip: 'text',
					color: 'transparent',
					filter: 'url(#bevel-chrome)',
				}}
			>
				{ch}
			</span>
			{/* brillo especular que barre en diagonal */}
			<span
				style={{
					...base,
					position: 'absolute',
					left: 0,
					top: 0,
					backgroundImage:
						'linear-gradient(115deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 44%, rgba(255,255,255,0.95) 50%, rgba(255,255,255,0) 56%, rgba(255,255,255,0) 100%)',
					backgroundSize: '300% 100%',
					backgroundPosition: `${(100 - sweep * 100).toFixed(1)}% 0%`,
					WebkitBackgroundClip: 'text',
					backgroundClip: 'text',
					color: 'transparent',
				}}
			>
				{ch}
			</span>
		</span>
	);
};

/** PÍA cromado + franja SAVE THE DATE. progress controla flips y franja; sirve también para la portada. */
export const ChromeName: React.FC<{cfg: InvitationConfig; frame: number; still?: boolean}> = ({cfg, frame, still}) => {
	const letters = Array.from(cfg.name.normalize('NFC'));
	// cada letra entra en un beat; si el nombre tiene más letras que beats medidos, siguen al mismo ritmo
	const step = D.letters[1] - D.letters[0];
	const starts = letters.map((_, i) => D.letters[i] ?? D.letters[0] + i * step);
	const sweepPeriod = 45;
	const sweepT = ((frame - D.letters[0]) % sweepPeriod) / 18;
	const sweep = still ? 0.35 : clamp01(sweepT);

	// como en el original: primero asoma "THE" en el centro y después se abre rápido
	const bandP = still ? 1 : Math.pow(clamp01((frame - D.band[0] + 1) / (D.band[1] - D.band[0])), 2.6);
	const bandH = CAP * 0.23;
	const {fontSize: bandSize} = fitText({
		text: cfg.saveTheDate,
		withinWidth: W * 0.8,
		fontFamily: MONTSERRAT,
		fontWeight: '600',
		letterSpacing: '0.25em',
	});
	const bandFont = Math.min(bandSize, bandH * 0.86);

	return (
		<AbsoluteFill>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: CENTER_Y - MONT_CAP_CENTER * SIZE,
					display: 'flex',
					justifyContent: 'center',
					letterSpacing: '0.01em',
					transform: `scaleX(${SCALE_X})`,
				}}
			>
				{letters.map((ch, i) => {
					// como en el original: la letra asoma despacio desde la base, termina rápido y rebota apenas
					const p = still ? 1 : clamp01((frame - starts[i]) / D.flip);
					const ease = p * p * (3 - 2 * p);
					const overshoot = -7 * Math.sin(Math.PI * clamp01((p - 0.78) / 0.22));
					const angle = still ? 0 : 90 * (1 - ease) + overshoot;
					return <Letter key={i} ch={ch} angle={angle} visible={still || frame >= starts[i]} sweep={sweep} />;
				})}
			</div>
			{(still || frame >= D.band[0]) && (
				<div
					style={{
						position: 'absolute',
						left: 0,
						width: W,
						top: CENTER_Y - bandH / 2,
						height: bandH,
						clipPath: `inset(0 ${((1 - bandP) * 50).toFixed(2)}% 0 ${((1 - bandP) * 50).toFixed(2)}%)`,
					}}
				>
					<div style={{position: 'absolute', left: W * 0.07, right: W * 0.07, top: 0, bottom: 0, background: 'rgba(6,6,6,0.9)'}} />
					<div
						style={{
							position: 'absolute',
							left: 0,
							width: W,
							top: bandH / 2 - MONT_CAP_CENTER * bandFont,
							textAlign: 'center',
							fontFamily: MONTSERRAT,
							fontWeight: 600,
							fontSize: bandFont,
							lineHeight: 1,
							letterSpacing: '0.25em',
							// el tracking agrega aire al final: se compensa para centrar
							paddingLeft: '0.25em',
							color: '#fff',
							whiteSpace: 'nowrap',
						}}
					>
						{cfg.saveTheDate}
					</div>
				</div>
			)}
		</AbsoluteFill>
	);
};

export const BlockD: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame === COVER) return <ChromeName cfg={cfg} frame={frame} still />;
	if (frame < D.letters[0] || frame >= D.smear[1]) return null;
	if (frame >= D.smear[0]) {
		// salida: smear vertical de 2 frames
		const k = frame - D.smear[0];
		return (
			<AbsoluteFill style={{filter: `url(#vsmear${k + 1})`, transform: `translateY(${(k + 1) * 40}px) scaleY(${1 + 0.25 * (k + 1)})`, opacity: 1 - 0.3 * k}}>
				<ChromeName cfg={cfg} frame={D.smear[0] - 1} />
			</AbsoluteFill>
		);
	}
	return <ChromeName cfg={cfg} frame={frame} />;
};
