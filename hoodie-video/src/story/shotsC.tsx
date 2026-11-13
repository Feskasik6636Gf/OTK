import React from 'react';
import {CrowdRow} from '../kit/kit';
import {Callout} from '../kit/graphics';
import {env} from '../kit/actions';
import {Onoma} from '../reference/PauseTime';
import type {ShotDef} from '../kit/coverage';
import {Ant, Band, Caiman, Cat, Eyes, Heli, Mosq, Spark, Tree} from './critters';
import {S, lerpF, man, pop, rel, sc, lying} from './dsl';
import {Fire} from './places';
import {CountUp, Round, Say, Slam, Stat} from './overlays';
import {Crown, Leaf, Ring, SpeedLines, Tag} from './props2';

const wob = (f: number, a: number, p = 6) => Math.sin(f / p) * a;

const Torch: React.FC<{f?: number}> = ({f = 0}) => (
	<g transform="translate(6,-30) rotate(-8)">
		<rect x={-5} y={-10} width={10} height={90} rx={4} fill="#6a4a2a" transform="translate(0,-70)" />
		<path d={`M-18,-76 C-30,-110 -2,-124 -6,${-150 - Math.sin(f / 2) * 8} C16,-124 24,-104 18,-76 Z`} fill="#ff7a1a" />
		<path d={`M-9,-80 C-14,-100 0,-110 0,${-126 - Math.sin(f / 2.3) * 6} C10,-108 12,-96 9,-80 Z`} fill="#ffe08a" />
		<circle cx={0} cy={-100} r={90} fill="#ffb040" opacity={0.18} />
	</g>
);
const Turtle: React.FC<{x: number; y: number; k: number}> = ({x, y, k}) => (
	<g transform={`translate(${x},${y})`}>
		<ellipse cx={0} cy={-34} rx={70} ry={42} fill="#5a8a3a" stroke="#2f5a20" strokeWidth={5} />
		<path d="M-40,-50 q40,-30 80,0 M-20,-30 h40 M0,-72 v44" stroke="#2f5a20" strokeWidth={4} fill="none" />
		<circle cx={82} cy={-30} r={20} fill="#8ab84a" />
		<circle cx={88} cy={-34} r={4} fill="#111" />
		{k > 0 ? <path d="M-30,-70 L-10,-40 L-24,-30 L0,0" stroke="#fff" strokeWidth={6} fill="none" strokeLinejoin="round" /> : null}
	</g>
);

/* 121-123 — Day 8 night, the loudest nights */
const s121 = S(
	'121',
	'jn',
	[960, 620, 1.0],
	[960, 580, 1.25],
	(c) => (
		<>
			<Fire x={960} y={910} s={0.9} f={c.gf} />
			<CrowdRow n={5} x0={520} x1={1400} floor={930} s={0.7} mode="stand" seed="sleepers" />
			{[
				['RIBBIT', '123', 0, 520, 420],
				['BZZZ', '123', 25, 1350, 380],
				['TWEET!', '123', 50, 760, 300],
				['AWOO!', '123', 72, 1500, 520],
				['OOH-OOH-AH!', '123', 92, 560, 460],
			].map(([t, l, o, x, y], i) => (
				<Onoma key={i} x={x as number} y={y as number} text={t as string} t={rel(c, l as string, o as number) % 40} c={['#8ae0ff', '#ffd23a', '#7cf0a0', '#ff8a98', '#ffb04a'][i]} size={70} rot={(i % 2 ? 8 : -8)} />
			))}
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '121', 0)} dur={60} text="DAY 8" sub="NIGHT" y={70} size={130} c="#8ab4ff" />
				<Slam t={rel(c, '122', 40)} dur={50} text="SO LOUD!" y={780} size={110} c="#ffd23a" />
			</>
		),
		shake: (c) => (rel(c, '123', 0) > 0 ? 3 : 0),
	},
);

