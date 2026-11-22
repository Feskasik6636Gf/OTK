import React from 'react';
import {Svg} from '../engine/camera';

/* ----------------------------- world library -----------------------------
   Outdoor and "big idea" locations in the semi-real cartoon style: thin dark outline,
   two-tone shading, soft depth blur on far layers, and several LIVING details each
   (leaves fall, waves run, stars twinkle, a car drives by...). Nothing here stands still.

   Use inside a shot:  <Layer depth={1.6}><Forest f={gf} /></Layer>
   Ground line for actors is y = 900 in every location (pass floor={900} to <Actor/>).
   Drawn across x = -500…2420 so the camera can pan and zoom without showing edges.
   The `WORLD` table at the bottom tells the story tool which location fits which words. */

const INK = '#1d1626';
const o = {stroke: INK, strokeWidth: 3.4, strokeLinejoin: 'round' as const};
const X0 = -500;
const WW = 3000;
const rnd = (i: number) => {
	const x = Math.sin(i * 127.1 + 3.7) * 43758.5453;
	return x - Math.floor(x);
};
const T = (f: number) => f / 30;

/* ================================= FOREST ================================= */
const Tree: React.FC<{x: number; base: number; w: number; h: number; c: string; canopy: string[]; t: number; ph: number; ink?: boolean}> = ({x, base, w, h, c, canopy, t, ph, ink}) => {
	const sw = Math.sin(t * 1.1 + ph) * 8;
	const st = ink ? o : {};
	return (
		<g>
			<path d={`M${x - w / 2},${base} Q${x - w * 0.4},${base - h * 0.5} ${x - w * 0.3},${base - h} L${x + w * 0.3},${base - h} Q${x + w * 0.4},${base - h * 0.5} ${x + w / 2},${base} Z`} fill={c} {...st} />
			{ink ? <path d={`M${x + w * 0.1},${base} Q${x + w * 0.15},${base - h * 0.5} ${x + w * 0.2},${base - h} L${x + w * 0.3},${base - h} Q${x + w * 0.4},${base - h * 0.5} ${x + w / 2},${base} Z`} fill="#000" opacity={0.16} /> : null}
			<g transform={`translate(${sw},0)`}>
				{[[0, 0, 1], [-0.38, 0.12, 0.8], [0.38, 0.1, 0.82], [-0.15, -0.16, 0.7], [0.2, -0.18, 0.66]].map((q, i) => (
					<ellipse key={i} cx={x + q[0] * h * 0.6} cy={base - h + q[1] * h * 0.4} rx={h * 0.3 * q[2]} ry={h * 0.24 * q[2]} fill={canopy[i % canopy.length]} {...st} />
				))}
			</g>
		</g>
	);
};
export const Forest: React.FC<{f: number; night?: boolean}> = ({f, night}) => {
	const t = T(f);
	return (
		<Svg>
			<defs>
				<linearGradient id="wf-sky" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={night ? '#0e1736' : '#b8e6b0'} />
					<stop offset="1" stopColor={night ? '#2a3a6a' : '#fff2b8'} />
				</linearGradient>
				<linearGradient id="wf-gr" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={night ? '#1f4a3a' : '#5aa564'} />
					<stop offset="1" stopColor={night ? '#133a2c' : '#2f7a4c'} />
				</linearGradient>
				<linearGradient id="wf-ray" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#fffbd0" stopOpacity="0.8" />
					<stop offset="1" stopColor="#fffbd0" stopOpacity="0" />
				</linearGradient>
				<filter id="wf-b1"><feGaussianBlur stdDeviation="6" /></filter>
				<filter id="wf-b2"><feGaussianBlur stdDeviation="2.6" /></filter>
			</defs>
			<rect x={X0} y={-200} width={WW} height={1400} fill="url(#wf-sky)" />
			<g filter="url(#wf-b1)" opacity={0.9}>
				{Array.from({length: 13}).map((_, i) => (
					<Tree key={i} x={i * 250 - 540} base={640} w={90} h={900 + rnd(i) * 120} c={night ? '#2c4a5a' : '#7fb08c'} canopy={night ? ['#365a68', '#2f5260'] : ['#8cc29a', '#7fb68e']} t={t} ph={i} />
				))}
			</g>
			<g filter="url(#wf-b2)">
				{Array.from({length: 10}).map((_, i) => (
					<Tree key={i} x={i * 320 - 520} base={700} w={130} h={1150 + rnd(i + 9) * 150} c={night ? '#20404a' : '#4d8a63'} canopy={night ? ['#2a5260', '#254a56'] : ['#5fa874', '#56a06b', '#6bb581']} t={t} ph={i * 2} />
				))}
			</g>
			{night ? null : [0, 1, 2, 3, 4].map((i) => <path key={i} d={`M${i * 380 - 100},0 L${i * 380 + 20},0 L${i * 380 - 220},900 L${i * 380 - 360},900 Z`} fill="url(#wf-ray)" opacity={0.5 + 0.25 * Math.sin(t * 1.3 + i * 1.7)} />)}
			<rect x={X0} y={690} width={WW} height={700} fill="url(#wf-gr)" />
			<path d="M-600,1000 Q200,820 700,860 T1700,780 T2500,820 L2500,1200 L-600,1200 Z" fill="#d9bd8a" {...o} />
			<path d="M-600,1010 Q200,840 700,880 T1700,800 T2500,840" stroke="#b79a68" strokeWidth={4} fill="none" strokeDasharray="30 22" />
			{Array.from({length: 40}).map((_, i) => {
				const x = X0 + ((i * 197) % WW);
				const y = 720 + ((i * 53) % 330);
				const sw = Math.sin(t * 2 + i) * 4;
				return <path key={i} transform={`translate(${x},${y})`} d={`M-12,0 L${-6 + sw},-34 L0,0 L${6 + sw},-40 L12,0 Z`} fill={i % 2 ? '#3f9a5c' : '#58b573'} stroke={INK} strokeWidth={2.6} strokeLinejoin="round" />;
			})}
			{[[300, 770], [1650, 760], [1100, 750], [-200, 780], [2150, 770]].map(([x, y], i) => (
				<g key={i} transform={`translate(${x},${y}) scale(0.5) translate(${-x},${-y})`}>
					<rect x={x - 6} y={y - 40} width={12} height={40} fill="#f4efe6" stroke={INK} strokeWidth={3} />
					<path d={`M${x - 34},${y - 38} Q${x},${y - 100} ${x + 34},${y - 38} Z`} fill={['#e0524a', '#ff8a5b', '#b58cff'][i % 3]} {...o} />
					<circle cx={x - 10} cy={y - 58} r={5} fill="#fff" opacity={0.85} />
					<circle cx={x + 12} cy={y - 52} r={4} fill="#fff" opacity={0.85} />
				</g>
			))}
			{[[620, 790], [1400, 770], [-100, 800]].map(([x, y], i) => (
				<g key={i}>
					<ellipse cx={x} cy={y} rx={52} ry={30} fill="#8c8ba0" {...o} />
					<ellipse cx={x - 14} cy={y - 10} rx={20} ry={10} fill="#b3b2c6" />
				</g>
			))}
			{Array.from({length: 34}).map((_, i) => {
				const k = (t * (0.12 + rnd(i) * 0.1) + rnd(i + 40)) % 1;
				const x = X0 + ((rnd(i + 5) * WW + Math.sin(t * 1.5 + i) * 60 + t * 20) % WW);
				const y = k * 1000 - 60;
				return <ellipse key={i} cx={x} cy={y} rx={13} ry={6} fill={['#ffb02e', '#e0724a', '#9acd5a', '#ffd84a'][i % 4]} stroke={INK} strokeWidth={2} transform={`rotate(${t * 140 * (i % 2 ? 1 : -1) + i * 30} ${x} ${y})`} />;
			})}
			{Array.from({length: 26}).map((_, i) => (
				<circle key={i} cx={X0 + ((rnd(i) * WW + Math.sin(t + i) * 30) % WW)} cy={300 + rnd(i + 3) * 520 + Math.cos(t * 1.3 + i) * 20} r={2.5 + rnd(i) * 2} fill={night ? '#c8ff9a' : '#fff9b0'} opacity={(night ? 0.55 : 0.35) + 0.35 * Math.sin(t * 3 + i)} />
			))}
			{(() => {
				const x = X0 + ((t * 170) % 3000);
				const fl = Math.sin(t * 18) * 12;
				return (
					<g transform={`translate(${x},${180 + Math.sin(t * 2) * 20})`}>
						<path d={`M0,0 q-26,${-18 - fl} -52,0 q26,${-8 - fl * 0.4} 52,0 Z`} fill="#3a3550" stroke={INK} strokeWidth={2.4} />
						<path d={`M0,0 q26,${-18 + fl} 52,0`} stroke={INK} strokeWidth={3} fill="none" />
					</g>
				);
			})()}
			{night ? <rect x={X0} y={-200} width={WW} height={1400} fill="#0a1030" opacity={0.28} /> : null}
		</Svg>
	);
};

