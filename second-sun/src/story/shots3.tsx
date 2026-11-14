import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Chair} from '../engine/props';
import {env, gesture, idle, walk} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {CrowdRow, Extra, Layer, Stage, Svg, camOn, mixCam, usePush} from '../kit/kit';
import {Kitchen} from '../kit/sets';
import {Board, Bubble, FONT, HAND} from '../kit/ui';
import {Callout} from '../kit/graphics';
import type {ShotDef} from '../kit/coverage';
import {Ball, Beach, Living, ORANGE_SUN, Planet, Road, SimpleCar, SpaceBG, Star, Studio, Turtle, WHITE_SUN} from './places';
import {Satellite} from './shots1';
import {Burst, FL, Flash, Hero, Inside, Outdoor, Pill, PopText, Punch, QMark, SpaceStage, beats, headY, hops, on, path, shake, tw} from './h';

const SEAT = (f: number, seed: number): Pose => ({...idle(f, seed), legB: [88, 85], legF: [92, 90]});

/* 144-148: astronomers finish the calculations: it's passing through */
const S144: React.FC = () => {
	const {f, gf, at} = useShot();
	const u = tw(f, at('146'), at('148') + 60, 0, 1);
	const sx = 520 + 900 * u;
	const sy = 560 - Math.sin(u * Math.PI) * 260;
	const sp = beats(idle(f, 4), f, at, [['144', 10, 70, 'presentF'], ['145', 0, 50, 'stop'], ['147', 0, 60, 'point'], ['148', 10, 60, 'presentF']]);
	const cam = mixCam(camOn(960, 430, 1.05), camOn(960, 400, 1.3), tw(f, at('146'), at('147'), 0, 1));
	return (
		<Stage cam={cam} bg="#0e1430" light={{x: 50, y: 10, o: 0.3}}>
			<Layer depth={1.2}>
				<Studio f={gf} ticker="ASTRONOMERS: THE SECOND SUN IS PASSING THROUGH">
					<SpaceBG f={gf} />
					<circle cx={960} cy={420} r={130} fill="none" stroke="#5a6aa0" strokeWidth={3} strokeDasharray="6 8" />
					<Star x={960} y={420} r={26} c={WHITE_SUN} f={gf} id="w144" />
					<path d="M520,560 Q960,40 1420,560" stroke={ORANGE_SUN} strokeWidth={4} fill="none" strokeDasharray="10 10" opacity={u > 0 ? 0.7 : 0} />
					{u > 0 ? <Star x={sx} y={sy} r={20} c={ORANGE_SUN} f={gf} id="o144" /> : null}
				</Studio>
			</Layer>
			<Layer depth={1}>
				<Svg>
					<Actor who="scientist" x={1560} s={1.05} facing={-1} pose={sp} handF={on(f, at, '147', 0, 60) > 0.5 ? 'point' : undefined} look={[-0.6, -0.2]} uid="sc144" />
					<Extra i={3} x={380} floor={FL} s={1} seed="astro" pose={beats(idle(f, 2), f, at, [['144', 30, 80, 'rubChin']])} facing={1} />
					<PopText t={f - at('144') - 30} x={960} y={110} text="CALCULATIONS DONE" size={50} c="#9ff0b0" out={at('145') - at('144') - 30} />
					<PopText t={f - at('145') - 4} x={960} y={110} text="NOT STAYING" size={70} c="#ff5a6a" out={at('146') - at('145')} />
					<PopText t={f - at('146') - 4} x={960} y={110} text="PASSING THROUGH" size={70} c="#ffd34a" out={at('147') - at('146')} />
					<PopText t={f - at('147') - 4} x={960} y={110} text="FROM DEEP SPACE" size={66} c="#c8d0ff" out={at('148') - at('147')} />
					<Pill t={f - at('148') - 20} x={960} y={110} text="LEAVES IN ~4 MONTHS" c="#ff8a2a" size={44} />
				</Svg>
			</Layer>
		</Stage>
	);
};

const TV: React.FC<{x: number; y: number; children?: React.ReactNode; f: number}> = ({x, y, children}) => (
	<g transform={`translate(${x},${y})`}>
		<rect x={-180} y={-120} width={360} height={230} rx={14} fill="#14141c" />
		<rect x={-164} y={-104} width={328} height={198} fill="#0a1640" />
		{children}
		<rect x={-20} y={110} width={40} height={40} fill="#14141c" />
		<rect x={-80} y={150} width={160} height={14} rx={6} fill="#14141c" />
	</g>
);

/* 149-150: good news… except for one thing */
const S149: React.FC = () => {
	const {f, gf, at} = useShot();
	const freeze = f > at('150');
	const hp = beats(SEAT(f, 2), f, at, [['149', 4, at('150') - at('149'), 'cheer']]);
	const cam = mixCam(camOn(700, 560, 1.2), camOn(620, 520, 1.9), tw(f, at('150'), at('150') + 8, 0, 1));
	return (
		<>
			<Inside cam={cam} set={<Living f={gf} />}>
				<TV x={1440} y={700} f={f}>
					<text x={0} y={10} textAnchor="middle" fontSize={44} fontFamily={FONT} fontWeight={900} fill="#9ff0b0">
						GOOD NEWS
					</text>
				</TV>
				<Hero x={600} seat={760} pose={freeze ? {...SEAT(f, 2), head: 10} : hp} mouth={freeze ? 'flat' : 'open'} expr={freeze ? 'worried' : 'wide'} look={[0.8, 0]} uid="h149" />
				<Actor who="sam" x={780} seat={790} s={0.72} pose={freeze ? SEAT(f, 3) : beats(SEAT(f, 3), f, at, [['149', 10, 999, 'cheer']])} mouth="open" look={[0.8, 0]} uid="sam149" />
				<PopText t={f - at('149') - 6} x={600} y={300} text="YAY!" size={80} c="#9ff0b0" out={at('150') - at('149') - 8} />
			</Inside>
			{freeze ? <AbsoluteFill style={{background: '#202030', mixBlendMode: 'saturation', opacity: 0.85}} /> : null}
			<Punch t={f - at('150') - 2} text="EXCEPT…" top={760} c="#ff5a6a" out={9999} />
		</>
	);
};

