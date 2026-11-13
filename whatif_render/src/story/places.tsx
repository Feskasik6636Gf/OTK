import React from 'react';
import {random} from 'remotion';
import {Svg} from '../engine/camera';
import {darken, lighten} from '../engine/color';
import {FONT, HAND} from '../kit/ui';

/* Locations made for this video. World 1920x1080, floor at y=900.
   Each: wall gradient, floor, 2–3 big objects, one light, one living detail. */

const G: React.FC<{id: string; a: string; b: string}> = ({id, a, b}) => (
	<defs>
		<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
			<stop offset="0" stopColor={a} />
			<stop offset="1" stopColor={b} />
		</linearGradient>
	</defs>
);
const Wall: React.FC<{id: string; a: string; b: string}> = ({id, a, b}) => (
	<>
		<G id={id} a={a} b={b} />
		<rect x={-500} y={-400} width={2900} height={1500} fill={`url(#${id})`} />
	</>
);
const Floor: React.FC<{c: string; y?: number; lines?: 'plank' | 'tile' | 'none'}> = ({c, y = 900, lines = 'plank'}) => (
	<g>
		<rect x={-500} y={y} width={2900} height={700} fill={c} />
		<rect x={-500} y={y} width={2900} height={10} fill={darken(c, 0.25)} />
		{lines === 'plank' ? Array.from({length: 8}).map((_, i) => <line key={i} x1={-500} y1={y + 22 + i * i * 9} x2={2400} y2={y + 22 + i * i * 9} stroke={darken(c, 0.12)} strokeWidth={2} />) : null}
		{lines === 'tile' ? Array.from({length: 34}).map((_, i) => <line key={i} x1={-500 + i * 100} y1={y} x2={-500 + i * 100 - 300} y2={y + 700} stroke={darken(c, 0.1)} strokeWidth={2} />) : null}
	</g>
);
const Window: React.FC<{x: number; y: number; w: number; h: number; sky: [string, string]; id: string; frame?: string; f?: number; night?: boolean}> = ({x, y, w, h, sky, id, frame = '#f4f1e8', f = 0, night}) => (
	<g>
		<G id={id} a={sky[0]} b={sky[1]} />
		<rect x={x - 14} y={y - 14} width={w + 28} height={h + 28} rx={6} fill={frame} />
		<rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} />
		{night
			? Array.from({length: 12}).map((_, i) => <circle key={i} cx={x + random(id + i) * w} cy={y + random(id + 'y' + i) * h * 0.6} r={1.6} fill="#fff" opacity={0.7} />)
			: [0, 1].map((i) => <ellipse key={i} cx={x + ((i * 0.5 + 0.2 + f * 0.0006) % 1) * w} cy={y + 40 + i * 50} rx={60} ry={16} fill="#fff" opacity={0.75} />)}
		<rect x={x + w / 2 - 5} y={y} width={10} height={h} fill={frame} />
		<rect x={x} y={y + h / 2 - 5} width={w} height={10} fill={frame} />
		<polygon points={`${x + 20},${y + h} ${x + 70},${y + h} ${x + w * 0.6},${y} ${x + w * 0.6 - 50},${y}`} fill="#fff" opacity={0.14} />
	</g>
);

/* --------------------------- principal's office --------------------------- */
export const Office: React.FC<{f: number; laugh?: number}> = ({f, laugh = 0}) => (
	<Svg>
		<Wall id="of-w" a="#3d5a7a" b="#2c4560" />
		<rect x={-500} y={600} width={2900} height={300} fill="#5b3f2e" />
		<rect x={-500} y={592} width={2900} height={12} fill="#7a5a40" />
		{/* bookshelf */}
		<rect x={80} y={150} width={420} height={450} fill="#5a3d28" />
		{[0, 1, 2].map((r) => (
			<g key={r}>
				<rect x={95} y={175 + r * 140} width={390} height={10} fill="#3e2a1c" />
				{Array.from({length: 12}).map((_, i) => (
					<rect key={i} x={100 + i * 31} y={190 + r * 140 + (i % 3) * 6} width={26} height={110 - (i % 3) * 6} fill={['#a33a3a', '#2f5e9c', '#c9a14a', '#3a7a5a', '#6a4a8a'][(i + r) % 5]} />
				))}
			</g>
		))}
		<Window x={1340} y={170} w={420} h={330} sky={['#8fc6ec', '#d9eefa']} id="of-win" f={f} frame="#d9cdb5" />
		{/* diploma + flag */}
		<rect x={760} y={170} width={260} height={190} fill="#c9a14a" />
		<rect x={775} y={185} width={230} height={160} fill="#f8f1dc" />
		<text x={890} y={240} textAnchor="middle" fontSize={22} fontFamily={HAND} fill="#5a4a2a">
			DIPLOMA
		</text>
		<text x={890} y={290} textAnchor="middle" fontSize={20} fontFamily={HAND} fill="#5a4a2a">
			R. Grayson
		</text>
		<line x1={1150} y1={130} x2={1150} y2={600} stroke="#c9a14a" strokeWidth={8} />
		<path d={`M1154,140 q60,${14 + Math.sin(f / 12) * 6} 120,0 v110 q-60,${-14 + Math.sin(f / 12 + 1) * 6} -120,0 z`} fill="#c62a3a" />
		{/* jar «23 years without a laugh» */}
		<g transform="translate(600,520)">
			<rect x={-40} y={-80} width={80} height={80} rx={12} fill="#cfe9f5" opacity={0.85} />
			<rect x={-34} y={-30} width={68} height={28} fill="#7cc46a" />
			<text x={0} y={-44} textAnchor="middle" fontSize={16} fontFamily={FONT} fill="#1d3a5a">
				$800
			</text>
		</g>
		<Floor c="#6a4a35" />
		{laugh > 0 ? <rect x={-500} y={-400} width={2900} height={1500} fill="#ffd34a" opacity={0.06 * laugh} /> : null}
	</Svg>
);
/* the principal's desk, drawn in front of whoever sits behind it */
export const BigDesk: React.FC<{x?: number}> = ({x = 1100}) => (
	<Svg>
		<rect x={x - 330} y={760} width={660} height={26} rx={6} fill="#7a4a2a" />
		<rect x={x - 310} y={786} width={620} height={114} fill="#5a3520" />
		<rect x={x - 290} y={800} width={250} height={84} rx={6} fill="#6a4028" />
		<rect x={x + 40} y={800} width={250} height={84} rx={6} fill="#6a4028" />
		<rect x={x - 230} y={712} width={150} height={48} rx={4} fill="#2b2f3a" />
		<rect x={x + 120} y={730} width={120} height={30} rx={3} fill="#f2efe6" />
		<rect x={x + 60} y={700} width={40} height={60} rx={6} fill="#c9a14a" />
		<text x={x} y={860} textAnchor="middle" fontSize={26} fontFamily={FONT} fill="#e8c88a">
			PRINCIPAL
		</text>
	</Svg>
);

