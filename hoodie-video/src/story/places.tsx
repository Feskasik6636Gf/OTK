import React from 'react';
import {random} from 'remotion';
import {Svg} from '../engine/camera';
import {darken, lighten} from '../engine/color';
import {Rain} from '../reference/PauseTime';
import {Rays} from '../kit/kit';

/* Locations of "Lion vs 100 Men vs Max": jungle (day / dusk / night / storm / dawn), savannah,
   river, flood, sky. Each location = far sky+canopy, mid trunks, ground, front leaves. */

export type Mood = 'day' | 'dusk' | 'night' | 'storm' | 'dawn';
type Pal = {sky: [string, string, string]; far: string; far2: string; trunk: string; leaf: string; leaf2: string; ground: string; ground2: string; fog: string; hl: string};
export const PAL: Record<Mood, Pal> = {
	day: {sky: ['#7fd0b4', '#cdeeb4', '#f6f2b6'], far: '#58a872', far2: '#3f8c5c', trunk: '#5a432d', leaf: '#2d7a44', leaf2: '#44a257', ground: '#68843c', ground2: '#46602b', fog: '#eaf7d4', hl: '#fff2b0'},
	dusk: {sky: ['#3b2a63', '#c4577a', '#ffb468'], far: '#41406a', far2: '#2e2d52', trunk: '#2a2030', leaf: '#27355a', leaf2: '#3a4670', ground: '#4a4a46', ground2: '#2f2f38', fog: '#ff9e72', hl: '#ffd08a'},
	night: {sky: ['#040813', '#0a1630', '#13264a'], far: '#10303a', far2: '#0a2028', trunk: '#101a1c', leaf: '#0b3a36', leaf2: '#12534a', ground: '#16301f', ground2: '#0c1c14', fog: '#2a4a6a', hl: '#cfe2ff'},
	storm: {sky: ['#151c26', '#273241', '#415062'], far: '#22403f', far2: '#18302f', trunk: '#1c1a18', leaf: '#1b4a3d', leaf2: '#27604f', ground: '#3b4a2c', ground2: '#242e1b', fog: '#7a8a96', hl: '#9fb4c8'},
	dawn: {sky: ['#5c9fc4', '#f2c6a2', '#ffe9b4'], far: '#4f9a78', far2: '#3a8264', trunk: '#4a3a2c', leaf: '#2a7447', leaf2: '#3f9a5a', ground: '#617f3d', ground2: '#42592b', fog: '#ffe2c0', hl: '#fff0c8'},
};

export const Sky: React.FC<{mood: Mood; f: number}> = ({mood, f}) => {
	const p = PAL[mood];
	return (
		<Svg>
			<defs>
				<linearGradient id={'sk' + mood} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={p.sky[0]} />
					<stop offset="0.55" stopColor={p.sky[1]} />
					<stop offset="1" stopColor={p.sky[2]} />
				</linearGradient>
				<radialGradient id={'sg' + mood}>
					<stop offset="0" stopColor={p.hl} stopOpacity="0.95" />
					<stop offset="1" stopColor={p.hl} stopOpacity="0" />
				</radialGradient>
			</defs>
			<rect x={-700} y={-600} width={3400} height={1900} fill={`url(#sk${mood})`} />
			{mood === 'day' || mood === 'dawn' ? (
				<>
					<circle cx={1450} cy={mood === 'dawn' ? 330 : 190} r={330} fill={`url(#sg${mood})`} />
					<circle cx={1450} cy={mood === 'dawn' ? 330 : 190} r={78} fill={p.hl} />
				</>
			) : null}
			{mood === 'dusk' ? (
				<>
					<circle cx={1180} cy={560} r={380} fill={`url(#sg${mood})`} />
					<circle cx={1180} cy={560} r={92} fill="#ffe2a0" />
				</>
			) : null}
			{mood === 'night' ? (
				<>
					{Array.from({length: 70}).map((_, i) => (
						<circle key={i} cx={-200 + random('st' + i) * 2400} cy={-100 + random('sy' + i) * 560} r={1 + random('sr' + i) * 2.2} fill="#fff" opacity={0.35 + 0.5 * Math.abs(Math.sin(f / 30 + i))} />
					))}
					<circle cx={420} cy={170} r={230} fill={`url(#sg${mood})`} opacity={0.5} />
					<circle cx={420} cy={170} r={64} fill="#f2f6ff" />
					<circle cx={444} cy={156} r={58} fill={p.sky[1]} opacity={0.45} />
				</>
			) : null}
			{mood === 'storm'
				? Array.from({length: 7}).map((_, i) => <ellipse key={i} cx={-100 + i * 330 + Math.sin(f / 90 + i) * 40} cy={80 + (i % 3) * 70} rx={320} ry={90} fill="#0d131b" opacity={0.55} />)
				: null}
		</Svg>
	);
};