/* 151-152: gravity — every star pulls on everything */
const S151: React.FC = () => {
	const {f, gf, at} = useShot();
	const drop = tw(f, at('151'), at('151') + 10, -300, 380);
	const cam = shake(usePush(camOn(960, 540, 1.0), camOn(960, 560, 1.2)), f, at('151') + 10, 16, 18);
	const objs: [number, number, number][] = [[400, 300, 30], [1500, 260, 40], [1600, 800, 26], [320, 820, 22], [1180, 900, 36]];
	return (
		<SpaceStage cam={cam}>
			<Star x={960} y={560} r={100} c={ORANGE_SUN} f={gf} id="o151" />
			{f > at('152')
				? objs.map(([x, y, r], i) => {
						const pull = 0.04 * tw(f, at('152'), at('152') + 60, 0, 1);
						const px = x + (960 - x) * pull + Math.sin(f / 4 + i) * 3;
						const py = y + (560 - y) * pull;
						return (
							<g key={i}>
								<line x1={960} y1={560} x2={px} y2={py} stroke="#ffd34a" strokeWidth={4} strokeDasharray="6 10" strokeDashoffset={-f * 2} opacity={0.6} />
								{i === 1 ? <Planet x={px} y={py} r={r} f={gf} /> : <circle cx={px} cy={py} r={r} fill={['#c0a080', '#2f7fe6', '#d0603a', '#9aa0aa', '#e0c060'][i]} />}
							</g>
						);
					})
				: null}
			<g transform={`translate(960,${drop})`}>
				<text textAnchor="middle" fontSize={150} fontFamily={FONT} fontWeight={900} fill="#10132a" stroke="#10132a" strokeWidth={28} strokeLinejoin="round">
					GRAVITY
				</text>
				<text textAnchor="middle" fontSize={150} fontFamily={FONT} fontWeight={900} fill="#ffd34a">
					GRAVITY
				</text>
			</g>
			<Callout f={f} t0={at('152') + 60} t1={9999} from={[1500 + (960 - 1500) * 0.04, 260 + 300 * 0.04]} to={[1700, 120]} text="INCLUDING US" c="#5ad0ff" />
		</SpaceStage>
	);
};

/* 153-154: with one sun the orbit is simple, year after year */
const S153: React.FC = () => {
	const {f, gf, at} = useShot();
	const a = gf / 14;
	const years = Math.floor(Math.max(0, f - at('154')) ** 2 * 3);
	const cam = usePush(camOn(960, 540, 1.1), camOn(960, 540, 0.95));
	return (
		<SpaceStage cam={cam}>
			<ellipse cx={960} cy={540} rx={420} ry={180} fill="none" stroke="#9ff0b0" strokeWidth={5} opacity={0.6} />
			<Star x={960} y={540} r={70} c={WHITE_SUN} f={gf} id="w153" />
			<Planet x={960 + Math.cos(a) * 420} y={540 + Math.sin(a) * 180} r={34} f={gf} />
			<PopText t={f - at('153') - 10} x={960} y={150} text="ONE SUN = SIMPLE" size={70} c="#9ff0b0" out={at('154') - at('153')} />
			{f > at('154') ? <PopText t={0} x={960} y={900} text={years > 9e8 ? 'BILLIONS OF YEARS' : `YEAR ${years.toLocaleString('en-US')}`} size={64} c="#fff" rot={0} /> : null}
		</SpaceStage>
	);
};

/* 155-158: two suns + one planet = the three-body problem */
const S155: React.FC = () => {
	const {f, gf, at} = useShot();
	const chaos = f > at('158');
	const t = gf / 18;
	const p = (i: number): [number, number] => {
		if (!chaos) {
			const base: [number, number][] = [[560, 520], [1380, 540], [960, 700 + Math.sin(f / 6) * 20]];
			return base[i];
		}
		const k = i * 2.1;
		return [960 + Math.sin(t * (1 + i * 0.37) + k) * 420 + Math.sin(t * 2.3 + k) * 120, 540 + Math.cos(t * (0.8 + i * 0.29) + k) * 260];
	};
	const trail = (i: number) =>
		chaos
			? Array.from({length: 24})
					.map((_, j) => {
						const tt = (gf - j * 2) / 18;
						const k = i * 2.1;
						return `${960 + Math.sin(tt * (1 + i * 0.37) + k) * 420 + Math.sin(tt * 2.3 + k) * 120},${540 + Math.cos(tt * (0.8 + i * 0.29) + k) * 260}`;
					})
					.join(' ')
			: '';
	const cam = usePush(camOn(960, 560, 1.0), camOn(960, 540, 1.15));
	const cols = [WHITE_SUN, ORANGE_SUN, '#2f7fe6'];
	return (
		<>
			<SpaceStage cam={cam}>
				{[0, 1, 2].map((i) => (chaos ? <polyline key={i} points={trail(i)} stroke={cols[i]} strokeWidth={6} fill="none" opacity={0.5} /> : null))}
				{!chaos && f > at('155') + 20
					? [0, 1].map((i) => <line key={i} x1={p(i)[0]} y1={p(i)[1]} x2={p(2)[0]} y2={p(2)[1]} stroke={cols[i]} strokeWidth={6} strokeDasharray="10 10" strokeDashoffset={f * 2} />)
					: null}
				<Star x={p(0)[0]} y={p(0)[1]} r={70} c={WHITE_SUN} f={gf} id="w155" />
				<Star x={p(1)[0]} y={p(1)[1]} r={50} c={ORANGE_SUN} f={gf} id="o155" />
				<Planet x={p(2)[0]} y={p(2)[1]} r={36} f={gf} />
				<Pill t={f - at('156') - 6} x={960} y={140} text="SCIENTISTS HAVE A WORD…" c="#c8d0ff" out={at('157') - at('156') - 4} />
			</SpaceStage>
			<Punch t={f - at('157') + 2} text="THE THREE-BODY PROBLEM" top={100} size={92} out={9999} />
			<Flash f={f} at={at('157')} />
		</>
	);
};