/* ================================== BEACH ================================== */
export const Beach: React.FC<{f: number}> = ({f}) => {
	const t = T(f);
	return (
		<Svg>
			<defs>
				<linearGradient id="wb-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#6fc8ff" /><stop offset="1" stopColor="#ffe9b8" /></linearGradient>
				<linearGradient id="wb-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2aa6c9" /><stop offset="1" stopColor="#7fe0d6" /></linearGradient>
				<linearGradient id="wb-sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f7e2a8" /><stop offset="1" stopColor="#ecc983" /></linearGradient>
				<radialGradient id="wb-sun"><stop offset="0" stopColor="#fff7c0" /><stop offset="0.4" stopColor="#ffe36a" /><stop offset="1" stopColor="#ffe36a" stopOpacity="0" /></radialGradient>
			</defs>
			<rect x={X0} y={-200} width={WW} height={1000} fill="url(#wb-sky)" />
			<circle cx={1500} cy={210} r={230 + 12 * Math.sin(t * 2)} fill="url(#wb-sun)" />
			<g transform={`rotate(${t * 6} 1500 210)`}>
				{Array.from({length: 12}).map((_, i) => <path key={i} d="M1500,210 l-18,-300 h36 Z" fill="#fff6b0" opacity={0.18} transform={`rotate(${i * 30} 1500 210)`} />)}
			</g>
			<circle cx={1500} cy={210} r={78} fill="#ffe14d" {...o} />
			{[0, 1, 2, 3].map((i) => {
				const x = X0 + ((t * (14 + i * 7) + i * 800) % 3200) - 100;
				return (
					<g key={i} transform={`translate(${x},${130 + i * 80})`}>
						<ellipse rx={120} ry={32} fill="#fff" {...o} />
						<ellipse cx={-40} cy={-24} rx={56} ry={34} fill="#fff" {...o} />
						<ellipse cx={40} cy={-18} rx={50} ry={28} fill="#fff" {...o} />
						<ellipse rx={118} ry={30} fill="#fff" />
					</g>
				);
			})}
			<rect x={X0} y={430} width={WW} height={260} fill="url(#wb-sea)" />
			{Array.from({length: 7}).map((_, r) => (
				<path key={r} d={`M-700,${470 + r * 34} ` + Array.from({length: 30}).map((_, i) => `q60,${-12 * Math.sin(t * 2 + r + i * 0.5)} 120,0`).join(' ')} stroke="#e8fffb" strokeWidth={3.5} fill="none" opacity={0.55} transform={`translate(${(t * 20 * (1 + r * 0.15)) % 120},0)`} />
			))}
			<g transform={`translate(${380 + Math.sin(t * 0.5) * 40},${455 + Math.sin(t * 1.8) * 8}) rotate(${Math.sin(t * 1.8) * 3})`}>
				<path d="M-70,0 L70,0 L46,34 L-46,34 Z" fill="#e0524a" {...o} />
				<line x1={0} y1={0} x2={0} y2={-120} stroke={INK} strokeWidth={5} />
				<path d="M6,-116 L6,-10 L66,-10 Z" fill="#fff" {...o} />
			</g>
			<path d={`M-600,690 ` + Array.from({length: 30}).map((_, i) => `q60,${14 * Math.sin(t * 2.2 + i)} 120,0`).join(' ') + ' L2500,740 L-600,740 Z'} fill="#f8fffd" stroke="#bff0ea" strokeWidth={3} opacity={0.9} />
			<rect x={X0} y={700} width={WW} height={700} fill="url(#wb-sand)" />
			{Array.from({length: 90}).map((_, i) => <circle key={i} cx={X0 + ((i * 263) % WW)} cy={730 + ((i * 97) % 340)} r={2 + (i % 3)} fill="#d3ab68" opacity={0.7} />)}
			<g transform="translate(1650,880) scale(1.9)">
				<path d="M0,0 Q-60,-220 20,-420" stroke={INK} strokeWidth={46} fill="none" strokeLinecap="round" />
				<path d="M0,0 Q-60,-220 20,-420" stroke="#b9854f" strokeWidth={36} fill="none" strokeLinecap="round" />
				<g transform="translate(20,-420)">
					{[-160, -120, -75, -30, 20, 60].map((a, i) => (
						<g key={i} transform={`rotate(${a + Math.sin(t * 1.6 + i) * 6})`}>
							<path d="M0,0 Q70,-90 220,-30 Q110,-50 0,14 Z" fill={['#3fae66', '#2f9a55'][i % 2]} {...o} />
						</g>
					))}
					<circle cx={-8} cy={10} r={14} fill="#7a4a24" stroke={INK} strokeWidth={3} />
					<circle cx={12} cy={16} r={14} fill="#7a4a24" stroke={INK} strokeWidth={3} />
				</g>
			</g>
			<g transform="translate(250,900) scale(1.45)">
				<line x1={0} y1={-10} x2={0} y2={-290} stroke={INK} strokeWidth={8} />
				<g transform={`rotate(${Math.sin(t * 1.2) * 1.5} 0 -290)`}>
					<path d="M-190,-250 Q0,-420 190,-250 Z" fill="#fff" {...o} strokeWidth={4} />
					<path d="M-190,-250 Q-120,-380 -64,-336 L-64,-250 Z M64,-250 L64,-340 Q130,-380 190,-250 Z" fill="#e0524a" {...o} />
					<path d="M-64,-336 Q0,-350 64,-340 L64,-250 L-64,-250 Z" fill="#ffd84a" {...o} />
				</g>
				<path d="M-120,0 L120,0 L150,50 L-90,50 Z" fill="#6fd0c0" {...o} />
			</g>
			<g transform="translate(1150,950)">
				<path d="M-70,0 L-60,-60 L60,-60 L70,0 Z" fill="#e9c27a" {...o} />
				<path d="M-40,-60 v-34 h16 v8 h12 v-8 h16 v8 h12 v-8 h16 v34 Z" fill="#e9c27a" {...o} />
				<path d="M0,-94 v-40" stroke={INK} strokeWidth={3} />
				<path d={`M0,-134 l36,${8 + Math.sin(t * 5) * 3} l-36,12Z`} fill="#e0524a" stroke={INK} strokeWidth={2.6} />
			</g>
			{(() => {
				const x = 560 + Math.sin(t * 1.4) * 150;
				const sw = Math.sin(t * 16) * 5;
				return (
					<g transform={`translate(${x},1020) scale(0.6)`}>
						<ellipse rx={36} ry={22} fill="#e0524a" {...o} />
						{[-1, 1].map((s) => (
							<g key={s}>
								<path d={`M${s * 30},-8 q${s * 26},-10 ${s * 22},-30`} stroke={INK} strokeWidth={4} fill="none" />
								<circle cx={s * 52} cy={-40} r={12} fill="#e0524a" stroke={INK} strokeWidth={3} />
								{[0, 1, 2].map((k) => <line key={k} x1={s * 26} y1={6 + k * 5} x2={s * (46 + sw * s)} y2={14 + k * 8} stroke={INK} strokeWidth={3} />)}
								<circle cx={s * 12} cy={-22} r={5} fill="#fff" stroke={INK} strokeWidth={2} />
							</g>
						))}
					</g>
				);
			})()}
			{[0, 1, 2, 3, 4].map((i) => {
				const x = X0 + ((t * (120 + i * 40) + i * 600) % 3400) - 200;
				const y = 120 + i * 50 + Math.sin(t * 3 + i) * 14;
				const w = Math.sin(t * 9 + i) * 16;
				return <path key={i} d={`M${x - 36},${y - w} Q${x - 14},${y - 10} ${x},${y + 4} Q${x + 14},${y - 10} ${x + 36},${y - w}`} stroke={INK} strokeWidth={5} fill="none" strokeLinecap="round" />;
			})}
		</Svg>
	);
};

