import React from 'react';
import {AbsoluteFill, interpolate, random} from 'remotion';
import {Pose} from '../engine/Stickman';
import {env, gesture, idle, walk} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {Extra, CrowdRow, Layer, Sleeper, Stage, Svg, camOn, clamp, mixCam, usePush} from '../kit/kit';
import {Bedroom, Blanket} from '../kit/sets';
import {Board, Bubble, FONT} from '../kit/ui';
import {Callout} from '../kit/graphics';
import type {ShotDef} from '../kit/coverage';
import {
	Ball, Mug, ORANGE_SUN, Phone, Planet, Road, School, SimpleCar, SpaceBG, Star, Studio, Telescope, Tree, WHITE_SUN,
} from './places';
import {FL, Flash, Hero, Outdoor, Pill, PopText, Punch, QMark, SpaceStage, Inside, beats, badgeY, headY, hop, hops, on, path, shake, tw, Burst} from './h';

const SUNS_DAY = [
	{x: 1450, y: 150, r: 62, c: WHITE_SUN},
	{x: 420, y: 230, r: 34, c: ORANGE_SUN, glow: 1.3},
];

/* ---------- props used only here ---------- */
const Rooster: React.FC<{x: number; y: number; f: number; crow: number; s?: number}> = ({x, y, f, crow, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s}) rotate(${-crow * 14 + Math.sin(f / 2) * crow * 4})`}>
		<path d="M-60,-20 q-50,-60 -10,-110 q10,40 30,50 Z" fill="#2a6a3a" />
		<ellipse cx={0} cy={-30} rx={56} ry={44} fill="#f2f2f2" />
		<circle cx={44} cy={-90} r={30} fill="#f2f2f2" />
		<path d="M30,-122 l8,-20 l8,16 l8,-18 l6,22 Z" fill="#e23a2a" />
		<circle cx={52} cy={-96} r={5} fill="#111" />
		<path d={`M70,-92 l30,${-4 - crow * 8} l-30,8 Z`} fill="#f2b21c" />
		<path d={`M70,-86 l30,${6 + crow * 10} l-30,0 Z`} fill="#d89a1c" />
		<path d="M60,-70 q6,20 -6,26" fill="#e23a2a" />
		<path d="M-10,12 l-6,36 M14,12 l6,36" stroke="#f2b21c" strokeWidth={6} />
	</g>
);
const Mower: React.FC<{x: number; y: number; f: number}> = ({x, y, f}) => (
	<g transform={`translate(${x},${y})`}>
		<rect x={-70} y={-60} width={140} height={50} rx={14} fill="#d8322a" />
		<rect x={-40} y={-80} width={60} height={26} rx={6} fill="#3a3f4a" />
		<line x1={-60} y1={-56} x2={-150} y2={-170} stroke="#3a3f4a" strokeWidth={8} />
		<circle cx={-48} cy={-6} r={18} fill="#1a1a1e" />
		<circle cx={50} cy={-6} r={18} fill="#1a1a1e" />
		{Array.from({length: 8}).map((_, i) => {
			const u = ((f / 12 + i / 8) % 1);
			return <rect key={i} x={-80 - u * 140} y={-30 - Math.sin(u * Math.PI) * 80 + random('gc' + i) * 20} width={10} height={4} fill="#3a9a3a" transform={`rotate(${i * 40})`} opacity={1 - u} />;
		})}
	</g>
);
const Fence: React.FC<{y: number; c?: string}> = ({y, c = '#f6efe0'}) => (
	<g>
		{Array.from({length: 40}).map((_, i) => (
			<path key={i} d={`M${-600 + i * 80},${y} l0,-120 l20,-20 l20,20 l0,120 Z`} fill={c} />
		))}
		<rect x={-600} y={y - 90} width={3200} height={14} fill={c} />
	</g>
);
const Cereal: React.FC<{x: number; y: number}> = ({x, y}) => (
	<g transform={`translate(${x},${y})`}>
		<path d="M-60,0 L60,0 Q50,50 0,52 Q-50,50 -60,0 Z" fill="#f2f2f2" />
		{Array.from({length: 7}).map((_, i) => (
			<circle key={i} cx={-40 + i * 13} cy={-4} r={7} fill="#f2b21c" />
		))}
	</g>
);
export const Satellite: React.FC<{x: number; y: number; f: number; s?: number}> = ({x, y, f, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s}) rotate(${Math.sin(f / 30) * 5})`}>
		<rect x={-150} y={-24} width={100} height={48} fill="#2a4aa0" stroke="#cfe0ff" strokeWidth={3} />
		<rect x={50} y={-24} width={100} height={48} fill="#2a4aa0" stroke="#cfe0ff" strokeWidth={3} />
		<rect x={-40} y={-50} width={80} height={100} rx={10} fill="#d8d8e0" />
		<circle cx={0} cy={-56} r={26} fill="#3a3a44" />
		<circle cx={0} cy={-56} r={16} fill="#5ad0ff" />
	</g>
);

/* 001: 2 AM, sunscreen under a blue sky */
const S001: React.FC = () => {
	const {f, at} = useShot();
	const w = path(f, [[0, 330], [36, 760]], 1);
	const pose = beats(w.pose, f, at, [['001', 50, 80, 'sunscreen']]);
	const cam = usePush(camOn(900, 520, 1.05), camOn(780, 560, 1.75));
	return (
		<Outdoor id="s1" cam={cam} mode="blue" suns={SUNS_DAY}>
			<Hero x={w.x} pose={pose} facing={w.facing} vx={w.vx} bob={w.bob} armOver={on(f, at, '001', 50, 80) > 0.4} expr="sleepy" uid="h001" />
			<PopText t={f - at('001') - 8} x={1060} y={380} text="2:00 AM" size={80} c="#fff" />
			<PopText t={f - at('001') - 60} x={1040} y={470} text="SUNSCREEN?!" size={48} c="#ffd34a" rot={5} />
		</Outdoor>
	);
};

/* 002-003: bright blue sky, Sam shooting hoops */
const S002: React.FC = () => {
	const {f, at, dur} = useShot();
	const tilt = tw(f, 0, at('003'), 0, 1);
	const cam = mixCam(camOn(900, 260, 1.2), camOn(1520, 600, 1.45), interpolate(tilt, [0, 1], [0, 1]));
	// Sam dribbles then shoots every 54 frames
	const cyc = Math.max(0, f - at('003') + 10);
	const ph = cyc % 54;
	const shooting = f > at('003') - 10 && ph > 22;
	const u = (ph - 22) / 32;
	const bx = shooting ? 1470 + (1660 - 1470) * u : 1460;
	const by = shooting ? 640 - Math.sin(u * Math.PI) * 260 + u * (500 - 640) : 860 - Math.abs(Math.sin(f / 4)) * 110;
	let sp: Pose = idle(f, 2);
	sp = shooting && u < 0.25 ? {...sp, armF: [160, 10], armB: [150, 10], head: -14} : {...sp, armF: [40 + Math.abs(Math.sin(f / 4)) * 30, 30]};
	const jump = shooting ? hop(f, f - ph + 22, 14, 40) : {lift: 0, squash: 0};
	const net = shooting && u > 0.95;
	return (
		<Outdoor id="s2" cam={cam} mode="blue" suns={SUNS_DAY}>
			<Actor who="sam" x={1420} s={0.72} pose={sp} bob={jump.lift / 0.72} squash={jump.squash} facing={1} look={[0.6, -0.6]} mouth="smile" uid="sam2" />
			<Ball x={bx} y={by} spin={f * 12} />
			{net ? <PopText t={0} x={1700} y={420} text="SWISH!" size={44} /> : null}
			<PopText t={f - at('002') - 20} x={900} y={330} text="BRIGHT BLUE" size={70} c="#fff" />
		</Outdoor>
	);
};