/* -------------------------------- classroom -------------------------------- */
export const Classroom: React.FC<{f: number; board?: string; science?: boolean}> = ({f, board = 'History', science}) => (
	<Svg>
		<Wall id="cl-w" a={science ? '#bfe0d4' : '#e9dcb4'} b={science ? '#a6cfc0' : '#dccb98'} />
		<rect x={-500} y={640} width={2900} height={260} fill={science ? '#8fbfae' : '#c9b37e'} />
		<rect x={280} y={130} width={1000} height={420} rx={6} fill="#6b4a2c" />
		<rect x={296} y={146} width={968} height={388} fill="#2f4a3a" />
		<text x={780} y={260} textAnchor="middle" fontSize={70} fontFamily={HAND} fill="#f6f2e4">
			{board}
		</text>
		{science ? (
			<g stroke="#f6f2e4" strokeWidth={4} fill="none" opacity={0.85}>
				<circle cx={600} cy={400} r={50} />
				<ellipse cx={600} cy={400} rx={110} ry={30} />
				<path d="M900,450 l60,-120 l60,120 z" />
			</g>
		) : (
			<text x={780} y={400} textAnchor="middle" fontSize={56} fontFamily={HAND} fill="#f6f2e4">
				1939 — 1945 ?
			</text>
		)}
		<Window x={1460} y={170} w={360} h={330} sky={['#9fd2f0', '#e6f4fb']} id="cl-win" f={f} />
		<g transform="translate(1600,90)">
			<circle r={42} fill="#fff" stroke="#333" strokeWidth={6} />
			<line x1={0} y1={0} x2={0} y2={-28} stroke="#222" strokeWidth={5} transform={`rotate(${f * 0.5})`} />
			<line x1={0} y1={0} x2={18} y2={0} stroke="#222" strokeWidth={5} />
		</g>
		{science ? (
			<g>
				<rect x={60} y={420} width={160} height={180} rx={8} fill="#e8f3f0" />
				{[0, 1, 2].map((i) => (
					<rect key={i} x={80 + i * 46} y={500 - i * 20} width={30} height={100 + i * 20} rx={10} fill={['#7cf04a', '#3fc1c9', '#ff6a9a'][i]} opacity={0.8} />
				))}
			</g>
		) : null}
		<Floor c={science ? '#9aa8a2' : '#b88e66'} />
	</Svg>
);
/* a row of school desks in front (depth ~1) */
export const SchoolDesks: React.FC<{xs: number[]; y?: number; c?: string}> = ({xs, y = 760, c = '#c99a62'}) => (
	<Svg>
		{xs.map((x, i) => (
			<g key={i}>
				<rect x={x - 120} y={y} width={240} height={20} rx={4} fill={c} />
				<rect x={x - 110} y={y + 20} width={14} height={900 - y - 20} fill="#3a3a44" />
				<rect x={x + 96} y={y + 20} width={14} height={900 - y - 20} fill="#3a3a44" />
				<rect x={x - 60} y={y - 10} width={80} height={12} rx={2} fill="#f6f2e8" transform={`rotate(-4 ${x} ${y})`} />
			</g>
		))}
	</Svg>
);

