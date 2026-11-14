import React from 'react';
import {random} from 'remotion';
import {Svg} from '../engine/camera';
import {darken, lighten} from '../engine/color';
import {FONT} from '../kit/ui';

/* Locations of "What if Earth got a second sun". World 1920x1080, floor ~900.
   Everything is flat and chunky; one light source per set; one living detail. */

export type SkyMode = 'blue' | 'dawn' | 'dusk' | 'gold' | 'orange' | 'hot' | 'night' | 'dark' | 'pink';
export const SKY: Record<SkyMode, {top: string; bot: string; ground: string; grass: string; house: string; amb: string}> = {
	blue: {top: '#2f7fe6', bot: '#a9dcff', ground: '#c9c2b4', grass: '#5fbf4a', house: '#f1e2c8', amb: '#ffffff'},
	dawn: {top: '#2b1b4a', bot: '#ff8a3a', ground: '#6a5560', grass: '#4a6a3a', house: '#b8908a', amb: '#ffb070'},
	pink: {top: '#5a4aa8', bot: '#ff9ab8', ground: '#a88aa0', grass: '#5a8a5a', house: '#e8c0c8', amb: '#ffc0d0'},
	dusk: {top: '#3a1f6a', bot: '#ff7a5a', ground: '#5a4060', grass: '#3a5a4a', house: '#a07890', amb: '#ff9a7a'},
	gold: {top: '#ff9a3a', bot: '#ffe08a', ground: '#b08a5a', grass: '#7a9a3a', house: '#f0c890', amb: '#ffd080'},
	orange: {top: '#c8501f', bot: '#ffb04a', ground: '#8a5a40', grass: '#6a7a30', house: '#e0a070', amb: '#ffa050'},
	hot: {top: '#ffb85a', bot: '#fff4d0', ground: '#e0c8a0', grass: '#b8b050', house: '#fff0d8', amb: '#fff0c0'},
	night: {top: '#05071a', bot: '#1a2350', ground: '#1e2236', grass: '#1a3028', house: '#2e3454', amb: '#8aa0ff'},
	dark: {top: '#000005', bot: '#0b1030', ground: '#121424', grass: '#0e1c18', house: '#1e2238', amb: '#6a80d0'},
};

export type Sun = {x: number; y: number; r: number; c: string; glow?: number};
export const WHITE_SUN = '#fffbe8';
export const ORANGE_SUN = '#ff8a2a';

/* sky with suns, stars and the milky way (put on a far layer) */
export const SkyDome: React.FC<{mode: SkyMode; f: number; suns?: Sun[]; stars?: number; milky?: number; id: string}> = ({mode, f, suns = [], stars = 0, milky = 0, id}) => {
	const p = SKY[mode];
	return (
		<Svg>
			<defs>
				<linearGradient id={'sk' + id} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={p.top} />
					<stop offset="1" stopColor={p.bot} />
				</linearGradient>
				{suns.map((s, i) => (
					<radialGradient key={i} id={`sg${id}${i}`}>
						<stop offset="0" stopColor={s.c} stopOpacity={0.9} />
						<stop offset="0.3" stopColor={s.c} stopOpacity={0.35} />
						<stop offset="1" stopColor={s.c} stopOpacity={0} />
					</radialGradient>
				))}
			</defs>
			<rect x={-600} y={-500} width={3120} height={2000} fill={`url(#sk${id})`} />
			{stars > 0
				? Array.from({length: Math.round(220 * Math.min(1, stars))}).map((_, i) => {
						const x = random(id + 'sx' + i) * 3000 - 540;
						const y = random(id + 'sy' + i) * 1100 - 400;
						const tw = 0.55 + 0.45 * Math.sin(f / (8 + (i % 7)) + i);
						return <circle key={i} cx={x} cy={y} r={0.8 + random(id + 'sr' + i) * 2.2} fill="#fff" opacity={tw * Math.min(1, stars)} />;
					})
				: null}
			{milky > 0 ? (
				<g opacity={milky}>
					<path d="M-500,600 C200,250 900,120 2400,-300 L2400,-80 C1000,320 300,480 -500,860 Z" fill="#c8d0ff" opacity={0.13} />
					<path d="M-500,660 C200,330 900,200 2400,-200 L2400,-140 C1000,250 300,420 -500,760 Z" fill="#fff" opacity={0.1} />
					{Array.from({length: 500}).map((_, i) => {
						const u = random('mw' + i);
						const x = -500 + u * 2900;
						const yc = 760 - u * 1020 + (random('mv' + i) - 0.5) * 260;
						return <circle key={i} cx={x} cy={yc} r={0.6 + random('mz' + i) * 1.6} fill={i % 9 === 0 ? '#ffd6a8' : '#fff'} opacity={0.4 + 0.6 * Math.abs(Math.sin(f / 11 + i))} />;
					})}
				</g>
			) : null}
			{suns.map((s, i) => (
				<g key={i}>
					<circle cx={s.x} cy={s.y} r={s.r * 6 * (s.glow ?? 1)} fill={`url(#sg${id}${i})`} />
					<circle cx={s.x} cy={s.y} r={s.r * (1 + 0.02 * Math.sin(f / 5 + i))} fill={s.c} />
					<circle cx={s.x - s.r * 0.25} cy={s.y - s.r * 0.25} r={s.r * 0.55} fill="#fff" opacity={0.35} />
				</g>
			))}
		</Svg>
	);
};

