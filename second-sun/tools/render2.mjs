// Robust chunk renderer: bundle once, render 300-frame chunks, each with a fresh browser, retry on hang.
// Chunk files match tools/render.mjs (--chunk 300), which then joins them and mixes the sound.
import path from 'node:path';
import fs from 'node:fs';
import {createRequire} from 'node:module';
import {ROOT, readJson, say} from './lib.mjs';
const require = createRequire(path.join(ROOT, 'package.json'));
const {bundle} = require('@remotion/bundler');
const {renderMedia, selectComposition, openBrowser} = require('@remotion/renderer');
const CH = 300;
import os from 'node:os';
const SHARD = Number(process.argv[2] ?? 0);
const SHARDS = Number(process.argv[3] ?? 1);
const CPU = Math.max(2, os.cpus().length);
const cfg = readJson('src/story/render.json').long;
const serveUrl = await bundle({entryPoint: path.join(ROOT, 'src', 'index.ts')});
const chromiumOptions = {gl: 'angle'};
const comp = await selectComposition({serveUrl, id: 'Long', chromiumOptions});
const total = comp.durationInFrames;
const dir = path.join(ROOT, 'out', 'chunks_Long');
fs.mkdirSync(dir, {recursive: true});
let n = 0;
for (let s = 0; s < total; s += CH, n++) {
	const e = Math.min(total - 1, s + CH - 1);
	const f = path.join(dir, `c${String(n).padStart(2, '0')}.mp4`);
	if (n % SHARDS !== SHARD) continue;
	if (fs.existsSync(f)) continue;
	let ok = false;
	for (let t = 0; t < 5 && !ok; t++) {
		const browser = await openBrowser('chrome', {chromiumOptions});
		const t0 = Date.now();
		try {
			await renderMedia({composition: comp, serveUrl, codec: 'h264', outputLocation: f + '.part.mp4', frameRange: [s, e], muted: true, crf: 18, scale: Number(process.env.RENDER_SCALE ?? cfg.scale ?? 1), concurrency: t < 2 ? CPU : Math.max(1, Math.floor(CPU / 2)), chromiumOptions, timeoutInMilliseconds: 60000, puppeteerInstance: browser, logLevel: 'error'});
			fs.renameSync(f + '.part.mp4', f);
			ok = true;
			say(`chunk ${n + 1}/${Math.ceil(total / CH)} done in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
		} catch (err) {
			say(`chunk ${n + 1} attempt ${t + 1} failed: ${String(err.message).slice(0, 120)}`);
		}
		try { await browser.close({silent: true}); } catch {}
	}
	if (!ok) { say('FAILED chunk ' + (n + 1)); process.exit(1); }
}
say('ALL CHUNKS DONE');
