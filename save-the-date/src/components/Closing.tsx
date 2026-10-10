import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame} from 'remotion';
import {ALLURA, CORMORANT, MONTSERRAT} from '../fonts';
import {E, F, H, LEAK, W} from '../timeline';
import {MONT_CAP_CENTER, Slices, clamp01, easeOut} from './fx';
import type {InvitationConfig} from '../config';
import logo from '../data/logo.json';

/** Flash blanco + light leak arcoíris (el único momento con color). */
export const LightLeak: React.FC = () => {
	const frame = useCurrentFrame();
	if (frame < LEAK.flash || frame >= LEAK.until) return null;
	const k = frame - LEAK.flash;
	const white = [1, 1, 0.97, 0.9][k];
	const shift = k * 26;
	return (
		<AbsoluteFill>
			<AbsoluteFill style={{background: '#fff', opacity: white}} />
			<AbsoluteFill
				style={{
					mixBlendMode: 'multiply',
					opacity: 0.92,
					filter: 'blur(46px)',
					WebkitMaskImage: 'linear-gradient(180deg, rgba(0,0,0,0) 38%, rgba(0,0,0,1) 72%)',
					maskImage: 'linear-gradient(180deg, rgba(0,0,0,0) 38%, rgba(0,0,0,1) 72%)',
					background: `linear-gradient(118deg, rgba(255,255,255,1) 0%, rgba(255,255,255,1) ${44 + k}%, #ff3b30 ${52 + k}%, #ff9500 ${57 + k}%, #ffe600 ${62 + k}%, #34e36b ${67 + k}%, #22c8ff ${72 + k}%, #3d5bff ${77 + k}%, #b44dff ${82 + k}%, rgba(255,255,255,1) ${90 + k}%)`,
					transform: `translateY(${shift}px)`,
				}}
			/>
			<AbsoluteFill
				style={{
					mixBlendMode: 'screen',
					background: 'radial-gradient(ellipse 60% 40% at 30% 75%, rgba(255,170,90,0.55), rgba(255,170,90,0) 70%)',
				}}
			/>
		</AbsoluteFill>
	);
};

/** Fondo del monograma: resto cálido del leak, después negro con patrón tenue de puntos. */
export const MonogramBg: React.FC = () => {
	const frame = useCurrentFrame();
	if (frame < E.in || frame >= E.out) return null;
	if (frame === E.in) {
		return (
			<AbsoluteFill
				style={{
					background:
						'radial-gradient(ellipse 70% 55% at 42% 38%, rgba(176,128,88,0.95) 0%, rgba(98,66,44,0.95) 45%, rgba(30,20,14,1) 100%)',
					filter: 'blur(6px)',
				}}
			/>
		);
	}
	const dots = frame < E.stable ? 0.16 : 0.12 * (1 - clamp01((frame - E.stable) / 20));
	if (dots <= 0) return null;
	return (
		<AbsoluteFill
			style={{
				backgroundImage: `radial-gradient(circle, rgba(255,255,255,${dots}) 1.2px, rgba(255,255,255,0) 1.8px)`,
				backgroundSize: '22px 22px',
			}}
		/>
	);
};

const Monogram: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	// Medido en el original (#600): inicial de ~19 % del alto centrada en y = 48,5 %,
	// script cruzando el tercio medio, FIFTEEN espaciado en y = 60 %.
	const pSize = 640;
	const cy = 0.485 * H;
	return (
		<AbsoluteFill>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: cy - 0.47 * pSize,
					textAlign: 'center',
					fontFamily: CORMORANT,
					fontWeight: 500,
					fontSize: pSize,
					lineHeight: 1,
					backgroundImage: 'linear-gradient(180deg, #ffffff 0%, #f0f0f0 45%, #b9b9b9 100%)',
					WebkitBackgroundClip: 'text',
					backgroundClip: 'text',
					color: 'transparent',
					opacity: 0.92,
				}}
			>
				{cfg.monogramInitial}
			</div>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: cy - 185,
					textAlign: 'center',
					fontFamily: ALLURA,
					fontSize: 420,
					lineHeight: 1.2,
					color: '#fff',
					transform: 'translateX(-10px) rotate(-10deg)',
					filter: 'drop-shadow(0 2px 6px rgba(0,0,0,0.6))',
				}}
			>
				{cfg.monogramScript}
			</div>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: 0.615 * H - MONT_CAP_CENTER * 36,
					textAlign: 'center',
					fontFamily: MONTSERRAT,
					fontWeight: 500,
					fontSize: 36,
					lineHeight: 1,
					letterSpacing: '0.45em',
					paddingLeft: '0.45em',
					color: 'rgba(255,255,255,0.92)',
				}}
			>
				{cfg.monogramSubtitle}
			</div>
		</AbsoluteFill>
	);
};

export const BlockE: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame < E.in || frame >= E.out) return null;
	if (frame >= E.stretch[0] && frame < E.stretch[1]) {
		// glitch de desenfoque/estiramiento horizontal
		const k = frame - E.stretch[0];
		const sx = [1.18, 1.3, 1.1][k];
		return (
			<AbsoluteFill style={{transform: `scaleX(${sx})`, filter: `url(#hblur${[1, 2, 3][k]})`}}>
				<Monogram cfg={cfg} />
			</AbsoluteFill>
		);
	}
	return <Monogram cfg={cfg} />;
};

/** Placa final M·DATOS. */
export const BlockF: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame < F.in) return null;
	const lp = easeOut((frame - F.logo) / F.logoDur);
	const logoW = W * 0.62;
	const logoH = (logoW * logo.height) / logo.width;
	const logoTop = 0.46 * H - logoH / 2;
	const fade = 1 - clamp01((frame - F.fadeOut + 1) / (F.out - F.fadeOut));
	const url = (
		<div
			style={{
				position: 'absolute',
				left: 0,
				width: W,
				top: logoTop + logoH + 70,
				textAlign: 'center',
				fontFamily: MONTSERRAT,
				fontWeight: 500,
				fontSize: 38,
				lineHeight: 1,
				letterSpacing: '0.2em',
				paddingLeft: '0.2em',
				color: 'rgba(255,255,255,0.85)',
			}}
		>
			{cfg.creditUrl}
		</div>
	);
	const urlP = clamp01((frame - F.url) / 4);
	return (
		<AbsoluteFill style={{background: '#000', opacity: fade}}>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: logoTop - 78,
					textAlign: 'center',
					fontFamily: MONTSERRAT,
					fontWeight: 400,
					fontSize: 30,
					lineHeight: 1,
					letterSpacing: '0.15em',
					paddingLeft: '0.15em',
					color: 'rgba(255,255,255,0.55)',
					opacity: lp,
				}}
			>
				{cfg.creditPrefix}
			</div>
			<Img
				src={staticFile('credit_logo.png')}
				style={{
					position: 'absolute',
					left: (W - logoW) / 2,
					top: logoTop,
					width: logoW,
					height: logoH,
					opacity: lp,
					transform: `scale(${1.04 - 0.04 * lp})`,
				}}
			/>
			{frame >= F.url && frame < F.url + 2 ? (
				<AbsoluteFill>
					<Slices seed={`url-${frame}`} bands={7} minShift={18} maxShift={70} dropout={0.15}>
						{url}
					</Slices>
				</AbsoluteFill>
			) : frame >= F.url ? (
				<AbsoluteFill style={{opacity: 0.6 + 0.4 * urlP}}>{url}</AbsoluteFill>
			) : null}
		</AbsoluteFill>
	);
};
