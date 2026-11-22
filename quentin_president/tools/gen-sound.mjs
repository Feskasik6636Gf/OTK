// builds src/story/sound.json from the same rules the director uses
import fs from 'node:fs';
import {clauses, FX_RULES, popFor} from '../src/story/rules.ts';
const TL = JSON.parse(fs.readFileSync('src/story/timeline.json', 'utf8'));
const amb = {'001':'room','005':'crowd','009':'room','010':'night','011':'rain','012':'room','015':'hall','018':'room','020':'crowd','024':'room','027':'street','031':'night','035':'crowd','040':'room','044':'fridge','045':'hall','049':'room','051':'night','057':'sea','058':'crowd','062':'crowd','067':'room','074':'hall','078':'fridge','083':'night','085':'night','089':'room','091':'hall','095':'rain','098':'street','101':'hall','104':'hall','108':'hall','114':'street','122':'hall','126':'street','131':'rain','132':'rain','134':'hall','136':'night','140':'crowd','142':'hall','145':'night','150':'hall','154':'fridge','162':'hall','165':'crowd'};
const keys = Object.keys(amb);
const ambience = keys.map((k, i) => ({from: k, to: keys[i + 1] ?? 'end', kind: amb[k], gain: amb[k] === 'rain' || amb[k] === 'crowd' ? 0.05 : 0.04}));
const sfx = [];
const starts = new Set(keys);
let lastFx = '';
for (const l of TL.lines) {
	const id = l.id.slice(0, 3);
	if (starts.has(id)) sfx.push({at: id, off: 4, type: 'steps', dur: 1.3, pan: -0.3});
	const cs = clauses(l.text ?? '');
	const tot = cs.reduce((a, c) => a + c.length + 6, 0);
	let acc = 0;
	for (const text of cs) {
		const off = Math.round(acc * l.dur);
		acc += (text.length + 6) / tot;
		let fx = '';
		for (const r of FX_RULES) if (r.re.test(text) && r.fx !== lastFx) { sfx.push({at: id, off: off + 8, type: r.sfx, amp: r.amp ?? 0.3}); fx = r.fx; break; }
		lastFx = fx;
		const p = popFor(text);
		if (p) sfx.push({at: id, off: off + 8, type: p.kind === 'day' ? 'stamp' : 'pop', amp: 0.25});
	}
}
fs.writeFileSync('src/story/sound.json', JSON.stringify({ambience, music: [], sfx}, null, 1));
console.log('sfx', sfx.length);