/* 124-125 — something is watching the camp: a jaguar */
const s124 = S(
	'124',
	'jn',
	[1000, 620, 1.1],
	[1250, 600, 1.3],
	(c) => (
		<>
			<Fire x={620} y={910} s={0.9} f={c.gf} />
			<CrowdRow n={4} x0={340} x1={900} floor={930} s={0.8} mode="stand" seed="watch" />
			<Eyes x={1600} y={620} s={1.4} o={rel(c, '124', 58) > 0 ? Math.min(1, rel(c, '124', 58) / 10) : 0} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '125', 0)} dur={50} text="A JAGUAR" y={90} size={140} c="#ffd23a" />, shake: (c) => (rel(c, '125', 0) > 0 && rel(c, '125', 0) < 8 ? 10 : 0)},
);

/* 126 — biggest cat in the Americas */
const s126 = S(
	'126',
	'jn2',
	[800, 640, 1.1],
	[1100, 620, 1.3],
	(c) => <Cat kind="jaguar" x={lerpF(c.f, 0, c.dur, -200, 1500)} y={900} s={1.3} f={c.gf} mode="walk" ph={c.gf * 0.2} />,
	{over: (c) => <Slam t={rel(c, '126', 8)} dur={80} text="BIGGEST CAT IN THE AMERICAS" y={80} size={76} c="#fff" />},
);

/* 127-128 — strongest bite, cracks a turtle shell */
const s127 = S(
	'127',
	'jn2',
	[960, 660, 1.2],
	[860, 640, 1.5],
	(c) => {
		const bite = env(c.f, c.at('128') + 34, c.at('128') + 60, 5, 12);
		return (
			<>
				<Cat kind="jaguar" x={760} y={910} s={1.4} f={c.gf} mode="stand" roar={0.3 + bite * 0.5} />
				<Turtle x={1380} y={900} k={bite > 0.5 ? 1 : 0} />
				<Onoma x={1380} y={680} text="CRACK!" t={rel(c, '128', 52)} c="#ffd23a" size={100} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '127', 40)} dur={110} text="STRONGEST BITE" sub="POUND FOR POUND" y={70} size={110} c="#ff5a6e" />, shake: (c) => (rel(c, '128', 52) > 0 && rel(c, '128', 52) < 8 ? 12 : 0)},
);

/* 129-130 — lions choke, jaguars go for the skull */
const s129 = S(
	'129',
	'studio',
	[960, 600, 1.0],
	[960, 580, 1.2],
	(c) => (
		<>
			<Cat kind="lion" x={480} y={880} s={0.85} f={c.gf} mode="stand" roar={0.3} />
			<Cat kind="jaguar" x={1460} y={880} s={0.9} f={c.gf} mode="stand" face={-1} roar={0.3} />
			<g opacity={pop(c.f, c.at('129') + 40)}>
				<Tag x={500} y={330} text="LIONS: CHOKE" size={44} c="#ffb04a" />
			</g>
			<g opacity={pop(c.f, c.at('130') + 20)}>
				<Tag x={1440} y={330} text="JAGUARS: THE SKULL" size={44} c="#ff5a6e" />
				<circle cx={1440} cy={250} r={52} fill="#f4f1e6" />
				<circle cx={1420} cy={244} r={11} fill="#14060c" />
				<circle cx={1462} cy={244} r={11} fill="#14060c" />
				<path d="M1440,262 l-8,18 h16 Z" fill="#14060c" />
			</g>
		</>
	),
);

/* 131-135 — the men don't see it: two yellow dots, then four, then gone */
const s131 = S(
	'131',
	'jn',
	[900, 620, 1.1],
	[1300, 640, 1.5],
	(c) => (
		<>
			<Fire x={560} y={910} s={0.9} f={c.gf} />
			<CrowdRow n={4} x0={260} x1={820} floor={930} s={0.8} mode="stand" seed="watch" />
			<Eyes x={1500} y={660} s={1.6} o={rel(c, '133', 0) > 0 && rel(c, '134', 0) < 0 ? 1 : 0} />
			{rel(c, '134', 0) > 0 && rel(c, '135', 0) < 0 ? (
				<>
					<Eyes x={1500} y={660} s={1.6} />
					<Eyes x={1700} y={600} s={1.3} />
				</>
			) : null}
			<Eyes x={1500} y={660} s={1.6} o={rel(c, '132', 28) > 0 && rel(c, '133', 0) < 0 ? 0.35 : 0} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '133', 0)} dur={22} text="TWO" y={90} size={130} c="#ffd23a" />},
);