/* =============================== MOON / SPACE =============================== */
export const Moon: React.FC<{f: number}> = ({f}) => {
	const t = T(f);
	return (
		<Svg>
			<defs>
				<linearGradient id="wm-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#04051a" /><stop offset="1" stopColor="#241a5c" /></linearGradient>
				<linearGradient id="wm-moon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#b9b6d6" /><stop offset="1" stopColor="#7d789e" /></linearGradient>
				<clipPath id="wm-pl"><circle cx={1380} cy={310} r={190} /></clipPath>
				<radialGradient id="wm-sh" cx="0.3" cy="0.3" r="0.9"><stop offset="0.5" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity="0.6" /></radialGradient>
			</defs>
			<rect x={X0} y={-300} width={WW} height={1100} fill="url(#wm-sky)" />
			{Array.from({length: 180}).map((_, i) => <circle key={i} cx={X0 + ((i * 397) % WW)} cy={-100 + ((i * 211) % 800)} r={0.8 + (i % 4) * 0.6} fill="#fff" opacity={0.35 + 0.65 * Math.abs(Math.sin(t * (1 + (i % 5) * 0.6) + i))} />)}
			<g transform="translate(300,170)">
				<circle r={70} fill="#4fa6ff" {...o} />
				<path d="M-40,-30 q20,-24 44,-8 q-8,22 -26,20 q-8,18 -22,6 Z M20,10 q22,-10 36,10 q-14,24 -34,12 Z" fill="#5ad07a" />
				<circle r={70} fill="url(#wm-sh)" />
			</g>
			<ellipse cx={1380} cy={320} rx={330} ry={52} fill="none" stroke="#ffe3b0" strokeWidth={14} opacity={0.9} transform="rotate(-14 1380 320)" />
			<circle cx={1380} cy={310} r={190} fill="#f2a45a" {...o} strokeWidth={4} />
			<g clipPath="url(#wm-pl)">
				{[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={1150 + ((t * 10 + i * 90) % 540) - 60} y={150 + i * 55} width={420} height={26} fill={['#e0794a', '#ffd89a', '#c4623a'][i % 3]} opacity={0.75} transform="skewX(-10)" />)}
			</g>
			<circle cx={1380} cy={310} r={190} fill="url(#wm-sh)" />
			<path d="M1050,320 A330,52 0 0 0 1710,320" fill="none" stroke="#ffe3b0" strokeWidth={14} transform="rotate(-14 1380 320)" />
			{(() => {
				const k = (t % 3) / 3;
				return (
					<g opacity={k < 0.4 ? Math.sin((k / 0.4) * Math.PI) : 0}>
						<line x1={900 + k * 1400} y1={40 + k * 300} x2={900 + k * 1400 + 160} y2={40 + k * 300 + 74} stroke="#fff" strokeWidth={5} strokeLinecap="round" />
					</g>
				);
			})()}
			<path d="M-700,720 Q-100,640 400,700 T1300,690 T2100,700 T2700,690 L2700,1200 L-700,1200 Z" fill="url(#wm-moon)" {...o} strokeWidth={4} />
			{[[260, 800, 150], [820, 760, 110], [1500, 790, 170], [1000, 930, 220], [160, 980, 120], [-300, 850, 160], [2100, 900, 190]].map(([x, y, r], i) => (
				<g key={i}>
					<ellipse cx={x} cy={y} rx={r} ry={r * 0.28} fill="#6b668c" {...o} />
					<ellipse cx={x} cy={y + 4} rx={r * 0.86} ry={r * 0.2} fill="#8f8bb2" />
				</g>
			))}
			{[[620, 860], [1260, 830], [1750, 930], [-100, 900]].map(([x, y], i) => <path key={i} d={`M${x - 40},${y} l10,-36 l34,-14 l36,22 l8,28 Z`} fill="#8d89ae" {...o} />)}
			<g transform="translate(1700,820)">
				<line x1={0} y1={0} x2={0} y2={-250} stroke={INK} strokeWidth={7} />
				<path d={`M0,-250 q40,${-14 + Math.sin(t * 3) * 6} 80,0 q40,${14 - Math.sin(t * 3) * 6} 80,0 L160,-170 q-40,${14 + Math.sin(t * 3 + 1) * 6} -80,0 q-40,${-14 - Math.sin(t * 3 + 1) * 6} -80,0 Z`} fill="#ff2540" {...o} />
				<path d="M40,-222 l8,18 20,2 -15,12 5,19 -18,-10 -18,10 5,-19 -15,-12 20,-2 Z" fill="#fff" transform="translate(10,-4) scale(0.9)" />
			</g>
			{(() => {
				const x = X0 + ((t * 90) % 3300);
				return (
					<g transform={`translate(${x},880) scale(1.9)`}>
						<rect x={-80} y={-70} width={160} height={46} rx={10} fill="#e9eaf2" {...o} />
						<rect x={-30} y={-110} width={70} height={42} rx={10} fill="#8fd0ff" {...o} />
						<line x1={50} y1={-110} x2={70} y2={-150} stroke={INK} strokeWidth={4} />
						<circle cx={72} cy={-154} r={9} fill="#ffd84a" stroke={INK} strokeWidth={3} />
						{[-52, 0, 52].map((wx) => (
							<g key={wx} transform={`translate(${wx},-12) rotate(${t * 240})`}>
								<circle r={24} fill="#3a3550" {...o} />
								<line x1={-18} y1={0} x2={18} y2={0} stroke="#9a96c0" strokeWidth={4} />
								<line x1={0} y1={-18} x2={0} y2={18} stroke="#9a96c0" strokeWidth={4} />
							</g>
						))}
					</g>
				);
			})()}
			{Array.from({length: 40}).map((_, i) => <circle key={i} cx={X0 + ((rnd(i) * WW + Math.sin(t * 0.8 + i) * 40) % WW)} cy={((rnd(i + 9) * 900 + 1000 - t * (14 + (i % 4) * 5)) % 900) + 120} r={1.8 + (i % 3)} fill="#d9d4ff" opacity={0.45} />)}
		</Svg>
	);
};

