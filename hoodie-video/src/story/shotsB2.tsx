import React from 'react';
import {CrowdRow} from '../kit/kit';
import {Callout} from '../kit/graphics';
import {env} from '../kit/actions';
import {Onoma} from '../reference/PauseTime';
import type {ShotDef} from '../kit/coverage';
import {Burger, Capy, Cat, Fish, Fruit, Larva, Monkey, Pod, Tree} from './critters';
import {S, man, pop, rel, sc, lerpF} from './dsl';
import {CountUp, Round, Say, Slam, Stat} from './overlays';
import {Confetti, Leaf, Ring, SpeedLines, Tag, Zebra} from './props2';

const wob = (f: number, a: number, p = 6) => Math.sin(f / p) * a;

/* 089-090 — hunts zebras on the savannah, most hunts fail */
const s089 = S(
	'089',
	'sav',
	[700, 640, 1.2],
	[1500, 640, 1.1],
	(c) => {
		const lx = lerpF(c.f, c.at('089') + 24, c.at('090') + 40, -200, 1500);
		const zx = lerpF(c.f, c.at('089') + 24, c.at('090') + 40, 500, 2400);
		const flop = env(c.f, c.at('090') + 44, c.dur, 6, 1000);
		return (
			<>
				<SpeedLines f={c.gf} y0={500} y1={880} dir={1} c="#fff4c8" />
				{[0, 1, 2].map((i) => (
					<Zebra key={i} x={zx + i * 150} y={900 - i * 6} s={0.8} ph={c.gf * 0.7 + i} />
				))}
				<Cat kind="lion" x={lx} y={900} s={1.1} f={c.gf} mode={flop > 0.5 ? 'lie' : 'walk'} ph={c.gf * 0.9} thin={0.6} />
				<Onoma x={lx} y={560} text="PANT PANT" t={rel(c, '090', 50)} c="#fff" size={60} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '090', 24)} dur={80} text="MOST HUNTS FAIL" y={80} size={110} c="#ff5a6e" />},
);

/* 091 — here the prey is small, fast and hidden */
const s091 = S(
	'091',
	'jd',
	[960, 640, 1.2],
	[1100, 600, 1.2],
	(c) => {
		const cx = lerpF(c.f, c.at('091') + 20, c.dur, 500, 1900);
		return (
			<>
				<Cat kind="lion" x={cx - 520} y={900} s={1.1} f={c.gf} mode="crouch" thin={0.7} />
				<Capy x={cx} y={900} s={0.5} f={c.gf} ph={c.gf} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '091', 24)} dur={32} text="SMALL" y={80} size={120} c="#fff" />
				<Slam t={rel(c, '091', 58)} dur={30} text="FAST" y={80} size={120} c="#ffd23a" />
				<Slam t={rel(c, '091', 86)} dur={50} text="HIDDEN" y={80} size={120} c="#7cf0a0" />
			</>
		),
	},
);

/* 092-094 — catches a capybara: dinner */
const s092 = S(
	'092',
	'jd2',
	[900, 640, 1.2],
	[1000, 620, 1.5],
	(c) => {
		const pounce = lerpF(c.f, c.at('092') + 40, c.at('092') + 62, 0, 1);
		return (
			<>
				<Capy x={1300} y={900} s={0.8} f={c.gf} ph={0} />
				<Cat kind="lion" x={560 + pounce * 640} y={900 - Math.sin(pounce * Math.PI) * 120} s={1.2} f={c.gf} mode={pounce > 0.9 ? 'stand' : 'crouch'} thin={0.8} />
				<Onoma x={1260} y={640} text="POUNCE!" t={rel(c, '092', 60)} c="#ffd23a" size={90} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '092', 66)} dur={50} text="CAPYBARA" y={80} size={120} c="#ffb04a" />
				<Slam t={rel(c, '093', 10)} dur={50} text="WORLD'S BIGGEST RODENT" y={820} size={70} c="#fff" />
				<Slam t={rel(c, '094', 38)} dur={60} text="DINNER!" y={80} size={130} c="#7cf0a0" />
			</>
		),
		shake: (c) => (rel(c, '092', 60) > 0 && rel(c, '092', 60) < 8 ? 10 : 0),
	},
);