/* far row of suburban houses (layer depth ~1.8) */
export const FarHouses: React.FC<{mode: SkyMode; lit?: number}> = ({mode, lit = 0}) => {
	const p = SKY[mode];
	const c = darken(p.house, 0.25);
	return (
		<Svg>
			{Array.from({length: 9}).map((_, i) => {
				const x = -300 + i * 300 + (i % 2) * 40;
				const w = 220 + (i % 3) * 30;
				const h = 150 + (i % 4) * 20;
				return (
					<g key={i}>
						<rect x={x} y={760 - h} width={w} height={h + 40} fill={c} />
						<path d={`M${x - 20},${760 - h} L${x + w / 2},${700 - h - (i % 2) * 20} L${x + w + 20},${760 - h} Z`} fill={darken(c, 0.25)} />
						<rect x={x + 30} y={790 - h} width={46} height={46} fill={lit ? '#ffd27a' : darken(c, 0.15)} opacity={lit ? lit : 1} />
						<rect x={x + w - 80} y={790 - h} width={46} height={46} fill={lit && i % 2 ? '#ffd27a' : darken(c, 0.15)} />
					</g>
				);
			})}
			{Array.from({length: 7}).map((_, i) => (
				<g key={'t' + i}>
					<rect x={-120 + i * 340} y={640} width={14} height={140} fill={darken(p.grass, 0.4)} />
					<circle cx={-113 + i * 340} cy={630} r={70 + (i % 3) * 14} fill={darken(p.grass, 0.25)} />
				</g>
			))}
			<rect x={-600} y={770} width={3120} height={400} fill={darken(p.grass, 0.15)} />
		</Svg>
	);
};

/* front yard: house with porch (left), driveway with a hoop (right), lawn, fence */
export const Yard: React.FC<{mode: SkyMode; f: number; hoop?: boolean; porch?: boolean; panels?: number; garden?: number; melt?: number}> = ({mode, f, hoop = true, porch = true, panels = 0, garden = 0, melt = 0}) => {
	const p = SKY[mode];
	const wall = p.house;
	const roof = darken(wall, 0.45);
	return (
		<Svg>
			<rect x={-600} y={860} width={3120} height={400} fill={p.grass} />
			<path d="M980,860 L1640,860 L1900,1300 L700,1300 Z" fill={p.ground} />
			{melt > 0 ? <path d={`M1000,${930} q120,${-10 * melt} 260,0 t260,6 l0,${30 * melt} q-120,${20 * melt} -520,0 Z`} fill="#1a1a1e" opacity={0.6 * melt} /> : null}
			<rect x={-300} y={420} width={900} height={460} fill={wall} />
			<path d="M-360,430 L150,170 L660,430 Z" fill={roof} />
			{panels > 0
				? Array.from({length: 4}).map((_, i) => (
						<g key={i} transform={`translate(${-60 + i * 110},300)`}>
							<rect x={0} y={0} width={96} height={60} fill="#1f3a8a" stroke="#cfe0ff" strokeWidth={3} />
							<line x1={48} y1={0} x2={48} y2={60} stroke="#cfe0ff" strokeWidth={2} />
							<rect x={0} y={0} width={96} height={60} fill="#fff" opacity={panels * (0.25 + 0.25 * Math.sin(f / 3 + i))} />
						</g>
					))
				: null}
			<rect x={-180} y={520} width={170} height={150} fill={darken(wall, 0.5)} />
			<rect x={-170} y={530} width={150} height={130} fill={mode === 'night' || mode === 'dark' ? '#ffcf6a' : lighten(p.bot, 0.3)} />
			<line x1={-95} y1={530} x2={-95} y2={660} stroke={darken(wall, 0.5)} strokeWidth={8} />
			<rect x={260} y={560} width={120} height={320} fill={darken(wall, 0.55)} />
			<circle cx={360} cy={720} r={7} fill="#ffd34a" />
			{porch ? (
				<>
					<rect x={-300} y={860} width={760} height={30} fill={darken(wall, 0.35)} />
					<rect x={-300} y={500} width={760} height={18} fill={darken(wall, 0.3)} />
					{[-260, 0, 420].map((x) => (
						<rect key={x} x={x} y={518} width={18} height={350} fill={lighten(wall, 0.2)} />
					))}
				</>
			) : null}
			{garden > 0 ? (
				<g>
					<rect x={500} y={840} width={360} height={50} rx={8} fill="#6a4228" />
					{[540, 620, 700, 780].map((x, i) => (
						<g key={x}>
							<path d={`M${x},850 q${-10},-90 0,${-170 - 40 * garden}`} stroke="#3a8a3a" strokeWidth={8} fill="none" />
							<circle cx={x + 18} cy={760 - 30 * garden + (i % 2) * 20} r={14 + 16 * garden} fill="#e23a2a" />
							<circle cx={x - 14} cy={720 - 50 * garden} r={12 + 12 * garden} fill="#ff4a2a" />
						</g>
					))}
				</g>
			) : null}
			{hoop ? (
				<g>
					<rect x={1700} y={420} width={16} height={480} fill="#3a3f4a" />
					<rect x={1610} y={380} width={190} height={130} rx={6} fill="#f6f6f6" stroke="#3a3f4a" strokeWidth={6} />
					<rect x={1675} y={430} width={60} height={46} fill="none" stroke="#e23a2a" strokeWidth={5} />
					<ellipse cx={1660} cy={500} rx={44} ry={9} fill="none" stroke="#ff6a2a" strokeWidth={6} />
					<path d={`M1620,503 L1636,560 L1684,560 L1700,503`} stroke="#fff" strokeWidth={3} fill="none" opacity={0.8} />
				</g>
			) : null}
			{Array.from({length: 10}).map((_, i) => (
				<rect key={i} x={1880 + i * 44} y={780} width={30} height={110} rx={4} fill={lighten(p.house, 0.2)} />
			))}
			<rect x={1870} y={810} width={460} height={12} fill={lighten(p.house, 0.1)} />
		</Svg>
	);
};

