// Builds src/story/sound.json from the beats (ambience per location, sfx per action).
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const ROOT = process.cwd();
const require = createRequire(path.join(ROOT, 'package.json'));
const esbuild = require('esbuild');
const out = path.join(ROOT, 'out', '.beats.cjs');
await esbuild.build({entryPoints: [path.join(ROOT, 'src/story/beats.ts')], bundle: true, platform: 'node', format: 'cjs', outfile: out, logLevel: 'error'});
const {BEATS} = require(out);
const TL = JSON.parse(fs.readFileSync('src/story/timeline.json', 'utf8'));
const pad = (n) => String(n).padStart(3, '0');
const AMB = {office: 'room', kitchen: 'room', kitchenN: 'fridge', classroom: 'hall', science: 'hall', cafeteria: 'crowd', corridor: 'hall', lab: 'room', road: 'street', stage: 'crowd', hall: 'crowd', club: 'crowd', studio: 'crowd', city: 'night', village: 'wind', living: 'room', livingDim: 'room', hospital: 'room', porchBen: 'street', porchBenDusk: 'street', porchAyva: 'street', bathroom: 'night', field: 'wind', fieldSmoke: 'wind', black: 'room'};
const amb = [];
let cur = null;
let effLoc = [];
BEATS.forEach((b, i) => {
	const loc = b.same ? effLoc[i - 1] : b.card ? 'card' : b.loc;
	effLoc[i] = loc;
	const kind = loc === 'card' ? 'room' : AMB[loc] ?? 'room';
	const gain = loc === 'card' ? 0.025 : kind === 'crowd' ? 0.06 : 0.045;
	if (!cur || cur.kind !== kind || cur.gain !== gain) {
		if (cur) cur.to = pad(i + 1);
		cur = {from: pad(i + 1), to: 'end', kind, gain};
		if (loc === 'porchBen' || loc === 'field' || loc === 'living') cur.birds = true;
		amb.push(cur);
	}
});
const sfx = [];
const add = (n, off, type, extra = {}) => sfx.push({at: pad(n), off: Math.round(off), type, ...extra});
BEATS.forEach((b, i) => {
	if (b.same) return;
	const n = i + 1;
	const D = TL.lines[i].dur;
	for (const a of b.cast ?? []) {
		if (a.to !== undefined && a.to !== a.x) {
			const t0 = (a.t0 ?? 0.02) * D;
			const dist = Math.abs(a.to - a.x);
			const t1 = a.t1 !== undefined ? a.t1 * D : Math.min(D - 4, t0 + dist / (a.a === 'run' ? 16 : 8));
			add(n, t0 + 2, 'steps', {dur: Math.max(0.4, (t1 - t0) / 30), pan: (a.x < 960 ? -0.4 : 0.4), a: a.a === 'run' ? 0.2 : 0.13});
		}
		for (const [act, at] of [[a.a, 0.02], [a.b, a.ab ?? 0.5]]) {
			if (!act) continue;
			const off = at * D + 4;
			if (act === 'laughFloor' || act === 'fall') add(n, off + 10, 'thud', {a: 0.45});
			if (act === 'give' || act === 'hug') add(n, off + 10, 'clap', {a: 0.14});
			if (act === 'knock') {
				add(n, off + 4, 'thud', {a: 0.35});
				add(n, off + 11, 'thud', {a: 0.35});
				add(n, off + 18, 'thud', {a: 0.35});
			}
			if (act === 'snap') add(n, off + 6, 'click', {a: 0.3});
			if (act === 'jump' || act === 'cheer') add(n, off, 'whooshUp', {dur: 0.5, a: 0.12});
			if (act === 'shock' || act === 'scared') add(n, off, 'swoosh', {a: 0.1});
		}
		if (a.sit && n > 1 && !BEATS[i - 1]?.cast?.some((c) => c.w === a.w && c.sit)) add(n, 2, 'thud', {a: 0.12});
	}
	for (const x of b.fx ?? []) {
		const off = (x.at ?? 0.1) * D;
		switch (x.k) {
			case 'text': add(n, off, 'pop', {a: 0.16}); break;
			case 'icon':
			case 'bubble': add(n, off, 'pop', {a: 0.12}); break;
			case 'title': add(n, off, 'whooshUp', {dur: 0.6, a: 0.16}); add(n, off + 8, 'stamp', {a: 0.35}); break;
			case 'acc': add(n, off, 'swoosh', {a: 0.1}); break;
			case 'count': add(n, off, 'whooshUp', {dur: 0.7, a: 0.12}); add(n, off + 20, 'ding', {a: 0.1}); break;
			case 'shake': add(n, off, 'thud', {a: 0.5}); break;
			case 'flash':
			case 'burst': add(n, off, 'whoosh', {dur: 0.8, a: 0.16}); break;
			case 'hearts':
			case 'sparkle': add(n, off, 'ding', {a: 0.08}); break;
			case 'confetti': add(n, off, 'pop', {a: 0.14}); add(n, off + 4, 'pop', {a: 0.12}); add(n, off + 9, 'pop', {a: 0.1}); break;
			case 'alarm': add(n, off, 'alarm', {dur: Math.max(1, (D - off) / 30), a: 0.05}); break;
			case 'rec': add(n, off, 'click', {a: 0.2}); break;
		}
	}
	if (b.card) add(n, 2, 'swoosh', {a: 0.12});
	if (b.smoke) add(n, 0, 'crackle', {dur: D / 30, a: 0.03 + 0.04 * b.smoke});
	if (b.loc === 'fieldSmoke' && n >= 190 && n <= 198) add(n, 0, 'siren', {dur: D / 30, a: n === 190 ? 0.04 : 0.02});
	if (b.loc === 'fieldSmoke' && n < 190) add(n, 0, 'crackle', {dur: D / 30, a: 0.03});
});
fs.writeFileSync('src/story/sound.json', JSON.stringify({ambience: amb, music: [], sfx}, null, 0));
console.log('ambience', amb.length, 'sfx', sfx.length);