/* 095-097 — the calories: 2,500 a day, x100, 250,000 */
const s095 = S(
	'095',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => (
		<>
			<CrowdRow n={14} x0={200} x1={1720} floor={940} s={0.8} mode="stand" seed="cal" />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '095', 40)} dur={40} text="BIGGEST PROBLEM" y={80} size={100} c="#ff5a6e" />
				<CountUp t={rel(c, '096', 30)} dur={90} to={2500} suffix=" CAL" label="PER MAN PER DAY" side="c" y={200} size={150} c="#ffd23a" roll={30} />
				<Stat t={rel(c, '097', 8)} dur={50} big="× 100" side="r" y={400} size={140} c="#8ae0ff" />
				<CountUp t={rel(c, '097', 40)} dur={150} from={2500} to={250000} suffix=" CAL" label="EVERY SINGLE DAY" side="c" y={230} size={170} c="#ff5a6e" roll={80} />
			</>
		),
	},
);

/* 098-099 — 500 cheeseburgers, in a jungle with none */
const s098 = S(
	'098',
	'jd',
	[960, 620, 1.0],
	[960, 580, 1.15],
	(c) => {
		const dropT = c.at('098') + 16;
		return (
			<>
				{Array.from({length: 18}).map((_, i) => {
					const t0 = dropT + i * 3;
					const y = lerpF(c.f, t0, t0 + 24, -120, 860 + (i % 3) * 18);
					const gone = rel(c, '099', 40) > 0 ? 1 : 0;
					return gone ? null : <Burger key={i} x={200 + ((i * 97) % 1500)} y={y} s={1.5} rot={wob(c.f + i * 4, 14, 5)} />;
				})}
				<CrowdRow n={5} x0={300} x1={1600} floor={900} s={0.8} mode="stand" seed="bur" />
				<Ring x={960} y={700} t={rel(c, '099', 40)} c="#fff" r={700} n={2} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<CountUp t={rel(c, '098', 14)} dur={110} to={500} label="CHEESEBURGERS" side="c" y={70} size={150} c="#ffd23a" roll={20} fmt={false} />
				<Slam t={rel(c, '099', 38)} dur={60} text="NO CHEESEBURGERS" y={820} size={90} c="#ff5a6e" />
			</>
		),
	},
);

/* 100-101 — they fish, they catch almost nothing */
const s100 = S(
	'100',
	'riv',
	[900, 640, 1.2],
	[1100, 660, 1.3],
	(c) => {
		const jump = lerpF(c.f, c.at('101') + 4, c.at('101') + 40, 0, 1);
		return (
			<>
				{man(c, {who: 'sam', x: 780, s: 1.1, color: '#e8802a', face: 1, expr: 'worried', pose: (p) => ({...p, armF: [80 + wob(c.f, 6, 5), 30], lean: p.lean + 8})})}
				{man(c, {who: 'danny', x: 1180, s: 1.1, face: 1, expr: 'sad', pose: (p) => ({...p, armF: [80 + wob(c.f, 6, 6), 30], lean: p.lean + 8})})}
				{[800, 1200].map((x, i) => (
					<line key={i} x1={x + 90} y1={620} x2={x + 400} y2={780 + i * 10} stroke="#8a5e34" strokeWidth={6} />
				))}
				<Fish x={1500 + jump * 500} y={790 - Math.sin(jump * Math.PI) * 200} s={0.7} rot={-jump * 40} f={c.gf} face={1} />
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '100', 4)} dur={26} text="THEY FISH" y={80} size={110} c="#8ae0ff" />
			<Slam t={rel(c, '101', 10)} dur={60} text="ALMOST NOTHING" y={80} size={110} c="#ff5a6e" />
		</>
	)},
);

