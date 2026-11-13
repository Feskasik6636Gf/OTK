import React from 'react';
import {CrowdRow} from '../kit/kit';
import {Callout} from '../kit/graphics';
import {env} from '../kit/actions';
import {Onoma} from '../reference/PauseTime';
import type {ShotDef} from '../kit/coverage';
import {Band, Cat, Eyes, Fish, Heli, Pod, Rock, Spark, Tree} from './critters';
import {S, lerpF, lying, man, pop, rel, sc} from './dsl';
import {Fire, Water} from './places';
import {CountUp, Round, Say, Slam, Stat} from './overlays';
import {Confetti, Crown, Leaf, Ring, SpeedLines, Tag, Thermo} from './props2';

const wob = (f: number, a: number, p = 6) => Math.sin(f / p) * a;

const BigCar: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-200} y={-120} width={400} height={80} rx={26} fill="#d9372a" />
		<path d="M-120,-120 L-70,-190 L90,-190 L140,-120 Z" fill="#c02a20" />
		<rect x={-60} y={-180} width={130} height={56} fill="#cfeaf7" opacity={0.8} />
		<circle cx={-120} cy={-40} r={34} fill="#222" />
		<circle cx={120} cy={-40} r={34} fill="#222" />
	</g>
);

/* 201-205 — Day 18, Max meets the lion on the same riverbank */
const s201 = S(
	'201',
	'riv',
	[960, 620, 1.0],
	[960, 600, 1.3],
	(c) => {
		const mx = lerpF(c.f, c.at('201') + 10, c.at('202') + 40, -200, 560);
		const lx = lerpF(c.f, c.at('202') + 20, c.at('203') + 30, 2200, 1440);
		return (
			<>
				{man(c, {who: 'max', x: mx, s: 1.1, face: 1, to: undefined})}
				<Cat kind="lion" x={lx} y={900} s={1.2} f={c.gf} face={-1} mode={rel(c, '203', 30) > 0 ? 'crouch' : 'walk'} ph={c.gf * 0.16} thin={1} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '201', 0)} dur={40} text="DAY 18" y={80} size={130} c="#ffd23a" />
				<Slam t={rel(c, '202', 10)} dur={80} text="MAX MEETS THE LION" y={80} size={86} c="#fff" />
				<Slam t={rel(c, '204', 18)} dur={30} text="STARVING" y={780} size={110} c="#ff5a6e" />
				<Slam t={rel(c, '205', 8)} dur={30} text="ALONE" y={780} size={110} c="#8ae0ff" />
			</>
		),
	},
);

/* 206-210 — the stare, one punch, he doesn't */
const s206 = S(
	'206',
	'riv',
	[960, 620, 1.35],
	[960, 580, 1.8],
	(c) => {
		const cock = env(c.f, c.at('209'), c.at('210') + 6, 6, 8);
		return (
			<>
				{man(c, {who: 'max', x: 640, s: 1.2, face: 1, expr: 'angry', pose: (p) => ({...p, armF: [p.armF[0] + (-60 - p.armF[0]) * cock, 90], lean: p.lean - 6 * cock})})}
				<Cat kind="lion" x={1340} y={900} s={1.25} f={c.gf} face={-1} mode="crouch" thin={1} />
				<Ring x={960} y={620} t={rel(c, '206', 14)} c="#ff5a6e" r={200} n={2} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '208', 14)} dur={50} text="1 SECOND" y={80} size={120} c="#ffd23a" />
				<Slam t={rel(c, '209', 0)} dur={30} text="ONE PUNCH" y={80} size={120} c="#ff5a6e" />
				<Slam t={rel(c, '210', 6)} dur={70} text="HE DOESN'T" y={80} size={130} c="#7cf0a0" />
			</>
		),
	},
);

/* 211-213 — reaches for a Brazil nut, remembers lions don't eat nuts */
const s211 = S(
	'211',
	'riv',
	[900, 620, 1.35],
	[900, 580, 1.6],
	(c) => {
		const pull = env(c.f, c.at('211') + 22, c.at('212') + 30, 8, 8);
		return (
			<>
				{man(c, {who: 'max', x: 700, s: 1.2, face: 1, handItem: pull > 0.3 ? <Pod x={0} y={0} s={0.5} /> : null, g: [['presentF', '211', 28, 80], ['scratch', '213', 0, 40]], expr: rel(c, '212', 19) > 0 ? 'wide' : 'normal'})}
				<Cat kind="lion" x={1340} y={900} s={1.25} f={c.gf} face={-1} mode="crouch" thin={1} />
				<Say t={rel(c, '212', 19)} x={820} y={340} text="WAIT…" size={56} tail={[-30, 110]} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '213', 0)} dur={60} text="LIONS DON'T EAT NUTS" strike y={80} size={86} c="#ffd23a" />},
);

/* 214-216 — catches a fish with bare hands, throws it across the river */
const s214 = S(
	'214',
	'riv',
	[960, 700, 1.2],
	[1100, 640, 1.2],
	(c) => {
		const grab = env(c.f, c.at('214') + 36, c.at('216') + 10, 10, 6);
		const thr = lerpF(c.f, c.at('216') + 4, c.at('216') + 40, 0, 1);
		const fx = 820 + thr * 700;
		const fy = 640 - Math.sin(thr * Math.PI) * 220 + thr * 120;
		return (
			<>
				{man(c, {who: 'max', x: 760, s: 1.2, face: 1, floor: 930, pose: (p) => ({...p, lean: p.lean + 24 * (1 - env(c.f, c.at('215'), c.at('216') + 6, 4, 4)), armF: [p.armF[0] + (70 - p.armF[0]) * grab, 40], armB: [p.armB[0] + (60 - p.armB[0]) * grab, 40]})})}
				{c.f > c.at('214') + 38 ? <Fish x={thr > 0 ? fx : 880} y={thr > 0 ? fy : 610} s={0.9} f={c.gf} rot={thr > 0 ? -30 + thr * 60 : 0} /> : null}
				<Spark x={880} y={780} t={rel(c, '214', 40)} c="#8ae0ff" />
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '214', 44)} dur={50} text="BARE HANDS" y={80} size={120} c="#8ae0ff" />
			<Slam t={rel(c, '215', 4)} dur={34} text="A BIG ONE!" y={780} size={110} c="#ffd23a" />
		</>
	)},
);

/* 217-220 — the lion sniffs it, eats it, looks at Max, leaves */
const s217 = S(
	'217',
	'riv',
	[1300, 640, 1.3],
	[1200, 600, 1.9],
	(c) => {
		const away = lerpF(c.f, c.at('220') + 4, c.dur, 0, 1);
		return (
			<>
				{man(c, {who: 'max', x: 560, s: 1.15, face: 1, expr: 'normal'})}
				<g opacity={1 - away * 0.9}>
					<Cat kind="lion" x={1380 + away * 800} y={900} s={1.25} f={c.gf} face={away > 0 ? 1 : -1} mode={away > 0 ? 'walk' : 'stand'} ph={c.gf * 0.15} thin={1} />
				</g>
				{rel(c, '218', 8) < 0 ? <Fish x={1160} y={880} s={0.6} f={c.gf} rot={-8} /> : null}
				<Onoma x={1150} y={780} text="SNIFF" t={rel(c, '217', 15)} c="#fff" size={60} />
				<Onoma x={1150} y={780} text="NOM NOM" t={rel(c, '218', 4)} c="#ffd23a" size={70} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '219', 40)} dur={70} text="A LONG LOOK…" y={80} size={100} c="#fff" />},
);

