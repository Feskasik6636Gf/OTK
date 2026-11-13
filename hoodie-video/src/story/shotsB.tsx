import React from 'react';
import {CrowdRow} from '../kit/kit';
import {Callout} from '../kit/graphics';
import {env} from '../kit/actions';
import {Onoma} from '../reference/PauseTime';
import type {ShotDef} from '../kit/coverage';
import {Band, Capy, Cat, Fruit, Larva, LogHut, Monkey, Pod, Pot, Spark, Tree} from './critters';
import {S, man, lying, pop, rel, sc, lerpF} from './dsl';
import {Fire} from './places';
import {CountUp, Round, Say, Slam, Stat} from './overlays';
import {Burger} from './critters';
import {Confetti, Germ, Leaf, Ring, Sweat, Tag, Thermo} from './props2';

const wob = (f: number, a: number, p = 6) => Math.sin(f / p) * a;

/* 051 — Round 1: Shelter, Max */
const s051 = S(
	'051',
	'jd',
	[1000, 640, 1.0],
	[1000, 600, 1.2],
	(c) => (
		<>
			<LogHut x={1000} y={910} s={1.1} />
			{man(c, {who: 'max', x: 1400, s: 1.05, face: -1, g: [['fist', '051', 30, 80]], mouth: 'smile'})}
			<Confetti x={1000} y={500} t={rel(c, '051', 60)} />
		</>
	),
	{over: (c) => <Round t={rel(c, '051', 0)} dur={c.dur - 6} n={1} title="SHELTER" winner="MAX +1" c="#ff5a6e" />},
);

/* 052-054 — Day 2, the heat */
const s052 = S(
	'052',
	'jd',
	[960, 560, 1.0],
	[960, 560, 1.45],
	(c) => {
		const h = lerpF(c.f, 0, c.dur, 0.2, 1);
		return (
			<>
				{man(c, {who: 'max', x: 900, s: 1.1, expr: 'worried', g: [['touchFace', '053', 6, 60], ['scratch', '054', 0, 40]]})}
				<Sweat x={900} y={520} f={c.gf} n={7} s={1.1} />
				<Thermo x={1500} y={760} k={h} s={1.4} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '052', 6)} dur={60} text="DAY 2" sub="THE HEAT" y={70} size={130} c="#ff9a3a" />
				<Slam t={rel(c, '054', 8)} dur={52} text="WET HOT" y={780} size={140} c="#ff5a6e" />
			</>
		),
		tint: (c) => `rgba(255,120,30,${lerpF(c.f, 0, c.dur, 0.05, 0.28)})`,
	},
);

/* 055-056 — sweat can't dry */
const s055 = S(
	'055',
	'jd2',
	[1000, 560, 1.5],
	[960, 540, 1.9],
	(c) => (
		<>
			{man(c, {who: 'max', x: 1000, s: 1.3, expr: 'sad', g: [['facepalm', '056', 20, 70]]})}
			<Sweat x={1000} y={470} f={c.gf} n={10} s={1.4} />
			<Callout f={c.f} t0={c.at('055') + 58} t1={c.at('056') - 4} from={[1080, 560]} to={[1500, 400]} text="SWEAT CAN'T DRY" size={44} />
			<Callout f={c.f} t0={c.at('056') + 4} t1={c.dur - 4} from={[960, 640]} to={[520, 360]} text="COOLS ONLY WHEN IT DRIES" size={40} />
		</>
	),
	{tint: () => 'rgba(255,120,30,0.2)'},
);