/* ================================= CITY DAY =================================
   Proportions: a person on the near pavement is ~420 px tall (s = 1). A car on the road
   behind is further away, so ~190 px tall and ~470 px long; a lamp post ~520 px; one
   storey of the houses ~150 px (windows ~90 px). Buildings are far, so they are blurred. */
export const CityDay: React.FC<{f: number}> = ({f}) => {
	const t = T(f);
	const blds = [[-560, 340, 560, '#a8b4e0'], [-180, 300, 680, '#b7a8dc'], [150, 360, 500, '#9fc0d8'], [540, 320, 740, '#c4b2d8'], [900, 380, 560, '#a6bdd8'], [1310, 300, 680, '#bcb0dc'], [1650, 360, 520, '#a3c4cf'], [2050, 330, 700, '#b9acd6']] as const;
	return (
		<Svg>
			<defs>
				<linearGradient id="wc-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#7fc4ff" /><stop offset="1" stopColor="#ffeccc" /></linearGradient>
				<filter id="wc-b"><feGaussianBlur stdDeviation="3" /></filter>
			</defs>
			<rect x={X0} y={-300} width={WW} height={1000} fill="url(#wc-sky)" />
			{[0, 1, 2].map((i) => {
				const x = X0 + ((t * (10 + i * 6) + i * 1000) % 3400) - 100;
				return (
					<g key={i} transform={`translate(${x},${120 + i * 90})`}>
						<ellipse rx={110} ry={28} fill="#fff" {...o} />
						<ellipse cx={-34} cy={-20} rx={50} ry={30} fill="#fff" {...o} />
						<ellipse rx={108} ry={26} fill="#fff" />
					</g>
				);
			})}
			<g filter="url(#wc-b)">
				{blds.map(([x, w, h, c], i) => (
					<g key={i}>
						<rect x={x} y={640 - h} width={w} height={h} fill={c} {...o} />
						<rect x={x + w * 0.62} y={640 - h} width={w * 0.38} height={h} fill="#000" opacity={0.1} />
						{Array.from({length: Math.floor(h / 150) * Math.floor(w / 110)}).map((_, k) => {
							const cols = Math.floor(w / 110);
							const cx = k % cols;
							const cy = Math.floor(k / cols);
							return <rect key={k} x={x + 24 + cx * 110} y={640 - h + 30 + cy * 150} width={64} height={96} fill={rnd(i * 100 + k) > 0.6 ? '#ffe08a' : '#dff0ff'} stroke={INK} strokeWidth={2.6} />;
						})}
					</g>
				))}
			</g>
			<rect x={X0} y={640} width={WW} height={60} fill="#cfcae0" {...o} />
			<rect x={X0} y={700} width={WW} height={100} fill="#4a4c60" />
			{Array.from({length: 18}).map((_, i) => <rect key={i} x={X0 + i * 200 + ((t * 90) % 200)} y={746} width={110} height={8} fill="#e8e6f0" opacity={0.8} />)}
			<rect x={X0} y={800} width={WW} height={14} fill="#8f8aa8" {...o} />
			<rect x={X0} y={814} width={WW} height={500} fill="#d9d4e8" />
			{Array.from({length: 26}).map((_, i) => <line key={i} x1={X0 + i * 130} y1={814} x2={X0 + i * 130 - 70} y2={1200} stroke="#c3bdd8" strokeWidth={3} opacity={0.7} />)}
			{[0, 1].map((i) => {
				const dirn = i ? -1 : 1;
				const x = dirn > 0 ? X0 + ((t * 300 + i * 900) % 3600) - 300 : 2600 - ((t * 260 + i * 900) % 3600);
				const c = i ? '#e0524a' : '#3d6fe0';
				const base = i ? 735 : 788;
				const k = i ? 0.8 : 1;
				return (
					<g key={i} transform={`translate(${x},${base}) scale(${dirn * k},${k})`}>
						<ellipse cx={0} cy={4} rx={230} ry={14} fill="#000" opacity={0.22} />
						<path d="M-230,-18 L-230,-100 L-150,-112 L-80,-186 L110,-186 L180,-112 L240,-96 L240,-18 Z" fill={c} {...o} />
						<path d="M-62,-176 L-34,-112 L86,-112 L92,-176 Z" fill="#cfeaff" stroke={INK} strokeWidth={3.4} />
						<path d="M-230,-62 H240" stroke="#000" strokeWidth={4} opacity={0.18} />
						<rect x={214} y={-70} width={26} height={16} fill="#fff3b0" stroke={INK} strokeWidth={3} />
						{[-140, 130].map((wx) => (
							<g key={wx} transform={`translate(${wx},-24) rotate(${t * 500})`}>
								<circle r={40} fill="#2a2a38" {...o} />
								<circle r={20} fill="#9aa0c0" stroke={INK} strokeWidth={3} />
								<line x1={-30} y1={0} x2={30} y2={0} stroke="#cfd4ee" strokeWidth={4} />
							</g>
						))}
					</g>
				);
			})}
			{[0, 1, 2, 3].map((i) => (
				<g key={i} transform={`translate(${i * 800 - 350},830)`}>
					<rect x={-12} y={-520} width={24} height={520} fill="#5a5470" {...o} />
					<rect x={-12} y={-520} width={150} height={20} fill="#5a5470" {...o} />
					<ellipse cx={120} cy={-494} rx={34} ry={12} fill="#fff3b0" stroke={INK} strokeWidth={3} />
				</g>
			))}
			{[0, 1, 2, 3, 4].map((i) => {
				const x = X0 + ((t * (50 + i * 14) + i * 640) % 3300);
				const y = 880 + (i % 3) * 60;
				const w = Math.sin(t * 14 + i) * 6;
				return (
					<g key={i} transform={`translate(${x},${y}) scale(1.5)`}>
						<ellipse rx={20} ry={13} fill="#8a90b0" {...o} />
						<circle cx={20} cy={-8} r={9} fill="#7d8099" stroke={INK} strokeWidth={3} />
						<path d="M28,-8 l10,2 -10,4z" fill="#f0b43a" />
						<path d={`M-4,-6 q-14,${-14 - w} -26,${-2}`} fill="none" stroke={INK} strokeWidth={3} />
						<line x1={-4} y1={12} x2={-4} y2={22 + w * 0.4} stroke={INK} strokeWidth={3} />
						<line x1={8} y1={12} x2={8} y2={22 - w * 0.4} stroke={INK} strokeWidth={3} />
					</g>
				);
			})}
		</Svg>
	);
};