/* 004: neighbour mowing the lawn */
const S004: React.FC = () => {
	const {f, at, dur} = useShot();
	const x = tw(f, 0, dur, 200, 1300);
	const p = walk(f * 0.3);
	const pose = {...p, armF: [70, 20] as [number, number], armB: [60, 26] as [number, number], lean: 12};
	const cam = camOn(x + 60, 600, 1.35);
	return (
		<Outdoor id="s4" cam={cam} mode="blue" suns={SUNS_DAY} yard={{hoop: false, porch: false}}>
			<Mower x={x + 200} y={FL} f={f} />
			<Actor who="neighbor" x={x} pose={pose} bob={Math.abs(Math.sin(f * 0.3)) * 4} vx={3} look={[0.5, 0.2]} expr="sleepy" mouth="flat" uid="nb4" />
			<PopText t={f - at('004') - 10} x={x + 120} y={300} text="VRRRRM" size={58} c="#ff8a2a" rot={6} />
		</Outdoor>
	);
};

/* 005-006: the rooster screaming for six weeks, voice gone */
const S005: React.FC = () => {
	const {f, at} = useShot();
	const crow = f < at('006') ? 0.6 + 0.4 * Math.abs(Math.sin(f / 3)) : 0.4 * env(f, at('006') + 20, at('006') + 60, 4, 8);
	const cam = mixCam(camOn(900, 560, 1.2), camOn(980, 520, 1.9), tw(f, at('006') - 10, at('006') + 10, 0, 1));
	const hp = beats(idle(f, 3), f, at, [['005', 30, 999, 'cover']]);
	return (
		<Outdoor id="s5" cam={shake(cam, f, at('005') + 20, 40, 8)} mode="blue" suns={SUNS_DAY} yard={false} mid={<Svg><Fence y={860} /></Svg>}>
			<Rooster x={1000} y={720} f={f} crow={crow} s={1.3} />
			{f < at('006') ? <PopText t={f - at('005') - 6} x={1260} y={420} text="COCK-A-DOODLE-DOO!" size={58} rot={-8} /> : null}
			<PopText t={f - at('005') - 40} x={980} y={300} text="6 WEEKS" size={50} c="#fff" out={at('006') - at('005') - 40} />
			{f >= at('006') ? <PopText t={f - at('006') - 22} x={1200} y={500} text="...squeak" size={40} c="#fff" rot={4} /> : null}
			<Hero x={520} s={1.05} pose={hp} expr="angry" armOver facing={1} look={[0.8, 0]} badge={false} uid="h5" />
		</Outdoor>
	);
};

/* 007-008: no dark sky for 41 days */
const S007: React.FC = () => {
	const {f, at} = useShot();
	const w = path(f, [[0, 1500], [40, 960]], 4);
	const pose = beats(w.pose, f, at, [['007', 30, 80, 'lookUp'], ['008', 4, 60, 'shrug']]);
	const cam = usePush(camOn(960, 520, 1.1), camOn(960, 560, 1.6));
	return (
		<Outdoor id="s7" cam={cam} mode="blue" suns={SUNS_DAY}>
			<Hero x={w.x} pose={pose} facing={w.facing} vx={w.vx} bob={w.bob} look={[0, -0.8]} expr={f > at('008') ? 'worried' : 'normal'} uid="h7" />
			<PopText t={f - at('007') - 50} x={1350} y={300} text="41 DAYS" size={90} c="#ff8a2a" rot={4} />
			<Pill t={f - at('007') - 64} x={1350} y={400} text="NO DARK SKY" c="#5ad0ff" />
			<QMark t={f - at('008') - 6} x={1180} y={400} s={0.8} />
		</Outdoor>
	);
};

/* 009: Earth got a second sun (space) */
const S009: React.FC = () => {
	const {f, gf, at} = useShot();
	const arr = tw(f, at('009') + 30, at('009') + 60, 0, 1);
	const cam = shake(usePush(camOn(960, 540, 1.0), camOn(1100, 540, 1.25)), f, at('009') + 58, 14, 14);
	return (
		<>
			<SpaceStage cam={cam}>
				<Star x={260} y={560} r={130} c={WHITE_SUN} f={gf} id="w9" />
				<Planet x={960} y={560} r={120} f={gf} />
				<g opacity={arr}>
					<line x1={2400 - 800 * arr} y1={200 + 120 * arr} x2={2600} y2={80} stroke={ORANGE_SUN} strokeWidth={30} opacity={0.3} strokeLinecap="round" />
					<Star x={2400 - 800 * arr} y={200 + 120 * arr} r={70} c={ORANGE_SUN} f={gf} id="o9" />
				</g>
				<PopText t={f - at('009') - 62} x={1600} y={520} text="SUN #2" size={70} c="#ff8a2a" />
			</SpaceStage>
			<Flash f={f} at={at('009') + 58} />
			<Punch t={f - at('009') - 64} text="A SECOND SUN" top={820} size={90} />
		</>
	);
};

/* 010-011: in five months it decides where Earth goes */
const S010: React.FC = () => {
	const {f, gf, at} = useShot();
	const a = gf / 60;
	const ex = 960 + Math.cos(a) * 330;
	const ey = 540 + Math.sin(a) * 140;
	const br = tw(f, at('011'), at('011') + 30, 0, 1);
	const cam = usePush(camOn(960, 540, 1.05), camOn(960, 520, 1.2));
	return (
		<SpaceStage cam={cam}>
			<ellipse cx={960} cy={540} rx={330} ry={140} fill="none" stroke="#5a6aa0" strokeWidth={3} strokeDasharray="10 12" />
			<Star x={960} y={540} r={60} c={WHITE_SUN} f={gf} id="w10" />
			<Star x={1650} y={260} r={36} c={ORANGE_SUN} f={gf} id="o10" />
			<Planet x={ex} y={ey} r={36} f={gf} />
			{[[-500, -300], [520, 330], [-480, 360]].map(([dx, dy], i) => (
				<g key={i} opacity={br}>
					<line x1={ex} y1={ey} x2={ex + dx * br} y2={ey + dy * br} stroke="#ffd34a" strokeWidth={6} strokeDasharray="16 12" />
					<QMark t={f - at('011') - 20 - i * 6} x={ex + dx} y={ey + dy + 60} s={0.5} />
				</g>
			))}
			<Pill t={f - at('010') - 30} x={960} y={140} text="5 MONTHS" c="#ff8a2a" size={44} out={at('011') - at('010') - 20} />
			<PopText t={f - at('011') - 4} x={960} y={150} text="WHERE DO WE GO?" size={64} />
		</SpaceStage>
	);
};

/* 012: rewind to day one */
const S012: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const rw = env(f, 0, at('012') + 34, 1, 8);
	const cam = usePush(camOn(1400, 640, 1.3), camOn(1450, 640, 1.6));
	return (
		<>
			<Stage cam={cam} bg="#101225" light={{x: 70, y: 20, o: 0.3, night: true}}>
				<Layer depth={1.2}>
					<Bedroom night f={gf} />
				</Layer>
				<Layer depth={1}>
					<Svg>
						<Sleeper x={1560} y={640} s={0.9} />
					</Svg>
				</Layer>
				<Layer depth={1}>
					<Blanket night f={gf} />
				</Layer>
			</Stage>
			{rw > 0 ? (
				<AbsoluteFill style={{opacity: rw, pointerEvents: 'none'}}>
					<AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,255,255,.08) 0 2px, transparent 2px 6px)', transform: `translateY(${(f * 37) % 60}px)`}} />
					<div style={{position: 'absolute', left: 80, top: 70, fontFamily: FONT, fontWeight: 900, fontSize: 80, color: '#fff', textShadow: '0 0 12px #000'}}>◀◀ REWIND</div>
				</AbsoluteFill>
			) : null}
			<Punch t={f - at('012') - 40} text="DAY 1" top={160} size={150} c="#ff8a2a" out={dur} />
		</>
	);
};

