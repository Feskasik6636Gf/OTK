import React from 'react';
import {interpolate} from 'remotion';
import {CrowdRow} from '../kit/kit';
import {Callout} from '../kit/graphics';
import {env} from '../kit/actions';
import {Onoma} from '../reference/PauseTime';
import type {ShotDef} from '../kit/coverage';
import {Band, Cat, Heli, LogHut, Monkey, Rock, Spark, Tree} from './critters';
import {FL, S, man, pop, rel, sc, lerpF, clampO} from './dsl';
import {Fire} from './places';
import {CountUp, Say, Slam, Stat} from './overlays';
import {Blueprint, Bus, Calc, Clipboard, Confetti, Crown, Leaf, Megaphone, Phone, PizzaBox, Pillow, Pitchfork, Ring, Sign, SpeedLines, SteelDoor, Tag, Tooth, Wrench, XMark, Zebra} from './props2';

const cl = clampO;
const wob = (f: number, a: number, p = 6) => Math.sin(f / p) * a;

/* 001 — one lion, 100 men, one guy */
const s001 = S(
	'001',
	'studio',
	[960, 540, 1],
	[1100, 560, 1.18],
	(c) => {
		const k1 = pop(c.f, c.at('001') + 6);
		const k2 = pop(c.f, c.at('001') + 36);
		const k3 = pop(c.f, c.at('001') + 94);
		return (
			<>
				{sc(k1, 430, 760, <Cat kind="lion" x={430} y={800} s={0.95} f={c.gf} mode="stand" roar={env(c.f, c.at('001') + 20, c.at('001') + 40, 4, 8) * 0.7} ph={c.gf / 6} />)}
				{sc(k2, 960, 780, <CrowdRow n={14} x0={720} x1={1230} floor={840} s={0.5} mode="stand" seed="op" />)}
				{sc(k3, 1520, 700, man(c, {who: 'max', x: 1520, floor: 900, s: 1.2, g: [['fist', '001', 120, 175]]}))}
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '001', 6)} dur={34} text="1 LION" y={110} size={110} />
				<Slam t={rel(c, '001', 36)} dur={54} text="100 MEN" y={110} size={110} c="#8ae0ff" />
				<Slam t={rel(c, '001', 96)} dur={30} text="1 GUY" y={110} size={110} c="#ff5a6e" />
				<Stat t={rel(c, '001', 146)} dur={70} big="1,000" label="STRENGTH" side="r" y={180} size={130} />
			</>
		),
	},
);

/* 002 — dropped into the Amazon */
const s002 = S(
	'002',
	'canopy',
	[800, 480, 1.0],
	[1200, 520, 1.25],
	(c) => {
		const hx = lerpF(c.f, 0, c.dur, -350, 2350);
		const my = lerpF(c.f, c.at('002') + 20, c.dur, 110, 640);
		return (
			<>
				<Heli x={hx} y={250 + wob(c.f, 14, 14)} s={1.25} f={c.gf} tilt={7} />
				<g opacity={c.f > c.at('002') + 22 ? 1 : 0}>
					<path d={`M${960 - 150},${my - 330} C${960 - 150},${my - 470} ${960 + 150},${my - 470} ${960 + 150},${my - 330} Z`} fill="#ff2340" />
					<path d={`M${960 - 150},${my - 330} L${960 - 10},${my - 150} M${960 + 150},${my - 330} L${960 + 10},${my - 150}`} stroke="#fff" strokeWidth={4} />
					{man(c, {who: 'max', x: 960, floor: my + 40, s: 0.62, pose: (p) => ({...p, armF: [170, 6], armB: [-170, 6], legF: [8, 14], legB: [-6, 14]})})}
				</g>
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '002', 38)} dur={50} text="AMAZON" sub="RAINFOREST" y={780} size={130} c="#7cf0a0" />
				<Stat t={rel(c, '002', 88)} dur={80} big="30 DAYS" side="c" y={70} size={150} />
			</>
		),
	},
);