/* ================================== DESERT ================================== */
export const Desert: React.FC<{f: number}> = ({f}) => {
	const t = T(f);
	return (
		<Svg>
			<defs>
				<linearGradient id="wd-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#ff9a5a" /><stop offset="0.6" stopColor="#ffd08a" /><stop offset="1" stopColor="#fff0c0" /></linearGradient>
				<linearGradient id="wd-d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#f0b866" /><stop offset="1" stopColor="#d99a52" /></linearGradient>
				<linearGradient id="wd-d2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#e8a95a" /><stop offset="1" stopColor="#c98744" /></linearGradient>
				<radialGradient id="wd-sun"><stop offset="0" stopColor="#fffbe0" /><stop offset="0.5" stopColor="#ffe36a" /><stop offset="1" stopColor="#ffe36a" stopOpacity="0" /></radialGradient>
			</defs>
			<rect x={X0} y={-300} width={WW} height={1100} fill="url(#wd-sky)" />
			<circle cx={960} cy={420} r={320 + 14 * Math.sin(t * 2)} fill="url(#wd-sun)" />
			<circle cx={960} cy={420} r={110} fill="#fff4b0" {...o} />
			<path d="M-600,640 Q0,520 500,610 T1400,590 T2500,620 L2500,1200 L-600,1200 Z" fill="#e4a55a" {...o} opacity={0.9} />
			<path d="M-600,740 Q300,640 900,720 T2000,690 T2600,730 L2600,1200 L-600,1200 Z" fill="url(#wd-d1)" {...o} />
			<path d="M-600,860 Q200,780 800,850 T1800,820 T2600,860 L2600,1200 L-600,1200 Z" fill="url(#wd-d2)" {...o} />
			<path d="M-600,860 Q200,780 800,850 T1800,820 T2600,860" fill="none" stroke="#fff3c0" strokeWidth={4} opacity={0.5} transform="translate(0,-8)" />
			{[[240, 850], [1560, 830], [-180, 870], [2100, 860]].map(([x, y], i) => (
				<g key={i} transform={`translate(${x},${y}) scale(2.3)`}>
					<path d="M-18,0 V-150 Q-18,-176 0,-176 Q18,-176 18,-150 V0 Z" fill="#4fa86a" {...o} />
					<path d="M18,-70 h30 Q64,-70 64,-92 V-112 Q64,-124 52,-124 Q40,-124 40,-112 V-96 H18 Z" fill="#4fa86a" {...o} />
					<path d="M-18,-50 h-26 Q-58,-50 -58,-70 V-96 Q-58,-108 -46,-108 Q-34,-108 -34,-96 V-76 H-18 Z" fill="#4fa86a" {...o} />
					<path d="M-6,-150 V-8 M6,-150 V-8" stroke="#2f7a4c" strokeWidth={3} fill="none" opacity={0.6} />
					<circle cx={0} cy={-178} r={7} fill="#ff6fa0" stroke={INK} strokeWidth={2.4} />
				</g>
			))}
			{[[700, 900], [1320, 880], [-60, 940]].map(([x, y], i) => (
				<g key={i}>
					<ellipse cx={x} cy={y} rx={60} ry={30} fill="#b88650" {...o} />
					<ellipse cx={x - 16} cy={y - 10} rx={22} ry={10} fill="#d9a870" />
				</g>
			))}
			{(() => {
				const x = X0 + ((t * 150) % 3400);
				const y = 930 - Math.abs(Math.sin(t * 5)) * 26;
				return (
					<g transform={`translate(${x},${y}) rotate(${t * 220})`}>
						<circle r={34} fill="none" stroke={INK} strokeWidth={9} />
						<circle r={34} fill="none" stroke="#b99358" strokeWidth={5} strokeDasharray="7 5" />
						<path d="M-30,6 L30,-8 M-10,-30 L12,30 M-26,-14 L24,18" stroke="#8f6c3c" strokeWidth={4} />
					</g>
				);
			})()}
			{[0, 1].map((i) => {
				const a = t * 0.5 + i * 3.1;
				const x = 1300 + Math.cos(a) * (340 + i * 90);
				const y = 190 + Math.sin(a) * 60 + i * 50;
				const w = Math.sin(t * 6 + i) * 10;
				return <path key={i} d={`M${x - 46},${y - w} Q${x - 18},${y - 14} ${x},${y} Q${x + 18},${y - 14} ${x + 46},${y - w}`} stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />;
			})}
			{Array.from({length: 8}).map((_, i) => <path key={i} d={`M${X0 + i * 380},${770 + (i % 3) * 22} q40,${-10 + 6 * Math.sin(t * 3 + i)} 80,0 t80,0`} stroke="#fff3c0" strokeWidth={3} fill="none" opacity={0.35} />)}
			{Array.from({length: 40}).map((_, i) => <circle key={i} cx={X0 + ((rnd(i) * WW + t * (40 + (i % 4) * 14)) % WW)} cy={760 + rnd(i + 5) * 300 + Math.sin(t * 2 + i) * 10} r={1.8 + (i % 3)} fill="#fff3c0" opacity={0.5} />)}
		</Svg>
	);
};