/* 221-223 — Round 5: the jungle, nobody wins */
const s221 = S(
	'221',
	'rivdusk',
	[960, 640, 1.0],
	[960, 620, 1.15],
	(c) => (
		<>
			{man(c, {who: 'max', x: 480, s: 1.1, face: 1, expr: 'normal'})}
			<Cat kind="lion" x={1520} y={900} s={1.1} f={c.gf} face={-1} mode="stand" thin={1} />
		</>
	),
	{over: (c) => <Round t={rel(c, '221', 0)} dur={c.dur - 4} n={5} title="THE JUNGLE" winner="NOBODY WINS" c="#b8c0d0" />},
);

/* 224-226 — Day 20, the jungle starts winning, everyone gets weaker */
const s224 = S(
	'224',
	'jdusk',
	[960, 640, 1.0],
	[960, 600, 1.2],
	(c) => (
		<>
			<Cat kind="lion" x={420} y={900} s={0.95} f={c.gf} mode="stand" thin={1} />
			<CrowdRow n={4} x0={820} x1={1250} floor={900} s={0.8} mode="stand" seed="weak" />
			{man(c, {who: 'max', x: 1580, s: 1.0, expr: 'sad', pose: (p) => ({...p, lean: 14, head: 20})})}
		</>
	),
	{over: (c) => (
		<>
			<Slam t={rel(c, '224', 0)} dur={40} text="DAY 20" y={70} size={130} c="#ffd23a" />
			<Slam t={rel(c, '225', 14)} dur={46} text="THE JUNGLE STARTS WINNING" y={70} size={74} c="#ff5a6e" />
			<Slam t={rel(c, '226', 40)} dur={80} text="EVERYONE GETS WEAKER" y={780} size={80} c="#fff" />
		</>
	)},
);

/* 227-229 — lion 30 kg lighter, paws cut, no sleep */
const s227 = S(
	'227',
	'jdusk',
	[900, 640, 1.2],
	[960, 620, 1.5],
	(c) => (
		<>
			<Cat kind="lion" x={lerpF(c.f, 0, c.dur, 400, 1300)} y={900} s={1.25} f={c.gf} mode="walk" ph={c.gf * 0.09} thin={1} />
			{[0, 1, 2].map((i) => (
				<g key={i} opacity={pop(c.f, c.at('229') + 8 + i * 14)}>
					<text x={1500 + i * 70} y={520 - i * 50} fontSize={70} fontFamily="Rubik" fontWeight={900} fill="#cfe0ff" stroke="#102" strokeWidth={6} paintOrder="stroke">
						Z
					</text>
				</g>
			))}
		</>
	),
	{over: (c) => (
		<>
			<CountUp t={rel(c, '227', 24)} dur={70} to={30} suffix=" KG LIGHTER" side="l" y={150} size={110} c="#ff9a3a" roll={14} fmt={false} />
			<Slam t={rel(c, '228', 10)} dur={36} text="CUT PAWS" y={780} size={100} c="#ff5a6e" />
			<Slam t={rel(c, '229', 8)} dur={70} text="NO SLEEP IN WEEKS" y={780} size={90} c="#8ab4ff" />
		</>
	)},
);

/* 230 — savannah: sleeps 20 hours a day */
const s230 = S(
	'230',
	'sav',
	[960, 700, 1.2],
	[960, 660, 1.5],
	(c) => (
		<>
			<Cat kind="lion" x={900} y={910} s={1.3} f={c.gf} mode="lie" />
			{[0, 1, 2].map((i) => (
				<text key={i} x={1060 + i * 60} y={650 - i * 60 - ((c.f + i * 20) % 40)} fontSize={60 + i * 12} fontFamily="Rubik" fontWeight={900} fill="#fff" stroke="#6a3a10" strokeWidth={6} paintOrder="stroke">
					Z
				</text>
			))}
		</>
	),
	{over: (c) => <CountUp t={rel(c, '230', 56)} dur={80} to={20} suffix=" HOURS" label="SLEEP A DAY" side="r" y={140} size={140} c="#ffd23a" roll={16} fmt={false} />},
);
const s231 = S(
	'231',
	'jn2',
	[960, 660, 1.2],
	[960, 620, 1.5],
	(c) => {
		const jump = env(c.f, c.at('231') + 40, c.at('231') + 70, 3, 14);
		return (
			<>
				<Cat kind="lion" x={900} y={910 - jump * 90} s={1.25} f={c.gf} mode={jump > 0.2 ? 'stand' : 'lie'} thin={1} roar={jump * 0.3} />
				<Onoma x={1380} y={560} text="SNAP!" t={rel(c, '231', 38)} c="#ffd23a" size={90} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '231', 30)} dur={80} text="EVERY SOUND WAKES HIM" y={80} size={80} c="#fff" />, shake: (c) => (rel(c, '231', 40) > 0 && rel(c, '231', 40) < 8 ? 10 : 0)},
);

/* 232-234 — men start breaking: Danny wants a road, Sam says terrible idea */
const s232 = S(
	'232',
	'jd',
	[960, 620, 1.2],
	[960, 580, 1.5],
	(c) => (
		<>
			{man(c, {who: 'danny', x: 640, s: 1.15, face: 1, g: [['point', '233', 20, 120]], expr: 'angry'})}
			{man(c, {who: 'sam', x: 1260, s: 1.15, face: -1, g: [['shrug', '234', 8, 70]], expr: 'worried'})}
			<Say t={rel(c, '233', 52)} x={640} y={330} text="LET'S FIND A ROAD!" size={50} tail={[0, 100]} />
			<Say t={rel(c, '234', 26)} x={1260} y={330} text="TERRIBLE IDEA." size={50} tail={[0, 100]} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '232', 8)} dur={60} text="THE MEN START BREAKING" y={80} size={80} c="#ff5a6e" />},
);

/* 235-237 — can't see the sun, walk in circles, farm boy */
const s235 = S(
	'235',
	'jd',
	[960, 600, 1.0],
	[960, 540, 1.2],
	(c) => (
		<>
			<circle cx={1500} cy={120} r={60} fill="#fff0a0" />
			<g opacity={pop(c.f, c.at('235') + 20)}>
				<line x1={1420} y1={40} x2={1580} y2={200} stroke="#ff2340" strokeWidth={14} strokeLinecap="round" />
				<line x1={1580} y1={40} x2={1420} y2={200} stroke="#ff2340" strokeWidth={14} strokeLinecap="round" />
			</g>
			<ellipse cx={960} cy={860} rx={Math.max(1, lerpF(c.f, c.at('236') + 10, c.at('236') + 50, 0, 380))} ry={Math.max(1, lerpF(c.f, c.at('236') + 10, c.at('236') + 50, 0, 70))} fill="none" stroke="#ffd23a" strokeWidth={8} strokeDasharray="26 16" />
			{man(c, {who: 'danny', x: 640, s: 1.1, face: 1, g: [['point', '237', 8, 60]], expr: 'angry'})}
			{man(c, {who: 'sam', x: 1280, s: 1.1, face: -1})}
			<Say t={rel(c, '237', 34)} x={640} y={340} text="FARM BOY!" size={52} tail={[0, 100]} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '235', 26)} dur={110} text="NO SUN UNDER THE TREES" y={80} size={80} c="#fff" />},
);