/* 057 — car engine with no radiator */
const s057 = S(
	'057',
	'jd',
	[1000, 640, 1.0],
	[1000, 600, 1.35],
	(c) => {
		const t = c.at('057') + 81;
		const k = pop(c.f, t);
		return (
			<>
				{man(c, {who: 'max', x: 560, s: 1.0, expr: 'worried'})}
				{sc(k, 1300, 800, (
					<g transform="translate(1300,900)">
						<rect x={-200} y={-120} width={400} height={80} rx={26} fill="#d9372a" />
						<path d="M-120,-120 L-70,-190 L90,-190 L140,-120 Z" fill="#c02a20" />
						<rect x={-60} y={-180} width={130} height={56} fill="#cfeaf7" opacity={0.8} />
						<circle cx={-120} cy={-40} r={34} fill="#222" />
						<circle cx={120} cy={-40} r={34} fill="#222" />
						{[0, 1, 2, 3, 4].map((i) => {
							const u = ((c.f * 1.5 + i * 16) % 80) / 80;
							return <circle key={i} cx={170 + Math.sin(i + u * 6) * 24} cy={-130 - u * 200} r={14 + u * 36} fill="#fff" opacity={0.7 * (1 - u)} />;
						})}
					</g>
				))}
				<Sweat x={560} y={540} f={c.gf} n={8} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '057', 92)} dur={60} text="NO RADIATOR!" y={90} size={110} c="#ff5a6e" />, tint: () => 'rgba(255,120,30,0.2)', shake: (c) => (rel(c, '057', 90) > 0 ? 3 : 0)},
);

/* 058-061 — thirsty, drinks the river */
const s058 = S(
	'058',
	'riv',
	[960, 640, 1.1],
	[1200, 700, 1.4],
	(c) => {
		const dr = env(c.f, c.at('061') + 2, c.at('061') + 50, 8, 8);
		return (
			<>
				<LogHut x={420} y={910} s={0.8} />
				{man(c, {who: 'max', x: 760, to: 1220, w: ['059', 0, 60], s: 1.1, face: 1, expr: 'sad', pose: (p) => ({...p, lean: p.lean + 40 * dr, head: p.head + 20 * dr, armF: [p.armF[0] + (70 - p.armF[0]) * dr, p.armF[1] + (60 - p.armF[1]) * dr]})})}
				<Say t={rel(c, '058', 10)} x={760} y={420} text="SO THIRSTY..." size={44} tail={[10, 100]} />
				<Onoma x={1300} y={790} text="GLUG GLUG" t={rel(c, '061', 12)} c="#8ae0ff" size={70} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '059', 6)} dur={60} text="WATER EVERYWHERE" y={80} size={100} c="#8ae0ff" />},
);

/* 062-064 — the men thirsty, Danny walks to the river, Sam speaks */
const s062 = S(
	'062',
	'riv',
	[960, 620, 1.0],
	[1100, 600, 1.2],
	(c) => (
		<>
			<CrowdRow n={10} x0={140} x1={880} floor={900} s={0.7} mode="stand" seed="thirst" />
			{man(c, {who: 'danny', x: 780, to: 1240, w: ['063', 0, 60], s: 1.1, expr: 'sad'})}
			{man(c, {who: 'sam', x: 2100, to: 1500, w: ['064', 6, 40], s: 1.1, face: -1, g: [['stop', '064', 36, 80]]})}
		</>
	),
	{over: (c) => <Slam t={rel(c, '062', 6)} dur={50} text="THIRSTY!" y={80} size={110} c="#8ae0ff" />},
);

/* 065-066 — Don't. Boil it first. */
const s065 = S(
	'065',
	'riv',
	[1250, 620, 1.5],
	[1300, 580, 1.9],
	(c) => (
		<>
			{man(c, {who: 'danny', x: 1060, s: 1.15, face: 1, expr: 'wide', g: [['stop', '065', 0, 30]]})}
			{man(c, {who: 'sam', x: 1560, s: 1.15, face: -1, g: [['stop', '065', 0, 90]], expr: 'angry'})}
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '065', 0)} dur={22} text="DON'T!" y={90} size={170} c="#ff3a52" />
				<Slam t={rel(c, '066', 0)} dur={50} text="BOIL IT FIRST" y={90} size={120} c="#ffd23a" />
			</>
		),
		shake: (c) => (rel(c, '065', 0) > 0 && rel(c, '065', 0) < 8 ? 12 : 0),
	},
);