/* ----------------------- which words → which location -----------------------
   The story tool (and Claude) match the spoken line against `words` to choose a place.
   Add your own entries when you build a new location in story/places.tsx. */
export const WORLD: {id: string; words: string[]; living: string; make: (f: number) => React.ReactNode}[] = [
	{id: 'forest', words: ['лес', 'деревья', 'тропа', 'грибы', 'птицы', 'природа', 'парк', 'forest', 'wood'], living: 'качаются кроны, падают листья, светлячки, птица', make: (f) => <Forest f={f} />},
	{id: 'forest-night', words: ['ночной лес', 'ночью в лесу', 'тёмный лес', 'dark forest'], living: 'светлячки, качаются кроны', make: (f) => <Forest f={f} night />},
	{id: 'beach', words: ['пляж', 'море', 'океан', 'берег', 'отпуск', 'волны', 'остров', 'beach', 'sea'], living: 'бегут волны, качается лодка, чайки, краб, пальма', make: (f) => <Beach f={f} />},
	{id: 'moon', words: ['космос', 'луна', 'планета', 'звёзды', 'невесомость', 'марс', 'ракета', 'space', 'moon'], living: 'мерцают звёзды, едет вездеход, метеор, вращается планета', make: (f) => <Moon f={f} />},
	{id: 'city', words: ['город', 'улица', 'машины', 'дорога', 'люди идут', 'центр', 'city', 'street'], living: 'едут машины, летают голуби, плывут облака', make: (f) => <CityDay f={f} />},
	{id: 'desert', words: ['пустыня', 'жара', 'песок', 'кактус', 'засуха', 'desert'], living: 'катится куст, кружит птица, марево, пыль', make: (f) => <Desert f={f} />},
];