/* 013-014: alarm set for 7, wake at 4 to an orange glow */
const S013: React.FC = () => {
	const {f, gf, at} = useShot();
	const glow = tw(f, at('014') + 10, at('014') + 50, 0, 1);
	const wake = tw(f, at('014') + 30, at('014') + 46, 0, 1);
	const cam = mixCam(camOn(1085, 660, 2.0), camOn(1500, 620, 1.5), tw(f, at('014') - 6, at('014') + 14, 0, 1));
	return (
		<Stage cam={cam} bg="#101225" light={{x: 60, y: 20, o: 0.35 + 0.3 * glow, c: '255,150,60'}}>
			<Layer depth={1.2}>
				<Bedroom night f={gf} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					<rect x={760} y={170} width={420} height={330} fill={ORANGE_SUN} opacity={0.75 * glow} />
					<Sleeper x={1560} y={640} s={0.9} lift={wake * 30} expr={wake > 0.5 ? 'wide' : 'sleepy'} />
					<PopText t={f - at('013') - 6} x={1085} y={560} text="7:00" size={72} c="#fff" out={at('014') - at('013') - 10} />
					<PopText t={f - at('014') - 6} x={1300} y={420} text="4:00 AM" size={80} c="#ffb04a" />
				</Svg>
			</Layer>
			<Layer depth={1}>
				<Blanket night f={gf} lift={wake * 20} />
			</Layer>
			<AbsoluteFill style={{background: ORANGE_SUN, opacity: 0.25 * glow, mixBlendMode: 'overlay'}} />
		</Stage>
	);
};

/* 015-017: pull the curtain, the orange thing rising in the wrong place */
const S015: React.FC = () => {
	const {f, gf, at} = useShot();
	const pull = tw(f, at('015') + 6, at('015') + 24, 0, 1);
	const rise = tw(f, at('016'), at('017') + 60, 0, 1);
	const w = path(f, [[0, 1500], [at('015') + 4, 700]], 2);
	let p = beats(w.pose, f, at, [['016', 50, 999, 'lookUp'], ['017', 0, 999, 'shade']]);
	if (pull < 1 && f > at('015')) p = gesture('point', p, env(f, at('015'), at('015') + 30, 6, 6), f);
	const cam = mixCam(camOn(800, 520, 1.4), camOn(900, 420, 1.45), tw(f, at('016'), at('016') + 30, 0, 1));
	return (
		<Stage cam={cam} bg="#101225" light={{x: 50, y: 20, o: 0.6, c: '255,150,60'}}>
			<Layer depth={1.2}>
				<Bedroom night f={gf} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					<clipPath id="win15">
						<rect x={770} y={180} width={400} height={310} />
					</clipPath>
					<g clipPath="url(#win15)">
						<rect x={770} y={180} width={400} height={310} fill="#2a1a40" />
						<rect x={770} y={330} width={400} height={160} fill="#ff8a3a" opacity={0.6 * rise} />
						<Star x={1060} y={520 - 220 * rise} r={34} c={ORANGE_SUN} f={gf} id="o15" />
					</g>
					<rect x={760 + 200 * pull} y={170} width={210 - 180 * pull} height={340} fill="#3a4380" />
					<Hero x={w.x} s={1.05} pose={p} facing={w.facing} vx={w.vx} bob={w.bob} expr={f > at('017') ? 'sleepy' : f > at('016') ? 'wide' : 'normal'} look={[0.6, -0.6]} uid="h15" />
					<Callout f={f} t0={at('017') + 50} t1={at('017') + 200} from={[1060, 400]} to={[1400, 300]} text="WRONG PLACE!" />
					<PopText t={f - at('017') - 4} x={1250} y={180} text="TOO BRIGHT" size={48} c="#ffb04a" out={50} />
				</Svg>
			</Layer>
			<AbsoluteFill style={{background: ORANGE_SUN, opacity: 0.18 + 0.2 * rise, mixBlendMode: 'overlay'}} />
		</Stage>
	);
};

/* 018: you run outside in your socks */
const S018: React.FC = () => {
	const {f, at, dur} = useShot();
	const w = path(f, [[0, 330], [dur, 1500]], 5, 0.3, 1);
	const cam = camOn(w.x + 80, 560, 1.4);
	return (
		<Outdoor id="s18" cam={cam} mode="dawn" suns={[{x: 1300, y: 300, r: 34, c: ORANGE_SUN, glow: 1.6}]}>
			<Hero x={w.x} pose={w.pose} facing={1} vx={w.vx} bob={w.bob} expr="wide" uid="h18" />
			<Callout f={f} t0={at('018') + 20} t1={dur} from={[w.x + 10, FL - 4]} to={[w.x + 200, FL - 260]} text="SOCKS!" />
		</Outdoor>
	);
};

/* 019-020: every neighbour outside in pyjamas, phones up, silence */
const S019: React.FC = () => {
	const {f, at, dur} = useShot();
	const cam = usePush(camOn(500, 560, 1.25), camOn(1300, 560, 1.25));
	return (
		<Outdoor id="s19" cam={cam} mode="dawn" suns={[{x: 1100, y: 260, r: 34, c: ORANGE_SUN, glow: 1.6}]} yard={{hoop: false}}>
			{Array.from({length: 9}).map((_, i) => {
				const x = 150 + i * 200;
				const k = env(f, at('019') + i * 5, 9999, 10, 1);
				const base = idle(f, i);
				const pose = {...base, head: base.head - 18 * k, armF: [base.armF[0] + (150 - base.armF[0]) * k, base.armF[1] + (16 - base.armF[1]) * k] as [number, number]};
				return (
					<g key={i}>
						{i === 4 ? <Hero x={x} pose={pose} look={[0.3, -1]} uid="h19" /> : <Extra i={i} x={x} floor={FL + (i % 2) * 12} s={0.92 + (i % 3) * 0.05} pose={pose} seed="pj" facing={i % 2 ? -1 : 1} />}
						{k > 0.5 ? <Phone x={x + (i % 2 && i !== 4 ? -1 : 1) * 22} y={headY(0.95) - 120} s={0.8} screen="#ffb04a" /> : null}
					</g>
				);
			})}
			<Bubble x={960} y={260} w={160} h={90} t={f - at('020')} tail={[0, 120]}>
				<text x={0} y={18} textAnchor="middle" fontSize={60} fontFamily={FONT} fontWeight={900} fill="#222">
					...
				</text>
			</Bubble>
		</Outdoor>
	);
};

/* 021-022: your sun rises too: two suns */
const S021: React.FC = () => {
	const {f, at} = useShot();
	const rise = tw(f, at('021'), at('021') + 60, 0, 1);
	const cam = usePush(camOn(960, 420, 1.05), camOn(960, 360, 1.15));
	const suns = [
		{x: 1350, y: 860 - 560 * rise, r: 62, c: WHITE_SUN},
		{x: 560, y: 300, r: 36, c: ORANGE_SUN, glow: 1.4},
	];
	const hp = beats(idle(f, 2), f, at, [['021', 0, 999, 'lookUp'], ['022', 10, 50, 'point']]);
	return (
		<Outdoor id="s21" cam={cam} mode={rise > 0.5 ? 'gold' : 'dawn'} suns={suns} yard={{hoop: false}}>
			<Hero x={960} s={1.05} pose={hp} look={[0, -1]} expr="wide" handF={on(f, at, '022', 10, 50) > 0.5 ? 'point' : undefined} uid="h21" />
			<Pill t={f - at('022') - 16} x={1350} y={200} text="WHITE" c="#ffffff" size={40} />
			<Pill t={f - at('022') - 34} x={560} y={180} text="ORANGE" c="#ff8a2a" size={40} />
			<PopText t={f - at('022') - 2} x={960} y={140} text="TWO SUNS" size={90} />
		</Outdoor>
	);
};