/* 067-069 — germs you can't see or punch */
const s067 = S(
	'067',
	'studio',
	[960, 560, 1.0],
	[960, 560, 1.25],
	(c) => {
		const t = c.at('067');
		return (
			<>
				<circle cx={960} cy={560} r={330} fill="#7ac8e8" opacity={0.28} stroke="#cfeeff" strokeWidth={10} />
				{[[-160, -80, 1.0], [140, -140, 0.8], [-60, 130, 1.2], [180, 90, 0.9], [-220, 70, 0.7], [20, -30, 1.1]].map((g, i) => (
					<g key={i} opacity={pop(c.f, t + 58 + i * 6)}>
						<Germ x={960 + g[0]} y={560 + g[1]} s={g[2]} f={c.gf + i * 9} c={['#7ad84a', '#d8c84a', '#d86a8a'][i % 3]} />
					</g>
				))}
				{man(c, {who: 'max', x: 330, s: 0.95, face: 1, g: [['fist', '069', 12, 60]], expr: 'angry'})}
				<Onoma x={560} y={640} text="WHIFF" t={rel(c, '069', 30)} c="#fff" size={60} />
			</>
		);
	},
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '067', 62)} dur={26} text="BACTERIA" y={80} size={90} c="#7ad84a" />
				<Slam t={rel(c, '067', 90)} dur={30} text="PARASITES" y={80} size={90} c="#ff8aa0" />
				<Slam t={rel(c, '068', 8)} dur={34} text="CAN'T SEE THEM" y={820} size={80} c="#fff" />
				<Slam t={rel(c, '069', 14)} dur={50} text="CAN'T PUNCH THEM" y={820} size={80} c="#ff5a6e" />
			</>
		),
	},
);

/* 070-071 — six hours rubbing sticks */
const s070 = S(
	'070',
	'jdusk',
	[960, 640, 1.1],
	[960, 620, 1.3],
	(c) => (
		<>
			{[0, 1, 2, 3].map((i) =>
				man(c, {
					who: 'sam',
					x: 520 + i * 300,
					s: 1.0,
					seed: i,
					color: ['#d9372a', '#2f6fd8', '#8b5cf6', '#e8802a'][i],
					hair: ['short', 'cap', 'bun', 'spiky'][i] as any,
					hairColor: '#333',
					face: 1,
					expr: 'worried',
					pose: (p) => ({...p, lean: 20 + wob(c.f + i * 3, 4, 2), armF: [60 + wob(c.f * 2 + i, 20, 1.5), 60], armB: [50 + wob(c.f * 2 + i, 20, 1.5), 70]}),
				}),
			)}
			<Sweat x={820} y={540} f={c.gf} n={6} />
			{[0, 1, 2].map((i) => (
				<circle key={i} cx={1120 + wob(c.f, 20, 7) + i * 14} cy={720 - ((c.f * 1.3 + i * 20) % 90)} r={8 + (((c.f * 1.3 + i * 20) % 90) / 90) * 14} fill="#bbb" opacity={0.4} />
			))}
		</>
	),
	{
		over: (c) => (
			<>
				<CountUp t={rel(c, '070', 20)} dur={80} to={6} suffix=" HOURS" label="RUBBING STICKS" side="l" y={150} size={140} c="#ffd23a" roll={14} fmt={false} />
				<Stat t={rel(c, '071', 32)} dur={60} big="10 MEN" label="AT A TIME" side="r" y={150} size={120} c="#8ae0ff" />
				<Slam t={rel(c, '071', 100)} dur={50} text="BLISTERS!" y={780} size={110} c="#ff5a6e" />
			</>
		),
	},
);

/* 072-073 — spark, fire, cheer */
const s072 = S(
	'072',
	'jdusk',
	[960, 660, 1.1],
	[960, 600, 1.3],
	(c) => {
		const b = lerpF(c.f, c.at('072') + 14, c.at('073') + 6, 0.05, 1.5);
		const cheer = env(c.f, c.at('073') + 30, c.dur, 6, 10);
		return (
			<>
				<Fire x={960} y={910} s={1} f={c.gf} big={b} />
				<Spark x={960} y={800} t={rel(c, '072', 14)} c="#ffd27a" />
				{[0, 1, 2, 3, 4].map((i) =>
					man(c, {
						who: 'sam',
						x: 420 + i * 270 + (i > 2 ? 160 : 0),
						s: 1.0,
						seed: i,
						color: ['#d9372a', '#2f6fd8', '#8b5cf6', '#e8802a', '#3aa37a'][i],
						hair: ['short', 'cap', 'bun', 'spiky', 'short'][i] as any,
						hairColor: '#333',
						floor: 900 - cheer * Math.abs(Math.sin(c.f / 4 + i)) * 50,
						pose: (p) => ({...p, armF: [p.armF[0] + (160 - p.armF[0]) * cheer, 10], armB: [p.armB[0] + (-160 - p.armB[0]) * cheer, 10]}),
						expr: cheer > 0.3 ? 'wide' : 'normal',
						mouth: cheer > 0.3 ? 'open' : undefined,
					}),
				)}
				<Confetti x={960} y={560} t={rel(c, '073', 36)} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '073', 74)} dur={50} text="WORLD CUP!" y={80} size={130} c="#ffd23a" />, light: {night: true, o: 0.35, c: '255,170,90'}},
);

