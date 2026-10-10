import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import {defaultConfig} from './config';
import {FPS, H, TOTAL, W} from './timeline';

export const Root: React.FC = () => (
	<Composition id="SaveTheDate" component={Main} durationInFrames={TOTAL} fps={FPS} width={W} height={H} defaultProps={defaultConfig} />
);
