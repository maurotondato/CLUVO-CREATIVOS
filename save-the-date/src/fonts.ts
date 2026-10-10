import {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';
import manifest from './fonts.manifest.json';

// Montserrat, Cormorant Garamond y Allura de Google Fonts. Los woff2 son los mismos que
// carga @remotion/google-fonts (mismas URLs), bajados a public/fonts por
// scripts/fetch_fonts.mjs para que el render no dependa de la red.

export const MONTSERRAT = 'Montserrat';
export const CORMORANT = 'Cormorant Garamond';
export const ALLURA = 'Allura';

const allLoaded = Promise.all(
	manifest.map((f) =>
		loadFont({
			family: f.family,
			url: staticFile(f.file),
			weight: f.weight,
			unicodeRange: f.unicodeRange,
			format: 'woff2',
		}),
	),
).then(() => document.fonts.ready);

/** true cuando las fuentes están cargadas (para medir texto con la fuente real). */
export const useFontsReady = () => {
	const [ready, setReady] = useState(false);
	const [handle] = useState(() => delayRender('fuentes'));
	useEffect(() => {
		allLoaded.then(() => {
			setReady(true);
			continueRender(handle);
		});
	}, [handle]);
	return ready;
};