/* 023-025: two shadows moving in different directions */
const S023: React.FC = () => {
	const {f, at} = useShot();
	const w = path(f, [[0, 760], [at('025'), 760], [at('025') + 60, 1160]], 3);
	const swing = tw(f, at('025'), at('025') + 60, 0, 1);
	const hp = beats(w.pose, f, at, [['023', 0, at('025') - at('023') - 4, 'lookUp']]);
	const look = f < at('025') ? ([0, 1] as [number, number]) : ([0.5, 0.3] as [number, number]);
	const pose: Pose = f < at('025') ? {...hp, head: 24} : hp;
	const cam = usePush(camOn(860, 740, 1.5), camOn(1060, 700, 1.3));
	const L1 = 520, L2 = 200;
	const a1 = 200 - swing * 30, a2 = -14 + swing * 40;
	return (
		<Outdoor id="s23" cam={cam} mode="gold" suns={[{x: 1700, y: 200, r: 62, c: WHITE_SUN}, {x: 200, y: 420, r: 36, c: ORANGE_SUN, glow: 1.4}]} yard={{hoop: false}}>
			<g opacity={tw(f, at('023') + 10, at('023') + 30, 0, 1)}>
				<path d={`M${w.x - 20},${FL} L${w.x + Math.cos((a1 * Math.PI) / 180) * L1 - 30},${FL + 40 + Math.sin((a1 * Math.PI) / 180) * 30} L${w.x + Math.cos((a1 * Math.PI) / 180) * L1 + 30},${FL + 70} L${w.x + 20},${FL} Z`} fill="#3a2a50" opacity={0.25} />
				<path d={`M${w.x - 20},${FL} L${w.x + Math.cos((a2 * Math.PI) / 180) * L2},${FL + 30} L${w.x + Math.cos((a2 * Math.PI) / 180) * L2 + 40},${FL + 50} L${w.x + 20},${FL} Z`} fill="#c84a10" opacity={0.45} />
			</g>
			<Hero x={w.x} pose={pose} facing={w.facing} vx={w.vx} bob={w.bob} look={look} expr="wide" uid="h23" />
			<Pill t={f - at('024') - 6} x={w.x - 420} y={FL - 60} text="LONG & PALE" c="#c8c0ff" out={at('025') - at('024') + 40} />
			<Pill t={f - at('024') - 30} x={w.x + 330} y={FL - 60} text="SHORT & ORANGE" c="#ff8a2a" out={at('025') - at('024') + 20} />
		</Outdoor>
	);
};

/* 026-027: Sam jumps up and down — like that desert planet */
const S026: React.FC = () => {
	const {f, gf, at} = useShot();
	const j = hops(f, at('026'), at('027') + 40, 14, 90);
	const sp = beats(idle(f, 5), f, at, [['026', 0, 999, 'cheer']]);
	const cam = usePush(camOn(1000, 600, 1.35), camOn(1040, 560, 1.7));
	return (
		<Outdoor id="s26" cam={cam} mode="gold" suns={[{x: 1400, y: 180, r: 62, c: WHITE_SUN}, {x: 500, y: 260, r: 36, c: ORANGE_SUN, glow: 1.4}]}>
			<Actor who="sam" x={1000} s={0.75} pose={sp} bob={j.lift / 0.75} squash={j.squash} mouth="open" expr="wide" look={[0.3, -0.6]} uid="sam26" />
			<Bubble x={1340} y={330} w={280} h={190} t={f - at('027') + 4} tail={[-120, 160]}>
				<rect x={-130} y={10} width={260} height={80} fill="#f0b060" />
				<circle cx={-50} cy={-30} r={30} fill={WHITE_SUN} stroke="#f0c040" strokeWidth={4} />
				<circle cx={40} cy={-40} r={20} fill={ORANGE_SUN} />
				<path d="M-120,20 q60,-30 120,0 t130,0" fill="#e0a050" />
			</Bubble>
			<Hero x={640} s={1} pose={beats(idle(f, 1), f, at, [['026', 20, 999, 'clap']])} look={[0.8, -0.2]} uid="h26" />
			<Burst t={f - at('026') - 10} x={1000} y={500} seed="sam" />
			{gf < 0 ? null : null}
		</Outdoor>
	);
};

/* 028-030: grandpa with coffee whispers "That's not possible" */
const S028: React.FC = () => {
	const {f, gf, at} = useShot();
	const drop = tw(f, at('030') + 20, at('030') + 40, 0, 1);
	const gp = beats(idle(f, 7), f, at, [['028', 0, at('030') - at('028') + 18, 'presentF'], ['030', 0, 999, 'lookUp']]);
	const cam = mixCam(camOn(260, 520, 1.25), camOn(240, 520, 2.1), tw(f, at('029'), at('030'), 0, 1));
	return (
		<Outdoor id="s28" cam={cam} mode="gold" suns={[{x: 1400, y: 180, r: 62, c: WHITE_SUN}, {x: 700, y: 140, r: 36, c: ORANGE_SUN, glow: 1.4}]}>
			<Telescope x={20} y={FL - 30} tilt={-28} />
			<Actor who="grandpa" x={250} floor={FL - 30} s={1} pose={gp} look={[0.5, -0.8]} expr={f > at('030') ? 'wide' : 'normal'} uid="gp28" />
			<Mug x={drop > 0 ? 330 + drop * 30 : 330} y={drop > 0 ? 640 + drop * drop * 230 : 650} f={gf} />
			<Pill t={f - at('028') - 30} x={250} y={260} text="50 YEARS" c="#ffd34a" out={at('029') - at('028') + 10} />
			<Bubble x={330} y={340} w={340} h={84} t={f - at('030') + 2} tail={[-130, 110]}>
				<text x={0} y={12} textAnchor="middle" fontSize={34} fontFamily={FONT} fontWeight={700} fill="#222" fontStyle="italic">
					that's not possible…
				</text>
			</Bubble>
			{drop >= 1 ? <PopText t={f - at('030') - 40} x={380} y={FL - 10} text="CLINK" size={36} c="#fff" /> : null}
		</Outdoor>
	);
};

/* 031-033: but it's possible — binary stars dance */
const S031: React.FC = () => {
	const {f, gf, at} = useShot();
	const a = gf / 26;
	const cam = usePush(camOn(960, 540, 1.3), camOn(960, 540, 1.0));
	return (
		<>
			<SpaceStage cam={cam}>
				<ellipse cx={960} cy={540} rx={260} ry={90} fill="none" stroke="#5a6aa0" strokeWidth={3} strokeDasharray="8 10" />
				<Star x={960 + Math.cos(a) * 260} y={540 + Math.sin(a) * 90} r={70} c={WHITE_SUN} f={gf} id="w31" />
				<Star x={960 - Math.cos(a) * 260} y={540 - Math.sin(a) * 90} r={46} c={ORANGE_SUN} f={gf} id="o31" />
			</SpaceStage>
			<Punch t={f - at('032')} text="IT'S POSSIBLE" top={90} out={at('033') - at('032') - 4} />
			<Punch t={f - at('033')} text="IT'S NORMAL" top={90} c="#9ff0b0" out={200} />
		</>
	);
};

/* 034: half of all sun-like stars have a partner */
const S034: React.FC = () => {
	const {f, gf, at} = useShot();
	return (
		<Board tint="#1a1640">
			{Array.from({length: 10}).map((_, i) => {
				const x = 280 + (i % 5) * 340;
				const y = 380 + Math.floor(i / 5) * 300;
				const pk = tw(f, at('034') + 6 + i * 4, at('034') + 16 + i * 4, 0, 1);
				const partner = i % 2 === 0;
				const pk2 = tw(f, at('034') + 50 + i * 5, at('034') + 60 + i * 5, 0, 1);
				return (
					<g key={i} transform={`translate(${x},${y}) scale(${pk})`}>
						<Star x={partner ? -30 : 0} y={0} r={46} c={WHITE_SUN} f={gf} id={'b34' + i} />
						{partner ? <g transform={`scale(${pk2})`}><Star x={60} y={-20} r={28} c={ORANGE_SUN} f={gf} id={'p34' + i} /></g> : null}
					</g>
				);
			})}
			<text x={960} y={170} textAnchor="middle" fontSize={64} fontFamily={FONT} fontWeight={900} fill="#fff">
				STARS LIKE OUR SUN
			</text>
			<PopText t={f - at('034') - 80} x={960} y={1000} text="≈ 50% HAVE A PARTNER" size={64} />
		</Board>
	);
};