/* 238 — 30 men follow Danny */
const s238 = S(
	'238',
	'jd2',
	[960, 620, 1.0],
	[1200, 600, 1.0],
	(c) => {
		const t = lerpF(c.f, c.at('238') + 4, c.dur, 0, 1);
		return (
			<>
				{man(c, {who: 'danny', x: 700 + t * 900, s: 1.1, face: 1, to: undefined})}
				<CrowdRow n={9} x0={150 + t * 900} x1={600 + t * 900} floor={900} s={0.75} mode="walk" dir={1} seed="follow" t={rel(c, '238', 4) * 0.2} />
				{man(c, {who: 'sam', x: 1600, s: 1.1, face: -1, expr: 'worried'})}
			</>
		);
	},
	{over: (c) => <CountUp t={rel(c, '238', 0)} dur={90} to={30} label="MEN FOLLOW DANNY" side="c" y={80} size={130} c="#8ae0ff" roll={14} fmt={false} />},
);

/* 239-242 — three days later buttons one by one, lost, 41 men left */
const s239 = S(
	'239',
	'jdusk',
	[960, 640, 1.0],
	[960, 600, 1.15],
	(c) => {
		const hx = lerpF(c.f, c.at('239') + 36, c.at('240') + 30, 2300, 400);
		return (
			<>
				<Heli x={hx} y={250} s={0.9} f={c.gf} face={-1} tilt={-4} />
				<CrowdRow n={7} x0={300} x1={1600} floor={900} s={0.8} mode="stand" seed="lost" />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '239', 0)} dur={46} text="3 DAYS LATER" y={80} size={110} c="#fff" />
				<Slam t={rel(c, '241', 0)} dur={30} text="LOST." y={80} size={150} c="#ff3a52" />
				<Stat t={rel(c, '242', 0)} dur={80} big="41 LEFT" side="c" y={780} size={150} c="#ffd23a" />
			</>
		),
	},
);

/* 243-245 — and Max? completely alone */
const s243 = S(
	'243',
	'jd2',
	[960, 600, 1.4],
	[960, 560, 0.85],
	(c) => <>{man(c, {who: 'max', x: 960, s: 1.1, expr: 'sad', pose: (p) => ({...p, lean: 10, head: 14})})}</>,
	{over: (c) => (
		<>
			<Slam t={rel(c, '244', 14)} dur={60} text="A DIFFERENT PROBLEM" y={80} size={86} c="#fff" />
			<Slam t={rel(c, '245', 6)} dur={70} text="COMPLETELY ALONE" y={780} size={100} c="#8ab4ff" />
		</>
	)},
);

/* 246-247 — talks to a rock, names it Theo */
const s246 = S(
	'246',
	'jd',
	[960, 620, 1.3],
	[1000, 580, 1.7],
	(c) => {
		const named = rel(c, '247', 24) > 0;
		return (
			<>
				<Rock x={1240} y={915} s={1.5} face={named} f={c.gf} glasses={named} />
				{man(c, {who: 'max', x: 760, s: 1.2, face: 1, g: [['presentF', '246', 30, 90], ['point', '247', 24, 70]], mouth: 'open'})}
				<Tag x={1240} y={560} text="THEO" k={pop(c.f, c.at('247') + 34)} />
				<Say t={rel(c, '246', 36)} x={800} y={330} text="HEY ROCK." size={50} tail={[0, 100]} />
			</>
		);
	},
);

/* 248-249 — loneliness is as hard as not sleeping or eating */
const s248 = S(
	'248',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.15],
	(c) => {
		const bars = [
			['LONELINESS', '248', 60, '#8ab4ff'],
			['NO SLEEP', '249', 20, '#ff9a3a'],
			['NO FOOD', '249', 70, '#ff5a6e'],
		] as const;
		return (
			<>
				{bars.map((b, i) => {
					const t = c.at(b[1]) + b[2];
					const w = lerpF(c.f, t, t + 30, 0, 900);
					return (
						<g key={i} transform={`translate(520,${360 + i * 150})`}>
							<rect x={0} y={0} width={900} height={70} rx={35} fill="#1a0810" opacity={0.7} />
							<rect x={0} y={0} width={w} height={70} rx={35} fill={b[3]} />
							<text x={24} y={50} fontSize={40} fontFamily="Rubik" fontWeight={900} fill="#fff" stroke="#14060c" strokeWidth={5} paintOrder="stroke">
								{b[0]}
							</text>
						</g>
					);
				})}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '248', 0)} dur={160} text="SCIENTISTS FOUND:" y={70} size={90} c="#ffd23a" />},
);

/* 250-251 — can lift a car, can't lift that */
const s250 = S(
	'250',
	'jd',
	[960, 600, 1.1],
	[960, 540, 1.4],
	(c) => {
		const lift = env(c.f, c.at('250') + 24, c.at('251'), 10, 8);
		const cloud = lerpF(c.f, c.at('251') + 12, c.at('251') + 40, 0, 1);
		return (
			<>
				<g opacity={1 - cloud}>
					<BigCar x={960} y={900 - lift * 420 - 130} s={0.5} />
				</g>
				{man(c, {who: 'max', x: 960, s: 1.1, expr: cloud > 0.3 ? 'sad' : 'angry', pose: (p) => ({...p, armF: [p.armF[0] + (170 - p.armF[0]) * lift, 6], armB: [p.armB[0] + (-170 - p.armB[0]) * lift, 6], lean: p.lean + 28 * cloud, head: p.head + 20 * cloud})})}
				<g opacity={cloud}>
					<ellipse cx={960} cy={300} rx={340} ry={120} fill="#4a5060" />
					<ellipse cx={780} cy={340} rx={190} ry={90} fill="#3a4050" />
					<ellipse cx={1160} cy={340} rx={200} ry={90} fill="#3a4050" />
					<text x={960} y={320} textAnchor="middle" fontSize={64} fontFamily="Rubik" fontWeight={900} fill="#cfd5e0">
						LONELINESS
					</text>
				</g>
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '250', 26)} dur={50} text="LIFTS A CAR" y={80} size={110} c="#ffd23a" />
			<Slam t={rel(c, '251', 10)} dur={70} text="CAN'T LIFT THAT" y={80} size={110} c="#8ab4ff" />
		</>
	)},
);

/* 252-254 — Round 5 again: the jungle, nobody wins */
const s252 = S(
	'252',
	'jn',
	[960, 640, 1.0],
	[960, 620, 1.15],
	(c) => <>{man(c, {who: 'max', x: 960, s: 1.1, expr: 'sad', pose: (p) => ({...p, lean: 12})})}</>,
	{over: (c) => <Round t={rel(c, '252', 0)} dur={c.dur - 4} n={5} title="THE JUNGLE" winner="NOBODY WINS" c="#b8c0d0" />},
);