/* a round tree (foreground or mid) */
export const Tree: React.FC<{x: number; y: number; s?: number; c: string; f?: number; bloom?: number; fruit?: string}> = ({x, y, s = 1, c, f = 0, bloom = 0, fruit}) => (
	<g transform={`translate(${x},${y}) scale(${s}) rotate(${Math.sin(f / 40 + x) * 1.2})`}>
		<rect x={-14} y={-200} width={28} height={200} fill="#5a3a22" />
		<circle cx={0} cy={-250} r={120} fill={c} />
		<circle cx={-70} cy={-200} r={80} fill={darken(c, 0.1)} />
		<circle cx={70} cy={-210} r={86} fill={lighten(c, 0.08)} />
		{bloom > 0 ? Array.from({length: 26}).map((_, i) => <circle key={i} cx={(random('bl' + i) - 0.5) * 240} cy={-250 + (random('bm' + i) - 0.5) * 200} r={9 * bloom} fill="#ffd0e0" />) : null}
		{fruit ? Array.from({length: 10}).map((_, i) => <circle key={i} cx={(random('fr' + i) - 0.5) * 220} cy={-240 + (random('fs' + i) - 0.5) * 180} r={13} fill={fruit} />) : null}
	</g>
);

/* outer space: deep starfield and a soft nebula */
export const SpaceBG: React.FC<{f: number; tint?: string}> = ({f, tint = '#3a1f6a'}) => (
	<Svg>
		<defs>
			<radialGradient id="neb">
				<stop offset="0" stopColor={tint} stopOpacity={0.9} />
				<stop offset="1" stopColor={tint} stopOpacity={0} />
			</radialGradient>
		</defs>
		<rect x={-600} y={-500} width={3120} height={2100} fill="#04040f" />
		<ellipse cx={1300} cy={300} rx={900} ry={500} fill="url(#neb)" opacity={0.6} />
		<ellipse cx={300} cy={800} rx={700} ry={400} fill="url(#neb)" opacity={0.35} />
		{Array.from({length: 320}).map((_, i) => (
			<circle key={i} cx={random('ss' + i) * 3000 - 540} cy={random('st' + i) * 1900 - 400} r={0.7 + random('su' + i) * 2} fill="#fff" opacity={0.4 + 0.6 * Math.abs(Math.sin(f / 13 + i))} />
		))}
	</Svg>
);

