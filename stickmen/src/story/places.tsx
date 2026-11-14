import React from 'react';
import {random} from 'remotion';
import {Svg} from '../engine/camera';
import {Bedroom, Corridor, ClassroomEve, Kitchen, KitchenTable, SchoolYard, Toilet} from '../kit/sets';
import {FONT} from '../kit/ui';

/* Locations made for this video. All draw a 1920x1080 world with the floor line at y = 900. */
type PP = {f: number; night?: boolean; [k: string]: any};
const G: React.FC<{id: string; stops: [number, string][]}> = ({id, stops}) => (
	<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
		{stops.map(([o, c], i) => (
			<stop key={i} offset={o} stopColor={c} />
		))}
	</linearGradient>
);
const Floorline: React.FC<{y?: number; c: string; c2?: string}> = ({y = 900, c, c2}) => (
	<>
		<rect x={-500} y={y} width={2920} height={500} fill={c} />
		<rect x={-500} y={y} width={2920} height={10} fill={c2 ?? 'rgba(0,0,0,0.18)'} />
	</>
);
const Window: React.FC<{x: number; y: number; w: number; h: number; lit?: boolean; c?: string}> = ({x, y, w, h, lit, c = '#9fd2f0'}) => (
	<g>
		<rect x={x - 8} y={y - 8} width={w + 16} height={h + 16} rx={6} fill="#f1ece0" />
		<rect x={x} y={y} width={w} height={h} fill={lit ? '#ffd98a' : c} />
		<path d={`M${x + w / 2},${y} V${y + h} M${x},${y + h / 2} H${x + w}`} stroke="#f1ece0" strokeWidth={6} />
	</g>
);
const Tree: React.FC<{x: number; y: number; s?: number; c?: string; trunk?: string}> = ({x, y, s = 1, c = '#4f9b5a', trunk = '#7a4a28'}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-14} y={-150} width={28} height={150} fill={trunk} />
		<circle cx={0} cy={-210} r={96} fill={c} />
		<circle cx={-64} cy={-170} r={64} fill={c} />
		<circle cx={64} cy={-170} r={64} fill={c} />
	</g>
);
const House: React.FC<{x: number; w: number; h: number; wall: string; roof: string; night?: boolean; door?: string; seed?: number}> = ({x, w, h, wall, roof, night, door = '#6b3a1e', seed = 0}) => (
	<g>
		<rect x={x} y={900 - h} width={w} height={h} fill={wall} />
		<path d={`M${x - 24},${900 - h} L${x + w / 2},${900 - h - w * 0.28} L${x + w + 24},${900 - h} Z`} fill={roof} />
		<rect x={x + w * 0.42} y={900 - h * 0.5} width={w * 0.16} height={h * 0.5} fill={door} />
		<Window x={x + w * 0.12} y={900 - h * 0.78} w={w * 0.2} h={h * 0.3} lit={night && random('hw' + seed) > 0.3} />
		<Window x={x + w * 0.68} y={900 - h * 0.78} w={w * 0.2} h={h * 0.3} lit={night && random('hv' + seed) > 0.4} />
	</g>
);
const Sky: React.FC<{id: string; night?: boolean; dusk?: boolean}> = ({id, night, dusk}) => (
	<>
		<defs>
			<G id={id} stops={night ? [[0, '#0e1230'], [1, '#2b2f66']] : dusk ? [[0, '#ff9a5c'], [1, '#ffd9a0']] : [[0, '#6fb8ec'], [1, '#d6efff']]} />
		</defs>
		<rect x={-500} y={-400} width={2920} height={1400} fill={`url(#${id})`} />
		{night ? Array.from({length: 40}).map((_, i) => <circle key={i} cx={random('sx' + i) * 2200 - 150} cy={random('sy' + i) * 520} r={1 + random('sr' + i) * 2} fill="#fff" opacity={0.7} />) : <ellipse cx={1500} cy={150} rx={90} ry={90} fill={dusk ? '#fff1c8' : '#fff7d0'} opacity={0.9} />}
	</>
);
const Cloud: React.FC<{x: number; y: number; f: number; s?: number}> = ({x, y, f, s = 1}) => (
	<g transform={`translate(${((x + f * 0.3) % 2600) - 300},${y}) scale(${s})`} opacity={0.85}>
		<ellipse cx={0} cy={0} rx={90} ry={30} fill="#fff" />
		<ellipse cx={-40} cy={-16} rx={50} ry={30} fill="#fff" />
		<ellipse cx={30} cy={-24} rx={56} ry={34} fill="#fff" />
	</g>
);