/* 136-138 — 12 men press their buttons, 88 left */
const s136 = S(
	'136',
	'jdawn',
	[960, 600, 1.0],
	[960, 560, 1.15],
	(c) => {
		const hx = lerpF(c.f, c.at('137') - 4, c.at('137') + 70, 2300, 700);
		return (
			<>
				<Heli x={hx} y={260 + wob(c.f, 10, 9)} s={1.0} f={c.gf} face={-1} tilt={-4} />
				<CrowdRow n={12} x0={300} x1={1700} floor={900} s={0.75} mode="stand" seed="out" />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<CountUp t={rel(c, '136', 22)} dur={100} to={12} label="MEN PRESSED THE BUTTON" side="c" y={80} size={150} c="#ff5a6e" roll={14} fmt={false} />
				<Stat t={rel(c, '138', 0)} dur={50} big="88 LEFT" side="c" y={780} size={150} c="#ffd23a" />
			</>
		),
	},
);

/* 139-141 — deadliest animal: 2 milligrams, the mosquito */
const s139 = S(
	'139',
	'studio',
	[960, 540, 1.0],
	[960, 540, 1.3],
	(c) => (
		<>
			<Mosq x={960} y={580} s={5.5} f={c.gf} />
			<Callout f={c.f} t0={c.at('140') + 56} t1={c.dur - 4} from={[1100, 600]} to={[1500, 330]} text="2 MILLIGRAMS" size={50} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '141', 0)} dur={50} text="THE MOSQUITO" y={80} size={130} c="#ff5a6e" />},
);
const s142 = S(
	'142',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => <CrowdRow n={16} x0={160} x1={1760} floor={960} s={0.75} mode="stand" seed="die" />,
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '142', 0)} dur={170} text="KILLS MORE PEOPLE" sub="THAN ANY OTHER ANIMAL" y={110} size={100} c="#ffd23a" />
			</>
		),
	},
);

/* 144-146 — bullet ant */
const s144 = S(
	'144',
	'studio',
	[960, 600, 1.0],
	[1000, 560, 1.3],
	(c) => <Ant x={960} y={800} s={2.6} f={c.gf} />,
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '144', 28)} dur={60} text="BULLET ANT" y={80} size={130} c="#ff5a6e" />
				<Slam t={rel(c, '145', 50)} dur={80} text="MOST PAINFUL STING" y={800} size={90} c="#fff" />
				<Slam t={rel(c, '146', 24)} dur={50} text="LIKE BEING SHOT" y={800} size={90} c="#ff3a52" />
			</>
		),
		shake: (c) => (rel(c, '146', 38) > 0 && rel(c, '146', 38) < 8 ? 14 : 0),
	},
);

/* 147-148 — the math teacher sits on a nest */
const s147 = S(
	'147',
	'jd',
	[960, 620, 1.2],
	[960, 580, 1.5],
	(c) => {
		const sit = lerpF(c.f, c.at('147') + 56, c.at('147') + 76, 0, 1);
		return (
			<>
				<g>
					<ellipse cx={1000} cy={896} rx={110} ry={34} fill="#5a3a1c" />
					{[0, 1, 2, 3, 4].map((i) => (
						<circle key={i} cx={950 + i * 24} cy={870 - wob(c.f + i * 4, 6, 2)} r={6} fill="#6e1c10" />
					))}
				</g>
				{man(c, {who: 'sam', x: 560, to: 1000, w: ['147', 40, 80], s: 1.1, color: '#8e3a4f', outfit: 'suit', acc: ['glasses'], hair: 'bun', hairColor: '#333', face: 1, floor: 900 - sit * 0, expr: rel(c, '148', 0) > 0 ? 'wide' : 'normal', mouth: rel(c, '148', 0) > 0 ? 'open' : undefined, pose: (p) => (rel(c, '148', 0) > 0 ? {...p, armF: [150 + wob(c.f, 20, 2), 20], armB: [-150 - wob(c.f, 20, 2), 20], lean: -6} : p)})}
				<Tag x={760} y={400} text="MATH TEACHER" k={pop(c.f, c.at('147') + 36)} size={32} />
				<Say t={rel(c, '148', 41)} x={1180} y={420} text="AAAAAAAH!" size={60} tail={[-100, 110]} />
				<Spark x={1000} y={700} t={rel(c, '148', 70)} c="#ff5a6e" />
			</>
		);
	},
	{shake: (c) => (rel(c, '148', 41) > 0 ? 6 : 0)},
);