/* 035: our lonely sun is a bit unusual */
const S035: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 540, 1.0), camOn(960, 560, 1.4));
	return (
		<SpaceStage cam={cam}>
			{[160, 240, 330, 430].map((r, i) => (
				<g key={r}>
					<ellipse cx={960} cy={560} rx={r} ry={r * 0.36} fill="none" stroke="#4a5a90" strokeWidth={2} />
					<circle cx={960 + Math.cos(gf / (20 + i * 12) + i) * r} cy={560 + Math.sin(gf / (20 + i * 12) + i) * r * 0.36} r={10 + i * 4} fill={['#c0a080', '#e0c060', '#2f7fe6', '#d0603a'][i]} />
				</g>
			))}
			<Star x={960} y={560} r={70} c={WHITE_SUN} f={gf} id="w35" />
			<g transform="translate(960,560)">
				<circle cx={-20} cy={-6} r={6} fill="#5a4a2a" />
				<circle cx={20} cy={-6} r={6} fill="#5a4a2a" />
				<path d="M-16,26 q16,-12 32,0" stroke="#5a4a2a" strokeWidth={5} fill="none" />
				<circle cx={26} cy={6} r={4} fill="#7ad0ff" opacity={0.8} transform={`translate(0,${(f % 30) * 0.8})`} />
			</g>
			<PopText t={f - at('035') - 50} x={960} y={250} text="ONE LONELY SUN" size={70} c="#fff" rot={-3} />
			<PopText t={f - at('035') - 90} x={1380} y={850} text="UNUSUAL" size={80} c="#ff5a6a" rot={-12} />
		</SpaceStage>
	);
};

/* 036-037: 2011, a planet orbiting two suns */
const S036: React.FC = () => {
	const {f, gf, at} = useShot();
	const a = gf / 30;
	const cam = mixCam(camOn(500, 400, 1.4), camOn(1200, 560, 1.15), tw(f, at('036') + 40, at('036') + 100, 0, 1));
	return (
		<SpaceStage cam={cam}>
			<Satellite x={420} y={360} f={gf} />
			<path d={`M440,320 L1200,${520} L1200,${600} Z`} fill="#5ad0ff" opacity={0.08 + 0.05 * Math.sin(f / 4)} />
			<Star x={1200 + Math.cos(a) * 70} y={560 + Math.sin(a) * 30} r={42} c={WHITE_SUN} f={gf} id="w36" />
			<Star x={1200 - Math.cos(a) * 70} y={560 - Math.sin(a) * 30} r={30} c={ORANGE_SUN} f={gf} id="o36" />
			<ellipse cx={1200} cy={560} rx={300} ry={110} fill="none" stroke="#9ff0b0" strokeWidth={3} strokeDasharray="10 10" />
			<Planet x={1200 + Math.cos(gf / 50) * 300} y={560 + Math.sin(gf / 50) * 110} r={24} c="#c89a5a" land="#a07a40" f={gf} />
			<Pill t={f - at('036') - 10} x={420} y={180} text="2011" c="#ffd34a" size={48} />
			<Pill t={f - at('037') - 10} x={1200} y={300} text="KEPLER-16b" c="#9ff0b0" size={42} />
			<PopText t={f - at('037') - 50} x={1200} y={860} text="A REAL 2-SUN PLANET" size={56} />
		</SpaceStage>
	);
};

/* 038: worlds where two sunsets is just a normal Tuesday */
const S038: React.FC = () => {
	const {f, at, dur} = useShot();
	const set = tw(f, 0, dur, 0, 1);
	const cam = usePush(camOn(960, 560, 1.1), camOn(900, 620, 1.45));
	const sip = env(f, 40, 90, 8, 8) + env(f, 130, 180, 8, 8);
	const ap = {...idle(f, 9), armF: [30 + 100 * sip, 40 + 60 * sip] as [number, number]};
	return (
		<Outdoor
			id="s38"
			cam={cam}
			mode="dusk"
			houses={false}
			yard={false}
			suns={[{x: 760, y: 560 + 200 * set, r: 60, c: WHITE_SUN}, {x: 1240, y: 520 + 160 * set, r: 40, c: ORANGE_SUN, glow: 1.4}]}
			mid={
				<Svg>
					<path d="M-600,760 q300,-80 600,-20 t700,-40 t900,30 L2520,1300 L-600,1300 Z" fill="#a0603a" />
				</Svg>
			}
		>
			<rect x={-600} y={860} width={3120} height={400} fill="#c8804a" />
			<rect x={640} y={790} width={160} height={14} rx={6} fill="#5a3a2a" />
			<Actor who="hero" x={720} seat={790} s={1} pose={beats({...ap, legB: [88, 85], legF: [92, 90]}, f, at, [])} color="#3ac06a" rim="#d0ffd8" eyeStyle={undefined} gloss={false} mouth="smile" look={[0.6, -0.4]} uid="alien" />
			<path d="M700,350 q-6,-30 10,-50 M740,350 q6,-30 -10,-50" stroke="#3ac06a" strokeWidth={8} fill="none" transform="translate(0,170)" />
			<Pill t={f - at('038') - 60} x={960} y={200} text="JUST A NORMAL TUESDAY" c="#ffd34a" size={44} />
		</Outdoor>
	);
};

/* 039-042: scientists explain on TV: the drifting orange star */
const S039: React.FC = () => {
	const {f, gf, at} = useShot();
	const sx = tw(f, at('040'), at('042') + 60, 600, 1320);
	const sp = beats(idle(f, 4), f, at, [['039', 10, 50, 'wave'], ['040', 0, 60, 'presentF'], ['041', 10, 80, 'point'], ['042', 0, 40, 'shrug']]);
	const cam = mixCam(camOn(960, 460, 1.0), camOn(980, 400, 1.4), tw(f, at('040'), at('041'), 0, 1));
	return (
		<Stage cam={cam} bg="#0e1430" light={{x: 50, y: 10, o: 0.3}}>
			<Layer depth={1.2}>
				<Studio f={gf} ticker="SCIENTISTS EXPLAIN THE NEW STAR">
					<SpaceBG f={gf} />
					<line x1={540} y1={500} x2={sx} y2={500 - (sx - 540) * 0.2} stroke={ORANGE_SUN} strokeWidth={10} opacity={0.35} strokeDasharray="4 10" />
					<Star x={sx} y={500 - (sx - 540) * 0.2} r={36} c={ORANGE_SUN} f={gf} id="o39" />
				</Studio>
			</Layer>
			<Layer depth={1}>
				<Svg>
					<Actor who="scientist" x={1500} floor={900} s={1.05} facing={-1} pose={sp} handF={on(f, at, '041', 10, 80) > 0.5 ? 'point' : undefined} look={[-0.6, -0.3]} uid="sc39" />
					<PopText t={f - at('040') - 10} x={760} y={110} text="NOT NEW!" size={56} c="#ff5a6a" out={at('041') - at('040')} />
					<Pill t={f - at('041') - 50} x={960} y={700} text="MILLIONS OF YEARS" c="#ff8a2a" />
					<PopText t={f - at('042') - 4} x={1500} y={260} text="STARS DO THAT" size={44} c="#fff" />
				</Svg>
			</Layer>
		</Stage>
	);
};

