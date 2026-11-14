// Splits one full voiceover into per-line clips on whisper segment boundaries and builds
// timeline.json keeping the ORIGINAL pacing (no silence trimming).
// node tools/split-vo.mjs <voiceover.mp3> <transcript.json> [speakers.json]
import fs from 'node:fs';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {FPS, ROOT, decodePcm, ffbin} from './lib.mjs';
const [vo, trFile, spFile] = process.argv.slice(2);
const segs = JSON.parse(fs.readFileSync(trFile, 'utf8'));
const spk = spFile && fs.existsSync(spFile) ? JSON.parse(fs.readFileSync(spFile, 'utf8')) : {};
const pcm = decodePcm(vo);
const totalS = pcm.length / 16000;
const lines = [], tl = [];
const per = 16000 / FPS;
for (let i = 0; i < segs.length; i++) {
	const s = segs[i];
	const a = i === 0 ? 0 : (segs[i - 1].end + s.start) / 2;
	const b = i === segs.length - 1 ? totalS : (s.end + segs[i + 1].start) / 2;
	const from = Math.round(a * FPS), to = Math.round(b * FPS);
	const n = String(i + 1).padStart(3, '0');
	const sp = spk[n] ?? 'N';
	const id = `${n}_${sp}`;
	const out = path.join(ROOT, 'public', 'vo', id + '.wav');
	execFileSync(ffbin(), ['-v', 'error', '-y', '-ss', (from / FPS).toFixed(4), '-t', ((to - from) / FPS).toFixed(4), '-i', vo, '-ac', '1', '-ar', '44100', out]);
	const env = [];
	let peak = 0;
	for (let k = from; k < to; k++) {
		let acc = 0;
		const st = Math.floor(k * per), en = Math.min(pcm.length, Math.floor((k + 1) * per));
		for (let j = st; j < en; j++) acc += (pcm[j] / 32768) ** 2;
		const r = Math.sqrt(acc / Math.max(1, en - st));
		env.push(r);
		peak = Math.max(peak, r);
	}
	lines.push({id, sp, t: s.text});
	tl.push({id, sp, text: s.text, file: `vo/${id}.wav`, trimStart: 0, from, dur: to - from, env, peak});
}
const gpeak = [...tl.map((l) => l.peak)].sort((a, b) => a - b)[Math.floor(tl.length * 0.9)];
for (const l of tl) {
	l.env = l.env.map((v) => Math.round(Math.min(1, v / gpeak) * 100) / 100);
	delete l.peak;
}
const total = Math.round(totalS * FPS) + 4 * FPS;
fs.writeFileSync(path.join(ROOT, 'src/story/lines.json'), JSON.stringify(lines, null, 1));
fs.writeFileSync(path.join(ROOT, 'src/story/timeline.json'), JSON.stringify({fps: FPS, total, lines: tl}));
console.log('lines', tl.length, 'total s', (total / FPS).toFixed(1));
