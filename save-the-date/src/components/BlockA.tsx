import React from 'react';
import {AbsoluteFill, random, useCurrentFrame} from 'remotion';
import {fitText} from '@remotion/layout-utils';
import {MONTSERRAT} from '../fonts';
import {A, W} from '../timeline';
import {MONT_CAP_CENTER, Slices} from './fx';
import type {InvitationConfig} from '../config';

// Medido en el original (#45): SAVE THE DATE de borde a borde con el centro de las
// mayúsculas en y = 46,8 %; el nombre en contorno debajo, centrado en y = 53,4 %.
const TITLE_Y = 0.468 * 1920;
const NAME_Y = 0.534 * 1920;

export const BlockAText: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const {fontSize: titleSize} = fitText({
		text: cfg.saveTheDate,
		withinWidth: W - 30,
		fontFamily: MONTSERRAT,
		fontWeight: '800',
	});
	const nameSize = 140;
	return (
		<AbsoluteFill>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: TITLE_Y - MONT_CAP_CENTER * titleSize,
					textAlign: 'center',
					fontFamily: MONTSERRAT,
					fontWeight: 800,
					fontSize: titleSize,
					lineHeight: 1,
					whiteSpace: 'nowrap',
					backgroundImage: 'linear-gradient(180deg, #ffffff 0%, #ffffff 52%, #d4d4d4 100%)',
					WebkitBackgroundClip: 'text',
					backgroundClip: 'text',
					color: 'transparent',
					filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.55))',
				}}
			>
				{cfg.saveTheDate}
			</div>
			<div
				style={{
					position: 'absolute',
					left: 0,
					width: W,
					top: NAME_Y - MONT_CAP_CENTER * nameSize,
					textAlign: 'center',
					fontFamily: MONTSERRAT,
					fontWeight: 700,
					fontSize: nameSize,
					lineHeight: 1,
					// el contenedor deja aire arriba para que la tilde nunca se recorte
					paddingTop: 0,
					whiteSpace: 'nowrap',
					color: '#fff',
					filter: 'url(#outline-name) drop-shadow(0 2px 4px rgba(0,0,0,0.5))',
				}}
			>
				{cfg.name}
			</div>
		</AbsoluteFill>
	);
};

export const BlockA: React.FC<{cfg: InvitationConfig}> = ({cfg}) => {
	const frame = useCurrentFrame();
	if (frame < A.in || frame >= A.out) return null;
	const text = <BlockAText cfg={cfg} />;
	// Entrada con glitch digital: rebanadas desplazadas, letras incompletas.
	if (frame < A.stable) {
		const p = (frame - A.in) / (A.stable - A.in);
		const bands = 6 + Math.floor(random(`a-in-b-${frame}`) * 9);
		return (
			<AbsoluteFill>
				<Slices seed={`a-in-${frame}`} bands={bands} minShift={40 * (1 - p * 0.5)} maxShift={120 * (1 - p * 0.5)} dropout={0.55 - 0.4 * p}>
					{text}
				</Slices>
			</AbsoluteFill>
		);
	}
	// Glitch de 1-2 frames en algunos cortes
	const g = A.cutGlitches.find((c) => frame >= c && frame < c + 2);
	if (g !== undefined) {
		return (
			<AbsoluteFill>
				<Slices seed={`a-cut-${frame}`} bands={8} minShift={20} maxShift={80} dropout={0.1}>
					{text}
				</Slices>
			</AbsoluteFill>
		);
	}
	return text;
};