/* 043-044: Scholz's star grazed the edge of the solar system 70,000 years ago */
const S043: React.FC = () => {
	const {f, gf, at} = useShot();
	const u = tw(f, at('043') + 20, at('044') + 80, 0, 1);
	const cam = usePush(camOn(960, 540, 0.9), camOn(1250, 400, 1.2));
	return (
		<SpaceStage cam={cam} tint="#2a1a50">
			<circle cx={760} cy={600} r={520} fill="none" stroke="#7a8ac0" strokeWidth={3} strokeDasharray="4 14" />
			<circle cx={760} cy={600} r={200} fill="none" stroke="#4a5a90" strokeWidth={2} />
			<Star x={760} y={600} r={30} c={WHITE_SUN} f={gf} id="w43" />
			<line x1={2200} y1={-200} x2={2200 - 1500 * u} y2={-200 + 400 * u} stroke="#ff5a3a" strokeWidth={8} opacity={0.4} />
			<Star x={2200 - 1500 * u} y={-200 + 400 * u} r={22} c="#ff5a3a" f={gf} id="r43" />
			<Pill t={f - at('043') - 10} x={760} y={1000} text="70,000 YEARS AGO" c="#ffd34a" size={44} />
			<Pill t={f - at('043') - 60} x={2200 - 1500 * u} y={-200 + 400 * u - 70} text="SCHOLZ'S STAR" c="#ff5a3a" size={34} />
			<PopText t={f - at('044') - 30} x={760} y={1100} text="OUTER EDGE" size={46} c="#c8d0ff" />
		</SpaceStage>
	);
};

/* 045: our ancestors might have seen a faint red dot */
const S045: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 560, 1.15), camOn(960, 460, 1.4));
	const fire = 1 + 0.15 * Math.sin(f / 2);
	return (
		<Outdoor id="s45" cam={cam} mode="night" stars={1} houses={false} yard={false} mid={<Svg><path d="M-600,780 l500,-260 l300,140 l500,-300 l400,240 l500,-160 l900,380 L2520,1300 L-600,1300 Z" fill="#141a30" /></Svg>}>
			<rect x={-600} y={860} width={3120} height={400} fill="#1a2420" />
			<circle cx={1240} cy={220} r={6 + Math.sin(f / 5) * 1.5} fill="#ff4a3a" />
			<circle cx={1240} cy={220} r={22} fill="#ff4a3a" opacity={0.25} />
			<g transform={`translate(960,880) scale(${fire})`}>
				<path d="M-40,0 q0,-80 40,-120 q40,40 40,120 Z" fill="#ff8a2a" />
				<path d="M-20,0 q0,-40 20,-70 q20,30 20,70 Z" fill="#ffd34a" />
			</g>
			<circle cx={960} cy={820} r={260} fill="#ff8a2a" opacity={0.12} />
			{[700, 1220, 840].map((x, i) => (
				<Extra key={i} i={i + 3} x={x} floor={FL} s={0.95} seed="cave" facing={x < 960 ? 1 : -1} pose={gesture('point', idle(f, i), env(f, at('045') + 20 + i * 10, 999, 8, 1), f)} />
			))}
			<Callout f={f} t0={at('045') + 30} t1={9999} from={[1240, 220]} to={[1500, 160]} text="FAINT RED DOT" c="#ff5a3a" />
		</Outdoor>
	);
};

/* 046: this one came much, much closer */
const S046: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const u = tw(f, 0, dur, 0, 1);
	const cam = shake(usePush(camOn(960, 540, 1.0), camOn(900, 560, 1.7)), f, at('046') + 40, 20, 12);
	return (
		<SpaceStage cam={cam}>
			<circle cx={760} cy={600} r={200} fill="none" stroke="#4a5a90" strokeWidth={2} />
			<Star x={760} y={600} r={50} c={WHITE_SUN} f={gf} id="w46" />
			<Planet x={760 + 200} y={600} r={16} f={gf} />
			<path d="M1900,-100 Q1100,500 1900,1200" stroke={ORANGE_SUN} strokeWidth={6} fill="none" strokeDasharray="20 14" opacity={0.6} />
			<Star x={1900 - 700 * Math.sin(u * Math.PI * 0.5)} y={-100 + 650 * u} r={60} c={ORANGE_SUN} f={gf} id="o46" />
			<PopText t={f - at('046') - 20} x={1300} y={160} text="MUCH, MUCH CLOSER" size={70} c="#ff8a2a" />
		</SpaceStage>
	);
};

/* 047-048: the world loves it — Day 3 */
const S047: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 560, 1.0), camOn(960, 520, 1.3));
	const hp = beats(idle(f, 2), f, at, [['047', 4, 999, 'cheer']]);
	const j = hops(f, at('047') + 4, 9999, 18, 50);
	return (
		<Outdoor id="s47" cam={cam} mode="gold" suns={[{x: 1450, y: 170, r: 62, c: WHITE_SUN}, {x: 450, y: 220, r: 36, c: ORANGE_SUN, glow: 1.4}]} yard={{hoop: false}}>
			<CrowdRow n={10} x0={0} x1={1920} floor={FL + 30} s={0.85} mode="dance" seed="love" />
			<Hero x={960} s={1.05} pose={hp} bob={j.lift} squash={j.squash} look={[0, -0.6]} mouth="open" uid="h47" />
			{Array.from({length: 6}).map((_, i) => (
				<PopText key={i} t={f - at('047') - 6 - i * 8} x={300 + i * 260} y={260 + (i % 2) * 60} text="♥" size={70} c="#ff5a8a" />
			))}
		</Outdoor>
	);
};

/* 049-050: the most beautiful sunsets; white sun goes down, everything pink */
const S049: React.FC = () => {
	const {f, at, dur} = useShot();
	const set = tw(f, 0, dur, 0, 1);
	const cam = usePush(camOn(960, 520, 1.0), camOn(960, 600, 1.25));
	const fam: [string, number, number][] = [['mom', 620, 1], ['hero', 820, 1.02], ['sam', 980, 0.72], ['dad', 1130, 1.04], ['grandpa', 1300, 1]];
	return (
		<Outdoor id="s49" cam={cam} mode="pink" suns={[{x: 960, y: 520 + 300 * set, r: 70, c: WHITE_SUN}, {x: 1400, y: 380, r: 36, c: ORANGE_SUN, glow: 1.4}]} yard={false} mid={<Svg><path d="M-600,780 q600,-90 1300,-20 t1820,10 L2520,1300 L-600,1300 Z" fill="#7a5a8a" /></Svg>}>
			<rect x={-600} y={860} width={3120} height={400} fill="#5a4a6a" />
			{fam.map(([w, x, s], i) =>
				w === 'hero' ? <Hero key={w} x={x} s={s} facing={1} pose={beats(idle(f, i), f, at, [['050', 20, 999, 'lookUp']])} look={[0, -0.5]} faceTurn={0.1} uid="h49" /> : <Actor key={w} who={w} x={x} s={s} facing={i % 2 ? -1 : 1} faceTurn={0.1} pose={gesture('point', idle(f, i), env(f, at('049') + 30 + i * 15, at('049') + 120 + i * 15, 8, 8), f)} look={[0, -0.5]} uid={'f49' + i} />,
			)}
			<PopText t={f - at('050') - 30} x={960} y={200} text="PINK" size={90} c="#ff9ab8" />
		</Outdoor>
	);
};