/* ---------------------------- the red hook stage ---------------------------- */
const Void: React.FC<PP> = ({f}) => (
	<Svg>
		<defs>
			<radialGradient id="vd" cx="50%" cy="48%" r="70%">
				<stop offset="0" stopColor="#8a1020" />
				<stop offset="0.6" stopColor="#4a0a14" />
				<stop offset="1" stopColor="#12040a" />
			</radialGradient>
		</defs>
		<rect x={-600} y={-400} width={3200} height={1700} fill="url(#vd)" />
		{Array.from({length: 26}).map((_, i) => {
			const t = (f * (0.4 + random('vs' + i) * 0.6) + random('vo' + i) * 900) % 900;
			return <circle key={i} cx={random('vx' + i) * 2200 - 150 + Math.sin(f / 40 + i) * 18} cy={1000 - t * 1.25} r={2 + random('vr' + i) * 5} fill="#ff5a6e" opacity={0.18 + random('va' + i) * 0.3} />;
		})}
		<Floorline c="#1c070d" c2="#ff2340" />
		<ellipse cx={960} cy={940} rx={600} ry={40} fill="#ff2340" opacity={0.12} />
	</Svg>
);

/* ------------------------------- cafeteria ------------------------------- */
const Cafe: React.FC<PP> = ({f}) => (
	<Svg>
		<rect x={-500} y={-300} width={2920} height={1300} fill="#f3e9cf" />
		<rect x={-500} y={560} width={2920} height={340} fill="#7fc3b0" />
		{[0, 1, 2, 3].map((i) => <Window key={i} x={200 + i * 440} y={150} w={260} h={300} c="#bfe3ff" />)}
		<g>
			<rect x={1180} y={500} width={640} height={110} fill="#b9bfcc" />
			<rect x={1180} y={610} width={640} height={290} fill="#8e96a8" />
			{[0, 1, 2, 3].map((i) => <rect key={i} x={1210 + i * 150} y={440} width={120} height={60} rx={8} fill={['#ffd34a', '#ff6a5a', '#6ad08a', '#7aa8ff'][i]} />)}
			<text x={1500} y={405} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#d6342f">LUNCH</text>
		</g>
		{[0, 1].map((i) => (
			<g key={i}>
				<rect x={120 + i * 520} y={730} width={400} height={26} rx={6} fill="#c99a62" />
				<rect x={160 + i * 520} y={756} width={16} height={144} fill="#6a5238" />
				<rect x={344 + i * 520} y={756} width={16} height={144} fill="#6a5238" />
			</g>
		))}
		<Floorline c="#d8c79b" />
		<g opacity={0.1 + 0.05 * Math.sin(f / 20)}><rect x={0} y={0} width={1920} height={1080} fill="#fff" /></g>
	</Svg>
);

/* ------------------------------ porch street ------------------------------ */
const Porch: React.FC<PP> = ({f, night}) => (
	<Svg>
		<Sky id="po-s" night={night} dusk={false} />
		<Cloud x={200} y={170} f={f} />
		<Cloud x={1300} y={260} f={f} s={0.8} />
		<Tree x={140} y={900} s={1.2} />
		<Tree x={1850} y={900} s={1.1} c="#3f8a50" />
		<House x={-120} w={720} h={430} wall="#e8c9a0" roof="#a8432f" night={night} seed={1} />
		<House x={1060} w={760} h={460} wall="#bcd3e8" roof="#3d5a80" night={night} seed={2} door="#ffd34a" />
		<rect x={-140} y={760} width={760} height={30} fill="#7a5a3a" />
		<rect x={-140} y={790} width={760} height={110} fill="#a98255" />
		{[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={-120 + i * 140} y={720} width={16} height={72} fill="#f1ece0" />)}
		<rect x={1040} y={760} width={800} height={30} fill="#7a5a3a" />
		<rect x={1040} y={790} width={800} height={110} fill="#a98255" />
		{[0, 1, 2, 3, 4, 5].map((i) => <rect key={i} x={1060 + i * 140} y={720} width={16} height={72} fill="#f1ece0" />)}
		<Floorline c="#6fa36b" c2="#4e7f4a" />
		<rect x={-500} y={900} width={2920} height={36} fill="#b9b2a0" />
	</Svg>
);