/* 149-150 — Max stung 40 times */
const s149 = S(
	'149',
	'jd2',
	[960, 600, 1.2],
	[960, 580, 1.5],
	(c) => {
		const n = Math.min(40, Math.max(0, Math.floor((c.f - c.at('149') - 10) / 2.2)));
		return (
			<>
				{man(c, {who: 'max', x: 960, s: 1.2, expr: 'wide', mouth: 'open', pose: (p) => ({...p, armF: [100 + wob(c.f, 40, 2), 40], armB: [-100 - wob(c.f, 40, 2), 40], lean: wob(c.f, 5, 2)})})}
				{Array.from({length: 40}).map((_, i) =>
					i < n ? <Ant key={i} x={780 + ((i * 53) % 360)} y={480 + ((i * 97) % 380)} s={0.16} face={i % 2 ? 1 : -1} f={c.gf + i} /> : null,
				)}
			</>
		);
	},
	{over: (c) => <CountUp t={rel(c, '150', 0)} dur={80} to={40} suffix=" TIMES" label="STUNG" side="r" y={150} size={150} c="#ff5a6e" roll={10} fmt={false} />, shake: () => 4},
);

/* 151-154 — he punches the air, it doesn't help, 71 left */
const s151 = S(
	'151',
	'jd',
	[960, 620, 1.2],
	[960, 580, 1.5],
	(c) => (
		<>
			{man(c, {who: 'max', x: 960, s: 1.2, expr: 'angry', pose: (p) => ({...p, armF: [100 + 50 * Math.abs(Math.sin(c.f / 3)), 10], lean: 8 * Math.abs(Math.sin(c.f / 3))})})}
			{[0, 1, 2, 3, 4, 5].map((i) => (
				<circle key={i} cx={1150 + wob(c.f * 3 + i * 40, 90, 12)} cy={520 + wob(c.f * 2 + i * 70, 80, 9)} r={5} fill="#3a0e08" />
			))}
			<Onoma x={1150} y={560} text="WHIFF" t={rel(c, '151', 30) % 36} c="#fff" size={60} />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '152', 8)} dur={40} text="DOESN'T HELP" y={80} size={110} c="#ff5a6e" />
				<Slam t={rel(c, '153', 4)} dur={80} text="CAN'T HIT IT? CAN'T WIN." y={780} size={80} c="#fff" />
				<Stat t={rel(c, '154', 0)} dur={50} big="71 LEFT" side="c" y={150} size={150} c="#ffd23a" />
			</>
		),
	},
);

/* 155-157 — Day 12: lion meets jaguar */
const s155 = S(
	'155',
	'riv',
	[960, 640, 1.0],
	[960, 600, 1.35],
	(c) => {
		const lx = lerpF(c.f, c.at('155'), c.at('157') + 20, -250, 520);
		return (
			<>
				<Cat kind="lion" x={lx} y={900} s={1.2} f={c.gf} mode={rel(c, '157', 20) > 0 ? 'stand' : 'walk'} ph={c.gf * 0.2} />
				<Cat kind="jaguar" x={1500} y={900} s={1.1} f={c.gf} face={-1} mode="crouch" />
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '155', 0)} dur={46} text="DAY 12" y={80} size={130} c="#ffd23a" />
			<Slam t={rel(c, '157', 40)} dur={70} text="TWO CATS. ONE RIVERBANK." y={80} size={80} c="#fff" />
		</>
	)},
);

/* 158-160 — weights: jaguar 100 kg, lion almost twice that */
const s158 = S(
	'158',
	'riv',
	[960, 640, 1.0],
	[960, 600, 1.15],
	(c) => (
		<>
			<Cat kind="jaguar" x={520} y={900} s={0.9} f={c.gf} mode="stand" />
			<Cat kind="lion" x={1380} y={900} s={1.35} f={c.gf} face={-1} mode="stand" />
		</>
	),
	{
		over: (c) => (
			<>
				<CountUp t={rel(c, '158', 24)} dur={50} to={100} suffix=" KG" label="JAGUAR" side="l" y={130} size={130} c="#ffd23a" roll={16} fmt={false} />
				<CountUp t={rel(c, '159', 20)} dur={150} to={190} suffix=" KG" label="LION" side="r" y={130} size={130} c="#ffb04a" roll={16} fmt={false} />
				<Slam t={rel(c, '160', 60)} dur={80} text="LION WINS... IN THE OPEN" y={800} size={80} c="#7cf0a0" />
			</>
		),
	},
);