/* -------------------------------- cafeteria -------------------------------- */
export const Cafeteria: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="cf-w" a="#f7d9a8" b="#efc283" />
		{Array.from({length: 26}).map((_, c) => (
			<rect key={c} x={-400 + c * 110} y={560} width={106} height={340} fill={c % 2 ? '#e86a4a' : '#f2a14a'} opacity={0.35} />
		))}
		{/* serving counter */}
		<rect x={1150} y={430} width={800} height={60} fill="#c9cfdd" />
		<rect x={1150} y={490} width={800} height={410} fill="#9aa3b5" />
		{[0, 1, 2, 3].map((i) => (
			<g key={i}>
				<rect x={1180 + i * 190} y={404} width={160} height={30} rx={6} fill="#e8ecf2" />
				<ellipse cx={1260 + i * 190} cy={404} rx={60} ry={10} fill={['#d9a04a', '#7cc46a', '#e86a4a', '#f2e6c8'][i]} />
				{[0, 1, 2].map((k) => (
					<path key={k} d={`M${1240 + i * 190 + k * 20},390 q-10,-20 0,-40 q10,-20 0,-40`} stroke="#fff" strokeWidth={4} fill="none" opacity={0.35 + 0.25 * Math.sin(f / 9 + i + k)} />
				))}
			</g>
		))}
		<rect x={1260} y={150} width={560} height={110} rx={10} fill="#3a2a40" />
		<text x={1540} y={222} textAnchor="middle" fontSize={50} fontFamily={FONT} fill="#ffd34a">
			CAFETERIA
		</text>
		<Window x={120} y={160} w={300} h={260} sky={['#9fd2f0', '#e6f4fb']} id="cf-win" f={f} />
		<Window x={560} y={160} w={300} h={260} sky={['#9fd2f0', '#e6f4fb']} id="cf-win2" f={f} />
		<Floor c="#d8c49c" lines="tile" />
	</Svg>
);
/* long lunch table drawn in front of seated kids */
export const LunchTable: React.FC<{x0?: number; x1?: number; y?: number; trays?: number[]}> = ({x0 = 200, x1 = 1700, y = 760, trays = []}) => (
	<Svg>
		<rect x={x0} y={y} width={x1 - x0} height={22} rx={6} fill="#3d7ab8" />
		<rect x={x0 + 30} y={y + 22} width={x1 - x0 - 60} height={18} fill="#2c5a8a" />
		{[x0 + 60, x1 - 80].map((x) => (
			<rect key={x} x={x} y={y + 40} width={18} height={900 - y - 40} fill="#2b2f3a" />
		))}
		{trays.map((x, i) => (
			<g key={i}>
				<rect x={x - 60} y={y - 12} width={120} height={14} rx={4} fill="#f2a14a" />
				<ellipse cx={x - 20} cy={y - 16} rx={22} ry={8} fill="#a8643a" />
				<ellipse cx={x + 26} cy={y - 16} rx={16} ry={7} fill="#7cc46a" />
			</g>
		))}
	</Svg>
);

/* ----------------------------------- lab ----------------------------------- */
export const Lab: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="lb-w" a="#cfe8ef" b="#b4d6e2" />
		<rect x={-500} y={560} width={2900} height={340} fill="#9cc6d3" />
		{[0, 1, 2].map((r) => (
			<rect key={r} x={200} y={190 + r * 120} width={600} height={10} fill="#7aa8b8" />
		))}
		{Array.from({length: 18}).map((_, i) => (
			<rect key={i} x={210 + (i % 6) * 98} y={130 + Math.floor(i / 6) * 120} width={30} height={58} rx={10} fill={['#7cf04a', '#3fc1c9', '#ff6a9a', '#ffd34a'][i % 4]} opacity={0.75} />
		))}
		{/* rat cage */}
		<g transform="translate(1250,430)">
			<rect x={-260} y={0} width={520} height={240} rx={10} fill="#e8f3f6" opacity={0.5} />
			{Array.from({length: 14}).map((_, i) => (
				<line key={i} x1={-260 + i * 40} y1={0} x2={-260 + i * 40} y2={240} stroke="#8aa3ad" strokeWidth={3} />
			))}
			<rect x={-280} y={240} width={560} height={30} rx={6} fill="#5a6a78" />
		</g>
		<rect x={-500} y={700} width={2900} height={24} fill="#e9eef2" />
		<rect x={-500} y={724} width={2900} height={180} fill="#5a6a78" />
		<g transform="translate(1600,640)">
			<rect x={-40} y={-10} width={80} height={70} rx={8} fill="#2b2f3a" />
			<rect x={-30} y={-50} width={14} height={50} fill="#9aa3b5" />
			<circle cx={-23} cy={-60} r={18} fill="#cfd6df" />
		</g>
		<Floor c="#8a9aa6" lines="tile" />
	</Svg>
);
/* a lab rat (world space). laugh 0..1 = squeaks */
export const Rat: React.FC<{x: number; y: number; s?: number; f: number; laugh?: number; flip?: boolean}> = ({x, y, s = 1, f, laugh = 0, flip}) => {
	const hop = laugh > 0 ? Math.abs(Math.sin(f / 3)) * 10 * laugh : 0;
	return (
		<g transform={`translate(${x},${y - hop}) scale(${(flip ? -1 : 1) * s},${s})`}>
			<path d="M-60,0 q-50,-6 -80,20" stroke="#d9a0a8" strokeWidth={6} fill="none" strokeLinecap="round" />
			<ellipse cx={0} cy={-26} rx={64} ry={34} fill="#f2f0ee" />
			<ellipse cx={58} cy={-36} rx={32} ry={24} fill="#f2f0ee" />
			<circle cx={50} cy={-62} r={14} fill="#f6c6cc" />
			<circle cx={70} cy={-40} r={5} fill="#111" />
			<circle cx={90} cy={-34} r={5} fill="#f08a9a" />
			{laugh > 0 ? <path d="M70,-24 q10,8 20,0" stroke="#111" strokeWidth={3} fill="none" /> : null}
			<rect x={-40} y={0} width={10} height={10} rx={4} fill="#f6c6cc" />
			<rect x={30} y={0} width={10} height={10} rx={4} fill="#f6c6cc" />
		</g>
	);
};