/* 159-161: no simple formula; tiny changes, huge changes: chaos */
const S159: React.FC = () => {
	const {f, at} = useShot();
	const div = tw(f, at('160'), at('160') + 70, 0, 1);
	const pts = (d: number) =>
		Array.from({length: 60})
			.map((_, i) => {
				const u = i / 59;
				if (u > div) return null;
				const x = 300 + u * 1320;
				const y = 600 + Math.sin(u * 9) * 60 + d * Math.pow(u, 3) * 420 * Math.sin(u * 14);
				return `${x},${y}`;
			})
			.filter(Boolean)
			.join(' ');
	const glitch = f > at('161') ? (random('g' + Math.floor(f / 2)) - 0.5) * 20 : 0;
	return (
		<Board tint="#1a1640">
			{f < at('160') ? (
				<g>
					<text x={960} y={520} textAnchor="middle" fontSize={120} fontFamily={HAND} fontWeight={700} fill="#f4f1e6">
						where next = ???
					</text>
					<line x1={500} y1={480} x2={500 + 940 * tw(f, at('159') + 40, at('159') + 60, 0, 1)} y2={500} stroke="#ff2a3c" strokeWidth={14} strokeLinecap="round" />
					<PopText t={f - at('159') - 60} x={960} y={760} text="NO SIMPLE FORMULA" size={70} c="#ff5a6a" />
				</g>
			) : (
				<g transform={`translate(${glitch},0)`}>
					<polyline points={pts(1)} stroke="#5ad0ff" strokeWidth={8} fill="none" />
					<polyline points={pts(-1)} stroke="#ff8a2a" strokeWidth={8} fill="none" />
					<circle cx={300} cy={600} r={16} fill="#fff" />
					<Callout f={f} t0={at('160') + 4} t1={at('161')} from={[300, 600]} to={[480, 300]} text="TINY CHANGE NOW" c="#fff" />
					<PopText t={f - at('160') - 70} x={1500} y={220} text="HUGE CHANGE LATER" size={56} c="#ffd34a" />
					{f > at('161') ? (
						<>
							<text x={960 + glitch} y={960} textAnchor="middle" fontSize={140} fontFamily={FONT} fontWeight={900} fill="#ff2a3c" opacity={0.6}>
								CHAOS
							</text>
							<text x={960 - glitch} y={960} textAnchor="middle" fontSize={140} fontFamily={FONT} fontWeight={900} fill="#5ad0ff" opacity={0.6}>
								CHAOS
							</text>
						</>
					) : null}
				</g>
			)}
		</Board>
	);
};

/* 162-164: the second sun is already pulling — the orbit changes */
const S162: React.FC = () => {
	const {f, gf, at} = useShot();
	const shift = tw(f, at('162'), at('164') + 60, 0, 1);
	const a = gf / 20;
	const rx = 420 + 30 * shift;
	const ry = 170 + 14 * shift;
	const cx = 900 + 40 * shift;
	const cam = usePush(camOn(960, 540, 1.0), camOn(1150, 520, 1.3));
	return (
		<SpaceStage cam={cam}>
			<ellipse cx={900} cy={540} rx={420} ry={170} fill="none" stroke="#9ff0b0" strokeWidth={3} strokeDasharray="8 8" opacity={0.5} />
			<ellipse cx={cx} cy={540} rx={rx} ry={ry} fill="none" stroke="#ff8a2a" strokeWidth={4} />
			<Star x={900} y={540} r={60} c={WHITE_SUN} f={gf} id="w162" />
			<Star x={1700} y={300} r={60} c={ORANGE_SUN} f={gf} id="o162" />
			<Planet x={cx + Math.cos(a) * rx} y={540 + Math.sin(a) * ry} r={30} f={gf} />
			<line x1={1700} y1={300} x2={cx + Math.cos(a) * rx} y2={540 + Math.sin(a) * ry} stroke={ORANGE_SUN} strokeWidth={4} strokeDasharray="10 10" strokeDashoffset={-f * 2} opacity={0.6} />
			<Pill t={f - at('163') - 2} x={960} y={140} text="JUST A LITTLE" c="#ff8a2a" out={at('164') - at('163')} />
			<PopText t={f - at('164') - 6} x={960} y={150} text="ORBIT CHANGING" size={72} c="#ff8a2a" />
		</SpaceStage>
	);
};