/* 161-164 — not the open: jaguar climbs a tree, lions are bad climbers */
const s161 = S(
	'161',
	'riv',
	[1100, 560, 1.0],
	[1200, 480, 1.25],
	(c) => {
		const up = lerpF(c.f, c.at('162') + 16, c.at('162') + 50, 0, 1);
		const lj = env(c.f, c.at('163') + 22, c.at('163') + 50, 10, 10);
		return (
			<>
				<Tree x={1400} y={900} s={1.1} f={c.gf} h={640} />
				<Cat kind="jaguar" x={1400 - 40 * up} y={900 - up * 360} s={1.0} f={c.gf} face={-1} mode={up > 0.9 ? 'lie' : 'stand'} rot={up > 0.05 && up < 0.9 ? -40 : 0} shadow={false} />
				<Cat kind="lion" x={940} y={900 - lj * 120} s={1.25} f={c.gf} mode="stand" />
				<Onoma x={1100} y={800} text="THUD" t={rel(c, '163', 52)} c="#ffd23a" size={80} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '161', 30)} dur={60} text="THIS ISN'T THE OPEN" y={80} size={86} c="#fff" />},
);

/* 165-166 — they swim, they hunt caimans */
const s165 = S(
	'165',
	'riv',
	[1000, 760, 1.2],
	[1100, 760, 1.4],
	(c) => <Caiman x={lerpF(c.f, c.at('166') + 30, c.dur, 900, 1500)} y={860} s={1.1} f={c.gf} />,
	{
		back: (c) => <Cat kind="jaguar" x={lerpF(c.f, 0, c.dur, 300, 1250)} y={880} s={0.95} f={c.gf} mode="walk" ph={c.gf * 0.25} shadow={false} />,
		over: (c) => (
			<>
				<Slam t={rel(c, '165', 4)} dur={40} text="THEY SWIM" y={80} size={120} c="#8ae0ff" />
				<Slam t={rel(c, '166', 22)} dur={90} text="THEY HUNT CAIMANS" sub="(SMALL CROCODILES)" y={80} size={90} c="#7cf0a0" />
			</>
		),
	},
);

/* 167-169 — lion roars, jaguar yawns, vanishes into the leaves */
const s167 = S(
	'167',
	'jd2',
	[960, 620, 1.1],
	[960, 580, 1.4],
	(c) => {
		const gone = lerpF(c.f, c.at('169') + 16, c.at('169') + 60, 1, 0);
		return (
			<>
				<Cat kind="lion" x={560} y={900} s={1.2} f={c.gf} mode="stand" roar={env(c.f, c.at('167') + 14, c.at('167') + 50, 5, 10)} />
				<g opacity={gone}>
					<Cat kind="jaguar" x={1400} y={900} s={1.05} f={c.gf} face={-1} mode="sit" roar={env(c.f, c.at('168') + 30, c.at('168') + 70, 12, 12) * 0.7} />
				</g>
				<Ring x={640} y={700} t={rel(c, '167', 14)} c="#fff" r={700} n={3} />
			</>
		);
	},
	{
		fg: (c) => {
			const k = lerpF(c.f, c.at('169') + 20, c.at('169') + 60, 0, 1);
			return (
				<>
					<Leaf x={2100 - k * 760} y={760} s={2} rot={190} c="#1f6a3a" />
					<Leaf x={2100 - k * 520} y={520} s={1.8} rot={200} c="#256e40" />
				</>
			);
		},
		over: (c) => (
			<>
				<Slam t={rel(c, '167', 16)} dur={30} text="ROOOAR!" y={80} size={150} c="#ff5a6e" />
				<Slam t={rel(c, '168', 20)} dur={34} text="*yawn*" y={80} size={120} c="#fff" />
			</>
		),
		shake: (c) => 8 * env(c.f, c.at('167') + 14, c.at('167') + 50, 5, 10),
	},
);