/* ------------------------------- road (police) ------------------------------ */
export const Road: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="rd-sky" a="#7cc0ec" b="#ddf0fb" />
		{[0, 1, 2].map((i) => (
			<ellipse key={i} cx={((i * 700 + f * 0.4) % 2600) - 300} cy={120 + i * 40} rx={150} ry={36} fill="#fff" opacity={0.85} />
		))}
		{Array.from({length: 9}).map((_, i) => (
			<g key={i}>
				<rect x={-300 + i * 300} y={430 - (i % 3) * 30} width={200} height={300} fill={['#e8d4b0', '#c9dbe8', '#f2c4a0'][i % 3]} />
				<path d={`M${-320 + i * 300},${430 - (i % 3) * 30} l120,-80 l120,80 z`} fill={['#a84a3a', '#5a6a8a', '#8a5a3a'][i % 3]} />
			</g>
		))}
		{Array.from({length: 14}).map((_, i) => (
			<g key={i}>
				<rect x={-280 + i * 200} y={640} width={14} height={80} fill="#6b4a2a" />
				<circle cx={-273 + i * 200} cy={620} r={50} fill={i % 2 ? '#4aa04a' : '#5ab85a'} />
			</g>
		))}
		<rect x={-500} y={720} width={2900} height={500} fill="#4a4f5c" />
		{Array.from({length: 20}).map((_, i) => (
			<rect key={i} x={-400 + i * 180} y={880} width={100} height={12} fill="#f2e6a0" />
		))}
		<rect x={-500} y={712} width={2900} height={12} fill="#a9aeb8" />
	</Svg>
);
export const CarSide: React.FC<{x: number; y?: number; c?: string; police?: boolean; f: number; s?: number; open?: number}> = ({x, y = 900, c = '#3d6fd6', police, f, s = 1, open = 0}) => {
	const red = Math.floor(f / 6) % 2 === 0;
	return (
		<g transform={`translate(${x},${y}) scale(${s})`}>
			<ellipse cx={0} cy={6} rx={300} ry={20} fill="#000" opacity={0.25} />
			<path d="M-290,-40 L-290,-130 Q-280,-150 -230,-155 L-150,-160 L-90,-240 L120,-240 L200,-160 L270,-150 Q295,-140 295,-110 L295,-40 Z" fill={police ? '#f4f6fa' : c} />
			{police ? <rect x={-290} y={-120} width={585} height={40} fill="#2b3a7a" /> : null}
			{police ? <text x={0} y={-90} textAnchor="middle" fontSize={30} fontFamily={FONT} fill="#fff">POLICE</text> : null}
			<path d="M-70,-226 L110,-226 L172,-162 L-120,-162 Z" fill="#bfe3ff" />
			<line x1={30} y1={-226} x2={30} y2={-162} stroke={police ? '#f4f6fa' : c} strokeWidth={10} />
			{open > 0 ? <rect x={-60} y={-200} width={90} height={36} fill="#000" opacity={0.25 * open} /> : null}
			{[-180, 180].map((wx) => (
				<g key={wx}>
					<circle cx={wx} cy={-30} r={50} fill="#1b1e2a" />
					<circle cx={wx} cy={-30} r={22} fill="#9aa3b5" />
				</g>
			))}
			{police ? (
				<g>
					<rect x={-40} y={-262} width={36} height={22} rx={5} fill={red ? '#ff3a3a' : '#7a2020'} />
					<rect x={4} y={-262} width={36} height={22} rx={5} fill={red ? '#20307a' : '#3a7aff'} />
					<circle cx={red ? -22 : 22} cy={-252} r={120} fill={red ? '#ff3a3a' : '#3a7aff'} opacity={0.16} />
				</g>
			) : null}
			<rect x={270} y={-120} width={22} height={16} rx={4} fill="#ffe08a" />
		</g>
	);
};

