import React from 'react';
import {random} from 'remotion';
import {Layer, Svg} from '../engine/camera';
import {darken, lighten, mix} from '../engine/color';
import {CrowdRow} from '../kit/kit';
import {FONT} from '../kit/ui';
import {Bedroom, Corridor, Kitchen} from '../kit/sets';
import {Beach, CityDay} from '../kit/world';

/* Locations of the "Citizen President" story. Every place has: a far layer (wall / sky),
   a mid layer with big props and at least three living details (flags sway, lights blink,
   screens flicker, cars drive...). `f` is the global frame. Floor line = y 900. */

const W = {x: -500, w: 2900};
const Grd: React.FC<{id: string; a: string; b: string; c?: string}> = ({id, a, b, c}) => (
	<linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
		<stop offset="0" stopColor={a} />
		{c ? <stop offset="0.55" stopColor={c} /> : null}
		<stop offset="1" stopColor={b} />
	</linearGradient>
);
const Flag: React.FC<{x: number; y: number; f: number; s?: number; seed?: number}> = ({x, y, f, s = 1, seed = 0}) => {
	const w = Math.sin(f / 14 + seed) * 10;
	return (
		<g transform={`translate(${x},${y}) scale(${s})`}>
			<rect x={-4} y={0} width={8} height={520} fill="#c9a24a" />
			<circle cx={0} cy={-4} r={12} fill="#e6c25a" />
			<path d={`M4,20 Q${70 + w},${4 + w} 150,22 L150,${150} Q${80 - w},${172} 4,148 Z`} fill="#f4f1ea" />
			{[0, 1, 2, 3, 4].map((i) => (
				<path key={i} d={`M4,${22 + i * 25} Q${70 + w},${6 + i * 25 + w} 150,${24 + i * 25} L150,${44 + i * 25} Q${80 - w},${28 + i * 25} 4,${42 + i * 25} Z`} fill={i % 2 ? '#f4f1ea' : '#d9433d'} opacity={0.95} />
			))}
			<path d={`M4,22 Q${40 + w / 2},12 70,22 L70,86 Q${40 - w / 2},78 4,84 Z`} fill="#2d4a9a" />
		</g>
	);
};
const Win: React.FC<{x: number; y: number; w: number; h: number; sky?: [string, string]; f: number; id: string; curtain?: string}> = ({x, y, w, h, sky = ['#9fd2f0', '#eaf6fb'], f, id, curtain = '#b8923a'}) => (
	<g>
		<defs>
			<Grd id={id} a={sky[0]} b={sky[1]} />
		</defs>
		<rect x={x - 10} y={y - 10} width={w + 20} height={h + 20} fill="#efe6d0" />
		<rect x={x} y={y} width={w} height={h} fill={`url(#${id})`} />
		<ellipse cx={x + ((f * 0.4) % (w + 200)) - 100} cy={y + h * 0.35} rx={60} ry={14} fill="#fff" opacity={0.7} />
		<rect x={x + w / 2 - 3} y={y} width={6} height={h} fill="#efe6d0" />
		<path d={`M${x - 36},${y - 30} Q${x - 10 + Math.sin(f / 40) * 5},${y + h / 2} ${x - 40},${y + h + 30} L${x + 36},${y + h + 20} Q${x + 24},${y + h / 2} ${x + 34},${y - 30} Z`} fill={curtain} />
		<path d={`M${x + w + 36},${y - 30} Q${x + w + 10 + Math.sin(f / 40 + 2) * 5},${y + h / 2} ${x + w + 40},${y + h + 30} L${x + w - 36},${y + h + 20} Q${x + w - 24},${y + h / 2} ${x + w - 34},${y - 30} Z`} fill={curtain} />
	</g>
);
const Floor: React.FC<{y?: number; a: string; b: string; id: string}> = ({y = 880, a, b, id}) => (
	<g>
		<defs>
			<Grd id={id} a={a} b={b} />
		</defs>
		<rect x={W.x} y={y} width={W.w} height={400} fill={`url(#${id})`} />
		<rect x={W.x} y={y} width={W.w} height={5} fill="#000" opacity={0.18} />
	</g>
);