/* 170 — the king isn't the scariest thing around */
const s170 = S(
	'170',
	'jd',
	[960, 640, 1.2],
	[960, 600, 1.55],
	(c) => {
		const slip = lerpF(c.f, c.at('170') + 61, c.at('170') + 100, 0, 1);
		return (
			<>
				<Cat kind="lion" x={900} y={910} s={1.35} f={c.gf} mode="stand" thin={0.6} />
				<Crown x={1070 + slip * 220} y={548 + slip * slip * 300} s={1.1} rot={slip * 80} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '170', 60)} dur={110} text="NOT THE SCARIEST ANYMORE" y={80} size={80} c="#fff" />},
);

/* 171-175 — Day 14, the lion is really hungry, smells 71 men */
const s171 = S(
	'171',
	'jn',
	[960, 640, 1.1],
	[1100, 640, 1.3],
	(c) => {
		const lx = lerpF(c.f, c.at('173'), c.dur, -200, 900);
		return (
			<>
				<Cat kind="lion" x={lx} y={910} s={1.25} f={c.gf} mode="walk" ph={c.gf * 0.16} thin={1} />
				{rel(c, '175', 60) > 0
					? [0, 1, 2].map((i) => <path key={i} d={`M${lx + 220},${640 + i * 30} q60,-30 120,0 t120,0`} stroke="#7cf0a0" strokeWidth={5} fill="none" opacity={0.5} strokeDasharray="14 10" />)
					: null}
				<CrowdRow n={5} x0={1280} x1={1760} floor={930} s={0.6} mode="stand" seed="smell" />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '171', 0)} dur={36} text="DAY 14" y={80} size={130} c="#ffd23a" />
				<Slam t={rel(c, '172', 0)} dur={70} text="THE FIGHT EVERYONE WAITED FOR" y={80} size={72} c="#fff" />
				<Slam t={rel(c, '174', 0)} dur={36} text="REALLY HUNGRY" y={800} size={90} c="#ff5a6e" />
				<CountUp t={rel(c, '175', 10)} dur={70} from={0} to={20} suffix=" KG LOST" side="l" y={180} size={110} c="#ff9a3a" roll={14} fmt={false} />
				<Stat t={rel(c, '175', 74)} dur={90} big="71 MEN" label="ALL IN ONE PLACE" side="r" y={180} size={110} c="#8ae0ff" />
			</>
		),
	},
);

/* 176-178 — comes at night without a sound, Danny can't make a sound */
const s176 = S(
	'176',
	'jn2',
	[1000, 640, 1.1],
	[1100, 600, 1.4],
	(c) => (
		<>
			<Fire x={620} y={910} s={0.8} f={c.gf} />
			<Cat kind="lion" x={lerpF(c.f, 0, c.dur, 1900, 1300)} y={910} s={1.2} f={c.gf} mode="crouch" face={-1} thin={1} />
			{man(c, {who: 'danny', x: 940, s: 1.15, face: 1, expr: rel(c, '177', 8) > 0 ? 'wide' : 'normal', mouth: rel(c, '178', 20) > 0 ? 'open' : undefined, g: [['handsOnHead', '178', 36, 130]]})}
			<Say t={rel(c, '178', 58)} x={1110} y={400} text="......" size={70} tail={[-70, 110]} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '178', 58)} dur={90} text="NO SOUND" y={90} size={120} c="#ff5a6e" />},
);

/* 179-181 — Sam stands up: Fire! Everyone! Now! Stand together! */
const s179 = S(
	'179',
	'jn2',
	[1000, 620, 1.2],
	[1000, 560, 1.7],
	(c) => {
		const up = lerpF(c.f, c.at('179') + 14, c.at('179') + 36, 0, 1);
		return (
			<>
				<Fire x={560} y={910} s={0.8} f={c.gf} />
				{man(c, {who: 'sam', x: 1000, s: 1.2, face: 1, g: [['fist', '180', 0, 50], ['point', '181', 0, 40]], expr: 'angry', mouth: rel(c, '180', 0) > 0 ? 'open' : undefined, pose: (p) => ({...p, lean: p.lean + 40 * (1 - up)})})}
				<Say t={rel(c, '180', 0)} x={1180} y={380} text="FIRE! EVERYONE! NOW!" size={52} tail={[-80, 110]} />
				<Say t={rel(c, '181', 0)} x={820} y={300} text="STAND TOGETHER!" size={52} tail={[80, 110]} />
			</>
		);
	},
	{shake: (c) => (rel(c, '180', 0) > 0 && rel(c, '180', 0) < 40 ? 6 : 0)},
);