/* -------------------------- talent show / big stage ------------------------- */
export const BigStage: React.FC<{f: number; title?: string; smoke?: number; alarm?: number}> = ({f, title = 'SCHOOL TALENT SHOW', smoke = 0, alarm = 0}) => (
	<Svg>
		<Wall id="bs-w" a="#20163a" b="#3a1f4a" />
		{Array.from({length: 10}).map((_, i) => (
			<path key={i} d={`M${-300 + i * 120},-100 q24,520 0,1000 h120 q-24,-500 0,-1000 z`} fill={i % 2 ? '#8a1f2e' : '#a32a3a'} />
		))}
		{Array.from({length: 10}).map((_, i) => (
			<path key={'r' + i} d={`M${1100 + i * 120},-100 q24,520 0,1000 h120 q-24,-500 0,-1000 z`} fill={i % 2 ? '#8a1f2e' : '#a32a3a'} />
		))}
		<rect x={700} y={-100} width={520} height={1000} fill="#2a1430" />
		<rect x={-500} y={-120} width={2900} height={150} fill="#7a1a28" />
		<rect x={560} y={70} width={800} height={86} rx={12} fill="#141026" stroke="#ffd34a" strokeWidth={4} />
		<text x={960} y={128} textAnchor="middle" fontSize={40} fontFamily={FONT} fill="#ffd34a">
			{title}
		</text>
		{Array.from({length: 18}).map((_, i) => (
			<circle key={i} cx={580 + i * 45} cy={172} r={7} fill={['#ff4f8b', '#ffd34a', '#3fe0e8'][i % 3]} opacity={0.5 + 0.5 * Math.sin(f / 5 + i)} />
		))}
		{/* spotlights */}
		{[0, 1].map((i) => (
			<polygon key={i} points={`${700 + i * 520},-100 ${740 + i * 520},-100 ${1060 - i * 200},900 ${760 - i * 200},900`} fill="#fff6d0" opacity={0.07 + 0.03 * Math.sin(f / 20 + i)} />
		))}
		{alarm > 0 ? <rect x={-500} y={-400} width={2900} height={1500} fill="#ff2a2a" opacity={alarm * (Math.floor(f / 8) % 2 ? 0.12 : 0.02)} /> : null}
		{smoke > 0 ? (
			<g opacity={smoke}>
				{Array.from({length: 10}).map((_, i) => (
					<ellipse key={i} cx={1500 + Math.sin(f / 30 + i) * 80 - i * 40} cy={300 + (i % 4) * 90 - f * 0.1} rx={260} ry={110} fill="#6a6a78" opacity={0.5} style={{filter: 'blur(20px)'}} />
				))}
			</g>
		) : null}
		<rect x={-500} y={780} width={2900} height={20} fill="#6a4a5a" />
		<Floor c="#4a3048" y={790} />
	</Svg>
);
/* audience heads in the dark foreground (draw on a near layer) */
export const Audience: React.FC<{f: number; laugh?: number; n?: number; y?: number; seed?: string; stand?: number}> = ({f, laugh = 0, n = 16, y = 1010, seed = 'au', stand = 0}) => (
	<Svg>
		{Array.from({length: n}).map((_, i) => {
			const r = random(seed + i);
			const x = -200 + (i + 0.5) * (2300 / n) + (r - 0.5) * 50;
			const b = laugh > 0 ? Math.abs(Math.sin(f / (3 + r * 2) + i)) * 14 * laugh : 0;
			const yy = y - stand * 120 - b + (i % 2) * 30;
			return (
				<g key={i}>
					<rect x={x - 70} y={yy + 30} width={140} height={200} rx={40} fill={['#3a2a50', '#2a3050', '#4a2a3a'][i % 3]} />
					<circle cx={x} cy={yy} r={52} fill="#0b0b10" />
					{laugh > 0.3 ? <path d={`M${x - 14},${yy + 14} q14,${14} 28,0`} stroke="#fff" strokeWidth={4} fill="none" /> : null}
				</g>
			);
		})}
	</Svg>
);

/* ------------------------------- comedy club ------------------------------- */
export const Club: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="cb-w" a="#5a2a24" b="#3a1a18" />
		{Array.from({length: 22}).map((_, r) =>
			Array.from({length: 20}).map((__, c) => (
				<rect key={`${r}${c}`} x={-400 + c * 150 + (r % 2) * 75} y={-200 + r * 50} width={144} height={44} fill="#7a3a2e" opacity={0.55} />
			)),
		)}
		<g opacity={0.85 + 0.15 * Math.sin(f / 3)}>
			<text x={960} y={260} textAnchor="middle" fontSize={120} fontFamily={HAND} fontWeight={700} fill="#ff6ab0" style={{filter: 'drop-shadow(0 0 18px #ff2a8a)'}}>
				Comedy
			</text>
			<text x={960} y={360} textAnchor="middle" fontSize={70} fontFamily={FONT} fill="#7ff0ff" style={{filter: 'drop-shadow(0 0 14px #2ad0ff)'}}>
				COMEDY CLUB
			</text>
		</g>
		<ellipse cx={960} cy={900} rx={520} ry={60} fill="#fff6d0" opacity={0.18} />
		<polygon points="900,-100 1020,-100 1400,900 520,900" fill="#fff6d0" opacity={0.08} />
		{/* mic stand */}
		<line x1={1240} y1={900} x2={1240} y2={640} stroke="#2b2b30" strokeWidth={8} />
		<ellipse cx={1240} cy={900} rx={50} ry={10} fill="#2b2b30" />
		<rect x={-500} y={820} width={2900} height={80} fill="#2a1a1a" />
		<Floor c="#2a1a1a" y={900} />
	</Svg>
);