/* ------------------------------- OVAL OFFICE ------------------------------- */
export const Oval: React.FC<{f: number; night?: boolean; flash?: boolean}> = ({f, night, flash}) => {
	const wall = night ? ['#2a2f55', '#3d3a63'] : ['#efe2bd', '#e3cf9a'];
	return (
		<>
			<Layer depth={1.7}>
				<Svg>
					<defs>
						<Grd id="ov-w" a={wall[0]} b={wall[1]} />
					</defs>
					<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#ov-w)" />
					{[500, 960, 1420].map((x, i) => (
						<Win key={i} id={'ovw' + i} x={x - 110} y={120} w={220} h={420} f={f} sky={night ? ['#0b1030', '#2a2f63'] : ['#8fc7ec', '#e8f6fb']} curtain={night ? '#5a3a4a' : '#b8923a'} />
					))}
					{night ? [0, 1, 2].map((i) => <circle key={i} cx={440 + i * 460 + 80} cy={190 + (i % 2) * 40} r={4} fill="#fff" opacity={0.6 + 0.4 * Math.sin(f / 9 + i)} />) : null}
					<rect x={W.x} y={560} width={W.w} height={16} fill={darken(wall[1], 0.25)} />
					{[200, 1700].map((x, i) => (
						<g key={i}>
							<rect x={x - 70} y={190} width={140} height={190} fill="#6a4a2a" />
							<rect x={x - 58} y={202} width={116} height={166} fill={i ? '#7f9bb5' : '#b58f6a'} />
							<ellipse cx={x} cy={290} rx={34} ry={44} fill="#e3b690" />
						</g>
					))}
				</Svg>
			</Layer>
			<Layer depth={1.25}>
				<Svg>
					<Floor id="ov-f" a={night ? '#2d2a44' : '#6f5a46'} b={night ? '#1f1c33' : '#4a3a2c'} />
					<ellipse cx={960} cy={960} rx={780} ry={90} fill={night ? '#26396a' : '#2d4a9a'} opacity={0.9} />
					<ellipse cx={960} cy={960} rx={520} ry={58} fill="none" stroke="#e6c25a" strokeWidth={5} opacity={0.8} />
					<Flag x={110} y={160} f={f} s={1.15} />
					<Flag x={1760} y={160} f={f} s={1.15} seed={2} />
					{/* the desk */}
					<g>
						<rect x={1180} y={640} width={560} height={26} fill={night ? '#5a3f2e' : '#8a5a36'} />
						<rect x={1200} y={666} width={520} height={210} fill={night ? '#4a3225' : '#6f4527'} />
						<rect x={1230} y={690} width={200} height={170} fill="#00000022" />
						{!night ? <rect x={1560} y={612} width={90} height={30} fill="#f4f1ea" /> : null}
						<rect x={1330} y={604} width={70} height={36} fill="#2b2f3a" />
						<ellipse cx={1620} cy={612} rx={28} ry={8} fill="#d9433d" />
						{/* lamp */}
						<path d="M1690,640 L1690,560 L1640,540" stroke="#c9a24a" strokeWidth={8} fill="none" />
						<path d="M1620,530 L1664,530 L1652,556 L1632,556 Z" fill={night ? '#ffe9a8' : '#c9a24a'} />
						{night ? <path d="M1626,556 L1540,900 L1760,900 L1658,556 Z" fill="#ffe9a8" opacity={0.14 + 0.03 * Math.sin(f / 5)} /> : null}
					</g>
					{/* clock + bird fx */}
					<g transform="translate(960,70)">
						<circle r={40} fill="#f4f1ea" stroke="#6a4a2a" strokeWidth={6} />
						<line x1={0} y1={0} x2={0} y2={-26} stroke="#222" strokeWidth={4} transform={`rotate(${f * 0.4})`} />
						<line x1={0} y1={0} x2={14} y2={0} stroke="#222" strokeWidth={4} transform={`rotate(${f * 0.03})`} />
					</g>
					{flash ? <rect x={W.x} y={-300} width={W.w} height={1400} fill="#fff" opacity={0.0} /> : null}
				</Svg>
			</Layer>
		</>
	);
};