/* ---------------------------------- gym ---------------------------------- */
const Gym: React.FC<PP> = ({f}) => (
	<Svg>
		<defs><G id="gy-w" stops={[[0, '#c9893f'], [1, '#e8b66a']]} /></defs>
		<rect x={-500} y={-300} width={2920} height={1300} fill="url(#gy-w)" />
		{Array.from({length: 20}).map((_, i) => <rect key={i} x={-300 + i * 130} y={-300} width={6} height={1250} fill="#00000014" />)}
		<g transform="translate(1500,130)">
			<rect x={-90} y={0} width={180} height={120} fill="#fbf8ef" stroke="#14162a" strokeWidth={6} />
			<rect x={-34} y={44} width={68} height={50} fill="none" stroke="#e8772e" strokeWidth={6} />
			<rect x={-8} y={118} width={16} height={22} fill="#e8772e" />
			<path d="M-24,140 q24,70 48,0" stroke="#e8e8e8" strokeWidth={3} fill="none" />
			<rect x={-6} y={120} width={12} height={400} fill="#6a5a50" opacity={0.0} />
		</g>
		<rect x={-500} y={380} width={2920} height={14} fill="#d6342f" />
		<text x={400} y={350} fontSize={70} fontFamily={FONT} fontWeight={900} fill="#d6342f" opacity={0.85}>GO TIGERS</text>
		<Floorline c="#e0a458" c2="#fff" />
		<rect x={-500} y={930} width={2920} height={6} fill="#fff" opacity={0.7} />
		<ellipse cx={960} cy={960} rx={160} ry={30} fill="none" stroke="#fff" strokeWidth={5} opacity={0.7} />
		<g opacity={0.12}><rect x={0} y={0} width={1920} height={400} fill="#fff" /></g>
	</Svg>
);

/* ------------------------------- hospital hall ------------------------------- */
const Hospital: React.FC<PP> = ({f}) => (
	<Svg>
		<rect x={-500} y={-300} width={2920} height={1300} fill="#e8f3f1" />
		<rect x={-500} y={560} width={2920} height={340} fill="#bfe2dc" />
		<rect x={-500} y={556} width={2920} height={12} fill="#8fc7bd" />
		<g transform="translate(300,160)">
			<rect width={150} height={150} rx={20} fill="#fff" stroke="#d6342f" strokeWidth={6} />
			<path d="M75,30 V120 M30,75 H120" stroke="#d6342f" strokeWidth={26} />
		</g>
		{[0, 1, 2].map((i) => <Window key={i} x={760 + i * 360} y={170} w={220} h={260} c="#cfe9ff" />)}
		{[0, 1, 2].map((i) => (
			<g key={i}>
				<rect x={120 + i * 620} y={740} width={420} height={40} rx={10} fill="#4b8f80" />
				<rect x={120 + i * 620} y={690} width={420} height={60} rx={14} fill="#5aa896" />
				<rect x={140 + i * 620} y={780} width={14} height={120} fill="#3a6a60" />
				<rect x={506 + i * 620} y={780} width={14} height={120} fill="#3a6a60" />
			</g>
		))}
		<Floorline c="#cfd9d6" />
		<g opacity={0.9}>
			<rect x={920} y={60} width={110} height={44} rx={8} fill="#14162a" />
			<circle cx={Math.round(940 + (f % 60 < 30 ? 0 : 0))} cy={82} r={7} fill={f % 60 < 30 ? '#ff4d4d' : '#6e2230'} />
			<text x={985} y={92} textAnchor="middle" fontSize={26} fontFamily={FONT} fontWeight={800} fill="#fff">24</text>
		</g>
	</Svg>
);