/* -------------------------------- TV studio -------------------------------- */
export const Studio: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="st-w" a="#141a3a" b="#22285a" />
		{Array.from({length: 40}).map((_, i) => (
			<rect key={i} x={-300 + (i % 10) * 260} y={60 + Math.floor(i / 10) * 70} width={220} height={40} rx={6} fill="#ffd34a" opacity={(random('stw' + i) > 0.4 ? 0.7 : 0.2) * (0.6 + 0.4 * Math.sin(f / 10 + i))} />
		))}
		{/* city skyline backdrop */}
		{Array.from({length: 14}).map((_, i) => (
			<rect key={i} x={-200 + i * 170} y={420 - (random('sk' + i) * 200)} width={150} height={500} fill="#2c3570" />
		))}
		<rect x={-500} y={620} width={2900} height={20} fill="#ff4f8b" opacity={0.7} />
		<rect x={1360} y={360} width={420} height={70} rx={10} fill="#ff4f8b" />
		<text x={1570} y={410} textAnchor="middle" fontSize={34} fontFamily={FONT} fill="#fff">
			LATE NIGHT SHOW
		</text>
		{/* host desk */}
		<rect x={1250} y={700} width={520} height={200} rx={20} fill="#3a2a6a" />
		<rect x={1250} y={690} width={520} height={20} rx={8} fill="#5a4a9a" />
		<rect x={1460} y={630} width={40} height={60} rx={8} fill="#f2efe6" />
		{/* couch */}
		<rect x={300} y={740} width={760} height={160} rx={30} fill="#3fa0a8" />
		<rect x={300} y={640} width={760} height={120} rx={40} fill="#4ab4bc" />
		<Floor c="#1a1d3a" lines="none" />
	</Svg>
);

/* ------------------------------ grandpa's room ----------------------------- */
export const LivingRoom: React.FC<{f: number; dim?: boolean}> = ({f, dim}) => (
	<Svg>
		<Wall id={dim ? 'lv-wd' : 'lv-w'} a={dim ? '#5a5a6a' : '#d9c6a0'} b={dim ? '#4a4a58' : '#c9b48a'} />
		{Array.from({length: 30}).map((_, i) => (
			<line key={i} x1={-400 + i * 100} y1={-300} x2={-400 + i * 100} y2={900} stroke={dim ? '#555566' : '#c2ad80'} strokeWidth={14} opacity={0.5} />
		))}
		<Window x={760} y={160} w={400} h={340} sky={dim ? ['#6a7a90', '#9aa8b8'] : ['#ffb27a', '#ffe1a8']} id={dim ? 'lv-wn' : 'lv-wi'} f={f} />
		{/* photo of grandma */}
		<g transform="translate(400,300) rotate(-3)">
			<rect x={-80} y={-100} width={160} height={200} fill="#8a6a44" />
			<rect x={-66} y={-86} width={132} height={172} fill="#efe2c4" />
			<circle cx={0} cy={-20} r={30} fill="#000" />
			<path d="M-30,-40 q30,-30 60,0" fill="#ddd" />
			<rect x={-30} y={14} width={60} height={70} rx={14} fill="#c46a8a" />
		</g>
		{/* TV */}
		<rect x={1400} y={520} width={300} height={200} rx={14} fill="#2b2f3a" />
		<rect x={1416} y={536} width={268} height={168} fill={dim ? '#1a2030' : '#7ab0d0'} opacity={0.9 + 0.1 * Math.sin(f / 3)} />
		<rect x={1380} y={720} width={340} height={180} fill="#7a5a3a" />
		<Floor c={dim ? '#5a4a40' : '#9a6a44'} />
	</Svg>
);
export const Armchair: React.FC<{x: number; c?: string; front?: boolean}> = ({x, c = '#8a3a3a', front}) => (
	<Svg>
		{front ? (
			<g>
				<rect x={x - 150} y={720} width={300} height={70} rx={20} fill={c} />
				<rect x={x - 180} y={680} width={60} height={220} rx={26} fill={darken(c, 0.12)} />
				<rect x={x + 120} y={680} width={60} height={220} rx={26} fill={darken(c, 0.12)} />
			</g>
		) : (
			<g>
				<rect x={x - 160} y={520} width={320} height={300} rx={50} fill={darken(c, 0.15)} />
				<rect x={x - 150} y={790} width={300} height={110} rx={10} fill={darken(c, 0.25)} />
			</g>
		)}
	</Svg>
);

/* --------------------------------- hospital -------------------------------- */
export const Hospital: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="hs-w" a="#d6f0ec" b="#bfe2dc" />
		<rect x={-500} y={620} width={2900} height={280} fill="#9fd4cc" />
		<Window x={820} y={160} w={360} h={300} sky={['#9fd2f0', '#e6f4fb']} id="hs-win" f={f} />
		{/* drawings on the wall */}
		{[[300, 250, '#ffd34a'], [1400, 230, '#ff8ab0'], [1620, 300, '#7cc46a']].map(([x, y, c], i) => (
			<g key={i} transform={`rotate(${(i - 1) * 4} ${x} ${y})`}>
				<rect x={(x as number) - 80} y={(y as number) - 60} width={160} height={120} fill="#fff" />
				<circle cx={x as number} cy={y as number} r={34} fill={c as string} />
				<path d={`M${(x as number) - 14},${(y as number) + 4} q14,14 28,0`} stroke="#333" strokeWidth={4} fill="none" />
			</g>
		))}
		{/* beds */}
		{[300, 1500].map((x, i) => (
			<g key={i}>
				<rect x={x - 220} y={700} width={440} height={60} rx={14} fill="#f4f6fa" />
				<rect x={x - 220} y={600} width={24} height={300} fill="#9aa3b5" />
				<rect x={x + 196} y={650} width={24} height={250} fill="#9aa3b5" />
				<rect x={x - 200} y={690} width={400} height={30} rx={10} fill="#7fc0e8" />
			</g>
		))}
		{/* drip stand */}
		<line x1={600} y1={360} x2={600} y2={900} stroke="#9aa3b5" strokeWidth={6} />
		<rect x={570} y={360} width={60} height={90} rx={14} fill="#e6f6ff" stroke="#9aa3b5" strokeWidth={3} />
		<Floor c="#cfe0dc" lines="tile" />
	</Svg>
);