/* 102-103 — monkey with sticks, monkey throws fruit */
const s102 = S(
	'102',
	'jd',
	[1100, 600, 1.1],
	[1100, 560, 1.3],
	(c) => {
		const t = rel(c, '103', 24);
		const fx = lerpF(c.f, c.at('103') + 24, c.at('103') + 42, 1560, 860);
		const fy = lerpF(c.f, c.at('103') + 24, c.at('103') + 42, 560, 640) - Math.sin(Math.min(1, Math.max(0, (c.f - c.at('103') - 24) / 18)) * Math.PI) * 60;
		return (
			<>
				<Tree x={1560} y={900} s={0.9} f={c.gf} h={560} />
				<Monkey x={1560} y={470} s={1.3} face={-1} f={c.gf} throwT={t} />
				{t >= 0 && t < 20 ? <Fruit x={fx} y={fy} r={20} rot={c.f * 14} /> : null}
				{man(c, {who: 'danny', x: 640, s: 1.1, face: 1, g: [['fist', '102', 18, 80]], pose: (p) => (rel(c, '103', 42) > 0 ? {...p, lean: p.lean - 14 * env(c.f, c.at('103') + 42, c.at('103') + 80, 3, 10)} : p), expr: rel(c, '103', 42) > 0 ? 'wide' : 'angry'})}
				<line x1={760} y1={560} x2={1000} y2={420} stroke="#8a5e34" strokeWidth={8} strokeLinecap="round" />
				<Onoma x={820} y={560} text="SPLAT!" t={rel(c, '103', 42)} c="#ff7a3a" size={90} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '102', 4)} dur={90} text="HUNTING A MONKEY… WITH STICKS" y={80} size={72} c="#fff" />},
);

/* 104-106 — Sam shows grubs */
const s104 = S(
	'104',
	'jd2',
	[960, 640, 1.3],
	[960, 600, 1.8],
	(c) => (
		<>
			{man(c, {who: 'sam', x: 900, s: 1.2, face: 1, g: [['presentF', '104', 22, 120]]})}
			{[0, 1, 2, 3].map((i) => (
				<g key={i} opacity={pop(c.f, c.at('104') + 38 + i * 6)}>
					<Larva x={1180 + (i % 2) * 130} y={680 + Math.floor(i / 2) * 60} s={1.4} f={c.gf} i={i} />
				</g>
			))}
			<Callout f={c.f} t0={c.at('105') + 4} t1={c.at('105') + 60} from={[1240, 650]} to={[1560, 400]} text="FAT WHITE LARVAE" size={40} />
			<Callout f={c.f} t0={c.at('106') + 4} t1={c.dur - 4} from={[1180, 700]} to={[1560, 840]} text="PROTEIN + FAT" size={40} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '104', 36)} dur={70} text="GRUBS" y={80} size={130} c="#ffe08a" />},
);

/* 107-109 — tastes like coconut, half eat, half hungry */
const s107 = S(
	'107',
	'jd',
	[960, 640, 1.2],
	[960, 600, 1.0],
	(c) => {
		const split = lerpF(c.f, c.at('108'), c.at('108') + 24, 0, 1);
		return (
			<>
				{man(c, {who: 'danny', x: 820, s: 1.2, face: 1, expr: c.f > c.at('107') + 30 ? 'wide' : 'worried', g: [['touchFace', '107', 40, 100]], mouth: 'open'})}
				<Larva x={1000} y={640} s={1.4} f={c.gf} />
				<Say t={rel(c, '107', 66)} x={820} y={330} text="COCONUT…?" size={50} tail={[0, 100]} />
				{split > 0 ? (
					<>
						<g opacity={split}>
							<CrowdRow n={5} x0={140} x1={760} floor={900} s={0.8} mode="dance" seed="ate" />
							<Tag x={460} y={400} text="ATE" k={split} c="#7cf0a0" />
						</g>
						<g opacity={split}>
							<CrowdRow n={5} x0={1160} x1={1780} floor={900} s={0.8} mode="stand" seed="hungry" />
							<Tag x={1470} y={400} text="HUNGRY" k={rel(c, '109', 0) > 0 ? 1 : 0} c="#ff5a6e" />
						</g>
					</>
				) : null}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '107', 66)} dur={80} text="TASTES LIKE COCONUT" sub="IF IT COULD WIGGLE" y={80} size={90} c="#ffe08a" />},
);

/* 110-113 — Max finds a tree with pods: Brazil nuts */
const s110 = S(
	'110',
	'jd2',
	[900, 560, 1.0],
	[1200, 540, 1.3],
	(c) => (
		<>
			<Tree x={1300} y={900} s={1.1} f={c.gf} h={600} />
			{[0, 1, 2, 3, 4].map((i) => (
				<g key={i} opacity={pop(c.f, c.at('111') + 48 + i * 6)}>
					<Pod x={1180 + i * 60} y={330 + (i % 2) * 60} s={0.9} />
				</g>
			))}
			{man(c, {who: 'max', x: 360, to: 900, w: ['110', 20, 110], s: 1.1, face: 1, g: [['point', '111', 4, 60]]})}
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '112', 14)} dur={46} text="HARD AS CANNONBALLS" y={80} size={86} c="#ffd23a" />
				<Slam t={rel(c, '113', 0)} dur={50} text="BRAZIL NUTS" y={780} size={130} c="#ffb04a" />
			</>
		),
	},
);

