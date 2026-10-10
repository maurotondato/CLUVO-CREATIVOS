import React from 'react';
import {AbsoluteFill} from 'remotion';
import {useFontsReady} from './fonts';
import type {InvitationConfig} from './config';
import {Crystals, Flashes, GlitchFrame, GrainAndVignette, Plates, SvgFilters} from './components/fx';
import {BlockA} from './components/BlockA';
import {BlockB} from './components/BlockB';
import {BlockC} from './components/BlockC';
import {BlockD} from './components/BlockD';
import {BlockE, BlockF, LightLeak, MonogramBg} from './components/Closing';

export const Main: React.FC<InvitationConfig> = (cfg) => {
	const ready = useFontsReady();
	if (!ready) return <AbsoluteFill style={{background: '#000'}} />;
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<SvgFilters />
			<GlitchFrame>
				<Plates />
				<BlockA cfg={cfg} />
				<BlockB cfg={cfg} />
				<BlockC cfg={cfg} />
				<BlockD cfg={cfg} />
				<MonogramBg />
				<BlockE cfg={cfg} />
				<BlockF cfg={cfg} />
				<Crystals />
			</GlitchFrame>
			<LightLeak />
			<Flashes />
			<GrainAndVignette />
		</AbsoluteFill>
	);
};