/* ------------------------------ house front door --------------------------- */
export const Porch: React.FC<{f: number; c?: string; door?: string; dusk?: boolean; open?: number; doorX?: number}> = ({f, c = '#e8c49a', door = '#3d6fd6', dusk, open = 0, doorX = 1300}) => (
	<Svg>
		<Wall id={dusk ? 'pc-sd' : 'pc-s'} a={dusk ? '#f08a5a' : '#8fc6ec'} b={dusk ? '#ffd08a' : '#dff0fb'} />
		<rect x={600} y={60} width={1600} height={840} fill={c} />
		{Array.from({length: 18}).map((_, i) => (
			<line key={i} x1={600} y1={80 + i * 46} x2={2200} y2={80 + i * 46} stroke={darken(c, 0.12)} strokeWidth={3} />
		))}
		<path d="M520,80 L1400,-120 L2300,80 Z" fill="#8a3a2e" />
		<Window x={760} y={260} w={240} h={220} sky={dusk ? ['#ffcf80', '#ffe8b0'] : ['#bfe3ff', '#eaf6ff']} id={dusk ? 'pc-wd' : 'pc-w'} f={f} />
		<Window x={1600} y={260} w={240} h={220} sky={dusk ? ['#ffcf80', '#ffe8b0'] : ['#bfe3ff', '#eaf6ff']} id={dusk ? 'pc-wd2' : 'pc-w2'} f={f} />
		{/* door */}
		<rect x={doorX - 120} y={420} width={240} height={480} fill="#2a2030" />
		<g transform={`translate(${doorX - 120},420) scale(${1 - 0.75 * open},1)`}>
			<rect x={0} y={0} width={240} height={480} fill={door} />
			<rect x={30} y={40} width={180} height={160} rx={6} fill={darken(door, 0.15)} />
			<rect x={30} y={250} width={180} height={190} rx={6} fill={darken(door, 0.15)} />
			<circle cx={210} cy={250} r={12} fill="#ffd34a" />
		</g>
		<rect x={doorX - 150} y={890} width={300} height={20} fill="#8a7a6a" />
		{/* bushes + path */}
		{[-200, 140, 420].map((x, i) => (
			<g key={i}>
				<circle cx={x} cy={840} r={90} fill="#3d8f3d" />
				<circle cx={x + 80} cy={860} r={70} fill="#4aa04a" />
			</g>
		))}
		<line x1={-500} y1={700} x2={560} y2={700} stroke="#f4f1e8" strokeWidth={10} />
		{Array.from({length: 12}).map((_, i) => (
			<rect key={i} x={-480 + i * 90} y={690} width={10} height={210} fill="#f4f1e8" />
		))}
		<Floor c="#7cb85a" lines="none" />
		<rect x={doorX - 200} y={900} width={400} height={300} fill="#c9b9a0" />
	</Svg>
);

/* ------------------------------ football field ----------------------------- */
export const Field: React.FC<{f: number; smoke?: number; trucks?: number; dusk?: boolean}> = ({f, smoke = 0, trucks = 0, dusk}) => {
	const red = Math.floor(f / 6) % 2 === 0;
	return (
		<Svg>
			<Wall id="fd-s" a={dusk ? '#f0a070' : '#7cc0ec'} b={dusk ? '#ffe0a0' : '#dff0fb'} />
			{/* school building */}
			<rect x={300} y={300} width={1200} height={400} fill="#c4604a" />
			{Array.from({length: 2}).map((_, r) =>
				Array.from({length: 8}).map((__, c) => <rect key={`${r}${c}`} x={350 + c * 145} y={340 + r * 150} width={100} height={100} fill="#d6eefa" />),
			)}
			<rect x={760} y={260} width={280} height={60} fill="#2b3366" />
			<text x={900} y={302} textAnchor="middle" fontSize={30} fontFamily={FONT} fill="#fff">
				SCHOOL
			</text>
			{smoke > 0 ? (
				<g opacity={smoke}>
					{Array.from({length: 12}).map((_, i) => {
						const k = (f / 90 + i / 12) % 1;
						return <circle key={i} cx={1300 + Math.sin(i * 2 + f / 30) * 40 + k * 200} cy={320 - k * 420} r={60 + k * 120} fill="#55555f" opacity={0.55 * (1 - k)} style={{filter: 'blur(10px)'}} />;
					})}
				</g>
			) : null}
			<rect x={-500} y={680} width={2900} height={240} fill="#4aa04a" />
			{Array.from({length: 12}).map((_, i) => (
				<rect key={i} x={-500 + i * 260} y={680} width={130} height={240} fill="#5ab85a" />
			))}
			<line x1={-500} y1={760} x2={2400} y2={760} stroke="#f4f1e8" strokeWidth={6} opacity={0.7} />
			{/* goal */}
			<g stroke="#f4f1e8" strokeWidth={8} fill="none">
				<path d="M1650,800 L1650,600 L1900,600 L1900,800" />
			</g>
			{trucks > 0
				? [0, 1].map((i) => (
						<g key={i} transform={`translate(${-500 + trucks * (700 + i * 500)},${700})`}>
							<rect x={0} y={-150} width={380} height={130} rx={10} fill="#c62a2a" />
							<rect x={290} y={-200} width={110} height={180} rx={12} fill="#d63a3a" />
							<rect x={305} y={-185} width={80} height={60} rx={6} fill="#9fd2f0" />
							<rect x={10} y={-172} width={260} height={14} fill="#c9cfdd" />
							{[70, 320].map((x) => (
								<circle key={x} cx={x} cy={-16} r={32} fill="#141826" />
							))}
							<rect x={310} y={-215} width={60} height={16} rx={5} fill={red ? '#ff3a3a' : '#3a7aff'} />
							<circle cx={340} cy={-207} r={110} fill={red ? '#ff3a3a' : '#3a7aff'} opacity={0.18} />
						</g>
					))
				: null}
			<Floor c="#3d8f3d" lines="none" />
		</Svg>
	);
};

