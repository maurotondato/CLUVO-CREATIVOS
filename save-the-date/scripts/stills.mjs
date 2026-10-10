// Renderiza frames sueltos de la composición a PNG (un solo bundle para todos).
// uso: node scripts/stills.mjs <outDir> <frame> [frame...]
import path from 'node:path';
import {mkdirSync} from 'node:fs';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';

const [outDir, ...frames] = process.argv.slice(2);
mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: 'SaveTheDate'});
for (const f of frames.map(Number)) {
	const output = path.join(outDir, `s${String(f).padStart(4, '0')}.png`);
	await renderStill({serveUrl, composition, frame: f, output, chromiumOptions: {gl: 'swangle'}});
	console.log(output);
}