/* 255-257 — Day 29, rain at midnight */
const s255 = S(
	'255',
	'js',
	[960, 640, 1.1],
	[960, 600, 1.3],
	(c) => (
		<>
			{man(c, {who: 'max', x: 560, s: 1.05, expr: 'worried'})}
			<Cat kind="lion" x={1380} y={900} s={1.1} f={c.gf} face={-1} mode="lie" thin={1} wet={1} />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '255', 0)} dur={46} text="DAY 29" y={70} size={130} c="#ff5a6e" />
				<Slam t={rel(c, '256', 24)} dur={50} text="MIDNIGHT" sub="IT STARTS RAINING" y={70} size={110} c="#8ab4ff" />
				<Slam t={rel(c, '257', 8)} dur={60} text="AND DOESN'T STOP" y={780} size={90} c="#fff" />
			</>
		),
		flash: (c) => (rel(c, '257', 12) > 0 ? Math.max(0, 0.7 - rel(c, '257', 12) / 9) : 0),
	},
);

/* 258-261 — Amazon rain, rivers rise, forest underwater */
const s258 = S(
	'258',
	'rivflood',
	[960, 640, 1.0],
	[960, 580, 1.2],
	(c) => <>{man(c, {who: 'max', x: 560, s: 1.05, expr: 'worried'})}</>,
	{
		fg: (c) => {
			const y = lerpF(c.f, c.at('260'), c.at('261') + 60, 1080, 640);
			return <Water f={c.gf} y0={y} y1={1500} flood o={0.8} />;
		},
		over: (c) => (
			<>
				<Slam t={rel(c, '258', 20)} dur={90} text="MORE RAIN THAN ALMOST ANYWHERE" y={70} size={64} c="#fff" />
				<Slam t={rel(c, '260', 20)} dur={46} text="RIVERS RISE METERS" y={70} size={80} c="#8ab4ff" />
				<Slam t={rel(c, '261', 20)} dur={70} text="FOREST UNDERWATER" y={70} size={80} c="#ff9a3a" />
			</>
		),
	},
);

/* 262-263 — the river is a monster, the camp is gone */
const s262 = S(
	'262',
	'rivflood',
	[960, 640, 1.0],
	[960, 600, 1.4],
	(c) => (
		<>
			<g transform={`translate(${lerpF(c.f, c.at('263') + 20, c.dur, 700, 1500)},820) rotate(${wob(c.f, 8, 12)})`}>
				<rect x={-250} y={-60} width={500} height={60} fill="#7a5632" />
				<path d="M-250,-60 L0,-190 L250,-60 Z" fill="#5a3a1c" />
			</g>
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '262', 50)} dur={60} text="A MONSTER" y={80} size={140} c="#ff3a52" />
				<Slam t={rel(c, '263', 22)} dur={60} text="CAMP: GONE" y={780} size={100} c="#fff" />
			</>
		),
		shake: () => 5,
	},
);

/* 264-265 — 41 men on a shrinking muddy island */
const s264 = S(
	'264',
	'rivflood',
	[960, 700, 1.1],
	[960, 700, 1.3],
	(c) => {
		const r = lerpF(c.f, 0, c.dur, 520, 260);
		return (
			<>
				<ellipse cx={960} cy={900} rx={r} ry={r * 0.18} fill="#7a5a34" />
				<CrowdRow n={9} x0={960 - r * 0.7} x1={960 + r * 0.7} floor={890} s={0.7} mode="panic" seed="island" />
			</>
		);
	},
	{over: (c) => <Stat t={rel(c, '264', 0)} dur={c.dur - 6} big="41 MEN" label="ON A SHRINKING ISLAND" side="c" y={80} size={130} c="#ffd23a" />, shake: () => 3},
);

/* 266-267 — Sam knows there's high ground; river 50 m wide moving like a highway */
const s266 = S(
	'266',
	'rivflood',
	[700, 640, 1.2],
	[1100, 640, 1.2],
	(c) => (
		<>
			<SpeedLines f={c.gf} y0={740} y1={900} dir={1} c="#e8d4b0" />
			{man(c, {who: 'sam', x: 600, s: 1.2, face: 1, g: [['point', '266', 30, 120]], expr: 'worried'})}
			<ellipse cx={1760} cy={900} rx={320} ry={50} fill="#4a7a30" />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '266', 40)} dur={60} text="HIGH GROUND!" y={70} size={110} c="#7cf0a0" />
				<CountUp t={rel(c, '267', 18)} dur={110} to={50} suffix=" M WIDE" label="MOVING LIKE A HIGHWAY" side="c" y={70} size={120} c="#ff9a3a" roll={14} fmt={false} />
			</>
		),
	},
);

/* 268-272 — lion on a fallen tree in the river */
const s268 = S(
	'268',
	'rivflood',
	[960, 700, 1.1],
	[960, 700, 1.5],
	(c) => (
		<>
			<g transform={`translate(0,${wob(c.f, 10, 8)}) rotate(${wob(c.f, 4, 14)} 960 780)`}>
				<rect x={560} y={770} width={800} height={46} rx={22} fill="#4a2e18" />
				<Cat kind="lion" x={960} y={782} s={1.05} f={c.gf} mode="crouch" thin={1} wet={1} shadow={false} />
			</g>
			<Eyes x={1500} y={600} s={0} />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '269', 8)} dur={40} text="THE LION" y={70} size={120} c="#ffb04a" />
				<Slam t={rel(c, '270', 0)} dur={70} text="SOAKING WET. EXHAUSTED." y={780} size={72} c="#fff" />
				<Slam t={rel(c, '272', 56)} dur={40} text="NOT IN THIS" y={70} size={110} c="#ff5a6e" />
			</>
		),
		shake: () => 4,
	},
);

/* 273-275 — Max on the far bank, safe on high ground */
const s273 = S(
	'273',
	'rivflood',
	[1300, 620, 1.1],
	[1500, 580, 1.4],
	(c) => (
		<>
			{man(c, {who: 'max', x: 1560, s: 1.15, face: -1, g: [['armsCrossed', '273', 40, 120], ['think', '274', 40, 120]], expr: 'normal'})}
			<g opacity={pop(c.f, c.at('275') + 4)}>
				<g transform="translate(1560,330)">
					<path d="M-60,-40 h120 v40 c0,50 -40,70 -60,70 c-20,0 -60,-20 -60,-70 Z" fill="#ffc72a" stroke="#b8860b" strokeWidth={6} />
					<rect x={-14} y={60} width={28} height={36} fill="#e8a010" />
					<rect x={-50} y={96} width={100} height={20} rx={6} fill="#b8860b" />
				</g>
			</g>
		</>
	),
	{over: (c) => (
		<>
			<Slam t={rel(c, '273', 66)} dur={60} text="MAX: SAFE" y={70} size={110} c="#7cf0a0" />
			<Slam t={rel(c, '275', 0)} dur={50} text="WIN THE WHOLE GAME" y={780} size={80} c="#ffd23a" />
		</>
	)},
);