/* ------------------------------- BANQUET / DINNER ------------------------------- */
export const Banquet: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="bq-w" a="#5a1f33" b="#8a3a4a" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#bq-w)" />
				{[300, 960, 1620].map((x, i) => (
					<g key={i}>
						<rect x={x - 100} y={130} width={200} height={380} rx={8} fill="#2b0f1c" />
						<rect x={x - 88} y={142} width={176} height={356} rx={4} fill={['#3a5a8a', '#7a5a3a', '#4a7a5a'][i]} />
					</g>
				))}
				{/* chandelier */}
				<g transform={`translate(960,${40 + Math.sin(f / 30) * 4})`}>
					<line x1={0} y1={-200} x2={0} y2={40} stroke="#e6c25a" strokeWidth={5} />
					<path d="M-200,60 Q0,150 200,60 L170,40 Q0,110 -170,40 Z" fill="#e6c25a" />
					{[-170, -110, -50, 10, 70, 130, 170].map((x, i) => (
						<g key={i}>
							<rect x={x - 5} y={10 + Math.abs(x) * 0.06} width={10} height={26} fill="#fff6dc" />
							<ellipse cx={x} cy={6 + Math.abs(x) * 0.06} rx={7} ry={11 + Math.sin(f / 4 + i) * 2} fill="#ffd36a" />
						</g>
					))}
				</g>
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<Floor id="bq-f" a="#3a1522" b="#220c15" />
				<rect x={100} y={650} width={1720} height={36} fill="#f4efe6" />
				<rect x={120} y={686} width={1680} height={200} fill="#e8dfd0" />
				<rect x={120} y={700} width={1680} height={14} fill="#c9bfae" />
				{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
					<g key={i} transform={`translate(${240 + i * 210},${640})`}>
						<ellipse cx={0} cy={6} rx={56} ry={13} fill="#fff" />
						{i % 2 === 0 ? (
							<g>
								<rect x={-52} y={-26} width={104} height={26} fill="#d9a548" />
								<circle cx={-14} cy={-14} r={9} fill="#d9433d" />
								<circle cx={14} cy={-12} r={8} fill="#6bbd5a" />
							</g>
						) : null}
						<path d={`M-10,-34 q8,-14 0,-28 q-8,-14 4,-28`} stroke="#fff" strokeWidth={5} fill="none" opacity={0.35 + 0.2 * Math.sin(f / 6 + i)} />
					</g>
				))}
				{/* waiter crossing */}
				<g opacity={0.0} />
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- FOOTBALL FIELD / BLEACHERS ------------------------------- */
export const Field: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={2}>
			<Svg>
				<defs>
					<Grd id="fd-s" a="#6fb8ee" b="#e8f6fb" />
				</defs>
				<rect x={W.x} y={-400} width={W.w} height={1100} fill="url(#fd-s)" />
				{[0, 1, 2, 3].map((i) => (
					<ellipse key={i} cx={((i * 700 + f * (0.3 + i * 0.1)) % 3200) - 600} cy={120 + i * 70} rx={170} ry={36} fill="#fff" opacity={0.85} />
				))}
				<path d="M-500,560 Q300,420 900,540 T2400,500 L2400,700 L-500,700 Z" fill="#6aa86a" opacity={0.8} />
			</Svg>
		</Layer>
		<Layer depth={1.4}>
			<Svg>
				<rect x={W.x} y={560} width={W.w} height={330} fill="#6a6a78" />
				{[0, 1, 2, 3].map((i) => (
					<rect key={i} x={W.x} y={560 + i * 82} width={W.w} height={10} fill="#4a4a58" />
				))}
				<CrowdRow n={26} x0={-200} x1={2100} floor={640} s={0.5} mode="dance" seed="bl1" />
				<CrowdRow n={24} x0={-100} x1={2000} floor={725} s={0.55} mode="dance" seed="bl2" />
				<CrowdRow n={22} x0={0} x1={1950} floor={810} s={0.6} mode="stand" seed="bl3" />
			</Svg>
		</Layer>
		<Layer depth={1.2}>
			<Svg>
				<defs>
					<Grd id="fd-g" a="#58a85a" b="#2f6f36" />
				</defs>
				<rect x={W.x} y={885} width={W.w} height={400} fill="url(#fd-g)" />
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<rect key={i} x={W.x + i * 500} y={885} width={250} height={400} fill="#fff" opacity={0.05} />
				))}
				<rect x={W.x} y={900} width={W.w} height={5} fill="#fff" opacity={0.6} />
				{/* banner */}
				<rect x={380} y={540} width={1160} height={90} fill="#d9433d" />
				<text x={960} y={602} textAnchor="middle" fontSize={54} fontFamily={FONT} fill="#fff" fontWeight={800}>
					WELCOME, MR. PRESIDENT
				</text>
			</Svg>
		</Layer>
	</>
);
export const Helicopter: React.FC<{f: number; x: number; y: number; s?: number}> = ({f, x, y, s = 1}) => (
	<g transform={`translate(${x},${y + Math.sin(f / 18) * 10}) scale(${s})`}>
		<ellipse cx={0} cy={0} rx={150} ry={80} fill="#3a5a8a" />
		<path d="M110,-10 L420,-30 L420,10 L110,40 Z" fill="#2f4a73" />
		<rect x={-130} y={-120} width={260} height={10} fill="#222" opacity={0.4 + 0.5 * Math.abs(Math.sin(f * 2))} transform={`scaleX(${0.6 + 0.4 * Math.sin(f * 1.3)})`} />
		<rect x={-8} y={-112} width={16} height={32} fill="#222" />
		<ellipse cx={-70} cy={-6} rx={64} ry={46} fill="#cfe9ff" opacity={0.9} />
		<line x1={-130} y1={96} x2={130} y2={96} stroke="#222" strokeWidth={8} />
		<line x1={-90} y1={70} x2={-100} y2={96} stroke="#222" strokeWidth={6} />
		<line x1={90} y1={70} x2={100} y2={96} stroke="#222" strokeWidth={6} />
		<circle cx={420} cy={-10} r={22 + Math.sin(f * 2.5) * 5} fill="#222" opacity={0.3} />
	</g>
);