/* 165-167: kilometres a day, measured so precisely… the star might drag Earth along */
const S165: React.FC = () => {
	const {f, gf, at} = useShot();
	const km = Math.floor(tw(f, at('165'), at('165') + 60, 0, 7));
	const drag = tw(f, at('167'), at('167') + 80, 0, 1);
	const cam = usePush(camOn(960, 540, 1.0), camOn(1000, 520, 1.15));
	return (
		<SpaceStage cam={cam}>
			{f < at('167') ? (
				<g>
					<Planet x={500} y={560} r={120} f={gf} />
					<g transform="translate(500,380)">
						<rect x={-40} y={-30} width={80} height={60} fill="#d8d8e0" />
						<path d="M-60,-30 Q0,-110 60,-30 Z" fill="#f4f4f4" stroke="#9aa0aa" strokeWidth={4} />
					</g>
					<Satellite x={1600} y={260} f={gf} s={0.6} />
					<path d={`M500,320 L1600,260`} stroke="#5ad0ff" strokeWidth={4} strokeDasharray="12 10" strokeDashoffset={-f * 3} />
					<Pill t={f - at('165') - 4} x={500} y={820} text={`+${km} KM / DAY`} c="#ffd34a" size={52} />
					<Pill t={f - at('166') - 4} x={1600} y={420} text="FAR SIDE OF THE SOLAR SYSTEM" c="#5ad0ff" size={34} />
				</g>
			) : (
				<g>
					<Star x={1200 + 600 * drag} y={500 - 100 * drag} r={70} c={ORANGE_SUN} f={gf} id="o165" />
					<path d={`M${1200 + 600 * drag},${500 - 100 * drag} Q${900 + 300 * drag},${700} ${700 + 80 * drag},${600 - 20 * drag}`} stroke="#c8a040" strokeWidth={8} fill="none" />
					<Planet x={700 + 80 * drag} y={600 - 20 * drag} r={60} f={gf} />
					<PopText t={f - at('167') - 30} x={900} y={200} text="A TINY BIT…" size={70} c="#ff8a2a" />
				</g>
			)}
		</SpaceStage>
	);
};

/* 168-173: thousands of simulations: most fine, some colder, some closer, a few lost */
const S168: React.FC = () => {
	const {f, gf, at} = useShot();
	const N = 24;
	const kind = (i: number) => (i === 17 ? 3 : i === 5 || i === 21 ? 2 : i % 5 === 1 ? 1 : 0);
	const reveal = [at('169'), at('170'), at('171'), at('173')];
	const cols = ['#4ab04a', '#5ad0ff', '#ff5a3a', '#000'];
	const lost = tw(f, at('173'), at('173') + 60, 0, 1);
	return (
		<Board tint="#101a30">
			<text x={960} y={110} textAnchor="middle" fontSize={54} fontFamily={FONT} fontWeight={900} fill="#fff">
				THOUSANDS OF SIMULATIONS
			</text>
			{Array.from({length: N}).map((_, i) => {
				const x = 230 + (i % 8) * 210;
				const y = 290 + Math.floor(i / 8) * 230;
				const pk = tw(f, at('168') + i * 2, at('168') + 10 + i * 2, 0, 1);
				const k = kind(i);
				const on2 = f > reveal[k];
				const a = gf / 12 + i;
				const r = k === 1 ? 74 : k === 2 ? 40 : 58;
				const ex = k === 3 && on2 ? lost * 900 : 0;
				return (
					<g key={i} transform={`translate(${x},${y}) scale(${pk})`}>
						<rect x={-95} y={-95} width={190} height={190} rx={14} fill={on2 ? cols[k] : '#1a2450'} opacity={on2 ? (k === 3 ? 0.9 : 0.35) : 1} stroke="#5a6aa0" strokeWidth={3} />
						<circle cx={0} cy={0} r={12} fill={WHITE_SUN} />
						<ellipse cx={0} cy={0} rx={r} ry={r * 0.6} fill="none" stroke="#fff" strokeWidth={2} opacity={0.4} />
						<circle cx={Math.cos(a) * r + ex} cy={Math.sin(a) * r * 0.6 - ex * 0.3} r={8} fill="#2f7fe6" />
						{on2 && k === 1 ? <text x={60} y={-60} fontSize={36} textAnchor="middle" fill="#fff">❄</text> : null}
						{on2 && k === 2 ? <text x={60} y={-56} fontSize={34} textAnchor="middle" fontFamily="Rubik" fontWeight={900} fill="#ffd34a">HOT</text> : null}
					</g>
				);
			})}
			<Pill t={f - at('169') - 10} x={480} y={1010} text="MOST: SAME ORBIT" c="#4ab04a" size={34} />
			<Pill t={f - at('170') - 10} x={1000} y={1010} text="SOME: COLDER" c="#5ad0ff" size={34} />
			<Pill t={f - at('171') - 10} x={1480} y={1010} text="A FEW: CLOSER" c="#ff5a3a" size={34} />
			{f > at('172') ? <PopText t={f - at('173') - 30} x={960} y={200} text="THROWN INTO THE DARK" size={64} c="#ff2a3c" /> : null}
			{f > at('173') + 40 ? <AbsoluteFill style={{background: '#000', opacity: tw(f, at('173') + 40, at('174'), 0, 0.5)}} /> : null}
		</Board>
	);
};

/* 174-177: nobody can tell — the world waits; countdown on every channel */
const S174: React.FC = () => {
	const {f, gf, at} = useShot();
	const left = Math.max(0, 120 * 24 * 60 - 1440 * 3 - f * 37);
	const d = Math.floor(left / 1440), h = Math.floor((left % 1440) / 60), m = left % 60;
	const cam = mixCam(camOn(960, 420, 1.0), camOn(960, 420, 1.35), tw(f, at('176'), at('176') + 30, 0, 1));
	return (
		<Stage cam={cam} bg="#0e1430" light={{x: 50, y: 10, o: 0.3}}>
			<Layer depth={1.2}>
				<Studio f={gf} red ticker="COUNTDOWN TO CLOSEST APPROACH">
					<text x={960} y={430} textAnchor="middle" fontSize={120} fontFamily={FONT} fontWeight={900} fill="#fff">
						{String(d).padStart(3, '0')}:{String(h).padStart(2, '0')}:{String(m).padStart(2, '0')}
					</text>
					<text x={960} y={520} textAnchor="middle" fontSize={36} fontFamily={FONT} fontWeight={700} fill="#ff9aa8" letterSpacing={8} opacity={tw(f, at('177'), at('177') + 10, 0, 1)}>
						DAYS     HOURS     MINUTES
					</text>
				</Studio>
			</Layer>
			<Layer depth={0.85}>
				<Svg>
					<CrowdRow n={9} x0={-100} x1={2020} floor={1180} s={1.1} mode="stand" seed="watch" />
				</Svg>
			</Layer>
			<Layer depth={1}>
				<Svg>
					<PopText t={f - at('174') - 10} x={960} y={110} text="NOBODY CAN TELL" size={60} c="#fff" out={at('175') - at('174')} />
					<PopText t={f - at('175') - 6} x={960} y={110} text="THE WORLD WAITS" size={66} c="#ffd34a" out={at('176') - at('175')} />
				</Svg>
			</Layer>
		</Stage>
	);
};