/* a row of tree trunks with round canopies — the far jungle */
const TreeRow: React.FC<{f: number; mood: Mood; row: number; base: number; seed: string; n?: number; k?: number}> = ({f, mood, row, base, seed, n = 14, k = 1}) => {
	const p = PAL[mood];
	const col = row === 0 ? p.far2 : p.far;
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const r = (s: string) => random(seed + row + s + i);
				const x = -300 + (i * 2700) / n + (r('x') - 0.5) * 140;
				const top = base - (200 + r('h') * 260) * k;
				const w = (150 + r('w') * 110) * k;
				const sw = Math.sin(f / 70 + i * 1.7 + row) * 5;
				return (
					<g key={i}>
						<rect x={x - 12 * k} y={top} width={24 * k} height={base - top + 60} fill={darken(col, 0.35)} />
						<ellipse cx={x + sw} cy={top} rx={w} ry={w * 0.62} fill={col} />
						<ellipse cx={x - w * 0.55 + sw} cy={top + w * 0.3} rx={w * 0.7} ry={w * 0.45} fill={darken(col, 0.08)} />
						<ellipse cx={x + w * 0.6 + sw} cy={top + w * 0.25} rx={w * 0.68} ry={w * 0.42} fill={lighten(col, 0.06)} />
					</g>
				);
			})}
		</g>
	);
};

export const JungleFar: React.FC<{f: number; mood: Mood; seed?: string}> = ({f, mood, seed = 'a'}) => {
	const p = PAL[mood];
	return (
		<>
			<Sky mood={mood} f={f} />
			<Svg>
				<TreeRow f={f} mood={mood} row={0} base={760} seed={seed} n={12} k={0.8} />
				<defs>
					<linearGradient id={'fog' + mood} x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor={p.fog} stopOpacity="0" />
						<stop offset="1" stopColor={p.fog} stopOpacity={mood === 'night' ? 0.35 : 0.55} />
					</linearGradient>
				</defs>
				<rect x={-700} y={420} width={3400} height={520} fill={`url(#fog${mood})`} />
				<TreeRow f={f} mood={mood} row={1} base={850} seed={seed + 'b'} n={10} k={1.1} />
				<rect x={-700} y={700} width={3400} height={300} fill={`url(#fog${mood})`} opacity={0.5} />
			</Svg>
		</>
	);
};

/* big trunks with vines close to the camera */
export const JungleMid: React.FC<{f: number; mood: Mood; seed?: string; n?: number}> = ({f, mood, seed = 'm', n = 6}) => {
	const p = PAL[mood];
	return (
		<Svg>
			{Array.from({length: n}).map((_, i) => {
				const r = (s: string) => random(seed + s + i);
				const x = -150 + (i * 2300) / n + (r('x') - 0.5) * 200;
				const w = 54 + r('w') * 70;
				return (
					<g key={i}>
						<rect x={x - w / 2} y={-200} width={w} height={1200} fill={p.trunk} />
						<rect x={x - w / 2} y={-200} width={w * 0.28} height={1200} fill={lighten(p.trunk, 0.12)} opacity={0.6} />
						<rect x={x + w * 0.2} y={-200} width={w * 0.16} height={1200} fill={darken(p.trunk, 0.3)} opacity={0.5} />
						<path d={`M${x + w * 0.5},${20 + r('v') * 120} q${30 * Math.sin(f / 40 + i)},${150} ${10 * Math.cos(f / 33 + i)},${300 + r('l') * 200}`} stroke={darken(p.leaf, 0.1)} strokeWidth={9} fill="none" strokeLinecap="round" />
						<ellipse cx={x} cy={0} rx={w * 2.8} ry={160} fill={p.leaf} opacity={0.9} />
					</g>
				);
			})}
		</Svg>
	);
};