/* 051-052: gold, then purple, then a colour nobody has a name for */
const S051: React.FC = () => {
	const {f, at, dur} = useShot();
	const set = tw(f, 0, dur, 0, 1);
	const cam = usePush(camOn(960, 460, 1.2), camOn(960, 400, 1.0));
	const mode = f < at('051') + 60 ? 'gold' : 'dusk';
	const weird = env(f, at('052'), 9999, 20, 1);
	return (
		<>
			<Outdoor id="s51" cam={cam} mode={mode} suns={[{x: 1100, y: 600 + 260 * set, r: 44, c: ORANGE_SUN, glow: 1.6}]} yard={false} mid={<Svg><path d="M-600,780 q600,-90 1300,-20 t1820,10 L2520,1300 L-600,1300 Z" fill="#3a2a4a" /></Svg>}>
				<rect x={-600} y={860} width={3120} height={400} fill="#2a2038" />
				<Hero x={760} pose={beats(idle(f, 1), f, at, [['052', 10, 999, 'touchFace']])} faceTurn={0.1} look={[0.3, -0.6]} expr={weird > 0.5 ? 'wide' : 'normal'} armOver={weird > 0.5} uid="h51" />
				<PopText t={f - at('051') - 40} x={500} y={220} text="GOLD" size={70} c="#ffd34a" out={70} />
				<PopText t={f - at('051') - 80} x={1400} y={260} text="PURPLE" size={70} c="#c88aff" />
				<PopText t={f - at('052') - 20} x={960} y={140} text="???" size={110} c="#7affd0" />
			</Outdoor>
			{weird > 0 ? <AbsoluteFill style={{background: `linear-gradient(${f * 3}deg, #7affd0, #ff7ae0, #7ab0ff)`, opacity: 0.35 * weird, mixBlendMode: 'color', pointerEvents: 'none'}} /> : null}
		</>
	);
};

/* 053: people stop their cars on highways to watch */
const S053: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const cam = usePush(camOn(700, 600, 1.2), camOn(1300, 600, 1.2));
	return (
		<Stage cam={cam} bg="#ff9a3a" light={{x: 70, y: 30, o: 0.45, c: '255,170,90'}}>
			<Layer depth={4}>
				<SkyDomeLite />
			</Layer>
			<Layer depth={1.3}>
				<Road mode="gold" f={gf} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					{[200, 640, 1080, 1520].map((x, i) => {
						const brake = tw(f, i * 6, i * 6 + 30, 1, 0);
						return <SimpleCar key={x} x={x - brake * 300} y={860} c={['#2f6fd8', '#e23a2a', '#3aa37a', '#f2b21c'][i]} s={0.95} />;
					})}
					{[360, 800, 1240].map((x, i) => (
						<Extra key={x} i={i + 20} x={x} floor={720} s={0.8} seed="road" pose={gesture('point', idle(f, i), env(f, 40 + i * 12, 9999, 8, 1), f)} facing={1} />
					))}
					<PopText t={f - at('053') - 20} x={960} y={200} text="STOP! LOOK!" size={64} />
				</Svg>
			</Layer>
		</Stage>
	);
};
const SkyDomeLite: React.FC = () => {
	const {gf} = useShot();
	return (
		<Svg>
			<defs>
				<linearGradient id="sdl" x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor="#ff7a3a" />
					<stop offset="1" stopColor="#ffd08a" />
				</linearGradient>
			</defs>
			<rect x={-600} y={-500} width={3120} height={2000} fill="url(#sdl)" />
			<circle cx={1300} cy={560 + Math.sin(gf / 50) * 4} r={60} fill="#fff6d0" />
			<circle cx={1700} cy={420} r={36} fill={ORANGE_SUN} />
		</Svg>
	);
};

/* 054: couples get engaged at every sunset */
const S054: React.FC = () => {
	const {f, at} = useShot();
	const kneel = tw(f, at('054'), at('054') + 16, 0, 1);
	const mp: Pose = {...idle(f, 2), legF: [-60 * kneel + 4, 80 * kneel], legB: [10, 100 * kneel], armF: [80, 10], lean: -4};
	const yes = env(f, at('054') + 40, 9999, 6, 1);
	const cam = usePush(camOn(960, 620, 1.5), camOn(960, 600, 1.8));
	return (
		<Outdoor id="s54" cam={cam} mode="dusk" suns={[{x: 960, y: 760, r: 70, c: ORANGE_SUN, glow: 1.6}]} yard={false} houses={false}>
			<rect x={-600} y={860} width={3120} height={400} fill="#2a2038" />
			<Extra i={2} x={820} floor={FL + kneel * 40} s={1} pose={mp} seed="love" facing={1} />
			<g transform={`translate(${820 + 120},${FL - 160 + kneel * 40})`}>
				<rect x={-16} y={-16} width={32} height={26} rx={4} fill="#c8102e" />
				<circle cx={0} cy={-22} r={10} fill="none" stroke="#ffd34a" strokeWidth={4} />
				<circle cx={0} cy={-32} r={5} fill="#bfefff" />
			</g>
			<Extra i={5} x={1120} floor={FL} s={0.98} pose={custom2(f, yes)} seed="love2" facing={-1} expr={yes > 0.5 ? 'wide' : 'normal'} />
			<Burst t={f - at('054') - 44} x={970} y={500} c={['#ff5a8a', '#ffd34a', '#fff']} seed="ring" />
			<PopText t={f - at('054') - 48} x={1120} y={340} text="YES!" size={80} c="#ff5a8a" />
		</Outdoor>
	);
};
const custom2 = (f: number, k: number): Pose => ({...idle(f, 5), armF: [20 + 140 * k, 30], armB: [-20 - 140 * k, 30], head: -10 * k});

/* 055-056: the two-sunset festival: band, food truck, Two Suns Special */
const S055: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = mixCam(camOn(760, 560, 1.15), camOn(1400, 600, 1.45), tw(f, at('056') + 30, at('056') + 70, 0, 1));
	const hp = beats(path(f, [[0, 900], [at('056') + 40, 900], [at('056') + 80, 1260]], 3).pose, f, at, [['055', 10, 60, 'wave'], ['056', 110, 120, 'carry']]);
	const hx = path(f, [[0, 900], [at('056') + 40, 900], [at('056') + 80, 1260]], 3);
	return (
		<Outdoor id="s55" cam={cam} mode="gold" suns={[{x: 1450, y: 170, r: 62, c: WHITE_SUN}, {x: 400, y: 200, r: 36, c: ORANGE_SUN, glow: 1.4}]} yard={false}>
			<rect x={-600} y={860} width={3120} height={400} fill="#7a9a3a" />
			{/* banner */}
			<g transform={`translate(760,${180 + Math.sin(f / 12) * 6})`}>
				<line x1={-460} y1={-20} x2={-460} y2={700} stroke="#5a3a22" strokeWidth={12} />
				<line x1={460} y1={-20} x2={460} y2={700} stroke="#5a3a22" strokeWidth={12} />
				<path d={`M-460,0 Q0,${30 + Math.sin(f / 10) * 8} 460,0 L460,110 Q0,${140 + Math.sin(f / 10) * 8} -460,110 Z`} fill="#c8102e" />
				<text x={0} y={80} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill="#fff">
					TWO-SUNSET FESTIVAL
				</text>
			</g>
			{/* band */}
			{[420, 560, 700].map((x, i) => (
				<Extra key={x} i={i + 40} x={x} floor={FL - 20} s={0.9} seed="band" pose={{...idle(f, i), armF: [60 + Math.sin(f / 2 + i) * 20, 60], head: Math.sin(f / 4 + i) * 10}} facing={1} />
			))}
			{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
				<text key={i} x={500 + i * 70 + Math.sin(f / 8 + i) * 20} y={520 - ((f * 2 + i * 40) % 260)} fontSize={44} fill="#fff" opacity={0.8}>
					♪
				</text>
			))}
			{/* food truck */}
			<g transform="translate(1560,880)">
				<rect x={-260} y={-300} width={520} height={260} rx={20} fill="#f2e6d0" />
				<rect x={-200} y={-250} width={300} height={130} fill="#3a3f4a" />
				<rect x={-280} y={-330} width={560} height={50} rx={10} fill="#ff8a2a" />
				<text x={0} y={-294} textAnchor="middle" fontSize={34} fontFamily={FONT} fontWeight={900} fill="#fff">
					TWO SUNS SPECIAL
				</text>
				<circle cx={-170} cy={-30} r={40} fill="#1a1a1e" />
				<circle cx={170} cy={-30} r={40} fill="#1a1a1e" />
			</g>
			<Actor who="seller" x={1520} floor={FL - 190} s={0.75} pose={beats(idle(f, 8), f, at, [['056', 20, 80, 'wave']])} hideLegs facing={-1} uid="sell55" />
			<Hero x={hx.x} pose={hp} facing={hx.facing} vx={hx.vx} bob={hx.bob} mouth={f > at('056') + 120 ? 'open' : undefined} uid="h55" />
			{/* the double-yolk egg */}
			<g transform={`translate(${f > at('056') + 110 ? hx.x + 70 : 1460},${f > at('056') + 110 ? 760 : 700}) scale(${env(f, at('056') + 60, 9999, 10, 1)})`}>
				<ellipse cx={0} cy={0} rx={70} ry={50} fill="#fff" />
				<circle cx={-22} cy={0} r={18} fill="#ffb020" />
				<circle cx={24} cy={4} r={18} fill="#ff8a10" />
			</g>
			<Callout f={f} t0={at('056') + 80} t1={9999} from={[1460, 700]} to={[1250, 440]} text="DOUBLE YOLK!" />
		</Outdoor>
	);
};