/* glowing star / sun for space shots */
export const Star: React.FC<{x: number; y: number; r: number; c: string; f: number; id: string}> = ({x, y, r, c, f, id}) => (
	<g>
		<defs>
			<radialGradient id={'st' + id}>
				<stop offset="0" stopColor={c} stopOpacity={0.8} />
				<stop offset="1" stopColor={c} stopOpacity={0} />
			</radialGradient>
		</defs>
		<circle cx={x} cy={y} r={r * 3.2} fill={`url(#st${id})`} />
		<circle cx={x} cy={y} r={r * (1 + 0.03 * Math.sin(f / 4))} fill={c} />
		<circle cx={x - r * 0.2} cy={y - r * 0.2} r={r * 0.6} fill="#fff" opacity={0.4} />
	</g>
);

export const Planet: React.FC<{x: number; y: number; r: number; c?: string; land?: string; f?: number}> = ({x, y, r, c = '#2f7fe6', land = '#4ab04a', f = 0}) => {
	const cid = `pl${Math.round(x)}_${Math.round(y)}_${Math.round(r)}`;
	return (
		<g>
			<clipPath id={cid}>
				<circle cx={x} cy={y} r={r} />
			</clipPath>
			<circle cx={x} cy={y} r={r} fill={c} />
			<g clipPath={`url(#${cid})`}>
				<g transform={`translate(${((f * 0.6) % (r * 4)) - r * 2},0)`}>
					{[-2, 0, 2].map((k) => (
						<g key={k} transform={`translate(${k * r * 2},0)`}>
							<path d={`M${x - r * 0.6},${y - r * 0.4} q${r * 0.3},${-r * 0.3} ${r * 0.6},0 t${r * 0.2},${r * 0.5} q${-r * 0.4},${r * 0.2} ${-r * 0.8},${-r * 0.1} Z`} fill={land} />
							<path d={`M${x + r * 0.2},${y + r * 0.2} q${r * 0.3},${-r * 0.1} ${r * 0.5},${r * 0.2} t${-r * 0.1},${r * 0.4} q${-r * 0.3},0 ${-r * 0.4},${-r * 0.6} Z`} fill={land} />
						</g>
					))}
				</g>
				<circle cx={x + r * 0.35} cy={y + r * 0.3} r={r * 1.05} fill="#000" opacity={0.25} />
			</g>
		</g>
	);
};

/* TV news studio: desk, big screen (children drawn in screen box 540..1380 x 150..640) */
export const Studio: React.FC<{f: number; children?: React.ReactNode; ticker?: string; red?: boolean}> = ({f, children, ticker = 'BREAKING NEWS', red}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={2100} fill="#0e1430" />
		{Array.from({length: 14}).map((_, i) => (
			<rect key={i} x={-300 + i * 180} y={-100} width={60} height={1200} fill="#1b2450" opacity={0.6} />
		))}
		<rect x={520} y={130} width={880} height={530} rx={14} fill="#05070f" stroke="#3a4aa0" strokeWidth={10} />
		<clipPath id="scr">
			<rect x={540} y={150} width={840} height={490} />
		</clipPath>
		<g clipPath="url(#scr)">
			<rect x={540} y={150} width={840} height={490} fill={red ? '#3a0a14' : '#0a1640'} />
			{children}
		</g>
		<rect x={-600} y={860} width={3120} height={400} fill="#1a1f3a" />
		<path d="M360,700 L1560,700 L1620,900 L300,900 Z" fill="#2b3a7a" />
		<rect x={300} y={700} width={1320} height={22} fill="#5a7aff" opacity={0.8} />
		<rect x={-600} y={980} width={3120} height={70} fill="#c8102e" />
		<text x={-500 - ((f * 6) % 600)} y={1028} fontSize={40} fontFamily={FONT} fill="#fff">
			{(ticker + '   •   ').repeat(8)}
		</text>
	</Svg>
);

/* beach: sand, sea with moving waves, horizon */
export const Beach: React.FC<{f: number; mode: SkyMode}> = ({f, mode}) => {
	const p = SKY[mode];
	const sea = mode === 'night' || mode === 'dark' ? '#14305a' : mode === 'orange' || mode === 'gold' || mode === 'dawn' ? '#3a5a8a' : '#2a8ad8';
	return (
		<Svg>
			<rect x={-600} y={600} width={3120} height={260} fill={sea} />
			{Array.from({length: 6}).map((_, i) => (
				<path key={i} d={`M-600,${630 + i * 38} ${Array.from({length: 30}).map((_, k) => `q50,${(k % 2 ? 1 : -1) * 6} 110,0`).join(' ')}`} transform={`translate(${((f * (1 + i * 0.3)) % 220) - 110},0)`} stroke={lighten(sea, 0.3)} strokeWidth={4} fill="none" opacity={0.5} />
			))}
			<path d={`M-600,${840 + Math.sin(f / 20) * 10} Q300,${800 + Math.sin(f / 20) * 14} 960,${830 + Math.sin(f / 20) * 10} T2520,${820} L2520,1300 L-600,1300 Z`} fill="#fff" opacity={0.75} />
			<path d={`M-600,${860 + Math.sin(f / 20) * 10} Q300,${830 + Math.sin(f / 20) * 14} 960,${850 + Math.sin(f / 20) * 10} T2520,${840} L2520,1300 L-600,1300 Z`} fill={mode === 'night' ? '#b8a07a' : '#f0d49a'} />
			{Array.from({length: 40}).map((_, i) => (
				<circle key={i} cx={random('sd' + i) * 2600 - 300} cy={900 + random('se' + i) * 160} r={3} fill={darken(p.ground, 0.1)} opacity={0.4} />
			))}
		</Svg>
	);
};