const Fern: React.FC<{x: number; y: number; s: number; col: string; f: number; i: number}> = ({x, y, s, col, f, i}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		{[-60, -35, -10, 15, 40, 62].map((a, j) => (
			<path key={j} d={`M0,0 Q${a * 1.2 + Math.sin(f / 25 + i + j) * 5},${-70 - (j % 2) * 24} ${a * 2.2},${-30 + Math.abs(a) * 0.6}`} stroke={col} strokeWidth={14} fill="none" strokeLinecap="round" />
		))}
	</g>
);

export const GroundLayer: React.FC<{f: number; mood: Mood; y?: number; seed?: string}> = ({f, mood, y = 900, seed = 'g'}) => {
	const p = PAL[mood];
	return (
		<Svg>
			<defs>
				<linearGradient id={'gr' + mood} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={p.ground} />
					<stop offset="0.25" stopColor={p.ground2} />
					<stop offset="1" stopColor={darken(p.ground2, 0.35)} />
				</linearGradient>
			</defs>
			<rect x={-800} y={y - 14} width={3500} height={900} fill={`url(#gr${mood})`} />
			<rect x={-800} y={y - 16} width={3500} height={8} fill={lighten(p.ground, 0.2)} opacity={0.6} />
			{Array.from({length: 18}).map((_, i) => (
				<Fern key={i} x={-300 + i * 150 + random(seed + i) * 80} y={y + 4 + random(seed + 'y' + i) * 20} s={0.45 + random(seed + 's' + i) * 0.4} col={i % 2 ? p.leaf : p.leaf2} f={f} i={i} />
			))}
		</Svg>
	);
};

/* big dark leaves in the corners, drifting: the blurred foreground */
export const Front: React.FC<{f: number; mood: Mood}> = ({f, mood}) => {
	const p = PAL[mood];
	const col = darken(p.leaf, 0.35);
	const leaf = (x: number, y: number, rot: number, s: number, i: number) => (
		<g key={i} transform={`translate(${x},${y}) rotate(${rot + Math.sin(f / 50 + i) * 4}) scale(${s})`}>
			<path d="M0,0 C80,-120 260,-120 400,0 C260,60 80,60 0,0 Z" fill={col} />
			<path d="M0,0 L380,-4" stroke={darken(col, 0.3)} strokeWidth={5} />
		</g>
	);
	return (
		<Svg>
			{leaf(-120, 1040, -40, 1.5, 0)}
			{leaf(-80, 980, -70, 1.2, 1)}
			{leaf(2040, 1060, 220, 1.6, 2)}
			{leaf(1990, 220, 130, 1.1, 3)}
			{leaf(-90, 120, 20, 1.2, 4)}
		</Svg>
	);
};