/* 178-180: Sam asks; you tell him the truth: dark, cold, colder */
const S178: React.FC = () => {
	const {f, gf, at} = useShot();
	const sp = beats(SEAT(f, 3), f, at, [['178', 4, 80, 'point']]);
	const hp = beats(SEAT(f, 1), f, at, [['179', 10, 60, 'presentF'], ['180', 0, 999, 'touchFace']]);
	const stage = f < at('180') ? 0 : f < at('180') + 40 ? 1 : f < at('180') + 80 ? 2 : 3;
	const cam = f < at('179') ? camOn(760, 600, 1.7) : f < at('180') ? camOn(560, 560, 1.7) : camOn(700, 480, 1.4);
	return (
		<Inside cam={cam} set={<Living f={gf} night />} light={{x: 60, y: 30, o: 0.4, c: '255,200,140'}}>
			<Hero x={560} seat={760} pose={hp} facing={1} look={[0.8, 0.2]} expr="sad" armOver={f > at('180')} uid="h178" />
			<Actor who="sam" x={780} seat={790} s={0.72} facing={-1} pose={sp} handF={on(f, at, '178', 4, 80) > 0.5 ? 'point' : undefined} look={[-0.8, -0.3]} expr="worried" uid="sam178" />
			<Bubble x={900} y={330} w={260} h={170} t={f - at('178') - 20} tail={[-90, 160]}>
				<Planet x={-40} y={0} r={40} f={gf} />
				<path d="M10,0 l80,-20" stroke="#222" strokeWidth={6} strokeDasharray="8 8" />
				<text x={90} y={30} fontSize={60} fontFamily={FONT} fontWeight={900} fill="#ff2a3c">
					?
				</text>
			</Bubble>
			{stage > 0 ? (
				<Bubble x={560} y={260} w={380} h={180} t={f - at('180') + 2} thought tail={[0, 170]} fill={['#fbf8ef', '#222a40', '#7ab0e0', '#c8f0ff'][stage]}>
					<text x={0} y={20} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill={stage === 1 ? '#fff' : '#14304a'}>
						{['', 'DARK', 'COLD', 'COLDER…'][stage]}
					</text>
					{stage === 3 ? [-140, -70, 0, 70, 140].map((x) => <path key={x} d={`M${x},-90 l10,30 l10,-30 Z`} fill="#fff" />) : null}
				</Bubble>
			) : null}
		</Inside>
	);
};

/* 181-185: he thinks… can he bring his basketball? Yes. He's fine. You are not. */
const S181: React.FC = () => {
	const {f, gf, at} = useShot();
	const sp = beats(SEAT(f, 3), f, at, [['181', 4, 80, 'rubChin'], ['182', 4, 70, 'carry'], ['184', 0, 999, 'cheer']]);
	const j = hops(f, at('184'), at('185'), 14, 30);
	const hp = beats(SEAT(f, 1), f, at, [['183', 0, 40, 'presentF']]);
	const nod = f > at('183') && f < at('183') + 30 ? Math.sin((f - at('183')) / 3) * 10 : 0;
	const cam =
		f < at('182') ? usePushX(camOn(780, 560, 2.1), f, at('181')) : f < at('183') ? camOn(780, 560, 1.8) : f < at('185') ? camOn(680, 540, 1.4) : camOn(560, 520, 2.2);
	return (
		<Inside cam={cam} set={<Living f={gf} night />} light={{x: 60, y: 30, o: 0.4, c: '255,200,140'}}>
			<Hero x={560} seat={760} pose={{...hp, head: hp.head + nod}} facing={1} look={[0.8, 0.2]} expr={f > at('185') ? 'worried' : 'normal'} mouth={f > at('185') ? 'frown' : undefined} uid="h181" />
			<Actor who="sam" x={780} seat={790 - j.lift} s={0.72} facing={-1} pose={sp} look={[-0.6, -0.4]} expr={f > at('184') ? 'normal' : 'worried'} mouth={f > at('184') ? 'smile' : undefined} uid="sam181" />
			{f > at('182') ? <Ball x={720} y={700 - j.lift} r={26} spin={f * 4} /> : null}
			<Bubble x={940} y={360} w={150} h={110} t={f - at('182') - 10} tail={[-70, 100]}>
				<Ball x={0} y={0} r={34} />
				<text x={50} y={-20} fontSize={40} fontFamily={FONT} fontWeight={900} fill="#222">
					?
				</text>
			</Bubble>
			<PopText t={f - at('183') - 2} x={560} y={330} text="YES" size={70} c="#9ff0b0" out={at('184') - at('183')} />
			{f > at('185') ? <circle cx={600} cy={headY() + 10 + ((f - at('185')) % 30) * 2} r={7} fill="#7ad0ff" /> : null}
			<PopText t={f - at('185') - 10} x={560} y={230} text="YOU ARE NOT." size={60} c="#ff5a6a" />
		</Inside>
	);
};
const usePushX = (c: ReturnType<typeof camOn>, f: number, t0: number) => ({...c, zoom: c.zoom + (f - t0) * 0.002});