/* ------------------------------- UN HALL ------------------------------- */
export const UNHall: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="un-w" a="#15346a" b="#2a5a9a" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#un-w)" />
				<circle cx={960} cy={300} r={170} fill="#4a8ad0" opacity={0.5} />
				<circle cx={960} cy={300} r={120} fill="none" stroke="#cfe6ff" strokeWidth={6} opacity={0.8} />
				{[0, 1, 2, 3].map((i) => (
					<ellipse key={i} cx={960} cy={300} rx={120} ry={30 + i * 26} fill="none" stroke="#cfe6ff" strokeWidth={3} opacity={0.6} transform={`rotate(${i * 45 + f * 0.3},960,300)`} />
				))}
				{Array.from({length: 18}).map((_, i) => (
					<g key={i} transform={`translate(${-300 + i * 150},130)`}>
						<rect x={0} y={0} width={5} height={110} fill="#ddd" />
						<path d={`M5,6 Q40,${-4 + Math.sin(f / 12 + i) * 6} 78,8 L78,60 Q40,${50 + Math.sin(f / 12 + i) * 6} 5,58 Z`} fill={['#d9433d', '#f2b21c', '#3aa37a', '#f4f1ea', '#2d4a9a', '#8b5cf6'][i % 6]} />
					</g>
				))}
			</Svg>
		</Layer>
		<Layer depth={1.3}>
			<Svg>
				<Floor id="un-f" a="#1d2a46" b="#10192e" />
				{[0, 1, 2].map((r) => (
					<g key={r}>
						{Array.from({length: 11}).map((_, i) => (
							<g key={i} transform={`translate(${-100 + i * 220 + (r % 2) * 90},${690 + r * 70})`}>
								<rect x={-70} y={0} width={140} height={34 + r * 4} rx={8} fill={darken('#5a3a6a', r * 0.15)} />
							</g>
						))}
					</g>
				))}
				<rect x={760} y={640} width={400} height={260} fill="#d8c8a0" />
				<rect x={740} y={620} width={440} height={34} fill="#efe6d0" />
				<rect x={940} y={560} width={6} height={70} fill="#555" />
				<circle cx={943} cy={552} r={10} fill="#333" />
				<path d={`M${900},${540} Q${943},${520} ${986},${540}`} stroke="#333" strokeWidth={4} fill="none" />
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- TV STUDIO ------------------------------- */
export const Studio: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="tv-w" a="#2a1250" b="#7a2a7a" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#tv-w)" />
				{[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => {
					const h = 160 + random('tvb' + i) * 260;
					return <rect key={i} x={-200 + i * 260} y={640 - h} width={170} height={h} fill="#1c0a3a" />;
				})}
				{Array.from({length: 40}).map((_, i) => (
					<rect key={i} x={-180 + (i % 10) * 260 + (i % 4) * 30} y={440 + Math.floor(i / 10) * 40} width={12} height={16} fill="#ffe08a" opacity={random('tvw' + i + Math.floor(f / 40)) > 0.4 ? 0.9 : 0.1} />
				))}
				{['#ff3a8a', '#3acaff', '#ffe03a'].map((c, i) => (
					<path key={i} d={`M${300 + i * 650},-100 L${100 + i * 650 + Math.sin(f / 20 + i) * 60},900 L${520 + i * 650 + Math.sin(f / 20 + i) * 60},900 Z`} fill={c} opacity={0.12} />
				))}
				<rect x={600} y={180} width={720} height={90} rx={12} fill="#14082c" stroke="#ff3a8a" strokeWidth={6} />
				<text x={960} y={246} textAnchor="middle" fontSize={64} fontFamily={FONT} fill="#ff6aa8" fontWeight={800} opacity={0.75 + 0.25 * Math.sin(f / 7)}>
					LATE NIGHT LIVE
				</text>
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<Floor id="tv-f" a="#3a1a5a" b="#1c0a30" />
				<rect x={1080} y={660} width={640} height={240} fill="#e8d6f2" />
				<rect x={1060} y={640} width={680} height={30} fill="#fff" />
				<rect x={1500} y={600} width={60} height={40} fill="#f2b21c" />
				<path d="M-300,900 Q960,820 2200,900" fill="#1c0a30" opacity={0.0} />
				{Array.from({length: 14}).map((_, i) => (
					<g key={i} transform={`translate(${-150 + i * 160},${1010 + (i % 2) * 18})`}>
						<circle r={38} fill="#0d0620" />
						<rect x={-48} y={30} width={96} height={80} fill="#0d0620" />
					</g>
				))}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- SITUATION ROOM ------------------------------- */