/* 003 — no food, no phones, no weapons */
const s003 = S(
	'003',
	'studio',
	[960, 540, 1.0],
	[960, 520, 1.12],
	(c) => {
		const items = [
			{x: 440, t: 0, el: <Burger2 />},
			{x: 960, t: 29, el: <Phone x={0} y={0} s={1.5} />},
			{x: 1480, t: 62, el: <Spear x={0} y={0} s={1.3} />},
		];
		return (
			<>
				{items.map((it, i) => {
					const t = c.at('003') + it.t;
					const k = pop(c.f, t);
					const xk = Math.max(0, Math.min(1, (c.f - t - 12) / 14));
					return (
						<g key={i} transform={`translate(${it.x},${520 + wob(c.f + i * 7, 8, 9)}) scale(${k})`} opacity={1 - xk * 0.35}>
							{it.el}
							<XMark x={0} y={0} k={xk} s={1.2} />
						</g>
					);
				})}
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '003', 0)} dur={26} text="NO FOOD" y={780} size={100} c="#ffb04a" />
				<Slam t={rel(c, '003', 29)} dur={32} text="NO PHONES" y={780} size={100} c="#6ac0ff" />
				<Slam t={rel(c, '003', 62)} dur={60} text="NO WEAPONS" y={780} size={100} c="#ff5a6e" />
			</>
		),
		shake: (c) => (rel(c, '003', 74) > 0 && rel(c, '003', 74) < 8 ? 10 : 0),
	},
);
const Burger2: React.FC = () => (
	<g transform="scale(3)">
		<path d="M-40,-24 C-40,-62 40,-62 40,-24 Z" fill="#e0a050" />
		<path d="M-44,-24 q8,10 16,0 q8,10 16,0 q8,10 16,0 q8,10 16,0 q8,10 16,0 L44,-18 L-44,-18 Z" fill="#5aba40" />
		<rect x={-42} y={-20} width={84} height={12} rx={6} fill="#6a3a1c" />
		<path d="M-40,-8 h80 l-6,10 h-68 Z" fill="#f2c438" />
		<path d="M-40,2 C-40,12 40,12 40,2 Z" fill="#e0a050" />
		<g transform="translate(0,28)" />
	</g>
);
const Spear: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x},${y}) rotate(35) scale(${s})`}>
		<rect x={-7} y={-150} width={14} height={300} rx={7} fill="#8a5e34" />
		<path d="M0,-230 L26,-140 L-26,-140 Z" fill="#cfd5dc" stroke="#7a828c" strokeWidth={4} />
	</g>
);

/* 004 — wristband with one red button */
const s004 = S(
	'004',
	'studio',
	[960, 520, 1.0],
	[960, 500, 1.55],
	(c) => {
		const k = pop(c.f, c.at('004') + 2, 14);
		return (
			<>
				{sc(k, 960, 520, <g transform="rotate(-8 960 520)"><Band x={960} y={520} s={1.55} f={c.gf} /></g>)}
				<Callout f={c.f} t0={c.at('004') + 48} t1={c.dur - 4} from={[960, 500]} to={[1380, 280]} text="ONE RED BUTTON" size={48} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '004', 0)} dur={50} text="EVERY PLAYER" y={80} size={90} c="#fff" />},
);

/* 005-006 — press it, heli takes you home, but you're out */
const s005 = S(
	'005',
	'jd',
	[900, 560, 1.1],
	[1060, 470, 1.0],
	(c) => {
		const hx = lerpF(c.f, c.at('005') + 20, c.at('005') + 62, 2400, 1280);
		const press = env(c.f, c.at('005') + 0, c.at('005') + 10, 3, 5);
		const walkAway = lerpF(c.f, c.at('006') + 6, c.dur, 0, 1);
		return (
			<>
				<Heli x={hx} y={220 + wob(c.f, 10, 9)} s={1.1} f={c.gf} tilt={-4} face={-1} />
				{man(c, {who: 'max', x: 760 - walkAway * 300, s: 1.05, face: walkAway > 0.02 ? -1 : 1, g: [['point', '005', 0, 18], ['wave', '005', 44, 84], ['armsCrossed', '006', 6, 40]], expr: c.f > c.at('006') + 6 ? 'sad' : 'normal'})}
				<Spark x={820} y={640} t={rel(c, '005', 4)} c="#ff6a78" />
				<Ring x={1280} y={420} t={rel(c, '005', 40)} c="#fff" r={260} n={2} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '006', 12)} dur={30} text="OUT!" y={300} size={190} c="#ff3a52" rot={-6} />, shake: (c) => (rel(c, '006', 14) > 0 && rel(c, '006', 14) < 7 ? 12 : 0)},
);

/* 007-008 — internet argues, who survives */
const s007 = S(
	'007',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.22],
	(c) => {
		const t1 = c.at('007') + 16;
		const t2 = c.at('007') + 40;
		const t3 = c.at('007') + 56;
		return (
			<>
				{sc(pop(c.f, t1), 420, 800, <Cat kind="lion" x={420} y={870} s={0.7} f={c.gf} mode="stand" ph={c.gf / 7} roar={env(c.f, t1 + 6, t1 + 30, 4, 8) * 0.6} />)}
				<Say t={c.f - t1} x={430} y={440} text="LION!" size={56} tail={[10, 120]} />
				{sc(pop(c.f, t2), 960, 800, <CrowdRow n={5} x0={800} x1={1120} floor={880} s={0.62} mode="panic" seed="arg" />)}
				<Say t={c.f - t2} x={960} y={440} text="100 MEN!" size={56} tail={[0, 120]} />
				{sc(pop(c.f, t3), 1500, 800, man(c, {who: 'max', x: 1500, floor: 880, s: 0.85, g: [['point', '007', 56, 110], ['fist', '008', 0, 40]]}))}
				<Say t={c.f - t3} x={1500} y={440} text="MAX!" size={56} tail={[-10, 120]} />
			</>
		);
	},
	{
		over: (c) => <Slam t={rel(c, '008', 0)} dur={90} text="WHO SURVIVES?" y={760} size={140} c="#ffd23a" />,
		shake: (c) => (rel(c, '008', 0) > 0 && rel(c, '008', 0) < 8 ? 9 : 0),
	},
);

/* 009 — same river, same flood */
const s009 = S(
	'009',
	'rivdusk',
	[960, 600, 1.0],
	[1100, 560, 1.12],
	(c) => (
		<>
			{sc(pop(c.f, c.at('009') + 45), 380, 760, man(c, {who: 'max', x: 380, s: 1.0, face: 1, g: [['stop', '009', 60, 100]]}))}
			{sc(pop(c.f, c.at('009') + 52), 960, 780, <Cat kind="lion" x={960} y={900} s={0.95} f={c.gf} mode="stand" ph={c.gf / 8} />)}
			{sc(pop(c.f, c.at('009') + 62), 1500, 780, <CrowdRow n={6} x0={1380} x1={1680} floor={900} s={0.85} mode="stand" seed="rv9" />)}
		</>
	),
	{over: (c) => <Slam t={rel(c, '009', 6)} dur={44} text="DAY 29" y={90} size={150} c="#ff5a6e" />},
);
/* 010-011 — flood, surprise */
const s010 = S(
	'010',
	'rivflood',
	[960, 640, 1.0],
	[960, 600, 1.25],
	(c) => (
		<>
			{man(c, {who: 'max', x: 300, s: 1.0, g: [['stop', '010', 20, 60]], expr: 'wide'})}
			<g transform={`rotate(${wob(c.f, 3, 20)} 960 700)`}>
				<rect x={640} y={690} width={600} height={34} rx={17} fill="#4a2e18" />
				<Cat kind="lion" x={960} y={706} s={0.8} f={c.gf} mode="stand" shadow={false} wet={1} />
			</g>
			<CrowdRow n={5} x0={1560} x1={1800} floor={900} s={0.7} mode="panic" seed="fl" />
		</>
	),
	{
		over: (c) => <Slam t={rel(c, '011', 40)} dur={80} text="SURPRISE?!" y={90} size={150} c="#ffd23a" />,
		flash: (c) => (rel(c, '010', 26) > 0 ? Math.max(0, 0.8 - rel(c, '010', 26) / 8) : 0),
		shake: (c) => (rel(c, '010', 26) > 0 && rel(c, '010', 26) < 14 ? 14 : 3),
	},
);

/* 012 — meet the players */
const s012 = S(
	'012',
	'sav',
	[960, 640, 1.0],
	[1040, 600, 1.1],
	(c) => {
		const lx = lerpF(c.f, 0, c.at('013') + 30, -300, 760);
		return <Cat kind="lion" x={lx} y={900} s={0.95} f={c.gf} mode="walk" ph={c.gf * 0.2} />;
	},
	{over: (c) => <Slam t={rel(c, '012', 26)} dur={50} text="MEET THE PLAYERS" y={80} size={110} c="#fff" />},
);

/* 013-014 — Player 1 the lion, 200 kilos of muscle teeth and attitude */
const s013 = S(
	'013',
	'sav',
	[900, 640, 1.15],
	[900, 600, 1.45],
	(c) => (
		<>
			<Cat kind="lion" x={900} y={910} s={1.5} f={c.gf} mode="stand" ph={c.gf / 9} roar={env(c.f, c.at('014') + 60, c.at('014') + 100, 6, 10) * 0.8} />
			<Callout f={c.f} t0={c.at('014') + 10} t1={c.at('014') + 36} from={[960, 740]} to={[1380, 800]} text="MUSCLE" size={44} />
			<Callout f={c.f} t0={c.at('014') + 38} t1={c.at('014') + 78} from={[1100, 640]} to={[1500, 520]} text="TEETH" size={44} />
			<Callout f={c.f} t0={c.at('014') + 82} t1={c.dur - 4} from={[1060, 560]} to={[1440, 360]} text="ATTITUDE" size={44} />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '013', 0)} dur={70} text="PLAYER 1" sub="THE LION" y={70} size={120} c="#ffb04a" />
				<CountUp t={rel(c, '014', 0)} dur={70} to={200} suffix=" KG" side="l" y={300} size={130} c="#ffd23a" />
			</>
		),
	},
);

/* 015 — 60 km/h */
const s015 = S(
	'015',
	'sav',
	[700, 640, 1.2],
	[1500, 640, 1.2],
	(c) => {
		const lx = lerpF(c.f, c.at('015') + 6, c.dur - 4, -250, 2250);
		return (
			<>
				<SpeedLines f={c.gf} y0={420} y1={880} dir={1} c="#fff4c8" />
				<Cat kind="lion" x={lx} y={900 + wob(c.f, 4, 2)} s={1.1} f={c.gf} mode="walk" ph={c.gf * 0.9} />
			</>
		);
	},
	{over: (c) => <CountUp t={rel(c, '015', 10)} dur={90} to={60} suffix=" KM/H" side="c" y={110} size={150} c="#ffd23a" roll={20} />},
);

/* 016 — roar heard 8 km away */
const s016 = S(
	'016',
	'sav',
	[900, 620, 1.2],
	[960, 580, 1.6],
	(c) => {
		const r = env(c.f, c.at('016') + 4, c.dur - 10, 5, 10);
		return (
			<>
				<Ring x={1040} y={640} t={rel(c, '016', 8)} c="#fff3c0" r={900} n={4} />
				<Cat kind="lion" x={820} y={910} s={1.4} f={c.gf} mode="stand" ph={0} roar={r} />
				{[0, 1, 2, 3].map((i) => (
					<g key={i} transform={`translate(${1500 + ((c.f * (6 + i) + i * 300) % 800)},${220 + i * 60 - ((c.f * (2 + i)) % 90)})`} opacity={rel(c, '016', 20) > 0 ? 1 : 0}>
						<path d="M0,0 q14,-14 28,0 q14,-14 28,0" stroke="#3a2a1a" strokeWidth={5} fill="none" strokeLinecap="round" />
					</g>
				))}
			</>
		);
	},
	{
		over: (c) => <CountUp t={rel(c, '016', 32)} dur={80} to={8} suffix=" KM" label="HEARD AWAY" side="r" y={110} size={150} c="#ffd23a" roll={18} />,
		shake: (c) => 6 * env(c.f, c.at('016') + 4, c.dur - 20, 5, 10),
	},
);

/* 017 — king of the savannah */
const s017 = S(
	'017',
	'sav',
	[960, 600, 1.1],
	[1060, 520, 1.35],
	(c) => {
		const t = c.at('017') + 42;
		const cy = lerpF(c.f, t, t + 12, -300, 548) + (c.f > t + 12 ? wob(c.f - t, 6, 3) * Math.exp(-(c.f - t - 12) / 12) : 0);
		return (
			<>
				<Rock x={860} y={915} s={2.4} />
				<Cat kind="lion" x={860} y={720} s={1.2} f={c.gf} mode="sit" shadow={false} />
				<Crown x={1020} y={cy} s={1.0} rot={wob(c.f, 5, 8)} />
				<Spark x={1020} y={500} t={rel(c, '017', 58)} c="#ffe08a" />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '017', 44)} dur={50} text="THE KING" y={80} size={130} c="#ffd23a" />},
);

/* 018 — Player 2: 100 ordinary men */
const s018 = S(
	'018',
	'jd',
	[960, 640, 1.0],
	[960, 600, 1.35],
	(c) => (
		<>
			<CrowdRow n={26} x0={150} x1={1770} floor={840} s={0.55} mode="stand" seed="m18b" />
			<CrowdRow n={22} x0={200} x1={1720} floor={900} s={0.7} mode="stand" seed="m18a" />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '018', 0)} dur={40} text="PLAYER 2" y={70} size={120} c="#8ae0ff" />
				<CountUp t={rel(c, '018', 26)} dur={110} from={0} to={100} label="ORDINARY MEN" side="c" y={220} size={170} c="#8ae0ff" roll={26} fmt={false} />
			</>
		),
	},
);

/* 019 — plumber, dentist, pizza guy */
const s019 = S(
	'019',
	'jd',
	[960, 580, 1.25],
	[960, 560, 1.4],
	(c) => {
		const t = (n: number) => c.at('019') + n;
		const jump = (n: number) => Math.max(0, Math.sin(Math.min(1, Math.max(0, (c.f - t(n)) / 18)) * Math.PI)) * 40;
		return (
			<>
				{man(c, {who: 'sam', x: 560, s: 1.1, color: '#e8802a', hair: 'cap', hairColor: '#e8802a', face: 1, floor: 900 - jump(4), handItem: <Wrench />, g: [['point', '019', 4, 24]]})}
				{man(c, {who: 'danny', x: 960, s: 1.1, color: '#f4f4f4', outfit: 'coat', acc: [], hair: 'bob', face: 1, floor: 900 - jump(29), handItem: <Tooth />, g: [['presentF', '019', 29, 52]]})}
				{man(c, {who: 'sam', x: 1360, s: 1.1, color: '#d9372a', hair: 'cap', hairColor: '#d9372a', face: -1, floor: 900 - jump(56), handItem: <PizzaBox />, g: [['presentF', '019', 56, 90]]})}
				<Tag x={560} y={420} text="PLUMBER" k={pop(c.f, t(4))} />
				<Tag x={960} y={420} text="DENTIST" k={pop(c.f, t(29))} c="#8ae0ff" />
				<Tag x={1360} y={420} text="PIZZA GUY" k={pop(c.f, t(56))} c="#ff8a98" />
			</>
		);
	},
);

/* 020 — accountants, math teacher, 94 others */
const s020 = S(
	'020',
	'jd2',
	[960, 600, 1.1],
	[960, 560, 1.0],
	(c) => {
		const t = (n: number) => c.at('020') + n;
		const hop = (n: number) => Math.max(0, Math.sin(Math.min(1, Math.max(0, (c.f - t(n)) / 16)) * Math.PI)) * 34;
		const cx = lerpF(c.f, t(66), c.dur, 2300, 1300);
		return (
			<>
				{man(c, {who: 'sam', x: 420, s: 1.05, color: '#6a6e84', hair: 'bun', hairColor: '#333', acc: ['glasses'], floor: 900 - hop(5), handItem: <Calc />, g: [['presentF', '020', 5, 26]]})}
				{man(c, {who: 'sam', x: 640, s: 1.05, color: '#6a6e84', hair: 'short', acc: ['glasses'], face: 1, floor: 900 - hop(14), handItem: <Calc />, g: [['presentF', '020', 14, 30]]})}
				{man(c, {who: 'danny', x: 900, s: 1.1, color: '#8e3a4f', outfit: 'suit', acc: ['glasses'], hair: 'grey', face: 1, floor: 900 - hop(36), handItem: <Clipboard />, g: [['point', '020', 36, 60]]})}
				<Tag x={530} y={440} text="2 ACCOUNTANTS" k={pop(c.f, t(5))} size={30} c="#8ae0ff" />
				<Tag x={900} y={420} text="MATH TEACHER" k={pop(c.f, t(38))} size={30} />
				<CrowdRow n={14} x0={cx - 450} x1={cx} floor={900} s={0.8} mode="walk" dir={-1} seed="m94" t={rel(c, '020', 66) * 0.3} />
			</>
		);
	},
	{over: (c) => <CountUp t={rel(c, '020', 68)} dur={80} from={0} to={94} label="OTHER GUYS" side="r" y={170} size={140} c="#ffd23a" roll={24} fmt={false} />},
);

/* 021 — never slept outside */
const s021 = S(
	'021',
	'jdusk',
	[960, 620, 1.2],
	[980, 600, 1.4],
	(c) => (
		<>
			{[0, 1, 2].map((i) =>
				man(c, {
					who: 'sam',
					x: 560 + i * 400,
					s: 1.05,
					color: ['#8ab4ff', '#ffb0d0', '#b0e8b0'][i],
					hair: ['short', 'bun', 'cap'][i] as any,
					hairColor: '#334',
					seed: i,
					face: 1,
					handItem: <Pillow />,
					pose: (p) => ({...p, lean: p.lean + wob(c.f + i * 5, 2.5, 2), armF: [30 + wob(c.f, 3, 3), 50], armB: [-30, 55]}),
					expr: 'worried',
				}),
			)}
			{[0, 1, 2].map((i) => (
				<g key={i} transform={`translate(${620 + i * 400},${470 - ((c.f + i * 20) % 60)})`} opacity={rel(c, '021', 8 + i * 10) > 0 ? 0.9 : 0}>
					<text fontSize={48} fontFamily="Rubik" fontWeight={900} fill="#cfe0ff" stroke="#102" strokeWidth={5} paintOrder="stroke">
						Z
					</text>
				</g>
			))}
		</>
	),
	{over: (c) => <Slam t={rel(c, '021', 18)} dur={70} text="NEVER SLEPT OUTSIDE" y={90} size={90} c="#ffd23a" />},
);

/* 022 — Danny, loudest */
const s022 = S(
	'022',
	'jd',
	[900, 600, 1.2],
	[940, 560, 1.7],
	(c) => (
		<>
			<CrowdRow n={5} x0={1260} x1={1700} floor={900} s={0.75} mode="stand" seed="ears" />
			{man(c, {who: 'danny', x: 820, s: 1.2, handItem: <Megaphone />, face: 1, g: [['point', '022', 28, 80]], pose: (p) => ({...p, lean: p.lean + 6 * env(c.f, c.at('022') + 26, c.at('022') + 110, 6, 10) * Math.abs(Math.sin(c.f / 4))})})}
			<Say t={rel(c, '022', 26)} x={1060} y={380} text="I'M IN CHARGE!" size={52} tail={[-80, 110]} />
			<Tag x={820} y={290} text="DANNY" sub="CAR SALESMAN · OHIO" k={pop(c.f, c.at('022') + 52)} />
		</>
	),
	{shake: (c) => 4 * env(c.f, c.at('022') + 26, c.at('022') + 100, 6, 10)},
);

/* 023-024 — Sam, quietest */
const s023 = S(
	'023',
	'jd2',
	[1000, 600, 1.15],
	[1000, 570, 1.6],
	(c) => (
		<>
			{man(c, {who: 'sam', x: 1000, s: 1.2, handItem: <Pitchfork />, g: [['armsCrossed', '023', 20, 120]], expr: 'normal', mouth: 'flat', face: -1})}
			<Tag x={1000} y={300} text="SAM" sub="GREW UP ON A FARM" k={pop(c.f, c.at('023') + 34)} c="#7cf0a0" />
			<Say t={rel(c, '024', 28)} x={1160} y={400} text="..." size={70} tail={[-70, 110]} />
		</>
	),
);

/* 025-027 — Player 3: Max, 16, 100x stronger */
const s025 = S(
	'025',
	'studio',
	[1000, 600, 1.1],
	[1000, 560, 1.7],
	(c) => {
		const mx = lerpF(c.f, c.at('025') + 0, c.at('025') + 40, 2100, 1000);
		return (
			<>
				{man(c, {who: 'max', x: mx, s: 1.3, floor: 920, to: undefined, g: [['fist', '027', 8, 70]], face: -1})}
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '025', 30)} dur={64} text="PLAYER 3" sub="MAX" y={60} size={120} c="#ff5a6e" />
				<Stat t={rel(c, '026', 0)} dur={48} big="16" label="YEARS OLD" side="l" y={300} size={150} c="#fff" />
				<Stat t={rel(c, '027', 4)} dur={90} big="×100" label="STRONGER THAN A HUMAN" side="l" y={300} size={150} c="#ffd23a" />
			</>
		),
	},
);

/* 028-029 — flashback: steel door */
const s028 = S(
	'028',
	'jd2',
	[900, 600, 1.0],
	[960, 540, 1.3],
	(c) => {
		const up = lerpF(c.f, c.at('029') + 28, c.at('029') + 62, 0, 1);
		const dy = 900 - up * 330;
		return (
			<>
				<SteelDoor x={700} y={dy} s={1.0} />
				{man(c, {who: 'max', x: 700, s: 1.05, floor: 900, pose: (p) => ({...p, armF: [168, 6], armB: [-168, 6], lean: -2 + up * 0})})}
				{rel(c, '029', 66) > 0 ? man(c, {who: 'theo', x: 1320, s: 1.0, face: -1, handItem: <Blueprint x={0} y={0} s={0.5} />, g: [['point', '029', 80, 130]]}) : null}
				<Tag x={1320} y={430} text="THEO" sub="HIS BROTHER" k={pop(c.f, c.at('029') + 82)} c="#ffd23a" />
				<Onoma x={700} y={500} text="CLANG!" t={rel(c, '029', 62)} c="#ffd23a" size={90} />
			</>
		);
	},
	{tint: () => 'rgba(150,96,30,0.22)', shake: (c) => (rel(c, '029', 62) > 0 && rel(c, '029', 62) < 8 ? 10 : 0)},
);

/* 030-031 — no Theo, no plan, just muscles */
const s030 = S(
	'030',
	'jd2',
	[960, 600, 1.1],
	[960, 570, 1.5],
	(c) => {
		const gone = env(c.f, c.at('030') + 28, c.at('030') + 60, 1, 1000);
		return (
			<>
				{man(c, {who: 'max', x: 700, s: 1.15, face: 1, g: [['shrug', '030', 36, 90], ['fist', '031', 62, 150]]})}
				{gone < 0.95 ? <g opacity={1 - Math.min(1, rel(c, '030', 30) / 30)}>{man(c, {who: 'theo', x: 1250, s: 1.0, face: -1, expr: 'worried'})}</g> : null}
				<Ring x={1250} y={700} t={rel(c, '030', 30)} c="#ffd23a" r={160} n={2} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '031', 0)} dur={30} text="NO THEO" strike y={80} size={110} c="#ffd23a" />
				<Slam t={rel(c, '031', 31)} dur={34} text="NO PLAN" strike y={80} size={110} c="#8ae0ff" />
				<Slam t={rel(c, '031', 64)} dur={70} text="JUST MUSCLES" y={80} size={120} c="#ff5a6e" />
			</>
		),
	},
);

/* 032 — Day 1: helicopter disappears, jungle closes in */
const s032 = S(
	'032',
	'jd',
	[960, 560, 1.0],
	[960, 500, 1.1],
	(c) => {
		const hx = lerpF(c.f, c.at('032') + 20, c.at('032') + 90, 700, 1900);
		const hs = lerpF(c.f, c.at('032') + 20, c.at('032') + 90, 1.0, 0.25);
		const hy2 = lerpF(c.f, c.at('032') + 20, c.at('032') + 90, 300, 40);
		return (
			<>
				<Heli x={hx} y={hy2} s={hs} f={c.gf} face={1} tilt={-10} />
				{man(c, {who: 'max', x: 960, s: 1.05, g: [['wave', '032', 40, 90]], look: [0.4, -0.8]})}
			</>
		);
	},
	{
		fg: (c) => {
			const k = lerpF(c.f, c.at('032') + 96, c.at('032') + 128, 0, 1);
			return (
				<>
					<Leaf x={-500 + k * 640} y={820} s={1.7} rot={-22} c="#1f6a3a" />
					<Leaf x={2400 - k * 640} y={880} s={1.7} rot={202} c="#1b5e34" />
					<Leaf x={-400 + k * 600} y={300} s={1.5} rot={18} c="#256e40" />
					<Leaf x={2300 - k * 600} y={260} s={1.5} rot={160} c="#1f6a3a" />
				</>
			);
		},
		over: (c) => <Slam t={rel(c, '032', 4)} dur={50} text="DAY 1" y={80} size={150} c="#ffd23a" />,
	},
);

/* 033-034 — the lion's first problem */
const s033 = S(
	'033',
	'jd2',
	[900, 640, 1.1],
	[1080, 600, 1.25],
	(c) => {
		const lx = lerpF(c.f, 0, c.at('034') + 10, -200, 960);
		return (
			<>
				<Sign x={1500} y={906} text="AMAZON" s={1.0} />
				<Cat kind="lion" x={lx} y={900} s={1.15} f={c.gf} mode={rel(c, '034', 10) > 0 ? 'stand' : 'walk'} ph={c.gf * 0.18} />
				<Say t={rel(c, '033', 60)} x={lx + 220} y={560} text="?" size={80} tail={[-90, 120]} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '034', 0)} dur={70} text="LIONS DON'T LIVE HERE" y={80} size={86} c="#fff" />},
);

/* 035 — built for open grassland */
const s035 = S(
	'035',
	'sav',
	[760, 640, 1.2],
	[1100, 600, 0.95],
	(c) => (
		<>
			<Zebra x={1650} y={820} s={0.5} ph={c.gf / 6} />
			<Zebra x={1760} y={836} s={0.45} face={1} ph={c.gf / 6 + 1} />
			<Rock x={620} y={915} s={1.6} />
			<Cat kind="lion" x={620} y={760} s={1.0} f={c.gf} mode="sit" shadow={false} />
			<Callout f={c.f} t0={c.at('035') + 56} t1={c.dur - 4} from={[1660, 720]} to={[1280, 400]} text="SEES PREY FROM FAR" size={44} />
		</>
	),
);

/* 036 — can't see more than 10 meters */
const s036 = S(
	'036',
	'jd',
	[960, 620, 1.15],
	[960, 600, 1.0],
	(c) => {
		const r = lerpF(c.f, c.at('036') + 40, c.at('036') + 70, 0, 1);
		return (
			<>
				<Cat kind="lion" x={960} y={900} s={1.1} f={c.gf} mode="stand" ph={0} />
				<circle cx={960} cy={720} r={340 * r} fill="none" stroke="#ffd23a" strokeWidth={8} strokeDasharray="30 18" />
				<line x1={960} y1={720} x2={960 + 340 * r} y2={720} stroke="#ffd23a" strokeWidth={6} />
				<Tag x={960 + 170 * r} y={680} text="10 m" k={r} size={40} />
			</>
		);
	},
	{
		over: (c) => (
			<svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: lerpF(c.f, c.at('036') + 36, c.at('036') + 70, 0, 0.9)}}>
				<defs>
					<radialGradient id="fogv" cx="0.5" cy="0.62" r="0.5">
						<stop offset="0.45" stopColor="#d6eed2" stopOpacity="0" />
						<stop offset="1" stopColor="#d6eed2" stopOpacity="0.95" />
					</radialGradient>
				</defs>
				<rect width={1920} height={1080} fill="url(#fogv)" />
			</svg>
		),
	},
);

/* 037 — trees, vines, leaves, more leaves */
const s037 = S(
	'037',
	'jd2',
	[960, 620, 1.2],
	[860, 600, 1.35],
	(c) => (
		<>
			<Cat kind="lion" x={960} y={900} s={1.1} f={c.gf} mode="walk" ph={c.gf * 0.12} />
		</>
	),
	{
		fg: (c) => {
			const w = (n: number, side: 1 | -1) => {
				const k = lerpF(c.f, c.at('037') + n, c.at('037') + n + 20, 0, 1);
				return side * (1 - k) * 900;
			};
			return (
				<>
					<Leaf x={-300 + w(0, -1) * -1} y={760} s={1.8} rot={-16} c="#2a7a40" />
					<Leaf x={1900 + w(24, 1)} y={620} s={1.8} rot={196} c="#1f6a3a" />
					<Leaf x={-200 + w(51, -1) * -1} y={420} s={1.6} rot={12} c="#2f8a50" />
					<Leaf x={1900 + w(83, 1)} y={800} s={2.0} rot={190} c="#256e40" />
				</>
			);
		},
		over: (c) => (
			<>
				<Slam t={rel(c, '037', 0)} dur={22} text="TREES" y={90} size={110} c="#7cf0a0" />
				<Slam t={rel(c, '037', 24)} dur={26} text="VINES" y={90} size={110} c="#7cf0a0" />
				<Slam t={rel(c, '037', 51)} dur={30} text="LEAVES" y={90} size={110} c="#7cf0a0" />
				<Slam t={rel(c, '037', 83)} dur={50} text="MORE LEAVES" y={90} size={110} c="#7cf0a0" />
			</>
		),
	},
);

/* 038 — tourist who took the wrong bus */
const s038 = S(
	'038',
	'jd',
	[900, 620, 1.25],
	[960, 580, 1.4],
	(c) => {
		const bx = lerpF(c.f, c.at('038') + 70, c.dur, -500, 2300);
		return (
			<>
				<Bus x={bx} y={800} s={0.9} />
				<Cat kind="lion" x={820} y={910} s={1.2} f={c.gf} mode="stand" ph={0} />
				<g transform="translate(960,640)">
					<rect x={-40} y={-26} width={80} height={52} rx={10} fill="#2a2d3a" stroke="#cfd5dc" strokeWidth={4} />
					<circle cx={0} cy={0} r={16} fill="#6ac0ff" />
				</g>
				<Say t={rel(c, '038', 86)} x={1000} y={380} text="WRONG BUS?!" size={52} tail={[-80, 110]} />
			</>
		);
	},
);

/* 039-040 — hundred men argue about who's in charge */
const s039 = S(
	'039',
	'jd',
	[960, 620, 1.15],
	[960, 590, 1.35],
	(c) => (
		<>
			<CrowdRow n={9} x0={260} x1={1700} floor={880} s={0.8} mode="panic" seed="argu" />
			{man(c, {who: 'danny', x: 960, s: 1.1, g: [['point', '040', 30, 70], ['fist', '040', 74, 120]], handItem: <Megaphone />})}
			<Say t={rel(c, '040', 10)} x={420} y={430} text="ME!" size={52} tail={[10, 110]} />
			<Say t={rel(c, '040', 36)} x={1500} y={430} text="NO, ME!" size={52} tail={[-10, 110]} />
			<Say t={rel(c, '040', 64)} x={960} y={330} text="I'M THE BOSS!" size={52} tail={[0, 110]} />
		</>
	),
	{over: (c) => <Stat t={rel(c, '040', 24)} dur={90} big="40 MIN" label="OF ARGUING" side="r" y={160} size={130} c="#ffd23a" />},
);

/* 041-042 — Danny votes for Danny, Danny wins */
const s041 = S(
	'041',
	'jd2',
	[960, 620, 1.2],
	[900, 580, 1.4],
	(c) => (
		<>
			<g transform="translate(1250,900)">
				<rect x={-90} y={-170} width={180} height={170} rx={14} fill="#c89a5a" stroke="#6a4a22" strokeWidth={6} />
				<rect x={-50} y={-176} width={100} height={12} rx={4} fill="#2a1808" />
				<text x={0} y={-72} textAnchor="middle" fontSize={34} fontFamily="Rubik" fontWeight={900} fill="#3a2410">
					VOTE
				</text>
			</g>
			{man(c, {who: 'danny', x: 900, s: 1.15, face: 1, g: [['presentF', '041', 4, 30]], pose: (p) => (rel(c, '042', 0) > 0 ? {...p, armF: [150, 20], armB: [-150, 20]} : p), expr: rel(c, '042', 0) > 0 ? 'wide' : 'normal', floor: 900 - (rel(c, '042', 4) > 0 ? Math.abs(Math.sin(rel(c, '042', 4) / 5)) * 36 : 0)})}
			{rel(c, '041', 8) > 0 && rel(c, '041', 8) < 26 ? <rect x={lerpF(c.f, c.at('041') + 8, c.at('041') + 26, 1020, 1240)} y={lerpF(c.f, c.at('041') + 8, c.at('041') + 26, 640, 740)} width={30} height={40} fill="#fff" stroke="#999" strokeWidth={2} /> : null}
			<Confetti x={900} y={600} t={rel(c, '042', 2)} />
		</>
	),
	{over: (c) => <Slam t={rel(c, '042', 0)} dur={46} text="DANNY WINS!" y={80} size={130} c="#8ae0ff" />},
);

/* 043-044 — Sam says nothing, and Max? */
const s043 = S(
	'043',
	'jd2',
	[1000, 620, 1.3],
	[1100, 600, 1.1],
	(c) => (
		<>
			{man(c, {who: 'sam', x: 900, s: 1.15, face: 1, g: [['armsCrossed', '043', 0, 120]], mouth: 'flat'})}
			<Say t={rel(c, '043', 22)} x={1060} y={400} text="..." size={80} tail={[-70, 110]} />
			<g transform={`translate(1400,${560 + wob(c.f, 6, 5)})`} opacity={rel(c, '043', 20) > 0 ? 1 : 0}>
				<text fontSize={36} fontFamily="Rubik" fontWeight={800} fill="#fff" stroke="#102" strokeWidth={5} paintOrder="stroke">
					*cricket*
				</text>
			</g>
		</>
	),
);

/* 045-047 — Max punches a tree, it falls, another one */
const s045 = S(
	'045',
	'jd',
	[900, 560, 1.15],
	[1100, 520, 1.3],
	(c) => {
		const fall = lerpF(c.f, c.at('046') + 4, c.at('046') + 30, 0, 86);
		const hit = (n: number) => rel(c, '045', n);
		return (
			<>
				<Tree x={1250} y={900} s={1.0} fall={fall} dir={1} f={c.gf} shake={env(c.f, c.at('045') + 22, c.at('045') + 40, 1, 10) * 6} />
				{man(c, {who: 'max', x: 820, s: 1.1, face: 1, g: [['fist', '045', 8, 40]], pose: (p) => ({...p, lean: p.lean + 14 * env(c.f, c.at('045') + 18, c.at('045') + 34, 4, 6)})})}
				<Onoma x={1130} y={620} text="WHAM!" t={hit(24)} c="#ffd23a" size={90} />
				<Onoma x={1500} y={760} text="CRASH!" t={rel(c, '046', 26)} c="#ff5a6e" size={100} rot={6} />
			</>
		);
	},
	{shake: (c) => (rel(c, '045', 24) > 0 && rel(c, '045', 24) < 6 ? 9 : rel(c, '046', 28) > 0 && rel(c, '046', 28) < 10 ? 18 : 0)},
);
const s047 = S(
	'047',
	'jd2',
	[1000, 560, 1.15],
	[1000, 520, 1.3],
	(c) => {
		const fall = lerpF(c.f, c.at('047') + 28, c.at('047') + 52, 0, -86);
		return (
			<>
				<Tree x={560} y={900} s={0.95} fall={fall} dir={1} f={c.gf} shake={env(c.f, c.at('047') + 18, c.at('047') + 34, 1, 8) * 6} />
				{man(c, {who: 'max', x: 960, s: 1.1, face: -1, g: [['fist', '047', 10, 34]], pose: (p) => ({...p, lean: p.lean + 14 * env(c.f, c.at('047') + 15, c.at('047') + 30, 4, 6)})})}
				<Onoma x={700} y={620} text="POW!" t={rel(c, '047', 20)} c="#ffd23a" size={90} />
			</>
		);
	},
	{shake: (c) => (rel(c, '047', 20) > 0 && rel(c, '047', 20) < 6 ? 9 : 0)},
);

/* 048-050 — builds a log shelter, lies down: this is going to be easy */
const s048 = S(
	'048',
	'jd',
	[960, 620, 1.0],
	[960, 540, 1.3],
	(c) => {
		const b = lerpF(c.f, c.at('048') + 44, c.at('049') + 40, 0, 1);
		return (
			<>
				<LogHut x={1000} y={910} s={1.1} build={b} />
				{man(c, {who: 'max', x: 480 + 360 * b, s: 1.0, face: 1, g: [['presentF', '049', 40, 100]]})}
			</>
		);
	},
	{over: (c) => <Stat t={rel(c, '048', 22)} dur={60} big="1 HOUR" side="l" y={160} size={120} c="#ffd23a" />},
);
const s050 = S(
	'050',
	'jd',
	[1000, 640, 1.1],
	[1000, 560, 1.5],
	(c) => {
		const lie = lerpF(c.f, c.at('050') + 6, c.at('050') + 24, 0, 1);
		return (
			<>
				<LogHut x={1000} y={910} s={1.1} />
				<g opacity={1 - lie}>{man(c, {who: 'max', x: 760, to: 920, w: ['050', 0, 24], s: 1.0, face: 1})}</g>
				<g opacity={lie}>
					<g transform="translate(0,0)">{man(c, {who: 'max', x: 1000, s: 0.9, floor: 900, rot: -84 * lie, pose: () => ({lean: 0, head: -6, armB: [4, 10], armF: [10, 14], legB: [0, 0], legF: [3, 0]}), face: 1, hide: lie < 0.05})}</g>
				</g>
				<Say t={rel(c, '050', 61)} x={1000} y={330} text="THIS IS GOING TO BE EASY" size={44} tail={[0, 100]} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '051', 0)} dur={1} text="" />
			</>
		),
	},
);

export const SHOTS_A: ShotDef[] = [s001, s002, s003, s004, s005, s007, s009, s010, s012, s013, s015, s016, s017, s018, s019, s020, s021, s022, s023, s025, s028, s030, s032, s033, s035, s036, s037, s038, s039, s041, s043, s045, s047, s048, s050];