/* 074-076 — pot from clay, ugly, works */
const s074 = S(
	'074',
	'jdusk',
	[960, 640, 1.2],
	[960, 580, 1.55],
	(c) => (
		<>
			<Fire x={960} y={910} s={0.9} f={c.gf} />
			<Pot x={960} y={780} s={1.1} f={c.gf} />
			{man(c, {who: 'sam', x: 540, s: 1.1, color: '#e8802a', hair: 'cap', hairColor: '#e8802a', face: 1, g: [['point', '074', 36, 80], ['presentF', '075', 0, 40]]})}
			{man(c, {who: 'max', x: 1400, s: 1.1, face: -1, hide: true})}
			<Tag x={540} y={420} text="PLUMBER" k={pop(c.f, c.at('074') + 38)} />
		</>
	),
	{over: (c) => (
		<>
			<Slam t={rel(c, '075', 0)} dur={26} text="UGLY." y={80} size={130} c="#ff8a98" />
			<Slam t={rel(c, '076', 0)} dur={60} text="IT WORKS!" y={80} size={130} c="#7cf0a0" />
		</>
	)},
);

/* 077-078 — Max sick in the shelter */
const s077 = S(
	'077',
	'jd',
	[960, 700, 1.1],
	[880, 760, 1.5],
	(c) => (
		<>
			<LogHut x={1000} y={910} s={1.1} />
			{lying(c, 'max', 1100, 900, {s: 1.4, expr: 'sleepy'})}
			<Thermo x={1500} y={800} k={lerpF(c.f, c.at('078'), c.dur, 0.4, 1)} s={1.4} />
			<Sweat x={760} y={760} f={c.gf} n={4} />
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '077', 0)} dur={46} text="DAY 3" y={70} size={130} c="#ffd23a" />
				<Slam t={rel(c, '078', 0)} dur={36} text="FEVER" y={780} size={110} c="#ff5a6e" />
				<Slam t={rel(c, '078', 30)} dur={50} text="STOMACH CRAMPS" y={780} size={100} c="#ff9a3a" />
			</>
		),
		tint: () => 'rgba(120,200,90,0.16)',
	},
);

/* 079-080 — strongest human defeated by something smaller than a grain of sand */
const s079 = S(
	'079',
	'jd2',
	[900, 740, 1.2],
	[900, 740, 1.6],
	(c) => {
		const gk = pop(c.f, c.at('080') + 16);
		return (
			<>
				{lying(c, 'max', 1150, 900, {s: 1.5, expr: 'sleepy'})}
				{sc(gk, 900, 700, <Germ x={900} y={700} s={1.5} f={c.gf} />)}
				<Callout f={c.f} t0={c.at('080') + 56} t1={c.dur - 4} from={[900, 700]} to={[1400, 440]} text="SMALLER THAN A GRAIN OF SAND" size={40} />
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '079', 4)} dur={90} text="STRONGEST HUMAN" y={70} size={100} c="#ffd23a" />},
);

/* 081-083 — strength doesn't fight germs, immune system does */
const s081 = S(
	'081',
	'studio',
	[960, 560, 1.0],
	[960, 540, 1.25],
	(c) => (
		<>
			{man(c, {who: 'max', x: 960, s: 1.3, floor: 960, expr: 'sleepy', g: [['think', '083', 10, 60]]})}
			<Germ x={420} y={520} s={1.2} f={c.gf} />
			<g opacity={pop(c.f, c.at('082') + 6)}>
				<path d="M1500,330 C1640,330 1700,370 1700,370 C1700,500 1660,600 1500,680 C1340,600 1300,500 1300,370 C1300,370 1360,330 1500,330 Z" fill="#3aa0ff" stroke="#bfe0ff" strokeWidth={10} />
				<path d="M1440,500 l50,50 l100,-120" stroke="#fff" strokeWidth={26} fill="none" strokeLinecap="round" strokeLinejoin="round" />
			</g>
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '081', 0)} dur={50} text="STRENGTH" strike y={90} size={120} c="#ffd23a" />
				<Slam t={rel(c, '082', 0)} dur={50} text="IMMUNE SYSTEM" y={90} size={110} c="#8ae0ff" />
				<Slam t={rel(c, '083', 26)} dur={60} text="COMPLETELY NORMAL" y={820} size={80} c="#fff" />
			</>
		),
	},
);

