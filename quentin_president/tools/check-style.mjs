// Checks the story code BEFORE rendering against the house rules (sizes, life, variety).
// Reads src/story/shots.tsx, cast.ts, places.tsx. Fast: no rendering.
//   node tools/check-style.mjs
// ERROR = fix before rendering. WARN = look at it; if intended, add the comment  // ok-style
import fs from 'node:fs';
import path from 'node:path';
import {ROOT, say} from './lib.mjs';

const read = (f) => (fs.existsSync(path.join(ROOT, f)) ? fs.readFileSync(path.join(ROOT, f), 'utf8') : '');
const shots = read('src/story/shots.tsx');
const cast = read('src/story/cast.ts');
const places = read('src/story/places.tsx');
let errors = 0;
let warns = 0;
const err = (m) => (errors++, say('  ERROR: ' + m));
const warn = (m) => (warns++, say('  warn:  ' + m));
const lineOf = (src, idx) => src.slice(0, idx).split('\n').length;
const ok = (src, idx) => (src.split('\n')[lineOf(src, idx) - 1] || '').includes('ok-style');

// ---- 1. sizes: an adult is s = 1 (about 420 px); stay inside 0.55–1.6, prefer size="kid|teen|tall|giant"
const actorRe = /<Actor\b[\s\S]*?\/>/g;
let actors = 0;
let m;
while ((m = actorRe.exec(shots))) {
	actors++;
	const tag = m[0];
	const sm = tag.match(/\bs=\{([^}]+)\}/);
	if (sm && !ok(shots, m.index)) {
		const v = Number(sm[1].trim());
		if (Number.isFinite(v)) {
			if (v < 0.4 || v > 2.2) err(`shots.tsx:${lineOf(shots, m.index)} Actor s=${v}: impossible size (allowed 0.55–1.6). A tiny or huge person next to a car/door means the OBJECT is the wrong size, fix the object (references/world.md, "Масштаб").`);
			else if (v < 0.55 || v > 1.6) warn(`shots.tsx:${lineOf(shots, m.index)} Actor s=${v}: outside 0.55–1.6. Use size="kid" / "giant" or move the camera closer instead of scaling a person.`);
		}
	}
	if (/\bpose=\{\s*POSES\.\w+\s*\}/.test(tag) && !ok(shots, m.index)) warn(`shots.tsx:${lineOf(shots, m.index)} Actor with a fixed POSES pose. It still breathes (auto life), but give it an action or gesture on the line (gesture(), walkTo(), reach()).`);
	if (/\blife=\{0\}/.test(tag) && !/\bseat=/.test(tag) && !ok(shots, m.index)) warn(`shots.tsx:${lineOf(shots, m.index)} life={0}: this actor is frozen. Only for a sleeper.`);
	if (!/\bfloor=|\bseat=/.test(tag) && !ok(shots, m.index)) warn(`shots.tsx:${lineOf(shots, m.index)} Actor without floor: defaults to y=900. Pass floor= that matches the location.`);
}
if (!actors) warn('no <Actor> found in shots.tsx: are the people in the story drawn another way?');

// ---- 2. variety of places: not the same location over and over
const placeNames = [...new Set([...(read('src/kit/sets.tsx') + read('src/kit/world.tsx')).matchAll(/export const (\w+): React\.FC/g)].map((x) => x[1]))];
const shotBlocks = shots.split(/\n(?=const S\w+: React\.FC)/).slice(1);
const seq = shotBlocks.map((b) => placeNames.find((n) => new RegExp('<' + n + '\\b').test(b)) ?? '(own)');
let run = 1;
for (let i = 1; i < seq.length; i++) {
	run = seq[i] === seq[i - 1] ? run + 1 : 1;
	if (run === 4 && seq[i] !== '(own)') warn(`4 scenes in a row in the same place (${seq[i]}). Change the place, time of day, or at least framing and details (references/world.md).`);
}
if (seq.length > 5 && new Set(seq).size === 1) warn(`all ${seq.length} scenes use one location (${seq[0]}). Pick places from the words of each line.`);

// ---- 3. cast: hero look and variety
if (!/hero:\s*\{[^}]*hero:\s*true/.test(cast)) warn("cast.ts: the main hero has no `hero: true` (glossy black head, white eyes). The audience should know him instantly.");
const looks = [...cast.matchAll(/^\t(\w+):\s*\{([^\n]*)\},?$/gm)].map((x) => ({id: x[1], c: (x[2].match(/color:\s*'(#\w+)'/) || [])[1], h: (x[2].match(/hair:\s*'(\w+)'/) || [])[1], red: /#ff2540/i.test(x[2])}));
for (let i = 0; i < looks.length; i++) {
	for (let j = i + 1; j < looks.length; j++) if (looks[i].c && looks[i].c === looks[j].c && looks[i].h === looks[j].h) warn(`cast.ts: "${looks[i].id}" and "${looks[j].id}" look the same (colour + hair). Make everyone recognisable.`);
	if (looks[i].red && looks[i].id !== 'hero' && !/hero:\s*true/.test(cast.split(looks[i].id + ':')[1]?.split('\n')[0] || '')) warn(`cast.ts: "${looks[i].id}" wears the hero's red. Red belongs only to the hero.`);
}

// ---- 4. own locations must live: they have to use time (f, gf, useShot…)
if (places.replace(/\/\*[\s\S]*?\*\//g, '').trim().length > 40) {
	const comps = ('\n' + places).split(/\nexport const /).slice(1);
	for (const c of comps) {
		const name = c.split(/[:=\s]/)[0];
		if (!/\b(f|gf|t)\b\s*[\/*+)]|useShot|useCurrentFrame|Math\.sin/.test(c)) warn(`places.tsx: "${name}" has no animation (no f/gf/useShot/Math.sin). Every location needs 3 living details (references/world.md, section 5).`);
	}
}


// ---- 5. effects: enough of them, and every effect has a sound
const fxRe = /<(Shockwave|ImpactText|SpeedLines|Sparkles|Smoke|Confetti|Lightning|LightningFlash|Glitch|Pulse|Exclaim|Question|Bulb)\b|\bpunch\(|\bflash\(/g;
const fxCount = (shots.match(fxRe) || []).length;
let sfxCount = 0;
let seconds = 0;
try {
	sfxCount = (JSON.parse(read('src/story/sound.json') || '{}').sfx || []).length;
	const tl = JSON.parse(read('src/story/timeline.json') || '{}');
	seconds = (tl.total || 0) / (tl.fps || 30);
} catch {}
if (seconds > 20 && fxCount < Math.floor(seconds / 14)) warn(`only ${fxCount} effect(s) in ${seconds.toFixed(0)} s. Aim for one visible effect per 10–12 s (references/effects.md).`);
if (fxCount && sfxCount < fxCount) warn(`${fxCount} effect(s) but only ${sfxCount} sound cue(s) in sound.json. Every effect needs its own sound on the same line and frame (references/effects.md).`);

say(`checked: ${actors} actor(s), ${seq.length} scene(s), places: ${[...new Set(seq)].join(', ') || '-'}`);
say(errors ? `FAIL: ${errors} error(s), ${warns} warning(s)` : warns ? `OK with ${warns} warning(s): read them, fix or mark // ok-style` : 'OK: sizes, variety and life look right');
process.exit(errors ? 1 : 0);