/* 276-277 — looks at the wristband, then the men, then the lion */
const s276 = S(
	'276',
	'rivflood',
	[1500, 620, 1.7],
	[1000, 600, 1.0],
	(c) => {
		const look = rel(c, '276', 60) > 0 ? (rel(c, '277', 10) > 0 ? 1 : 0.5) : 0;
		return (
			<>
				{man(c, {who: 'max', x: 1560, s: 1.15, face: -1, g: [['presentF', '276', 10, 56]], look: [-0.6 - look, 0], expr: 'worried'})}
				<ellipse cx={600} cy={900} rx={240} ry={40} fill="#7a5a34" />
				<CrowdRow n={5} x0={420} x1={780} floor={890} s={0.6} mode="panic" seed="isl2" />
				<g transform={`translate(1060,830) rotate(${wob(c.f, 4, 14)})`}>
					<rect x={-200} y={-20} width={400} height={36} rx={18} fill="#4a2e18" />
					<Cat kind="lion" x={0} y={-10} s={0.55} f={c.gf} mode="crouch" thin={1} wet={1} shadow={false} />
				</g>
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '276', 16)} dur={36} text="THE BUTTON" y={70} size={100} c="#ff5a6e" />
			<Slam t={rel(c, '276', 68)} dur={26} text="THE MEN" y={70} size={100} c="#8ae0ff" />
			<Slam t={rel(c, '277', 24)} dur={40} text="THE LION" y={70} size={100} c="#ffb04a" />
		</>
	)},
);

/* 278-279 — walks into the river, the water hits like a truck */
const s278 = S(
	'278',
	'rivflood',
	[1500, 700, 1.1],
	[1100, 760, 1.4],
	(c) => {
		const x = lerpF(c.f, c.at('278') + 8, c.at('279') + 20, 1560, 1180);
		return (
			<>
				{man(c, {who: 'max', x, s: 1.1, face: -1, floor: 900 + lerpF(c.f, c.at('278') + 20, c.at('279') + 20, 0, 30), pose: (p) => ({...p, lean: 14 * env(c.f, c.at('279') + 6, c.dur, 4, 10)})})}
				<Onoma x={1160} y={640} text="WHAM!" t={rel(c, '279', 14)} c="#8ae0ff" size={100} />
			</>
		);
	},
	{
		fg: (c) => <Water f={c.gf} y0={lerpF(c.f, c.at('278') + 10, c.at('279') + 24, 1040, 780)} y1={1500} flood o={0.78} />,
		over: (c) => <Slam t={rel(c, '278', 10)} dur={44} text="HE WALKS IN" y={70} size={110} c="#ffd23a" />,
		shake: (c) => (rel(c, '279', 14) > 0 && rel(c, '279', 14) < 30 ? 12 : 0),
	},
);

/* 280-282 — grabs the biggest tree, pushes it across the river */
const s280 = S(
	'280',
	'rivflood',
	[1300, 520, 0.95],
	[1000, 560, 1.0],
	(c) => {
		const fall = lerpF(c.f, c.at('282') + 28, c.at('283') + 22, 0, 90);
		return (
			<>
				<Tree x={1500} y={900} s={1.5} f={c.gf} h={640} w={110} fall={fall} dir={-1} shake={env(c.f, c.at('282') + 6, c.at('282') + 40, 4, 10) * 5} />
				{man(c, {who: 'max', x: 1380, s: 1.15, face: 1, pose: (p) => ({...p, armF: [100, 6], armB: [90, 6], lean: 18 * env(c.f, c.at('280') + 40, c.at('283') + 10, 12, 10)})})}
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '280', 24)} dur={50} text="THE BIGGEST TREE" y={70} size={96} c="#fff" />
				<CountUp t={rel(c, '281', 14)} dur={90} to={100} suffix=" YEARS TO GROW" side="c" y={780} size={90} c="#ffd23a" roll={14} fmt={false} />
				<Slam t={rel(c, '282', 28)} dur={50} text="PUSH!" y={70} size={140} c="#ff5a6e" />
			</>
		),
	},
);

/* 283-285 — the trunk crashes onto the island: a bridge! Go! */
const s283 = S(
	'283',
	'rivflood',
	[960, 640, 1.0],
	[1000, 640, 1.2],
	(c) => (
		<>
			<ellipse cx={420} cy={900} rx={300} ry={46} fill="#7a5a34" />
			<g>
				<rect x={150} y={760} width={1500} height={56} rx={26} fill="#5a3a1c" />
				<rect x={150} y={764} width={1500} height={12} rx={6} fill="#7a5632" />
			</g>
			{man(c, {who: 'sam', x: 340, s: 1.0, face: 1, g: [['point', '285', 0, 60]], mouth: 'open', floor: 900})}
			<Say t={rel(c, '285', 0)} x={520} y={440} text="GO!" size={110} tail={[-80, 110]} />
			<Onoma x={440} y={720} text="CRASH!" t={rel(c, '283', 50)} c="#ffd23a" size={110} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '284', 0)} dur={44} text="A BRIDGE!" y={70} size={140} c="#7cf0a0" />, shake: (c) => (rel(c, '283', 50) > 0 && rel(c, '283', 50) < 14 ? 16 : 0)},
);

/* 286-288 — 41 men run across the trunk, Max holds it steady */
const s286 = S(
	'286',
	'rivflood',
	[960, 640, 1.0],
	[1100, 640, 1.15],
	(c) => {
		const t = (c.f - c.at('286') - 6) / 200;
		return (
			<>
				<rect x={150} y={760} width={1500} height={56} rx={26} fill="#5a3a1c" />
				{Array.from({length: 8}).map((_, i) => {
					const x = 220 + (t * 1500 - i * 110);
					return x > 150 && x < 1650 ? man(c, {who: 'sam', x, s: 0.6, seed: i, floor: 760, color: ['#d9372a', '#2f6fd8', '#8b5cf6', '#e8802a', '#3aa37a'][i % 5], hair: ['short', 'cap', 'bun', 'spiky'][i % 4] as any, hairColor: '#333', pose: (p) => ({...p, lean: 10, armF: [60, 20], armB: [-20, 30], legF: [20 * Math.sin(c.f / 2 + i), 20], legB: [-20 * Math.sin(c.f / 2 + i), 20]}), shadow: false}) : null;
				})}
				{man(c, {who: 'max', x: 1700, s: 1.1, face: -1, pose: (p) => ({...p, armF: [120, 10], armB: [120, 10], lean: 12 + wob(c.f, 2, 3)}), floor: 900})}
			</>
		);
	},
	{
		fg: (c) => <Water f={c.gf} y0={880} y1={1500} flood o={0.7} />,
		over: (c) => (
			<>
				<Stat t={rel(c, '286', 3)} dur={90} big="41" label="MEN ACROSS" side="l" y={150} size={150} c="#ffd23a" />
				<Slam t={rel(c, '287', 34)} dur={60} text="HOLDING EACH OTHER'S SHIRTS" y={70} size={70} c="#fff" />
				<Slam t={rel(c, '288', 36)} dur={70} text="MAX HOLDS IT STEADY" y={780} size={80} c="#ff5a6e" />
			</>
		),
		shake: () => 5,
	},
);