/* -------------------------------- savannah -------------------------------- */
const Acacia: React.FC<{x: number; y: number; s: number; col: string}> = ({x, y, s, col}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<path d="M-8,0 C-6,-90 -4,-150 -30,-210 M-8,-120 C30,-170 60,-180 90,-230" stroke={col} strokeWidth={14} fill="none" strokeLinecap="round" />
		<ellipse cx={-10} cy={-230} rx={190} ry={44} fill={col} />
		<ellipse cx={90} cy={-250} rx={110} ry={30} fill={col} />
	</g>
);
export const SavannaFar: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<defs>
			<linearGradient id="savsk" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor="#f2a23a" />
				<stop offset="0.6" stopColor="#ffd27a" />
				<stop offset="1" stopColor="#fff0c0" />
			</linearGradient>
			<radialGradient id="savsun">
				<stop offset="0" stopColor="#fff6cc" />
				<stop offset="1" stopColor="#fff6cc" stopOpacity="0" />
			</radialGradient>
		</defs>
		<rect x={-700} y={-600} width={3400} height={1700} fill="url(#savsk)" />
		<circle cx={1250} cy={500} r={420} fill="url(#savsun)" />
		<circle cx={1250} cy={500} r={110} fill="#fff1b8" />
		<path d="M-700,820 C-200,700 300,780 700,740 C1200,690 1700,780 2700,720 L2700,1100 L-700,1100 Z" fill="#c98a3a" />
		<Acacia x={300} y={790} s={0.8} col="#5a3a1c" />
		<Acacia x={1650} y={770} s={0.65} col="#5a3a1c" />
		<Acacia x={980} y={760} s={0.4} col="#6a4a24" />
		{Array.from({length: 6}).map((_, i) => (
			<ellipse key={i} cx={-100 + ((i * 420 + f * (0.2 + i * 0.03)) % 2400)} cy={140 + (i % 3) * 70} rx={170} ry={34} fill="#fff6dc" opacity={0.55} />
		))}
	</Svg>
);
export const SavannaGround: React.FC<{y?: number}> = ({y = 900}) => (
	<Svg>
		<defs>
			<linearGradient id="savgr" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor="#d9a24c" />
				<stop offset="1" stopColor="#8a5a22" />
			</linearGradient>
		</defs>
		<rect x={-800} y={y - 20} width={3500} height={900} fill="url(#savgr)" />
		{Array.from({length: 60}).map((_, i) => (
			<path key={i} d={`M${-400 + i * 50},${y + 6 + (i % 5) * 18} l6,-40 l6,40`} fill="#a87a30" />
		))}
	</Svg>
);

/* ---------------------------------- water --------------------------------- */
export const Water: React.FC<{f: number; y0: number; y1: number; flood?: boolean; o?: number}> = ({f, y0, y1, flood, o = 1}) => {
	const top = flood ? '#9a7248' : '#2f8fb0';
	const bot = flood ? '#5a3e24' : '#175a78';
	const sp = flood ? 9 : 2.2;
	const id = 'wt' + (flood ? 'f' : 'n');
	return (
		<Svg>
			<defs>
				<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={top} />
					<stop offset="1" stopColor={bot} />
				</linearGradient>
			</defs>
			<g opacity={o}>
				<rect x={-800} y={y0} width={3500} height={y1 - y0} fill={`url(#${id})`} />
				{Array.from({length: flood ? 34 : 22}).map((_, i) => {
					const yy = y0 + 10 + (i % 7) * ((y1 - y0 - 20) / 7);
					const xx = ((i * 211 + f * sp * (0.6 + (i % 4) * 0.25)) % 2800) - 400;
					return <path key={i} d={`M${xx},${yy} q30,${flood ? -16 : -8} 60,0 t60,0 t60,0`} stroke={flood ? '#e2c7a0' : '#bfe8f6'} strokeWidth={flood ? 6 : 4} fill="none" opacity={flood ? 0.7 : 0.45} strokeLinecap="round" />;
				})}
				{flood
					? Array.from({length: 5}).map((_, i) => {
							const lx = ((i * 700 + f * 11) % 3000) - 500;
							return <rect key={'d' + i} x={lx} y={y0 + 30 + (i % 3) * 50} width={170 + i * 20} height={22} rx={10} fill="#3a2614" transform={`rotate(${Math.sin(f / 15 + i) * 6} ${lx} ${y0 + 40})`} />;
					  })
					: null}
			</g>
		</Svg>
	);
};