/* 114-115 — almost no animal can crack them */
const s114 = S(
	'114',
	'jd',
	[960, 640, 1.3],
	[960, 620, 1.6],
	(c) => (
		<>
			<Pod x={1000} y={900} s={1.8} />
			<Monkey x={560} y={900} s={1.1} face={1} f={c.gf} />
			{c.f < c.at('115') ? <Onoma x={760} y={700} text="BONK" t={(rel(c, '114', 40) % 26)} c="#ff7a3a" size={70} /> : null}
			<g opacity={pop(c.f, c.at('115') + 20)}>
				<Capy x={1500} y={900} s={0.7} face={-1} f={c.gf} />
			</g>
			<Tag x={1500} y={640} text="ONE SMALL RODENT" sub="SUPER SHARP TEETH" k={pop(c.f, c.at('115') + 30)} size={34} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '114', 36)} dur={70} text="NO ANIMAL CAN CRACK THEM" y={80} size={70} c="#fff" />},
);

/* 116-119 — Max squeezes one: crack! 20 nuts, a hundred pods a day */
const s116 = S(
	'116',
	'jd2',
	[960, 600, 1.3],
	[960, 560, 1.7],
	(c) => {
		const crack = lerpF(c.f, c.at('117'), c.at('117') + 14, 0, 1);
		return (
			<>
				{man(c, {who: 'max', x: 700, s: 1.2, face: 1, g: [['presentF', '116', 20, 50]], pose: (p) => ({...p, lean: p.lean + 6 * env(c.f, c.at('116') + 26, c.at('117') + 4, 6, 4)})})}
				<Pod x={1080} y={760} s={1.6} crack={crack} />
				<Ring x={1080} y={700} t={rel(c, '117', 0)} c="#ffd23a" r={260} n={2} />
				<Onoma x={1080} y={520} text="CRACK!" t={rel(c, '117', 0)} c="#ffd23a" size={110} />
			</>
		);
	},
	{over: (c) => <CountUp t={rel(c, '118', 24)} dur={60} to={20} label="NUTS INSIDE" side="r" y={120} size={150} c="#ffd23a" roll={14} fmt={false} />, shake: (c) => (rel(c, '117', 0) > 0 && rel(c, '117', 0) < 8 ? 14 : 0)},
);
const s119 = S(
	'119',
	'jd',
	[960, 640, 1.1],
	[960, 600, 1.4],
	(c) => (
		<>
			{Array.from({length: 12}).map((_, i) => (
				<g key={i} opacity={pop(c.f, c.at('119') + 18 + i * 4)}>
					<Pod x={1060 + (i % 4) * 90} y={910 - Math.floor(i / 4) * 78} s={0.9} crack={1} />
				</g>
			))}
			{man(c, {who: 'max', x: 640, s: 1.2, face: 1, mouth: 'open', pose: (p) => ({...p, armF: [100 + wob(c.f, 20, 3), 90], lean: p.lean + wob(c.f, 3, 3)})})}
		</>
	),
	{over: (c) => <CountUp t={rel(c, '119', 26)} dur={90} to={100} label="PODS IN A DAY" side="l" y={140} size={150} c="#ffd23a" roll={20} fmt={false} />},
);

/* 120 — Round 3: food, Max */
const s120 = S(
	'120',
	'jd',
	[960, 620, 1.0],
	[960, 580, 1.2],
	(c) => (
		<>
			{man(c, {who: 'max', x: 960, s: 1.2, face: 1, g: [['fist', '120', 30, 100]], mouth: 'smile'})}
			<Confetti x={960} y={520} t={rel(c, '120', 56)} />
		</>
	),
	{over: (c) => <Round t={rel(c, '120', 0)} dur={c.dur - 4} n={3} title="FOOD" winner="MAX +1" c="#ff5a6e" />},
);

export const SHOTS_B2: ShotDef[] = [s089, s091, s092, s095, s098, s100, s102, s104, s107, s110, s114, s116, s119, s120];