/* 289-291 — last man crosses, Max looks back at the lion; the tree breaks */
const s289 = S(
	'289',
	'rivflood',
	[1300, 660, 1.1],
	[1100, 700, 1.4],
	(c) => {
		const split = lerpF(c.f, c.at('291') + 6, c.at('291') + 30, 0, 1);
		return (
			<>
				{man(c, {who: 'max', x: 1600, s: 1.1, face: -1, look: [-0.8, 0], g: [['stop', '289', 70, 120]]})}
				<g transform={`translate(${wob(c.f, 20, 18)},${wob(c.f, 8, 8)})`}>
					<rect x={620} y={810 + split * 40} width={260} height={44} rx={20} fill="#4a2e18" transform={`rotate(${split * -12} 750 830)`} />
					<rect x={880} y={810 + split * 60} width={260} height={44} rx={20} fill="#4a2e18" transform={`rotate(${split * 18} 1010 830)`} />
					<Cat kind="lion" x={880} y={810} s={0.7} f={c.gf} mode="crouch" thin={1} wet={1} shadow={false} />
				</g>
				<Onoma x={880} y={700} text="CRACK…" t={rel(c, '291', 12)} c="#ffd23a" size={80} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '291', 4)} dur={70} text="IT'S BREAKING APART" y={70} size={90} c="#ff5a6e" />, shake: () => 4},
);

/* 292-295 — wades chest deep, neck deep, grabs the lion, swims */
const s292 = S(
	'292',
	'rivflood',
	[1100, 720, 1.3],
	[1000, 740, 1.7],
	(c) => {
		const x = lerpF(c.f, c.at('292') + 6, c.at('293') + 6, 1500, 1000);
		const grab = rel(c, '293', 20) > 0;
		const sink = lerpF(c.f, c.at('292') + 30, c.at('292') + 90, 0, 90);
		return (
			<>
				{man(c, {who: 'max', x, s: 1.15, face: -1, floor: 900 + sink, expr: 'angry'})}
				<g opacity={grab ? 1 : 0}>
					<Cat kind="lion" x={x - 80} y={690 + wob(c.f, 14, 6)} s={0.9} f={c.gf} mode="lie" thin={1} wet={1} shadow={false} face={-1} rot={-8} />
				</g>
			</>
		);
	},
	{
		fg: (c) => <Water f={c.gf} y0={820} y1={1500} flood o={0.82} />,
		over: (c) => (
			<>
				<Slam t={rel(c, '292', 40)} dur={26} text="CHEST DEEP" y={70} size={100} c="#8ae0ff" />
				<Slam t={rel(c, '292', 70)} dur={34} text="NECK DEEP" y={70} size={100} c="#ff9a3a" />
				<Slam t={rel(c, '293', 24)} dur={70} text="BY THE SCRUFF" y={70} size={100} c="#ffd23a" />
				<Slam t={rel(c, '294', 24)} dur={70} text="LIKE A MOTHER LION" y={780} size={80} c="#fff" />
			</>
		),
		shake: () => 6,
	},
);
const s295 = S(
	'295',
	'rivflood',
	[1100, 760, 1.2],
	[700, 760, 1.4],
	(c) => {
		const x = lerpF(c.f, 0, c.dur, 1500, 600);
		return (
			<>
				<Cat kind="lion" x={x} y={730 + wob(c.f, 8, 5)} s={0.9} f={c.gf} mode="lie" thin={1} wet={1} shadow={false} face={-1} rot={-6} />
				{man(c, {who: 'max', x: x - 20, s: 1.1, face: -1, floor: 960, expr: 'angry', pose: (p) => ({...p, armF: [80, 20], armB: [80, 30], lean: 20})})}
			</>
		);
	},
	{
		fg: (c) => <Water f={c.gf} y0={800} y1={1500} flood o={0.82} />,
		over: (c) => (
			<>
				<CountUp t={rel(c, '295', 2)} dur={140} to={200} suffix=" KG" label="WET FURIOUS CAT" side="r" y={120} size={140} c="#ffd23a" roll={20} fmt={false} />
				<Slam t={rel(c, '295', 115)} dur={30} text="AND HE SWIMS" y={780} size={100} c="#8ae0ff" />
			</>
		),
		shake: () => 6,
	},
);

/* 296-297 — on the bank 41 men watch a teenager drag a lion out of a flood */
const s296 = S(
	'296',
	'rivdawn',
	[960, 640, 1.0],
	[1100, 640, 1.25],
	(c) => {
		const x = lerpF(c.f, 0, c.at('296') + 100, 200, 760);
		return (
			<>
				<CrowdRow n={14} x0={1100} x1={1800} floor={900} s={0.8} mode="stand" seed="watchm" />
				<Cat kind="lion" x={x + 40} y={900} s={1.1} f={c.gf} mode="lie" thin={1} wet={1} face={1} />
				{man(c, {who: 'max', x: x - 60, s: 1.1, face: 1, pose: (p) => ({...p, lean: 26, armF: [-50, 20], armB: [-50, 20]})})}
				<Onoma x={x + 200} y={680} text="COUGH!" t={rel(c, '297', 12)} c="#fff" size={80} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '296', 60)} dur={90} text="A TEENAGER DRAGS A LION" y={70} size={80} c="#fff" />},
);

/* 298-299 — the lion walks to the fire, lies down, falls asleep */
const s298 = S(
	'298',
	'rivdawn',
	[1000, 640, 1.2],
	[1100, 620, 1.5],
	(c) => {
		const x = lerpF(c.f, c.at('298') + 6, c.at('298') + 70, 520, 1020);
		const lie = rel(c, '298', 56) > 0;
		return (
			<>
				<Fire x={1200} y={910} s={0.9} f={c.gf} />
				<CrowdRow n={6} x0={1380} x1={1800} floor={900} s={0.8} mode="stand" seed="stillm" />
				{man(c, {who: 'max', x: 360, s: 1.1, face: 1, mouth: 'smile'})}
				<Cat kind="lion" x={x} y={910} s={1.1} f={c.gf} mode={lie ? 'lie' : 'walk'} ph={c.gf * 0.12} thin={1} wet={Math.max(0, 1 - rel(c, '297', 0) / 90)} />
				{rel(c, '299', 110) > 0
					? [0, 1, 2].map((i) => (
							<text key={i} x={1060 + i * 60} y={690 - i * 50 - ((c.f + i * 20) % 40)} fontSize={50 + i * 10} fontFamily="Rubik" fontWeight={900} fill="#fff" stroke="#14060c" strokeWidth={6} paintOrder="stroke">
								Z
							</text>
					  ))
					: null}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '299', 0)} dur={100} text="NOBODY MOVES. NOBODY BREATHES." y={70} size={72} c="#fff" />},
);