/* 057-058: solar panels go crazy; the neighbour gets a check */
const S057: React.FC = () => {
	const {f, at} = useShot();
	const cam = mixCam(camOn(150, 340, 1.6), camOn(800, 560, 1.4), tw(f, at('058'), at('058') + 30, 0, 1));
	const check = env(f, at('058') + 50, 9999, 12, 1);
	const np = beats(idle(f, 5), f, at, [['058', 50, 999, 'carry']]);
	const j = hops(f, at('058') + 70, 9999, 16, 40);
	return (
		<Outdoor id="s57" cam={cam} mode="hot" suns={[{x: 1450, y: 170, r: 70, c: WHITE_SUN}, {x: 700, y: 110, r: 40, c: ORANGE_SUN, glow: 1.5}]} yard={{panels: 1, hoop: false}}>
			{Array.from({length: 10}).map((_, i) => (
				<path key={i} d={`M${-40 + (i % 4) * 110 + 20},${300 - ((f * 4 + i * 30) % 120)} l12,-20 l-8,0 l12,-24`} stroke="#ffe04a" strokeWidth={5} fill="none" opacity={0.9} />
			))}
			<PopText t={f - at('057') - 8} x={180} y={250} text="ZAP! ZAP!" size={60} c="#ffe04a" />
			<Actor who="neighbor" x={760} s={1} pose={np} bob={j.lift} mouth={check > 0.5 ? 'open' : undefined} expr={check > 0.5 ? 'wide' : 'normal'} uid="nb57" />
			<g transform={`translate(${860},${700 - j.lift}) scale(${check}) rotate(-4)`}>
				<rect x={-60} y={-80} width={360} height={170} rx={10} fill="#e8f6e0" stroke="#3a8a3a" strokeWidth={5} />
				<text x={120} y={-30} textAnchor="middle" fontSize={26} fontFamily={FONT} fill="#3a6a3a">
					POWER CO.
				</text>
				<text x={120} y={40} textAnchor="middle" fontSize={64} fontFamily={FONT} fontWeight={900} fill="#2a7a2a">
					$$$$
				</text>
			</g>
		</Outdoor>
	);
};

/* 059-060: plants grow faster; mom's tomatoes double in a week */
const S059: React.FC = () => {
	const {f, at} = useShot();
	const g = tw(f, at('059'), at('060') + 70, 0, 1);
	const cam = usePush(camOn(700, 680, 1.4), camOn(680, 640, 1.8));
	const mp = beats(idle(f, 6), f, at, [['060', 60, 999, 'carry']]);
	return (
		<Outdoor id="s59" cam={cam} mode="gold" suns={[{x: 1450, y: 170, r: 62, c: WHITE_SUN}, {x: 900, y: 120, r: 36, c: ORANGE_SUN, glow: 1.4}]} yard={{garden: g, hoop: false}}>
			<Actor who="mom" x={1000} s={1} facing={-1} pose={mp} expr={g > 0.7 ? 'wide' : 'normal'} look={[-0.7, 0.2]} mouth={g > 0.7 ? 'open' : undefined} uid="mom59" />
			{env(f, at('060') + 60, 9999, 10, 1) > 0 ? <circle cx={920} cy={720} r={50 * env(f, at('060') + 60, 9999, 10, 1)} fill="#e23a2a" /> : null}
			<Pill t={f - at('060') - 20} x={680} y={420} text="×2 IN A WEEK" c="#e23a2a" size={44} />
			<PopText t={f - at('059') - 10} x={1240} y={300} text="GROW!" size={70} c="#9ff0b0" out={60} />
		</Outdoor>
	);
};

/* 061-062: teachers can't decide when the day starts */
const S061: React.FC = () => {
	const {f, gf, at} = useShot();
	const tp = beats(idle(f, 3), f, at, [['061', 10, 60, 'point'], ['061', 80, 60, 'scratch'], ['062', 0, 80, 'shrug']]);
	const cam = usePush(camOn(960, 520, 1.1), camOn(900, 520, 1.45));
	const write = tw(f, at('061') + 20, at('061') + 60, 0, 1);
	return (
		<Inside cam={cam} set={<School f={gf} />} light={{x: 50, y: 10, o: 0.35}}>
			<text x={960} y={330} textAnchor="middle" fontSize={70} fontFamily="'Caveat', cursive" fontWeight={700} fill="#f4f1e6" opacity={write}>
				SCHOOL STARTS AT: ???
			</text>
			<text x={960} y={460} textAnchor="middle" fontSize={60} fontFamily="'Caveat', cursive" fontWeight={700} fill="#ffd34a" opacity={tw(f, at('062'), at('062') + 20, 0, 1)}>
				...whenever?
			</text>
			<Actor who="teacher" x={1500} s={1.05} facing={-1} pose={tp} handF={on(f, at, '061', 10, 60) > 0.5 ? 'point' : undefined} expr="worried" look={[-0.6, -0.3]} uid="t61" />
			{[300, 520, 740].map((x, i) => (
				<Extra key={x} i={i + 60} x={x} floor={FL + 20} s={0.78} seed="kids" pose={gesture('shrug', idle(f, i), env(f, at('062') + 10 + i * 6, 9999, 8, 1), f)} facing={1} />
			))}
		</Inside>
	);
};

export const SHOTS1: ShotDef[] = [
	{at: '001', C: S001},
	{at: '002', C: S002},
	{at: '004', C: S004},
	{at: '005', C: S005},
	{at: '007', C: S007},
	{at: '009', C: S009, whip: true},
	{at: '010', C: S010},
	{at: '012', C: S012, whip: true},
	{at: '013', C: S013},
	{at: '015', C: S015},
	{at: '018', C: S018, whip: true},
	{at: '019', C: S019},
	{at: '021', C: S021},
	{at: '023', C: S023},
	{at: '026', C: S026},
	{at: '028', C: S028},
	{at: '031', C: S031, whip: true},
	{at: '034', C: S034},
	{at: '035', C: S035},
	{at: '036', C: S036},
	{at: '038', C: S038, whip: true},
	{at: '039', C: S039, whip: true},
	{at: '043', C: S043, whip: true},
	{at: '045', C: S045},
	{at: '046', C: S046},
	{at: '047', C: S047, whip: true},
	{at: '049', C: S049},
	{at: '051', C: S051},
	{at: '053', C: S053, whip: true},
	{at: '054', C: S054},
	{at: '055', C: S055, whip: true},
	{at: '057', C: S057},
	{at: '059', C: S059},
	{at: '061', C: S061, whip: true},
];
export {Cereal, Fence, Rooster, Mower, badgeY, Tree, Planet};