/* baby sea turtle, walking cycle */
export const Turtle: React.FC<{x: number; y: number; s?: number; f: number; dir?: 1 | -1; seed?: number}> = ({x, y, s = 1, f, dir = 1, seed = 0}) => {
	const ph = f * 0.5 + seed;
	return (
		<g transform={`translate(${x},${y}) scale(${s * dir},${s})`}>
			<ellipse cx={0} cy={4} rx={30} ry={6} fill="#000" opacity={0.2} />
			<path d={`M-14,-4 l-14,${8 + Math.sin(ph) * 5} M14,-4 l16,${8 - Math.sin(ph) * 5}`} stroke="#2a5a3a" strokeWidth={8} strokeLinecap="round" />
			<ellipse cx={0} cy={-12} rx={26} ry={16} fill="#3a7a4a" />
			<path d="M-14,-20 l10,10 l10,-10 l8,10" stroke="#5aa06a" strokeWidth={3} fill="none" />
			<circle cx={30} cy={-12 + Math.sin(ph) * 2} r={10} fill="#4a8a5a" />
			<circle cx={34} cy={-15 + Math.sin(ph) * 2} r={2.5} fill="#fff" />
		</g>
	);
};

/* farm: wheat field rows, barn */
export const Farm: React.FC<{f: number; mode: SkyMode; bloom?: number}> = ({f, mode, bloom = 0}) => {
	const p = SKY[mode];
	return (
		<Svg>
			<rect x={-600} y={640} width={3120} height={700} fill={darken(p.grass, 0.05)} />
			<rect x={1450} y={440} width={300} height={240} fill="#b8322a" />
			<path d="M1420,450 L1600,330 L1780,450 Z" fill="#7a1f1a" />
			<rect x={1560} y={560} width={80} height={120} fill="#f2e6d0" />
			{Array.from({length: 6}).map((_, r) => (
				<g key={r}>
					{Array.from({length: 40}).map((_, i) => {
						const x = -400 + i * 70 + (r % 2) * 35;
						const y = 720 + r * 40;
						const sw = Math.sin(f / 18 + i * 0.4 + r) * 6;
						return (
							<g key={i}>
								<line x1={x} y1={y + 40} x2={x + sw} y2={y - 20} stroke="#c8a040" strokeWidth={4} />
								<ellipse cx={x + sw} cy={y - 26} rx={6} ry={14} fill="#e8c050" />
								{bloom > 0 ? <circle cx={x + sw + 4} cy={y - 38} r={5 * bloom} fill="#fff6c0" /> : null}
							</g>
						);
					})}
				</g>
			))}
		</Svg>
	);
};

/* woods with branches for owls and birds */
export const Woods: React.FC<{f: number; mode: SkyMode}> = ({f, mode}) => {
	const p = SKY[mode];
	return (
		<Svg>
			<rect x={-600} y={860} width={3120} height={400} fill={darken(p.grass, 0.1)} />
			{[-200, 420, 1300, 1950].map((x, i) => (
				<g key={x}>
					<rect x={x} y={-200} width={90} height={1100} fill="#4a3020" />
					<circle cx={x + 45} cy={-120} r={320} fill={darken(p.grass, 0.2 + i * 0.05)} />
				</g>
			))}
			<path d="M450,420 L1180,400" stroke="#4a3020" strokeWidth={34} strokeLinecap="round" />
			<path d="M1330,520 L1700,500" stroke="#4a3020" strokeWidth={28} strokeLinecap="round" />
			{Array.from({length: 18}).map((_, i) => {
				const lx = random('lv' + i) * 2400 - 200;
				const ly = 390 + random('lw' + i) * 140;
				return <ellipse key={i} cx={lx} cy={ly} rx={22} ry={10} fill={lighten(p.grass, 0.1)} transform={`rotate(${Math.sin(f / 20 + i) * 20} ${lx} ${ly})`} />;
			})}
		</Svg>
	);
};