/* 186: some people panic */
const S186: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(700, 560, 1.2), camOn(1200, 560, 1.3));
	return (
		<Outdoor id="s186" cam={cam} mode="orange" suns={[{x: 1450, y: 160, r: 62, c: WHITE_SUN}, {x: 600, y: 220, r: 70, c: ORANGE_SUN, glow: 1.6}]} yard={{hoop: false}}>
			<CrowdRow n={9} x0={-300} x1={1500} floor={FL + 10} s={0.95} mode="panic" seed="pan" t={f} />
			<PopText t={f - at('186') - 6} x={960} y={200} text="PANIC!" size={100} c="#ff5a6a" />
		</Outdoor>
	);
};

/* 187: some people build bunkers */
const S187: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 620, 1.4), camOn(960, 640, 1.7));
	const dig = (i: number): Pose => ({...idle(f, i), lean: 20 + Math.sin(f / 4 + i) * 12, armF: [80 + Math.sin(f / 4 + i) * 30, 30], armB: [70 + Math.sin(f / 4 + i) * 30, 34]});
	return (
		<Outdoor id="s187" cam={cam} mode="orange" suns={[{x: 1450, y: 160, r: 62, c: WHITE_SUN}, {x: 600, y: 220, r: 70, c: ORANGE_SUN, glow: 1.6}]} yard={false}>
			<rect x={-600} y={860} width={3120} height={400} fill="#6a7a30" />
			<path d="M760,900 q200,-120 400,0 Z" fill="#5a5a60" />
			<rect x={900} y={830} width={120} height={60} rx={8} fill="#3a3f4a" />
			<circle cx={960} cy={840} r={18} fill="none" stroke="#9aa0aa" strokeWidth={6} />
			{[680, 1240].map((x, i) => (
				<g key={x}>
					<Extra i={i + 30} x={x} floor={FL} s={1} seed="dig" pose={dig(i)} facing={i ? -1 : 1} />
					{Array.from({length: 4}).map((_, k) => {
						const u = ((f / 16 + k / 4 + i / 2) % 1);
						return <circle key={k} cx={x + (i ? -1 : 1) * (60 + u * 120)} cy={880 - Math.sin(u * Math.PI) * 120} r={10} fill="#6a4a2a" opacity={1 - u} />;
					})}
				</g>
			))}
			<Pill t={f - at('187') - 6} x={960} y={600} text="BUNKER" c="#9aa0aa" size={46} />
		</Outdoor>
	);
};

/* 188: some quit their jobs and go see the ocean one last time */
const S188: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const x = tw(f, 0, dur, -200, 1500);
	const tie = tw(f, at('188') + 4, at('188') + 30, 0, 1);
	const cam = camOn(Math.max(700, Math.min(1300, x)), 600, 1.3);
	return (
		<Outdoor id="s188" cam={cam} mode="orange" houses={false} yard={false} suns={[{x: 1400, y: 360, r: 70, c: ORANGE_SUN, glow: 1.6}]} mid={<Beach f={gf} mode="orange" />}>
			<SimpleCar x={x} y={960} c="#2f6fd8" />
			<Extra i={44} x={x + 10} floor={940} s={0.62} seed="quit" pose={{...idle(f, 2), armF: [140, 10]}} facing={1} />
			<g transform={`translate(${x - 80 - tie * 300},${700 - Math.sin(tie * Math.PI) * 200}) rotate(${tie * 400})`}>
				<path d="M0,0 l14,0 l-4,20 l14,60 l-20,20 l-20,-20 l14,-60 l-4,-20 Z" fill="#c8102e" />
			</g>
			<PopText t={f - at('188') - 10} x={x} y={500} text="I QUIT!" size={64} c="#fff" out={60} />
			<PopText t={f - at('188') - 80} x={1100} y={260} text="ONE LAST TIME" size={60} c="#ffd34a" />
		</Outdoor>
	);
};

/* 189: Nia's family moves to the mountains */
const S189: React.FC = () => {
	const {f, at, dur} = useShot();
	const x = tw(f, 30, dur, 800, 1800);
	const cam = usePush(camOn(900, 600, 1.3), camOn(1100, 600, 1.2));
	return (
		<Outdoor id="s189" cam={cam} mode="orange" houses={false} yard={false} suns={[{x: 400, y: 260, r: 60, c: WHITE_SUN}, {x: 1300, y: 300, r: 70, c: ORANGE_SUN, glow: 1.6}]} mid={<Road mode="orange" f={0} />}>
			<g transform={`translate(${x},880)`}>
				<rect x={-200} y={-260} width={300} height={240} rx={10} fill="#f2e6d0" />
				<rect x={100} y={-180} width={120} height={160} rx={16} fill="#9b5cf6" />
				<rect x={130} y={-160} width={70} height={60} fill="#bfe0ff" />
				<circle cx={-120} cy={-14} r={34} fill="#1a1a1e" />
				<circle cx={140} cy={-14} r={34} fill="#1a1a1e" />
				<text x={-50} y={-130} textAnchor="middle" fontSize={34} fontFamily={FONT} fontWeight={900} fill="#9b5cf6">
					MOVING
				</text>
			</g>
			<Actor who="nia" x={x + 165} seat={760} s={0.5} pose={gesture('wave', idle(f, 3), 1, f)} facing={-1} uid="nia189" />
			<Pill t={f - at('189') - 10} x={1300} y={160} text="→ THE MOUNTAINS" c="#9b5cf6" size={44} />
		</Outdoor>
	);
};

