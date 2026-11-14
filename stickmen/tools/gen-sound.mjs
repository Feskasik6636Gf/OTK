// Builds src/story/sound.json from the shot data (places -> ambience, beats/fx -> effects).
import fs from 'node:fs';
import path from 'node:path';
import {ROOT} from './lib.mjs';
const id3 = (i) => String(i + 1).padStart(3, '0');
const files = ['ch1', 'ch2', 'ch3', 'ch4'].map((n) => fs.readFileSync(path.join(ROOT, 'src/story', n + '.ts'), 'utf8')).join('\n');
const shotLines = files.split('\n').filter((l) => /^\t\{at: \d+,/.test(l));
const AMB = {bedroom: 'room', bath: 'room', kitchen: 'room', corridor: 'hall', yard: 'street', class: 'hall', cafe: 'crowd', porch: 'street', gym: 'hall', hospital: 'room', steps: 'street', busstop: 'street', void: 'night'};
const shots = shotLines.map((l) => ({at: +l.match(/at: (\d+)/)[1], place: l.match(/place: '(\w+)'/)[1], night: /night: true/.test(l), line: l}));
const ambience = [];
shots.forEach((s, i) => {
	let kind = AMB[s.place];
	if (s.place === 'kitchen' && s.night) kind = 'fridge';
	const from = id3(s.at);
	const to = i + 1 < shots.length ? id3(shots[i + 1].at) : 'end';
	const last = ambience[ambience.length - 1];
	if (last && last.kind === kind) last.to = to;
	else ambience.push({from, to, kind, gain: kind === 'night' ? 0.035 : kind === 'crowd' ? 0.05 : 0.045, ...(kind === 'street' && s.place !== 'busstop' ? {birds: true} : {})});
});
const sfx = [];
const add = (line, off, type, extra = {}) => sfx.push({at: id3(line), off, type, ...extra});
for (const s of shots) {
	for (const m of s.line.matchAll(/'(\d+)(?:\+(-?\d+))?\s+(walk|run|jump|hop|stumble|hug|cheer|laugh|sob|onoma|stat|title|flash|shake|icon)\b([^']*)'/g)) {
		const line = +m[1];
		const off = m[2] ? +m[2] : 0;
		const kind = m[3];
		const rest = m[4].trim();
		if (kind === 'walk') add(line, off, 'steps', {dur: 1.4});
		else if (kind === 'run') add(line, off, 'steps', {dur: 1.1});
		else if (kind === 'jump' || kind === 'hop') add(line, off + 10, 'thud');
		else if (kind === 'stumble') add(line, off + 8, 'thud');
		else if (kind === 'hug') add(line, off, 'swoosh');
		else if (kind === 'cheer') add(line, off, 'ding');
		else if (kind === 'onoma') {
			const t = rest.split(/\s+/)[0].toUpperCase();
			if (/KNOCK/.test(t)) {
				add(line, off, 'thud');
				add(line, off + 12, 'thud');
			} else if (/CRACK|CRRK|CREAK|SQUEAK|CLICK|CHECK/.test(t)) add(line, off, 'click');
			else if (/THUD|SPLAT|STOMP|CLACK|CLINK|STOLEN|CRUNCH/.test(t)) add(line, off, 'thud');
			else if (/RIP|WHOOSH|SLIDE|ZIP|FLIP|FUSE/.test(t)) add(line, off, 'swoosh');
			else if (/DING|FIXED|GENIUS/.test(t)) add(line, off, 'ding');
			else add(line, off, 'pop');
		} else if (kind === 'stat') add(line, off, 'ding');
		else if (kind === 'title') add(line, off, 'stamp');
		else if (kind === 'flash') add(line, off, 'whooshUp');
		else if (kind === 'shake') add(line, off, 'thud');
		else if (kind === 'icon') add(line, off, 'pop');
	}
}
const out = {ambience, music: [], sfx};
fs.writeFileSync(path.join(ROOT, 'src/story/sound.json'), JSON.stringify(out, null, 1));
console.log('ambience', ambience.length, 'sfx', sfx.length);