/* ---------------------------------- fire ---------------------------------- */
export const Fire: React.FC<{x: number; y: number; s?: number; f: number; big?: number}> = ({x, y, s = 1, f, big = 1}) => {
	const fl = (i: number) => 1 + 0.16 * Math.sin(f / 2.6 + i * 2) + 0.1 * Math.sin(f / 1.3 + i * 5);
	return (
		<g transform={`translate(${x},${y}) scale(${s * big})`}>
			<defs>
				<radialGradient id="fireglow">
					<stop offset="0" stopColor="#ffb040" stopOpacity="0.7" />
					<stop offset="1" stopColor="#ff7a20" stopOpacity="0" />
				</radialGradient>
			</defs>
			<circle cx={0} cy={-50} r={240 * fl(0)} fill="url(#fireglow)" style={{mixBlendMode: 'screen'}} />
			<rect x={-70} y={-14} width={140} height={24} rx={11} fill="#4a2a14" transform="rotate(8)" />
			<rect x={-70} y={-14} width={140} height={24} rx={11} fill="#5a3418" transform="rotate(-10)" />
			<path d={`M-48,-6 C-62,-60 -20,-80 -26,${-130 * fl(1)} C10,-90 8,-60 20,-100 C60,-70 50,-30 46,-6 Z`} fill="#ff6a1a" />
			<path d={`M-30,-6 C-40,-44 -8,-60 -10,${-100 * fl(2)} C14,-66 12,-40 24,-70 C42,-44 34,-20 30,-6 Z`} fill="#ffb02e" />
			<path d={`M-14,-6 C-18,-28 -2,-36 0,${-60 * fl(3)} C10,-36 16,-24 14,-6 Z`} fill="#fff0a0" />
			{[0, 1, 2, 3, 4].map((i) => {
				const t = ((f * 1.4 + i * 17) % 70) / 70;
				return <circle key={i} cx={Math.sin(i * 3 + t * 6) * 26} cy={-90 - t * 160} r={3.2 * (1 - t)} fill="#ffd27a" opacity={1 - t} />;
			})}
		</g>
	);
};

/* ------------------------------ whole locations ---------------------------- */
export type Loc = {
	bg: string;
	far: (f: number) => React.ReactNode;
	mid: (f: number) => React.ReactNode;
	ground: (f: number) => React.ReactNode;
	front: (f: number) => React.ReactNode;
	light?: {x?: number; y?: number; c?: string; o?: number; night?: boolean} | false;
	dust?: string;
};
const jungle = (mood: Mood, seed: string, o: {rays?: boolean; river?: 'n' | 'f' | null; rain?: boolean} = {}): Loc => ({
	bg: PAL[mood].sky[1],
	far: (f) => <JungleFar f={f} mood={mood} seed={seed} />,
	mid: (f) => (
		<>
			{o.river ? <Water f={f} y0={760} y1={1100} flood={o.river === 'f'} /> : null}
			<JungleMid f={f} mood={mood} seed={seed + 'm'} n={o.river ? 4 : 6} />
			{o.rays ? <Rays x={500} y={-60} w={420} angle={26} c="#fff6c8" o={0.2} /> : null}
		</>
	),
	ground: (f) =>
		o.river ? (
			<Svg>
				<defs>
					<linearGradient id={'bank' + mood} x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor={PAL[mood].ground} />
						<stop offset="1" stopColor={darken(PAL[mood].ground2, 0.3)} />
					</linearGradient>
				</defs>
				<rect x={-800} y={900} width={3500} height={900} fill={`url(#bank${mood})`} />
				<rect x={-800} y={896} width={3500} height={10} fill="#d6c08a" opacity={0.7} />
			</Svg>
		) : (
			<GroundLayer f={f} mood={mood} seed={seed} />
		),
	front: (f) => (
		<>
			<Front f={f} mood={mood} />
			{o.rain ? <Rain wt={f} seed={'rn' + seed} n={150} len={64} w={2.6} speed={46} color="#cfe4ff" opacity={0.55} /> : null}
		</>
	),
	light: mood === 'night' || mood === 'storm' ? {night: true, o: 0.35} : mood === 'dusk' ? {c: '255,170,120', o: 0.4, x: 70, y: 40} : {x: 75, y: 8, o: 0.34},
	dust: mood === 'night' ? '#d6ff9a' : mood === 'day' ? '#fff3b0' : undefined,
});