export const Owl: React.FC<{x: number; y: number; s?: number; blink: number; look?: number}> = ({x, y, s = 1, blink, look = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<ellipse cx={0} cy={-60} rx={58} ry={74} fill="#8a6a4a" />
		<ellipse cx={0} cy={-40} rx={38} ry={44} fill="#d8c0a0" />
		<path d="M-50,-120 l14,-30 l14,24 M50,-120 l-14,-30 l-14,24" fill="#8a6a4a" stroke="#8a6a4a" strokeWidth={6} />
		{[-22, 22].map((dx) => (
			<g key={dx}>
				<circle cx={dx} cy={-86} r={22} fill="#fff" />
				<circle cx={dx + look * 8} cy={-86} r={11} fill="#111" />
				<rect x={dx - 24} y={-110} width={48} height={48 * blink} fill="#8a6a4a" />
			</g>
		))}
		<path d="M-6,-68 L6,-68 L0,-54 Z" fill="#f2b21c" />
	</g>
);

export const Bird: React.FC<{x: number; y: number; f: number; s?: number; c?: string}> = ({x, y, f, s = 1, c = '#2a3a5a'}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<path d={`M-30,${-Math.sin(f / 2) * 18} Q-14,-6 0,0 Q14,-6 30,${-Math.sin(f / 2) * 18}`} stroke={c} strokeWidth={7} fill="none" strokeLinecap="round" />
	</g>
);

/* a living room: couch, lamp, window full of light */
export const Living: React.FC<{f: number; glow?: string; night?: boolean}> = ({f, glow = '#ffcf8a', night}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={1400} fill={night ? '#2a2850' : '#e8d4b0'} />
		<rect x={-600} y={760} width={3120} height={30} fill={night ? '#1e1c3a' : '#c8a880'} />
		<rect x={1240} y={180} width={460} height={380} fill={glow} />
		<rect x={1240} y={180} width={460} height={380} fill="none" stroke="#6a4a2a" strokeWidth={16} />
		<line x1={1470} y1={180} x2={1470} y2={560} stroke="#6a4a2a" strokeWidth={10} />
		<rect x={-600} y={880} width={3120} height={400} fill={night ? '#3a2a40' : '#a8784a'} />
		<rect x={240} y={640} width={720} height={150} rx={40} fill="#c84a5a" />
		<rect x={200} y={720} width={800} height={150} rx={30} fill="#d85a6a" />
		<rect x={180} y={680} width={90} height={200} rx={30} fill="#b83a4a" />
		<rect x={930} y={680} width={90} height={200} rx={30} fill="#b83a4a" />
		<rect x={1080} y={500} width={10} height={380} fill="#2a2a32" />
		<path d="M1020,500 L1150,500 L1120,420 L1050,420 Z" fill="#f2d27a" />
		<circle cx={1085} cy={520} r={120 + Math.sin(f / 9) * 4} fill="#ffe3a0" opacity={0.15} />
		<rect x={420} y={260} width={240} height={170} fill="#f6f0e0" stroke="#6a4a2a" strokeWidth={10} />
		<circle cx={500} cy={330} r={26} fill={ORANGE_SUN} />
		<circle cx={580} cy={350} r={34} fill="#fff2a0" />
	</Svg>
);

/* hospital ward: teal wall, beds, monitor beeps */
export const Hospital: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={1400} fill="#5ab8b0" />
		<rect x={-600} y={620} width={3120} height={20} fill="#3a8a84" />
		<rect x={-600} y={880} width={3120} height={400} fill="#d8e8e4" />
		{[-120, 560, 1240, 1920].map((x, i) => (
			<g key={x}>
				<rect x={x} y={700} width={420} height={60} rx={10} fill="#f4f4f4" />
				<rect x={x} y={760} width={420} height={20} fill="#9aa8b0" />
				<rect x={x + 10} y={780} width={14} height={100} fill="#9aa8b0" />
				<rect x={x + 396} y={780} width={14} height={100} fill="#9aa8b0" />
				<rect x={x} y={650} width={110} height={60} rx={26} fill="#fff" />
				<path d={`M${x + 120},${700} q140,${-50 + Math.sin(f / 14 + i) * 6} 300,0`} fill="#7aa8e0" />
				<rect x={x + 340} y={420} width={110} height={80} rx={8} fill="#1a2030" />
				<polyline points={Array.from({length: 10}).map((_, k) => `${x + 350 + k * 10},${460 + ((k + Math.floor(f / 2)) % 5 === 0 ? -22 : 0)}`).join(' ')} stroke="#5aff9a" strokeWidth={3} fill="none" />
			</g>
		))}
		<rect x={760} y={120} width={400} height={90} rx={12} fill="#fff" />
		<text x={960} y={182} textAnchor="middle" fontSize={50} fontFamily={FONT} fill="#c8102e">
			ER • FULL
		</text>
	</Svg>
);