/* 182-185 — 71 men grab burning branches, make a wall */
const s182 = S(
	'182',
	'jn2',
	[960, 640, 1.0],
	[960, 600, 1.25],
	(c) => {
		const wall = lerpF(c.f, c.at('183'), c.at('184') + 20, 0, 1);
		const wave = env(c.f, c.at('185') + 40, c.dur, 10, 10);
		return (
			<>
				{[0, 1, 2, 3, 4, 5, 6, 7].map((i) =>
					man(c, {
						who: 'sam',
						x: 120 + i * 240 + (1 - wall) * (i % 2 ? 90 : -90),
						s: 0.95,
						seed: i,
						color: ['#d9372a', '#2f6fd8', '#8b5cf6', '#e8802a', '#3aa37a', '#2f6fd8', '#d9372a', '#8b5cf6'][i],
						hair: ['short', 'cap', 'bun', 'spiky', 'short', 'cap', 'bun', 'spiky'][i] as any,
						hairColor: '#333',
						face: 1,
						expr: 'angry',
						mouth: 'open',
						handItem: <Torch f={c.gf + i * 3} />,
						pose: (p) => ({...p, armF: [120 + wave * wob(c.f + i * 4, 30, 3) + (1 - wall) * -40, 20], lean: p.lean - 3}),
					}),
				)}
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Stat t={rel(c, '182', 0)} dur={60} big="71 MEN" label="GRAB BURNING BRANCHES" side="c" y={80} size={120} c="#ffd23a" />
				<Slam t={rel(c, '183', 4)} dur={26} text="THEY DON'T RUN" y={80} size={100} c="#fff" />
				<Slam t={rel(c, '184', 4)} dur={40} text="THEY MAKE A WALL" y={80} size={100} c="#ff9a3a" />
				<Slam t={rel(c, '185', 30)} dur={110} text="SHOULDER TO SHOULDER" y={80} size={86} c="#ffd23a" />
			</>
		),
		shake: (c) => 2 + 3 * env(c.f, c.at('185') + 40, c.dur, 10, 10),
	},
);

/* 186-187 — big cats attack weak and alone */
const s186 = S(
	'186',
	'jn',
	[960, 640, 1.0],
	[1000, 620, 1.2],
	(c) => (
		<>
			<Cat kind="lion" x={1550} y={910} s={1.1} f={c.gf} face={-1} mode="crouch" />
			<CrowdRow n={6} x0={160} x1={960} floor={910} s={0.85} mode="stand" seed="grp" />
			{man(c, {who: 'danny', x: 1250, s: 0.95, face: 1, expr: 'worried'})}
			<g opacity={pop(c.f, c.at('187') + 36)}>
				<circle cx={1250} cy={610} r={150} fill="none" stroke="#ff2340" strokeWidth={8} strokeDasharray="20 14" />
				<Tag x={1250} y={410} text="WEAK + ALONE" c="#ff5a6e" />
			</g>
		</>
	),
	{over: (c) => <Slam t={rel(c, '186', 10)} dur={110} text="CATS HATE A GROUP THAT STANDS ITS GROUND" y={80} size={60} c="#fff" />},
);

/* 188-189 — a wall of 71 screaming men holding fire is not weak and not alone */
const s188 = S(
	'188',
	'jn',
	[960, 640, 1.3],
	[960, 580, 1.8],
	(c) => (
		<>
			{[0, 1, 2, 3].map((i) =>
				man(c, {
					who: 'sam',
					x: 480 + i * 330,
					s: 1.15,
					seed: i,
					color: ['#d9372a', '#2f6fd8', '#8b5cf6', '#e8802a'][i],
					hair: ['short', 'cap', 'bun', 'spiky'][i] as any,
					hairColor: '#333',
					expr: 'angry',
					mouth: 'open',
					handItem: <Torch f={c.gf + i * 3} />,
					pose: (p) => ({...p, armF: [120 + wob(c.f + i * 4, 30, 3), 20]}),
				}),
			)}
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '188', 56)} dur={44} text="NOT WEAK" y={80} size={130} c="#ff9a3a" />
				<Slam t={rel(c, '189', 28)} dur={90} text="NOT ALONE" y={80} size={130} c="#ffd23a" />
			</>
		),
		shake: () => 3,
	},
);