/* 190-192: one last turtle together; "if the world ends…" */
const S190: React.FC = () => {
	const {f, gf, at} = useShot();
	const wx = tw(f, 0, at('191'), 1200, 800);
	const walking = f < at('191');
	const base = (s: number) => (walking ? {...walk(f * 0.3 + s), armF: [62, 40] as [number, number], armB: [56, 46] as [number, number]} : idle(f, s));
	const rel = tw(f, at('191') - 30, at('191') + 30, 0, 1);
	const cam = f < at('191') ? camOn(wx + 60, 600, 1.4) : f < at('192') ? camOn(880, 540, 1.9) : camOn(880, 520, 2.2);
	return (
		<Outdoor id="s190" cam={cam} mode="orange" houses={false} yard={false} suns={[{x: 1500, y: 300, r: 60, c: WHITE_SUN}, {x: 500, y: 400, r: 60, c: ORANGE_SUN, glow: 1.6}]} mid={<Beach f={gf} mode="orange" />}>
			<Hero x={wx - 60} pose={base(1)} facing={-1} bob={walking ? Math.abs(Math.sin(f * 0.3)) * 4 : 0} look={[0.6, 0.3]} faceTurn={0.5} uid="h190" />
			<Actor who="nia" x={wx + 60} pose={beats(base(3), f, at, [['192', 0, 999, 'touchFace']])} facing={-1} bob={walking ? Math.abs(Math.sin(f * 0.3 + 3)) * 4 : 0} look={[-0.6, 0.2]} faceTurn={0.5} expr={f > at('191') ? 'sad' : 'normal'} mouth={f > at('192') + 20 ? 'smile' : undefined} uid="nia190" />
			<Turtle x={wx - 120 * rel - 30} y={FL - 150 + 140 * rel - Math.sin(rel * Math.PI) * 40} s={0.8} f={gf} dir={-1} />
			{rel > 0.9 ? <PopText t={f - at('191') - 30} x={600} y={720} text="BYE, LITTLE ONE" size={40} c="#fff" out={60} /> : null}
		</Outdoor>
	);
};

/* 193-195: "turtles aren't normal" — she laughs; you don't say you're scared */
const S193: React.FC = () => {
	const {f, gf, at} = useShot();
	const laugh = env(f, at('194'), at('195') - 4, 6, 8);
	const np: Pose = {...idle(f, 3), lean: -14 * laugh + Math.sin(f / 2) * 4 * laugh, head: -18 * laugh};
	const hp = beats(idle(f, 1), f, at, [['193', 4, 60, 'shrug']]);
	const cam = f < at('195') ? camOn(880, 540, 1.7) : camOn(800, 520, 2.3);
	return (
		<Outdoor id="s193" cam={cam} mode="orange" houses={false} yard={false} suns={[{x: 1500, y: 300, r: 60, c: WHITE_SUN}, {x: 500, y: 400, r: 60, c: ORANGE_SUN, glow: 1.6}]} mid={<Beach f={gf} mode="orange" />}>
			<Hero x={780} pose={hp} facing={1} look={[0.6, 0]} expr={f > at('195') ? 'worried' : 'normal'} mouth={f > at('193') + 50 && f < at('195') ? 'smirk' : undefined} uid="h193" />
			<Actor who="nia" x={980} pose={np} facing={-1} look={[-0.6, -0.2]} mouth={laugh > 0.3 ? 'open' : 'smile'} expr={laugh > 0.3 ? 'sleepy' : 'normal'} uid="nia193" />
			{laugh > 0.3 ? <PopText t={f - at('194') - 4} x={1100} y={340} text="HA HA!" size={60} c="#ff9ab8" /> : null}
			<Bubble x={780} y={270} w={220} h={100} t={f - at('195') - 20} thought tail={[0, 110]}>
				<text x={0} y={14} textAnchor="middle" fontSize={34} fontFamily={HAND} fontWeight={700} fill="#222">
					(scared…)
				</text>
			</Bubble>
		</Outdoor>
	);
};

/* 196-198: everyone gets gentle; dad cooks every night, whatever time it is */
const S196: React.FC = () => {
	const {f, at} = useShot();
	const flip = Math.max(0, Math.sin(f / 9));
	const dp = {...idle(f, 4), armF: [70 + flip * 30, 40] as [number, number]};
	const cam = usePush(camOn(960, 560, 1.15), camOn(1000, 560, 1.55));
	return (
		<Inside cam={cam} set={<Kitchen />} light={{x: 60, y: 20, o: 0.5, c: '255,200,140'}}>
			<rect x={1040} y={660} width={360} height={230} fill="#9aa0aa" />
			<rect x={1040} y={650} width={360} height={20} fill="#2a2a32" />
			<Actor who="dad" x={960} s={1.05} pose={dp} facing={1} look={[0.6, 0.4]} mouth="smile" uid="dad196" />
			<g transform={`translate(1110,${640 - flip * 20})`}>
				<ellipse cx={0} cy={0} rx={60} ry={14} fill="#2a2a32" />
				<line x1={-60} y1={0} x2={-130} y2={10} stroke="#2a2a32" strokeWidth={10} />
				<ellipse cx={0} cy={-10 - flip * 60} rx={36} ry={10} fill="#ffd38a" />
			</g>
			{Array.from({length: 4}).map((_, i) => (
				<path key={i} d={`M${1080 + i * 20},${600 - ((f * 2 + i * 20) % 120)} q10,-15 0,-30`} stroke="#fff" strokeWidth={4} fill="none" opacity={0.4} />
			))}
			<g transform="translate(560,300)">
				<circle r={70} fill="#fff" stroke="#2a2a2a" strokeWidth={8} />
				<text y={20} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill="#c8102e">
					?
				</text>
			</g>
			<PopText t={f - at('196') - 10} x={960} y={180} text="STRANGELY GENTLE" size={56} c="#ff9ab8" out={at('197') - at('196') + 10} />
			<Pill t={f - at('198') - 6} x={560} y={430} text="DINNER TIME?" c="#ffd34a" />
		</Inside>
	);
};