export const Situation: React.FC<{f: number; alert?: boolean}> = ({f, alert}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="sr-w" a="#0b1424" b="#17243d" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#sr-w)" />
				{/* wall map */}
				<rect x={300} y={90} width={1320} height={560} rx={10} fill="#0d2a44" stroke="#4a7aa8" strokeWidth={8} />
				<path d="M300,330 Q500,300 640,360 T900,420 T1100,340 T1300,420 T1620,360 L1620,650 L300,650 Z" fill="#14507a" opacity={0.9} />
				<path d="M900,420 Q1000,300 1160,330 T1400,300 L1400,420 Z" fill="#2a8a5a" opacity={0.85} />
				<path d="M640,360 L760,330 L820,420 L700,450 Z" fill="#2a8a5a" opacity={0.85} />
				{/* storm swirl */}
				<g transform={`translate(560,290) rotate(${f * 1.2})`}>
					{[0, 1, 2, 3].map((i) => (
						<path key={i} d={`M0,0 Q${60 + i * 12},${-20} ${90 + i * 22},${40 + i * 10}`} stroke="#e8f4ff" strokeWidth={14} fill="none" opacity={0.7} transform={`rotate(${i * 90})`} />
					))}
					<circle r={14} fill="#0d2a44" />
				</g>
				<path d="M560,290 L1240,560 L1100,640 Z" fill="#ff3a3a" opacity={0.35 + (alert ? 0.15 * Math.sin(f / 4) : 0)} />
				<path d="M560,290 L1240,560 L1100,640 Z" fill="none" stroke="#ff6a6a" strokeWidth={5} strokeDasharray="14 10" />
				<circle cx={1170} cy={560} r={18 + Math.sin(f / 5) * 4} fill="#ffd23a" opacity={0.9} />
				{Array.from({length: 18}).map((_, i) => (
					<circle key={i} cx={420 + i * 70} cy={640 - (i % 3) * 10} r={0} fill="none" />
				))}
				{[420, 1480].map((x, i) => (
					<g key={i}>
						<rect x={x - 90} y={700} width={180} height={120} fill="#0d1a2c" stroke="#3a5a84" strokeWidth={5} />
						<polyline points={`${x - 76},780 ${x - 40},${740 + Math.sin(f / 6 + i) * 10} ${x},780 ${x + 40},${750 + Math.cos(f / 6) * 12} ${x + 76},770`} stroke="#3aff9a" strokeWidth={4} fill="none" />
					</g>
				))}
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<Floor id="sr-f" a="#1a2234" b="#0e1422" />
				<ellipse cx={960} cy={800} rx={820} ry={120} fill="#2b3a52" />
				<ellipse cx={960} cy={790} rx={780} ry={100} fill="#3a4a66" />
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<g key={i} transform={`translate(${300 + i * 232},760)`}>
						<rect x={-44} y={-30} width={88} height={56} rx={4} fill="#101826" />
						<rect x={-38} y={-24} width={76} height={42} fill={['#2a6aff', '#3aff9a', '#ff6a3a'][i % 3]} opacity={0.55 + 0.25 * Math.sin(f / 5 + i * 2)} />
					</g>
				))}
				{alert ? <rect x={W.x} y={-300} width={W.w} height={1400} fill="#ff1a1a" opacity={0.08 + 0.08 * Math.sin(f / 5)} /> : null}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- HOSPITAL ------------------------------- */