/* 084-085 — doesn't press the button, but thinks about it */
const s084 = S(
	'084',
	'studio',
	[1000, 560, 1.0],
	[1000, 540, 1.3],
	(c) => {
		const fx = lerpF(c.f, c.at('084') + 14, c.at('084') + 40, 1380, 1050) + env(c.f, c.at('085') + 6, c.at('085') + 26, 6, 10) * -60;
		return (
			<>
				<g transform="rotate(-8 900 560)">
					<Band x={900} y={560} s={1.5} f={c.gf} />
				</g>
				<circle cx={fx + 90} cy={500} r={40} fill="#0b0b0d" />
				<rect x={fx + 90} y={470} width={500} height={60} rx={30} fill="#ff2340" />
				<Sweat x={1500} y={760} f={c.gf} n={5} />
				{man(c, {who: 'max', x: 1560, s: 0.9, face: -1, expr: 'worried', g: [['think', '085', 4, 40]], floor: 940})}
			</>
		);
	},
	{over: (c) => <Slam t={rel(c, '085', 4)} dur={46} text="HE THINKS ABOUT IT..." y={90} size={90} c="#ffd23a" />},
);

/* 086 — Round 2: water, the men */
const s086 = S(
	'086',
	'jd',
	[960, 640, 1.0],
	[960, 600, 1.2],
	(c) => (
		<>
			<Fire x={960} y={910} s={0.8} f={c.gf} />
			<Pot x={1160} y={800} s={0.8} f={c.gf} />
			<CrowdRow n={10} x0={140} x1={800} floor={900} s={0.8} mode="dance" seed="r2" />
			<Confetti x={960} y={500} t={rel(c, '086', 70)} />
		</>
	),
	{over: (c) => <Round t={rel(c, '086', 0)} dur={c.dur - 6} n={2} title="WATER" winner="THE MEN +1" c="#8ae0ff" />},
);

/* 087-088 — Day 5 hunger, lion needs 7 kg of meat a day */
const s087 = S(
	'087',
	'jd2',
	[900, 640, 1.2],
	[960, 600, 1.45],
	(c) => (
		<>
			<Cat kind="lion" x={820} y={910} s={1.3} f={c.gf} mode="stand" thin={1} ph={0} />
			<Onoma x={1000} y={720} text="GRRRR" t={rel(c, '087', 24) % 34} c="#ffb04a" size={80} />
			{[0, 1, 2, 3, 4, 5, 6].map((i) => (
				<g key={i} opacity={pop(c.f, c.at('088') + 26 + i * 8)}>
					<ellipse cx={1380 + (i % 4) * 90} cy={860 - Math.floor(i / 4) * 60} rx={42} ry={30} fill="#d9452f" stroke="#fff3e0" strokeWidth={4} />
					<rect x={1380 + (i % 4) * 90 - 8} y={846 - Math.floor(i / 4) * 60} width={16} height={28} rx={8} fill="#fff3e0" />
				</g>
			))}
		</>
	),
	{
		over: (c) => (
			<>
				<Slam t={rel(c, '087', 4)} dur={50} text="DAY 5" sub="HUNGER" y={70} size={130} c="#ff9a3a" />
				<CountUp t={rel(c, '088', 20)} dur={90} to={7} suffix=" KG" label="OF MEAT A DAY" side="r" y={140} size={150} c="#ffd23a" roll={16} fmt={false} />
			</>
		),
	},
);
export const SHOTS_B: ShotDef[] = [s051, s052, s055, s057, s058, s062, s065, s067, s070, s072, s074, s077, s079, s081, s084, s086, s087];