/* 199: mom asleep on the couch with Sam on her lap */
const S199: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(600, 600, 1.35), camOn(600, 640, 1.7));
	return (
		<Inside cam={cam} set={<Living f={gf} night />} light={{x: 60, y: 30, o: 0.45, c: '255,190,130'}}>
			<Actor who="mom" x={520} seat={740} s={1} pose={{...SEAT(f, 2), head: 22, armF: [60, 70]}} expr="sleepy" uid="mom199" />
			<g transform="translate(650,700) rotate(-70)">
				<Actor who="sam" x={0} seat={0} s={0.7} pose={{...idle(f, 4), legB: [10, 10], legF: [14, 12]}} expr="sleepy" shadow={false} uid="sam199" />
			</g>
			<Zzz2 f={f} />
			<Pill t={f - at('199') - 30} x={560} y={330} text="DOUBLE SHIFT • OVER" c="#3fbfb0" />
		</Inside>
	);
};
const Zzz2: React.FC<{f: number}> = ({f}) => (
	<g>
		{[0, 1, 2].map((i) => {
			const u = (f / 40 + i / 3) % 1;
			return (
				<text key={i} x={560 + u * 60} y={470 - u * 120} fontSize={30 + i * 8} fontFamily={FONT} fontWeight={900} fill="#fff" opacity={Math.sin(u * Math.PI)}>
					Z
				</text>
			);
		})}
	</g>
);

/* 200-204: grandpa teaches the names of stars from a book. "When", not "if". */
const S200: React.FC = () => {
	const {f, gf, at} = useShot();
	const names: [string, number, number, string][] = [['VEGA', 0, 0, '#bfe0ff'], ['SIRIUS', 26, 1, '#ffffff'], ['BETELGEUSE', 56, 2, '#ff6a4a']];
	const cam = f < at('202') ? camOn(500, 600, 1.6) : f < at('203') ? camOn(760, 420, 1.2) : f < at('204') ? camOn(400, 560, 1.9) : camOn(600, 520, 1.3);
	const gp = beats(SEAT(f, 7), f, at, [['200', 0, 999, 'carry'], ['203', 10, 60, 'point']]);
	return (
		<Inside cam={cam} set={<Living f={gf} night glow="#ffb070" />} light={{x: 40, y: 30, o: 0.5, c: '255,190,130'}}>
			<Actor who="grandpa" x={400} seat={760} s={1} pose={gp} facing={1} look={[0.6, 0.6]} faceTurn={0.4} handF={on(f, at, '203', 10, 60) > 0.5 ? 'point' : undefined} uid="gp200" />
			<Hero x={640} seat={760} pose={SEAT(f, 1)} facing={-1} look={[-0.6, 0.6]} faceTurn={0.4} badge={false} uid="h200" />
			<g transform="translate(520,640) rotate(-6)">
				<rect x={-90} y={-60} width={180} height={110} rx={6} fill="#1a2350" stroke="#c8a040" strokeWidth={5} />
				<line x1={0} y1={-60} x2={0} y2={50} stroke="#c8a040" strokeWidth={4} />
				{[[-50, -20], [-30, 10], [40, -30], [50, 20]].map(([x, y], i) => (
					<circle key={i} cx={x} cy={y} r={4} fill="#fff" />
				))}
			</g>
			<Pill t={f - at('201') - 10} x={520} y={340} text="NO REAL STARS TO SHOW" c="#aab3d6" size={34} out={at('202') - at('201')} />
			{names.map(([n, off, i, c]) => {
				const t = f - at('202') - off;
				const x = 560 + i * 380;
				const y = 230 + (i % 2) * 90;
				return t > 0 ? (
					<g key={n}>
						<circle cx={x} cy={y} r={14 + 2 * Math.sin(f / 4 + i)} fill={c} />
						<circle cx={x} cy={y} r={40} fill={c} opacity={0.2} />
						<PopText t={t} x={x} y={y + 80} text={n} size={46} c={c} rot={0} />
					</g>
				) : null;
			})}
			{f > at('204') ? (
				<g>
					<PopText t={f - at('204') - 10} x={760} y={300} text="WHEN" size={110} c="#9ff0b0" rot={-4} />
					<g opacity={tw(f, at('204') + 30, at('204') + 40, 0, 1)}>
						<text x={1120} y={330} textAnchor="middle" fontSize={90} fontFamily={FONT} fontWeight={900} fill="#aab3d6">
							IF
						</text>
						<line x1={1060} y1={300} x2={1180} y2={300} stroke="#ff2a3c" strokeWidth={12} />
					</g>
				</g>
			) : null}
		</Inside>
	);
};

export const SHOTS3: ShotDef[] = [
	{at: '144', C: S144, whip: true},
	{at: '149', C: S149, whip: true},
	{at: '151', C: S151, whip: true},
	{at: '153', C: S153},
	{at: '155', C: S155},
	{at: '159', C: S159, whip: true},
	{at: '162', C: S162, whip: true},
	{at: '165', C: S165},
	{at: '168', C: S168, whip: true},
	{at: '174', C: S174, whip: true},
	{at: '178', C: S178, whip: true},
	{at: '181', C: S181},
	{at: '186', C: S186, whip: true},
	{at: '187', C: S187},
	{at: '188', C: S188, whip: true},
	{at: '189', C: S189, whip: true},
	{at: '190', C: S190, whip: true},
	{at: '193', C: S193},
	{at: '196', C: S196, whip: true},
	{at: '199', C: S199, whip: true},
	{at: '200', C: S200},
];
export {Burst, QMark, Chair, Callout};