export const Hospital: React.FC<{f: number; flood?: boolean}> = ({f, flood}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="hp-w" a="#d8efe9" b="#b8dcd2" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#hp-w)" />
				{[0, 1, 2, 3, 4, 5].map((i) => (
					<g key={i} transform={`translate(${-250 + i * 480},200)`}>
						<rect x={0} y={0} width={110} height={460} fill="#f4fbf9" stroke="#9ac4ba" strokeWidth={6} />
						<circle cx={55} cy={90} r={24} fill="none" stroke="#6abaa8" strokeWidth={5} />
					</g>
				))}
				<rect x={820} y={100} width={280} height={90} rx={10} fill="#d9433d" />
				<rect x={940} y={115} width={40} height={60} fill="#fff" />
				<rect x={920} y={135} width={80} height={20} fill="#fff" />
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<Floor id="hp-f" a="#a8cfc4" b="#7ea99e" />
				{[0, 1, 2, 3].map((i) => (
					<g key={i} transform={`translate(${200 + i * 520},720)`}>
						<rect x={0} y={0} width={330} height={26} fill="#fff" />
						<rect x={10} y={26} width={8} height={150} fill="#789" />
						<rect x={312} y={26} width={8} height={150} fill="#789" />
						<rect x={0} y={-40} width={330} height={46} rx={20} fill="#f2f6f6" />
						<rect x={260} y={-80} width={6} height={100} fill="#789" />
						<circle cx={263} cy={-86} r={16} fill="#6ac0ff" opacity={0.8} />
						<polyline points={`40,-100 80,${-100 + Math.sin(f / 3 + i) * 12} 120,-100 160,${-110 + Math.cos(f / 3) * 14} 200,-100`} stroke="#3aff9a" strokeWidth={4} fill="none" />
					</g>
				))}
				{flood ? (
					<g>
						<rect x={W.x} y={720 + Math.sin(f / 12) * 6} width={W.w} height={400} fill="#3a7ab0" opacity={0.65} />
						{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
							<ellipse key={i} cx={(i * 340 + f * 3) % 2600 - 300} cy={730 + Math.sin(f / 9 + i) * 5} rx={90} ry={8} fill="#fff" opacity={0.35} />
						))}
					</g>
				) : null}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- HIGHWAY (evacuation) ------------------------------- */