const none = () => null;
export const LOCS = {
	jd: jungle('day', 'jd', {rays: true}),
	jd2: jungle('day', 'jx', {rays: true}),
	jdusk: jungle('dusk', 'ju'),
	jn: jungle('night', 'jn'),
	jn2: jungle('night', 'jq'),
	js: jungle('storm', 'js', {rain: true}),
	jdawn: jungle('dawn', 'jw', {rays: true}),
	riv: jungle('day', 'rv', {river: 'n', rays: true}),
	rivdusk: jungle('dusk', 'rd', {river: 'n'}),
	rivflood: jungle('storm', 'rf', {river: 'f', rain: true}),
	rivdawn: jungle('dawn', 'rw', {river: 'n'}),
	sav: {
		bg: '#f2c46a',
		far: (f: number) => <SavannaFar f={f} />,
		mid: none,
		ground: () => <SavannaGround />,
		front: none,
		light: {x: 70, y: 20, c: '255,210,150', o: 0.4},
		dust: '#ffe9b0',
	} as Loc,
	// dark red studio from the character art: for titles, numbers and the scoreboard
	studio: {
		bg: '#3a0a14',
		far: () => (
			<Svg>
				<defs>
					<radialGradient id="redstudio" cx="0.5" cy="0.42" r="0.75">
						<stop offset="0" stopColor="#8a0f24" />
						<stop offset="0.6" stopColor="#4a0814" />
						<stop offset="1" stopColor="#14030a" />
					</radialGradient>
				</defs>
				<rect x={-800} y={-600} width={3500} height={2200} fill="url(#redstudio)" />
			</Svg>
		),
		mid: none,
		ground: none,
		front: none,
		light: false,
		dust: '#ff6a7a',
	} as Loc,
	sky: {
		bg: '#8fd0e8',
		far: (f: number) => (
			<Svg>
				<defs>
					<linearGradient id="airsk" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#4f9fd8" />
						<stop offset="1" stopColor="#d6efff" />
					</linearGradient>
				</defs>
				<rect x={-800} y={-600} width={3500} height={2200} fill="url(#airsk)" />
				{Array.from({length: 7}).map((_, i) => {
					const base = i * 420 - f * (2 + i * 0.6);
					return <ellipse key={i} cx={(((base + 300) % 2600) + 2600) % 2600 - 300} cy={120 + (i % 4) * 150} rx={170 + (i % 3) * 40} ry={40} fill="#fff" opacity={0.7} />;
				})}
			</Svg>
		),
		mid: none,
		ground: none,
		front: none,
		light: {x: 60, y: 5, o: 0.3},
	} as Loc,
	canopy: {
		bg: '#2f8a52',
		far: (f: number) => (
			<Svg>
				<defs>
					<linearGradient id="airsk2" x1="0" y1="0" x2="0" y2="1">
						<stop offset="0" stopColor="#5ab0e0" />
						<stop offset="0.5" stopColor="#cdeaf5" />
					</linearGradient>
				</defs>
				<rect x={-800} y={-600} width={3500} height={2200} fill="url(#airsk2)" />
				{[0, 1, 2].map((r) =>
					Array.from({length: 20}).map((_, i) => {
						const x = -300 + i * 140 + (r % 2) * 70 + random('cn' + r + i) * 40;
						const y = 640 + r * 120 + random('cy' + r + i) * 50;
						return <ellipse key={r + '-' + i} cx={x} cy={y + Math.sin(f / 40 + i) * 3} rx={110} ry={90} fill={['#3f9a5a', '#2f8650', '#256f43'][r]} />;
					}),
				)}
			</Svg>
		),
		mid: none,
		ground: none,
		front: none,
		light: {x: 60, y: 5, o: 0.3},
	} as Loc,
};
export type LocKey = keyof typeof LOCS;