/* 190-193 — the lion stops, looks at the fire, the men, walks back into the dark */
const s190 = S(
	'190',
	'jn2',
	[1100, 640, 1.3],
	[1000, 620, 1.6],
	(c) => {
		const away = lerpF(c.f, c.at('193') + 6, c.dur, 0, 1);
		return (
			<>
				<Fire x={420} y={910} s={0.9} f={c.gf} />
				<CrowdRow n={4} x0={160} x1={700} floor={930} s={0.9} mode="stand" seed="wl" />
				<g opacity={1 - away}>
					<Cat kind="lion" x={1400 + away * 700} y={910} s={1.25} f={c.gf} mode={away > 0 ? 'walk' : 'stand'} ph={c.gf * 0.12} face={away > 0 ? 1 : -1} thin={1} />
				</g>
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '190', 8)} dur={22} text="STOPS" y={90} size={130} c="#ffd23a" />
				<Slam t={rel(c, '191', 0)} dur={34} text="THE FIRE" y={90} size={110} c="#ff9a3a" />
				<Slam t={rel(c, '192', 0)} dur={34} text="THE MEN" y={90} size={110} c="#8ae0ff" />
				<Slam t={rel(c, '193', 20)} dur={70} text="...INTO THE DARK" y={90} size={100} c="#fff" />
			</>
		),
		tint: (c) => `rgba(0,0,0,${lerpF(c.f, c.at('193') + 20, c.dur, 0, 0.5)})`,
	},
);

/* 194-197 — lion vs one man: lion. lion vs 100 men: different fight */
const s194 = S(
	'194',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => {
		const fly = env(c.f, c.at('195'), c.at('195') + 40, 4, 30);
		return (
			<>
				<Cat kind="lion" x={540} y={900} s={0.95} f={c.gf} mode="stand" roar={fly} />
				{man(c, {who: 'danny', x: 1300 + fly * 500, s: 1, floor: 900 - fly * 200, rot: -fly * 70, face: -1, expr: 'wide'})}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '195', 0)} dur={60} text="LION. EVERY TIME." y={80} size={110} c="#ffb04a" />},
);
const s196 = S(
	'196',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.25],
	(c) => (
		<>
			<Cat kind="lion" x={380} y={900} s={0.95} f={c.gf} mode="stand" />
			<g opacity={pop(c.f, c.at('196') + 26)}>
				<CrowdRow n={14} x0={800} x1={1800} floor={900} s={0.85} mode="stand" seed="d100" />
			</g>
		</>
	),
	{over: (c) => (
		<>
			<Slam t={rel(c, '196', 56)} dur={60} text="WORK TOGETHER?" y={80} size={110} c="#8ae0ff" />
			<Slam t={rel(c, '197', 14)} dur={70} text="A VERY DIFFERENT FIGHT" y={80} size={90} c="#ffd23a" />
		</>
	)},
);

/* 198-200 — Round 4: lion vs 100 men, the men */
const s198 = S(
	'198',
	'jn',
	[960, 640, 1.0],
	[960, 600, 1.15],
	(c) => (
		<>
			<Fire x={960} y={910} s={0.9} f={c.gf} />
			<CrowdRow n={10} x0={160} x1={1760} floor={920} s={0.8} mode="dance" seed="r4" />
			<Confetti2 c={c} />
		</>
	),
	{over: (c) => <Round t={rel(c, '198', 0)} dur={c.dur - 4} n={4} title="LION vs 100 MEN" winner="THE MEN +1" c="#8ae0ff" />},
);
const Confetti2: React.FC<{c: any}> = ({c}) => null;

export const SHOTS_C: ShotDef[] = [s121, s124, s126, s127, s129, s131, s136, s139, s142, s144, s147, s149, s151, s155, s158, s161, s165, s167, s170, s171, s176, s179, s182, s186, s188, s190, s194, s196, s198];