const CarShape: React.FC<{x: number; y: number; c: string; s?: number; dir?: 1 | -1; jam?: boolean}> = ({x, y, c, s = 1, dir = 1, jam}) => (
	<g transform={`translate(${x},${y}) scale(${dir * s},${s})`}>
		<rect x={-70} y={-44} width={140} height={44} rx={12} fill={c} />
		<path d="M-40,-44 L-24,-78 L30,-78 L48,-44 Z" fill={darken(c, 0.15)} />
		<path d="M-30,-46 L-18,-72 L-2,-72 L-2,-46 Z M6,-46 L6,-72 L26,-72 L40,-46 Z" fill="#cfe9ff" opacity={0.9} />
		<circle cx={-40} cy={2} r={15} fill="#222" />
		<circle cx={42} cy={2} r={15} fill="#222" />
		<rect x={-72} y={-34} width={10} height={14} fill={jam ? '#ff3a3a' : '#ffe08a'} />
	</g>
);
export const Highway: React.FC<{f: number; jam?: boolean; night?: boolean; flow?: number; bridge?: boolean}> = ({f, jam, night, flow = 1, bridge}) => (
	<>
		<Layer depth={2}>
			<Svg>
				<defs>
					<Grd id="hw-s" a={night ? '#0b1030' : '#6a5a9a'} b={night ? '#3a3f6a' : '#ffb27a'} />
				</defs>
				<rect x={W.x} y={-400} width={W.w} height={1100} fill="url(#hw-s)" />
				{Array.from({length: 14}).map((_, i) => (
					<rect key={i} x={-200 + i * 190} y={560 - random('sk' + i) * 220} width={120} height={300} fill={night ? '#14183a' : '#7a6a9a'} opacity={0.7} />
				))}
				<path d="M-500,560 L2400,560 L2400,700 L-500,700 Z" fill={night ? '#0e1230' : '#5a4a7a'} />
			</Svg>
		</Layer>
		<Layer depth={1.3}>
			<Svg>
				<rect x={W.x} y={640} width={W.w} height={400} fill="#3a3a48" />
				<rect x={W.x} y={640} width={W.w} height={14} fill="#9a9aa8" />
				{[0, 1, 2].map((i) => (
					<g key={i}>
						{Array.from({length: 20}).map((_, j) => (
							<rect key={j} x={-500 + j * 180 - ((f * (jam ? 2 : 14) * flow) % 180)} y={760 + i * 70} width={90} height={7} fill="#f4f1ea" opacity={0.8} />
						))}
					</g>
				))}
				{[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => {
					const spd = jam ? 3 : 9 + (i % 3) * 3;
					const x = ((i * 330 - f * spd * flow * (i % 2 ? -1 : 1)) % 2900 + 2900) % 2900 - 400;
					return <CarShape key={i} x={x} y={730 + (i % 3) * 70} c={['#d9433d', '#3d6fe0', '#f2b21c', '#3aa37a', '#8b5cf6', '#e86aa0'][i % 6]} s={0.8 + (i % 3) * 0.12} dir={i % 2 ? -1 : 1} jam={jam} />;
				})}
				{bridge ? (
					<g>
						<rect x={W.x} y={560} width={W.w} height={22} fill="#7a7a88" />
						{Array.from({length: 14}).map((_, i) => (
							<path key={i} d={`M${-400 + i * 200},560 L${-300 + i * 200},380 L${-200 + i * 200},560`} stroke="#9a9aa8" strokeWidth={8} fill="none" />
						))}
					</g>
				) : null}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- PRESS ROOM ------------------------------- */
export const Press: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={1.7}>
			<Svg>
				<defs>
					<Grd id="pr-w" a="#1d3a7a" b="#2f5aa8" />
				</defs>
				<rect x={W.x} y={-300} width={W.w} height={1300} fill="url(#pr-w)" />
				{Array.from({length: 12}).map((_, i) => (
					<g key={i}>
						<line x1={-200 + i * 220} y1={-300} x2={-200 + i * 220} y2={1000} stroke="#fff" strokeWidth={2} opacity={0.14} />
					</g>
				))}
				<Flag x={260} y={120} f={f} s={1.2} />
				<Flag x={1500} y={120} f={f} s={1.2} seed={1} />
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<Floor id="pr-f" a="#2b2538" b="#1a1624" />
				<path d="M780,900 L840,600 L1080,600 L1140,900 Z" fill="#6a4a2a" />
				<rect x={820} y={560} width={280} height={50} fill="#8a5a36" />
				<circle cx={960} cy={500} r={0} />
				{Array.from({length: 16}).map((_, i) => (
					<g key={i} transform={`translate(${-100 + i * 140},${1000 + (i % 2) * 14})`}>
						<circle r={34} fill="#0d0a18" />
						<rect x={-44} y={28} width={88} height={90} fill="#0d0a18" />
						{random('fl' + i + Math.floor(f / 11)) > 0.93 ? <circle cx={0} cy={-60} r={50} fill="#fff" opacity={0.7} /> : null}
					</g>
				))}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- LAWN / WHITE HOUSE ------------------------------- */
export const Lawn: React.FC<{f: number}> = ({f}) => (
	<>
		<Layer depth={2}>
			<Svg>
				<defs>
					<Grd id="lw-s" a="#6fb8ee" b="#fff1d0" />
				</defs>
				<rect x={W.x} y={-400} width={W.w} height={1100} fill="url(#lw-s)" />
				{[0, 1, 2].map((i) => (
					<ellipse key={i} cx={((i * 900 + f * (0.4 + i * 0.1)) % 3200) - 500} cy={110 + i * 80} rx={190} ry={38} fill="#fff" opacity={0.85} />
				))}
				{/* house */}
				<rect x={300} y={330} width={1320} height={260} fill="#f6f2ea" />
				<rect x={300} y={316} width={1320} height={18} fill="#e0dacb" />
				{Array.from({length: 8}).map((_, i) => (
					<rect key={i} x={420 + i * 150} y={380} width={44} height={170} fill="#fff" stroke="#d9d3c4" strokeWidth={3} />
				))}
				<path d="M700,330 L960,200 L1220,330 Z" fill="#efe9dc" />
				{Array.from({length: 7}).map((_, i) => (
					<rect key={i} x={420 + i * 168} y={430} width={34} height={60} fill="#7a9ab8" opacity={0.7} />
				))}
				<Flag x={1650} y={100} f={f} s={0.9} />
			</Svg>
		</Layer>
		<Layer depth={1.25}>
			<Svg>
				<defs>
					<Grd id="lw-g" a="#6ab85a" b="#2f7a3a" />
				</defs>
				<rect x={W.x} y={590} width={W.w} height={600} fill="url(#lw-g)" />
				{Array.from({length: 5}).map((_, i) => (
					<ellipse key={i} cx={300 + i * 420} cy={640} rx={90} ry={110} fill="#2f7a3a" />
				))}
				<path d="M780,1000 L900,600 L1020,600 L1140,1000 Z" fill="#e8dcc0" opacity={0.9} />
				{Array.from({length: 12}).map((_, i) => (
					<circle key={i} cx={random('lf' + i) * 2400 - 200} cy={620 + ((f * (1 + i * 0.1) + i * 60) % 340)} r={5} fill={['#e86aa0', '#f2b21c', '#fff'][i % 3]} opacity={0.8} />
				))}
			</Svg>
		</Layer>
	</>
);

/* ------------------------------- GENERIC KIT WRAPPERS ------------------------------- */
export const KBedroom: React.FC<{f: number; night?: boolean; ring?: boolean}> = ({f, night, ring}) => (
	<Layer depth={1.4}>
		<Bedroom f={f} night={night} ring={ring} />
	</Layer>
);
export const KKitchen: React.FC<{f: number; night?: boolean}> = ({f, night}) => (
	<>
		<Layer depth={1.4}>
			<Kitchen night={night} />
		</Layer>
		<Layer depth={1.4}>
			<Svg>
				<g transform={`translate(1500,${520 + Math.sin(f / 30) * 1})`}>
					<rect x={0} y={0} width={190} height={280} rx={14} fill="#e8ecf0" stroke="#aab" strokeWidth={4} />
					<rect x={0} y={90} width={190} height={5} fill="#aab" />
					<rect x={30} y={160} width={54} height={36} fill="#fffbe0" transform="rotate(-4,56,178)" />
					<line x1={38} y1={170} x2={74} y2={168} stroke="#999" strokeWidth={2} />
					<line x1={38} y1={180} x2={70} y2={178} stroke="#999" strokeWidth={2} />
				</g>
			</Svg>
		</Layer>
	</>
);
export const KCorridor: React.FC<{f: number}> = ({f}) => (
	<Layer depth={1.5}>
		<Corridor f={f} />
	</Layer>
);
export const KCoast: React.FC<{f: number}> = ({f}) => (
	<Layer depth={1.6}>
		<Beach f={f} />
	</Layer>
);
export const KCity: React.FC<{f: number}> = ({f}) => (
	<Layer depth={1.6}>
		<CityDay f={f} />
	</Layer>
);
export const mixC = mix;
export const lightenC = lighten;