/* ------------------------------ back steps (yard) ------------------------------ */
const Steps: React.FC<PP> = ({f}) => (
	<Svg>
		<Sky id="st-s" dusk />
		<Cloud x={300} y={190} f={f} />
		<Cloud x={1400} y={120} f={f} s={0.7} />
		<Tree x={160} y={900} s={1.3} c="#5aa862" />
		<Tree x={1700} y={900} s={1.15} c="#4a9a56" />
		<rect x={-600} y={470} width={1500} height={430} fill="#e9d2a8" />
		<path d="M-640,470 L150,300 L940,470 Z" fill="#a8432f" />
		<Window x={80} y={560} w={200} h={200} lit />
		<rect x={540} y={560} width={190} height={340} fill="#6b3a1e" />
		<rect x={500} y={900 - 36} width={270} height={36} fill="#b9b2a0" />
		<rect x={540} y={864 - 36} width={190} height={36} fill="#c9c2b0" />
		<rect x={1100} y={640} width={700} height={260} fill="#c9a06a" />
		{Array.from({length: 9}).map((_, i) => <rect key={i} x={1100 + i * 80} y={620} width={40} height={280} fill="#d9b680" />)}
		<Floorline c="#78b36e" c2="#5a9650" />
		{Array.from({length: 40}).map((_, i) => <path key={i} d={`M${random('gx' + i) * 2200 - 150},${905 + random('gy' + i) * 100} q4,-26 8,0`} stroke="#4e8f46" strokeWidth={3} fill="none" />)}
	</Svg>
);

/* ------------------------------- bus stop street ------------------------------- */
const BusStop: React.FC<PP> = ({f, night}) => (
	<Svg>
		<Sky id="bs-s" night={night} />
		<Cloud x={100} y={140} f={f} />
		<Cloud x={1100} y={210} f={f} s={0.9} />
		{[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-100 + i * 480} y={560 - (i % 3) * 110} width={300} height={340 + (i % 3) * 110} fill={['#9fb4d6', '#c9a98a', '#a9bcd0', '#d6b48a', '#9fb4d6'][i]} />)}
		{[0, 1, 2, 3, 4].flatMap((i) => [0, 1, 2].map((j) => <rect key={i + '-' + j} x={-60 + i * 480 + j * 86} y={600 - (i % 3) * 110 + (j % 2) * 20} width={52} height={70} fill={night ? '#ffd98a' : '#e9f4ff'} opacity={0.8} />))}
		<g transform="translate(1040,0)">
			<rect x={0} y={560} width={560} height={14} fill="#37405a" />
			<rect x={0} y={574} width={10} height={326} fill="#37405a" />
			<rect x={550} y={574} width={10} height={326} fill="#37405a" />
			<rect x={10} y={580} width={540} height={230} fill="#cfe9ff" opacity={0.25} />
			<rect x={50} y={770} width={430} height={20} rx={6} fill="#8a5a2b" />
			<rect x={400} y={430} width={110} height={130} rx={6} fill="#ffd34a" />
			<text x={455} y={520} textAnchor="middle" fontSize={64} fontFamily={FONT} fontWeight={900} fill="#14162a">24</text>
		</g>
		<Floorline c="#6c7280" c2="#e8e8e8" />
		<rect x={-500} y={900} width={2920} height={90} fill="#575d6a" />
		<rect x={-500} y={990} width={2920} height={90} fill="#454b57" />
		{Array.from({length: 12}).map((_, i) => <rect key={i} x={-300 + i * 240 - (f * 6) % 240} y={995} width={120} height={10} fill="#fbf8ef" opacity={0.5} />)}
	</Svg>
);

const Street: React.FC<PP> = BusStop;

export const PLACES = {
	bedroom: ({f, night}: PP) => <Bedroom f={f} night={night} />,
	bath: ({f}: PP) => <Toilet f={f} />,
	kitchen: ({night}: PP) => (
		<>
			<Kitchen night={night} />
			<KitchenTable night={night} />
		</>
	),
	corridor: ({f}: PP) => <Corridor f={f} />,
	yard: ({f}: PP) => <SchoolYard f={f} />,
	class: () => <ClassroomEve />,
	cafe: Cafe,
	porch: Porch,
	gym: Gym,
	hospital: Hospital,
	steps: Steps,
	busstop: BusStop,
	street: Street,
	void: Void,
};
export type PlaceKey = keyof typeof PLACES;
