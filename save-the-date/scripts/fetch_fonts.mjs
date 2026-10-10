// Baja a public/fonts/ los mismos woff2 de Google Fonts que pediría @remotion/google-fonts
// (mismas URLs y versiones, tomadas de su getInfo()), para que el render no dependa de la red.
// uso: node scripts/fetch_fonts.mjs
import {execFileSync} from 'node:child_process';
import {mkdirSync, writeFileSync, existsSync} from 'node:fs';
import {createRequire} from 'node:module';

const require = createRequire(import.meta.url);
const WANT = [
	['Montserrat', ['400', '500', '600', '700', '800', '900']],
	['CormorantGaramond', ['300', '500']],
	['Allura', ['400']],
];
const SUBSETS = ['latin', 'latin-ext'];

mkdirSync('public/fonts', {recursive: true});
const manifest = [];
for (const [mod, weights] of WANT) {
	const info = require(`@remotion/google-fonts/${mod}`).getInfo();
	for (const w of weights) {
		for (const subset of SUBSETS) {
			const url = info.fonts.normal[w][subset];
			const file = `fonts/${mod}-${w}-${subset}.woff2`;
			if (!existsSync(`public/${file}`)) {
				execFileSync('curl', ['-sSfL', '-o', `public/${file}`, url]);
			}
			manifest.push({family: info.fontFamily, weight: w, subset, file, unicodeRange: info.unicodeRanges[subset], url});
		}
	}
}
writeFileSync('src/fonts.manifest.json', JSON.stringify(manifest, null, 1));
console.log(`${manifest.length} archivos en public/fonts`);