/* -------------------------------- bathroom mirror -------------------------- */
export const Bathroom: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="bt-w" a="#2a3048" b="#1d2238" />
		{Array.from({length: 18}).map((_, r) =>
			Array.from({length: 30}).map((__, c) => <rect key={`${r}${c}`} x={-300 + c * 80} y={-200 + r * 60} width={76} height={56} fill="#3a4262" opacity={0.5} />),
		)}
		<rect x={1100} y={140} width={560} height={520} rx={16} fill="#8a92a8" />
		<rect x={1116} y={156} width={528} height={488} rx={10} fill="#5a6a8a" />
		<polygon points="1180,644 1240,644 1500,156 1440,156" fill="#fff" opacity={0.08} />
		<rect x={1150} y={690} width={460} height={40} rx={12} fill="#d9dde6" />
		<rect x={1310} y={730} width={140} height={170} fill="#b9c0cc" />
		<rect x={1340} y={70} width={80} height={30} rx={8} fill="#fff6d0" opacity={0.85 + 0.15 * Math.sin(f / 7)} />
		<ellipse cx={1380} cy={110} rx={340} ry={160} fill="#fff6d0" opacity={0.08} />
		<Floor c="#3a4058" lines="tile" />
	</Svg>
);

/* ---------------------------- generic city at night ------------------------ */
export const NightCity: React.FC<{f: number; lit?: number}> = ({f, lit = 1}) => (
	<Svg>
		<Wall id="nc-s" a="#070b26" b="#2a2a6a" />
		{Array.from({length: 60}).map((_, i) => (
			<circle key={i} cx={random('ncs' + i) * 2400 - 200} cy={random('ncy' + i) * 300} r={1.5} fill="#fff" opacity={0.6} />
		))}
		<circle cx={1600} cy={160} r={60} fill="#f6f2dc" />
		{Array.from({length: 11}).map((_, i) => {
			const h = 300 + random('nch' + i) * 280;
			const x = -300 + i * 230;
			return (
				<g key={i}>
					<rect x={x} y={900 - h} width={200} height={h} fill={['#1d2350', '#252a5c', '#1a1f45'][i % 3]} />
					{Array.from({length: 12}).map((_, k) => {
						const on = random('ncw' + i + k) < 0.3 + 0.6 * lit;
						const shake = on ? Math.sin(f / 3 + i + k) * 0.25 + 0.75 : 1;
						return <rect key={k} x={x + 24 + (k % 3) * 56} y={900 - h + 30 + Math.floor(k / 3) * 70} width={36} height={42} fill={on ? '#ffd27a' : '#2e3466'} opacity={on ? shake : 1} />;
					})}
				</g>
			);
		})}
		<Floor c="#14183a" lines="none" />
	</Svg>
);

/* --------------------------------- africa 1962 ----------------------------- */
export const Village: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<Wall id="vl-s" a="#f0a050" b="#ffe0a0" />
		<circle cx={1500} cy={320} r={110} fill="#fff1c0" opacity={0.9} />
		<path d="M-500,640 Q300,560 900,640 T2400,620 L2400,900 L-500,900 Z" fill="#c98a4a" />
		{/* acacia */}
		{[200, 1700].map((x, i) => (
			<g key={i}>
				<rect x={x - 10} y={480} width={20} height={300} fill="#5a3a20" />
				<ellipse cx={x} cy={470} rx={190} ry={44} fill="#4a7a2a" />
			</g>
		))}
		{/* huts + school */}
		{[500, 1200].map((x, i) => (
			<g key={i}>
				<rect x={x - 120} y={620} width={240} height={180} fill="#d9b080" />
				<path d={`M${x - 160},640 L${x},${520} L${x + 160},640 Z`} fill="#8a6a3a" />
				<rect x={x - 30} y={700} width={60} height={100} fill="#5a3a20" />
			</g>
		))}
		<rect x={760} y={560} width={260} height={50} fill="#2b3366" />
		<text x={890} y={596} textAnchor="middle" fontSize={26} fontFamily={FONT} fill="#fff">
			SCHOOL, 1962
		</text>
		<Floor c="#b97a3a" lines="none" />
	</Svg>
);

/* ---------------------------- hallway outside a door ----------------------- */
export const lightenC = lighten;