/* 300-301 — Day 30, the helicopters come */
const s300 = S(
	'300',
	'jdawn',
	[960, 560, 1.0],
	[960, 520, 1.15],
	(c) => (
		<>
			{[0, 1, 2].map((i) => (
				<Heli key={i} x={lerpF(c.f, c.at('301') - 10 + i * 8, c.dur, 2300, 500 + i * 460)} y={220 + i * 70} s={0.7 + i * 0.1} f={c.gf + i * 4} face={-1} tilt={-4} />
			))}
			<CrowdRow n={6} x0={400} x1={1500} floor={900} s={0.8} mode="stand" seed="d30" />
		</>
	),
	{over: (c) => <Slam t={rel(c, '300', 6)} dur={60} text="DAY 30" y={70} size={150} c="#ffd23a" />},
);

/* 302-305 — who survived? the lion survived */
const s302 = S(
	'302',
	'jdawn',
	[960, 640, 1.0],
	[960, 600, 1.4],
	(c) => <Cat kind="lion" x={960} y={910} s={1.3} f={c.gf} mode="sit" thin={0.7} />,
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '302', 8)} dur={90} text="WHO SURVIVED?" y={70} size={120} c="#fff" />
				<Slam t={rel(c, '303', 4)} dur={60} text="THE LION SURVIVED" y={70} size={100} c="#ffb04a" />
				<CountUp t={rel(c, '304', 2)} dur={60} to={30} suffix=" KG LIGHTER" label="BUT ALIVE" side="c" y={780} size={100} c="#7cf0a0" roll={12} fmt={false} />
				<Slam t={rel(c, '305', 40)} dur={50} text="IT WASN'T HIS HOME" y={70} size={90} c="#fff" />
			</>
		),
	},
);

/* 306-308 — 41 of 100 men survived: fire, a quiet farm boy, each other */
const s306 = S(
	'306',
	'jdawn',
	[960, 620, 1.0],
	[960, 580, 1.2],
	(c) => (
		<>
			<Fire x={960} y={910} s={0.8} f={c.gf} />
			<CrowdRow n={9} x0={180} x1={800} floor={900} s={0.8} mode="stand" seed="surv" />
			<CrowdRow n={7} x0={1140} x1={1760} floor={900} s={0.8} mode="stand" seed="surv2" />
			{man(c, {who: 'sam', x: 1000, s: 1.1, face: 1})}
		</>
	),
	{
		over: (c) => (
			<>
				<CountUp t={rel(c, '306', 0)} dur={80} to={41} suffix=" / 100" label="MEN SURVIVED" side="c" y={70} size={140} c="#ffd23a" roll={14} fmt={false} />
				<Slam t={rel(c, '307', 70)} dur={30} text="FIRE" y={780} size={100} c="#ff9a3a" />
				<Slam t={rel(c, '308', 10)} dur={50} text="A QUIET FARM BOY" y={780} size={90} c="#7cf0a0" />
				<Slam t={rel(c, '308', 72)} dur={40} text="EACH OTHER" y={780} size={90} c="#8ae0ff" />
			</>
		),
	},
);

/* 309-313 — Max survived; what he learned (checklist) */
const s309 = S(
	'309',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.15],
	(c) => {
		const rows: [string, string, number, boolean][] = [
			['BUILD A HOUSE', '311', 26, true],
			['CRACK NUTS', '311', 55, true],
			['GERMS', '312', 27, false],
			['INSECTS', '312', 61, false],
			['LONELINESS', '313', 22, false],
		];
		return (
			<>
				{man(c, {who: 'max', x: 300, s: 1.1, floor: 960, mouth: 'smile', g: [['fist', '309', 20, 70]]})}
				{rows.map((r, i) => {
					const k = pop(c.f, c.at(r[1]) + r[2]);
					return (
						<g key={i} transform={`translate(640,${300 + i * 120}) scale(${k})`} opacity={Math.min(1, k * 2)}>
							<rect x={0} y={-44} width={760} height={90} rx={30} fill="#14060c" opacity={0.85} stroke={r[3] ? '#7cf0a0' : '#ff3a52'} strokeWidth={5} />
							<text x={36} y={16} fontSize={48} fontFamily="Rubik" fontWeight={900} fill="#fff">
								{r[0]}
							</text>
							<text x={700} y={20} textAnchor="end" fontSize={64} fontFamily="Rubik" fontWeight={900} fill={r[3] ? '#7cf0a0' : '#ff3a52'}>
								{r[3] ? '✓' : '✗'}
							</text>
						</g>
					);
				})}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '309', 8)} dur={110} text="AND MAX SURVIVED" y={70} size={100} c="#ff5a6e" />},
);

/* 314-315 — the two times he mattered: not strength, he chose to help */
const s314 = S(
	'314',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => (
		<>
			{man(c, {who: 'max', x: 700, s: 1.2, floor: 960, g: [['presentF', '315', 30, 120]], mouth: 'smile'})}
			<g opacity={pop(c.f, c.at('314') + 38)}>
				<rect x={1060} y={640} width={620} height={46} rx={22} fill="#5a3a1c" />
				<text x={1370} y={600} textAnchor="middle" fontSize={44} fontFamily="Rubik" fontWeight={900} fill="#fff">
					THE BRIDGE
				</text>
			</g>
			<g opacity={pop(c.f, c.at('314') + 80)}>
				<Cat kind="lion" x={1340} y={900} s={0.7} f={c.gf} mode="lie" wet={1} thin={1} />
				<text x={1370} y={440} textAnchor="middle" fontSize={44} fontFamily="Rubik" fontWeight={900} fill="#fff">
					THE LION
				</text>
			</g>
		</>
	),
	{over: (c) => (
		<>
			<Slam t={rel(c, '314', 60)} dur={80} text="NOT BECAUSE HE WAS STRONG" strike y={70} size={72} c="#ffd23a" />
			<Slam t={rel(c, '315', 20)} dur={90} text="HE CHOSE TO HELP" y={70} size={110} c="#7cf0a0" />
		</>
	)},
);

/* 316-319 — who wins: not the strongest, not the biggest; those who work with others */
const s316 = S(
	'316',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.25],
	(c) => {
		const link = lerpF(c.f, c.at('319') + 30, c.at('319') + 70, 0, 1);
		return (
			<>
				<g opacity={1 - (rel(c, '319', 0) > 0 ? 0.6 : 0)}>
					<Cat kind="lion" x={420} y={900} s={0.85} f={c.gf} mode="stand" />
					{man(c, {who: 'max', x: 1500, s: 1.15, floor: 960})}
				</g>
				<CrowdRow n={9} x0={760} x1={1260} floor={920} s={0.65} mode="stand" seed="team" />
				<line x1={760} y1={700} x2={760 + 500 * link} y2={700} stroke="#ffd23a" strokeWidth={10} strokeLinecap="round" />
				{rel(c, '317', 10) > 0 ? <text x={420} y={430} textAnchor="middle" fontSize={50} fontFamily="Rubik" fontWeight={900} fill="#ff3a52">✗ STRONGEST</text> : null}
				{rel(c, '317', 48) > 0 ? <text x={1500} y={430} textAnchor="middle" fontSize={50} fontFamily="Rubik" fontWeight={900} fill="#ff3a52">✗ BIGGEST</text> : null}
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '316', 20)} dur={60} text="WHO ACTUALLY WINS?" y={70} size={100} c="#fff" />
			<Slam t={rel(c, '318', 20)} dur={100} text="THE JUNGLE DOESN'T CARE" y={70} size={90} c="#ff9a3a" />
			<Slam t={rel(c, '319', 28)} dur={90} text="WORK WITH OTHERS" y={780} size={110} c="#7cf0a0" />
		</>
	)},
);