/* store with empty shelves and a SOLD OUT sign */
export const Store: React.FC<{f: number; sold?: number}> = ({f, sold = 1}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={1400} fill="#f2ead8" />
		<rect x={-600} y={880} width={3120} height={400} fill="#c8c0b0" />
		{[0, 1, 2].map((r) => (
			<g key={r}>
				{[-200, 520, 1240].map((x) => (
					<g key={x}>
						<rect x={x} y={300 + r * 190} width={560} height={16} fill="#8a7a6a" />
						{random('it' + x + r) > sold * 0.85
							? Array.from({length: 6}).map((_, k) => <rect key={k} x={x + 20 + k * 90} y={220 + r * 190} width={70} height={80} rx={6} fill={['#2a2a3a', '#3a2a4a', '#1a2a3a'][k % 3]} />)
							: null}
					</g>
				))}
			</g>
		))}
		<g transform={`translate(960,170) rotate(${-4 + Math.sin(f / 9) * 2})`}>
			<rect x={-260} y={-70} width={520} height={140} rx={14} fill="#c8102e" />
			<text x={0} y={30} textAnchor="middle" fontSize={84} fontFamily={FONT} fill="#fff">
				SOLD OUT
			</text>
		</g>
	</Svg>
);

/* bathroom with a window */
export const Bathroom: React.FC<{f: number}> = ({f}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={1400} fill="#bfe0ea" />
		{Array.from({length: 30}).map((_, i) => (
			<line key={i} x1={-600 + i * 110} y1={-500} x2={-600 + i * 110} y2={900} stroke="#a8ccd8" strokeWidth={3} />
		))}
		{Array.from({length: 14}).map((_, i) => (
			<line key={'h' + i} x1={-600} y1={i * 80} x2={2520} y2={i * 80} stroke="#a8ccd8" strokeWidth={3} />
		))}
		<rect x={-600} y={880} width={3120} height={400} fill="#8aa8b4" />
		<rect x={1500} y={180} width={260} height={320} rx={16} fill="#e8f4ff" stroke="#8aa0b0" strokeWidth={10} />
		<rect x={1500} y={180} width={260} height={320} rx={16} fill="#ffd27a" opacity={0.25 + 0.05 * Math.sin(f / 7)} />
	</Svg>
);
export const Tub: React.FC = () => (
	<g>
		<rect x={420} y={690} width={900} height={200} rx={70} fill="#ffffff" stroke="#c0d4dc" strokeWidth={8} />
		<rect x={470} y={880} width={40} height={40} rx={10} fill="#c0d4dc" />
		<rect x={1220} y={880} width={40} height={40} rx={10} fill="#c0d4dc" />
		<rect x={1270} y={600} width={20} height={100} fill="#a0b0b8" />
		<path d="M1280,600 q-60,0 -60,40" stroke="#a0b0b8" strokeWidth={14} fill="none" />
	</g>
);

/* road with mountains */
export const Road: React.FC<{mode: SkyMode; f: number}> = ({mode}) => {
	const p = SKY[mode];
	return (
		<Svg>
			{Array.from({length: 6}).map((_, i) => (
				<path key={'m' + i} d={`M${-600 + i * 600},700 l200,-${120 + (i % 3) * 50} l240,${120 + (i % 3) * 50} Z`} fill={darken(p.house, 0.4)} opacity={0.7} />
			))}
			<rect x={-600} y={700} width={3120} height={600} fill={darken(p.ground, 0.35)} />
			<rect x={-600} y={690} width={3120} height={16} fill={darken(p.ground, 0.1)} />
			{Array.from({length: 18}).map((_, i) => (
				<rect key={i} x={-600 + i * 190} y={870} width={100} height={14} fill="#f2e6a0" opacity={0.8} />
			))}
		</Svg>
	);
};