/* 320-322 — the last helicopter lands, the pilot takes off his helmet: Theo */
const s320 = S(
	'320',
	'jdawn',
	[960, 560, 1.0],
	[960, 620, 1.3],
	(c) => {
		const hy2 = lerpF(c.f, c.at('320') + 10, c.at('320') + 40, 200, 700);
		const out = lerpF(c.f, c.at('321') + 10, c.at('321') + 30, 0, 1);
		const helm = rel(c, '322', 0) > 0 ? 0 : 1;
		return (
			<>
				<Heli x={960} y={hy2} s={1.1} f={c.gf} tilt={-2} />
				{out > 0 ? man(c, {who: 'theo', x: 1360 - (1 - out) * 100, s: 1.1, face: -1, hair: helm ? 'cap' : 'short', hairColor: '#222', acc: helm ? [] : ['glasses'], faceTurn: 0.5}) : null}
			</>
		);
	},
	{over: (c) => (
		<>
			<Slam t={rel(c, '320', 20)} dur={60} text="THE LAST HELICOPTER" y={70} size={90} c="#fff" />
			<Slam t={rel(c, '322', 0)} dur={70} text="IT'S THEO!" y={70} size={150} c="#ffd23a" />
		</>
	)},
);

/* 323-327 — reunion: named a rock after me? mom's furious, our sister did something */
const s323 = S(
	'323',
	'jdawn',
	[1000, 620, 1.3],
	[1000, 580, 1.6],
	(c) => (
		<>
			<Rock x={1280} y={915} s={1.0} face f={c.gf} glasses />
			{man(c, {who: 'theo', x: 1040, s: 1.15, face: -1, g: [['point', '323', 20, 70]], expr: 'wide'})}
			{man(c, {who: 'max', x: 660, s: 1.15, face: 1, mouth: 'smile', g: [['scratch', '324', 0, 50]]})}
			<Say t={rel(c, '323', 0)} x={1040} y={330} text="YOU NAMED A ROCK AFTER ME?" size={44} tail={[0, 100]} />
			<Say t={rel(c, '324', 0)} x={660} y={330} text="IT WAS A GOOD ROCK." size={44} tail={[0, 100]} />
		</>
	),
);
const s325 = S(
	'325',
	'jdawn',
	[1000, 620, 1.4],
	[1000, 580, 1.8],
	(c) => (
		<>
			{man(c, {who: 'theo', x: 1040, s: 1.15, face: -1, g: [['point', '325', 20, 60], ['presentF', '327', 0, 40]], expr: 'worried'})}
			{man(c, {who: 'max', x: 660, s: 1.15, face: 1, expr: rel(c, '326', 30) > 0 ? 'wide' : 'normal'})}
			<Say t={rel(c, '325', 0)} x={1040} y={330} text="GET IN. MOM'S FURIOUS." size={44} tail={[0, 100]} />
			<Say t={rel(c, '326', 20)} x={1040} y={230} text="OUR SISTER DID SOMETHING…" size={44} tail={[0, 100]} />
			<Say t={rel(c, '327', 0)} x={1040} y={330} text="YOU NEED TO SEE IT." size={44} tail={[0, 100]} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '326', 36)} dur={70} text="TO BE CONTINUED?" y={780} size={80} c="#ffd23a" />},
);

/* 328-329 — who would you bet on? lion, the 100 men, or Max */
const s328 = S(
	'328',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => (
		<>
			<g opacity={1}>
				{sc(pop(c.f, c.at('328') + 6), 420, 760, <Cat kind="lion" x={420} y={900} s={0.9} f={c.gf} mode="stand" />)}
				{sc(pop(c.f, c.at('329') + 26), 960, 760, <CrowdRow n={7} x0={780} x1={1140} floor={900} s={0.7} mode="stand" seed="bet" />)}
				{sc(pop(c.f, c.at('329') + 62), 1500, 760, man(c, {who: 'max', x: 1500, s: 1.15, floor: 940, g: [['wave', '329', 70, 130]]}))}
				<Tag x={420} y={330} text="LION" k={pop(c.f, c.at('328') + 6)} />
				<Tag x={960} y={330} text="100 MEN" k={pop(c.f, c.at('329') + 28)} c="#8ae0ff" />
				<Tag x={1500} y={330} text="MAX" k={pop(c.f, c.at('329') + 64)} c="#ff5a6e" />
			</g>
		</>
	),
	{over: (c) => <Slam t={rel(c, '328', 6)} dur={80} text="WHO WOULD YOU BET ON?" y={70} size={96} c="#fff" />},
);

/* 330-332 — tell us in the comments, like and subscribe */
const s330 = S(
	'330',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.2],
	(c) => (
		<>
			{man(c, {who: 'max', x: 960, s: 1.4, floor: 980, g: [['wave', '330', 4, 80], ['point', '332', 8, 80]], mouth: 'smile'})}
			<g opacity={pop(c.f, c.at('330') + 20)}>
				<g transform="translate(460,420)">
					<rect x={-150} y={-70} width={300} height={140} rx={34} fill="#fff" />
					<path d="M-60,70 l-20,50 l70,-50 Z" fill="#fff" />
					<text x={0} y={18} textAnchor="middle" fontSize={64} fontFamily="Rubik" fontWeight={900} fill="#14060c">COMMENT</text>
				</g>
			</g>
			<g opacity={pop(c.f, c.at('332') + 4)}>
				<g transform="translate(1480,400)">
					<rect x={-170} y={-60} width={340} height={120} rx={30} fill="#ff2340" />
					<text x={0} y={18} textAnchor="middle" fontSize={56} fontFamily="Rubik" fontWeight={900} fill="#fff">LIKE 👍</text>
				</g>
			</g>
			<g opacity={pop(c.f, c.at('332') + 24)}>
				<g transform="translate(1480,580)">
					<rect x={-210} y={-60} width={420} height={120} rx={30} fill="#fff" />
					<text x={0} y={18} textAnchor="middle" fontSize={56} fontFamily="Rubik" fontWeight={900} fill="#ff2340">SUBSCRIBE</text>
				</g>
			</g>
		</>
	),
	{over: (c) => <Slam t={rel(c, '331', 10)} dur={120} text="WOULD YOU JUMP IN TOO?" y={70} size={90} c="#ffd23a" />},
);

export const SHOTS_D: ShotDef[] = [
	s201, s206, s211, s214, s217, s221, s224, s227, s230, s231, s232, s235, s238, s239, s243, s246, s248, s250, s252, s255, s258, s262, s264, s266, s268, s273, s276, s278, s280, s283, s286, s289, s292, s295, s296, s298, s300, s302, s306, s309, s314, s316, s320, s323, s325, s328, s330,
];