export const SimpleCar: React.FC<{x: number; y: number; c: string; s?: number; dir?: 1 | -1; lights?: boolean}> = ({x, y, c, s = 1, dir = 1, lights}) => (
	<g transform={`translate(${x},${y}) scale(${s * dir},${s})`}>
		<ellipse cx={0} cy={6} rx={170} ry={14} fill="#000" opacity={0.25} />
		<path d="M-160,-20 L-150,-70 L-80,-74 L-40,-130 L80,-130 L120,-74 L165,-60 L170,-20 Z" fill={c} />
		<path d="M-30,-120 L70,-120 L100,-76 L-60,-76 Z" fill="#bfe0ff" opacity={0.85} />
		<line x1={20} y1={-120} x2={20} y2={-76} stroke={c} strokeWidth={8} />
		<circle cx={-95} cy={-14} r={30} fill="#1a1a1e" />
		<circle cx={-95} cy={-14} r={12} fill="#9aa0aa" />
		<circle cx={105} cy={-14} r={30} fill="#1a1a1e" />
		<circle cx={105} cy={-14} r={12} fill="#9aa0aa" />
		<rect x={150} y={-62} width={18} height={12} rx={4} fill={lights ? '#fff6c0' : '#f2e6a0'} />
	</g>
);

/* classroom with a clock spinning madly */
export const School: React.FC<{f: number; night?: boolean}> = ({f, night}) => (
	<Svg>
		<rect x={-600} y={-500} width={3120} height={1400} fill={night ? '#2a3058' : '#f0e2c0'} />
		<rect x={-600} y={880} width={3120} height={400} fill={night ? '#2a2440' : '#b8946a'} />
		<rect x={300} y={160} width={1320} height={460} rx={10} fill="#24493a" stroke="#7a5a3a" strokeWidth={18} />
		<rect x={1700} y={160} width={300} height={300} fill={night ? '#0a1030' : '#bfe6ff'} stroke="#7a5a3a" strokeWidth={12} />
		<g transform={`translate(160,240)`}>
			<circle r={70} fill="#fff" stroke="#2a2a2a" strokeWidth={8} />
			<line x1={0} y1={0} x2={Math.sin(f / 4) * 50} y2={-Math.cos(f / 4) * 50} stroke="#c8102e" strokeWidth={6} strokeLinecap="round" />
			<line x1={0} y1={0} x2={Math.sin(f / 30) * 34} y2={-Math.cos(f / 30) * 34} stroke="#2a2a2a" strokeWidth={8} strokeLinecap="round" />
		</g>
	</Svg>
);

/* the old telescope on a tripod; tilt in degrees */
export const Telescope: React.FC<{x: number; y: number; tilt?: number; s?: number}> = ({x, y, tilt = -30, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<path d="M0,-150 L-60,0 M0,-150 L60,0 M0,-150 L0,0" stroke="#4a3a2a" strokeWidth={10} strokeLinecap="round" />
		<g transform={`translate(0,-160) rotate(${tilt})`}>
			<rect x={-110} y={-22} width={220} height={44} rx={10} fill="#c8a040" />
			<rect x={100} y={-30} width={40} height={60} rx={8} fill="#8a6a2a" />
			<rect x={-140} y={-12} width={40} height={24} rx={6} fill="#2a2a2a" />
			<rect x={-30} y={-26} width={14} height={52} fill="#8a6a2a" />
		</g>
	</g>
);

/* a phone with a glowing screen */
export const Phone: React.FC<{x: number; y: number; s?: number; rot?: number; screen?: string; children?: React.ReactNode}> = ({x, y, s = 1, rot = 0, screen = '#bfe0ff', children}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<rect x={-30} y={-55} width={60} height={110} rx={10} fill="#1a1a22" />
		<rect x={-25} y={-48} width={50} height={94} rx={6} fill={screen} />
		{children}
	</g>
);

export const Mug: React.FC<{x: number; y: number; s?: number; f?: number}> = ({x, y, s = 1, f = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-16} y={-34} width={32} height={34} rx={5} fill="#f2f2f2" />
		<path d="M16,-26 q14,0 14,10 q0,10 -14,10" stroke="#f2f2f2" strokeWidth={5} fill="none" />
		<path d={`M-6,-40 q${Math.sin(f / 6) * 6},-12 0,-24 M6,-40 q${Math.cos(f / 6) * 6},-12 0,-24`} stroke="#fff" strokeWidth={3} fill="none" opacity={0.6} />
	</g>
);

export const Ball: React.FC<{x: number; y: number; r?: number; spin?: number}> = ({x, y, r = 22, spin = 0}) => (
	<g transform={`translate(${x},${y}) rotate(${spin})`}>
		<circle r={r} fill="#ff7a2a" />
		<path d={`M${-r},0 L${r},0 M0,${-r} L0,${r}`} stroke="#3a1a0a" strokeWidth={2.5} />
		<path d={`M${-r * 0.7},${-r * 0.7} Q0,0 ${-r * 0.7},${r * 0.7} M${r * 0.7},${-r * 0.7} Q0,0 ${r * 0.7},${r * 0.7}`} stroke="#3a1a0a" strokeWidth={2.5} fill="none" />
	</g>
);
