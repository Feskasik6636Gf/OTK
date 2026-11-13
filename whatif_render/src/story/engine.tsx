import React from 'react';
import {AbsoluteFill, interpolate, random, spring, Easing} from 'remotion';
import {Pose} from '../engine/Stickman';
import {blend, env, gesture, idle, reach, run, walk, walkTo, SIT} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {HeroBadge, Layer, Stage, Svg, camOn, mixCam, clamp} from '../kit/kit';
import {Accent, FONT, HAND} from '../kit/ui';
import {Kitchen, Corridor, KitchenTable, Lamp} from '../kit/sets';
import {Chair} from '../engine/props';
import type {Cam} from '../engine/camera';
import {
	Office, BigDesk, Classroom, SchoolDesks, Cafeteria, LunchTable, Lab, Rat, Road, CarSide, BigStage, Audience, Club, Studio,
	LivingRoom, Armchair, Hospital, Porch, Field, Bathroom, NightCity, Village,
} from './places';
import {Stickman} from '../engine/Stickman';
import {CAST} from './cast';

/* ============================== BEAT ENGINE ===============================
   Every voice line is a beat: a location, the actors with what they do during the line,
   props, effects and a camera move. One beat = one shot, so the picture changes with
   every sentence (~3 s); longer lines also get automatic coverage cuts. */

export type Act =
	| 'idle' | 'talk' | 'laugh' | 'laughBig' | 'laughFloor' | 'cry' | 'shrug' | 'think' | 'facepalm' | 'scratch' | 'point' | 'wave'
	| 'shock' | 'cross' | 'jump' | 'dance' | 'conga' | 'fall' | 'pickup' | 'give' | 'knock' | 'mic' | 'raise' | 'stare' | 'wipe'
	| 'sad' | 'nod' | 'no' | 'cheer' | 'tour' | 'bow' | 'scared' | 'phone' | 'write' | 'fist' | 'hold' | 'snap' | 'run' | 'hug';

export type ActorB = {
	w: string; // cast id
	x: number;
	to?: number; // walks (or runs) to this x during the line
	t0?: number; // walk start (0..1 of line), default 0.02
	t1?: number; // walk end (0..1), default by distance
	a?: Act; // action
	b?: Act; // second action from `ab` (0..1, default 0.5)
	ab?: number;
	fc?: 1 | -1; // facing
	s?: number; // scale
	sit?: boolean; // sits on a chair
	chair?: boolean; // draw the chair (default true when sitting)
	lie?: boolean; // lying in bed / on the floor
	floor?: number;
	e?: 'normal' | 'angry' | 'sad' | 'sleepy' | 'wide' | 'worried';
	m?: 'line' | 'frown' | 'open' | 'smile' | 'flat' | 'smirk' | 'none';
	say?: boolean; // mouth follows the voice (his quoted words)
	item?: 'mic' | 'phone' | 'pencil' | 'clipboard' | 'note' | 'cup' | 'ticket' | 'pizza' | 'tray' | 'fruit' | 'flower';
	badge?: boolean; // force / hide the counter badge
	hide?: boolean;
	until?: number; // disappears after this point of the line (0..1)
};
export type Fx = {
	k: 'text' | 'acc' | 'title' | 'shake' | 'flash' | 'icon' | 'bubble' | 'alarm' | 'smoke' | 'hearts' | 'confetti' | 'burst' | 'rec' | 'count' | 'tears' | 'zzz' | 'dark' | 'sweat' | 'milk' | 'sparkle' | 'ha';
	t?: string;
	sub?: string;
	at?: number; // 0..1 of the line
	to?: number; // end 0..1
	x?: number;
	y?: number;
	on?: number; // actor index it attaches to
	c?: string;
	i?: Icon;
	n?: [number, number];
	size?: number;
};
export type Icon = 'heart' | 'fire' | 'phone' | 'star' | 'bulb' | 'q' | 'ex' | 'note' | 'skull' | 'clock' | 'ticket' | 'tv' | 'brain' | 'pizza' | 'medal' | 'eye' | 'bell' | 'money' | 'dog' | 'tea' | 'drop' | 'bone' | 'shoe' | 'like' | 'fruit';
export type PropB = {p: 'desk' | 'table' | 'lunch' | 'desks' | 'car' | 'police' | 'armchair' | 'chairF' | 'rat' | 'mic' | 'bed' | 'lamp' | 'door'; x?: number; front?: boolean; c?: string; xs?: number[]; open?: number; laugh?: boolean; move?: number};
export type Crowd = {mode: 'laugh' | 'sit' | 'stand' | 'conga' | 'run' | 'panic' | 'dance' | 'walk' | 'sitLaugh' | 'cheer'; n: number; x0: number; x1: number; s?: number; floor?: number; depth?: number; seed?: string; dir?: 1 | -1};
export type CamK = 'push' | 'pull' | 'panL' | 'panR' | 'close' | 'wide' | 'low' | 'two' | 'orbit' | 'crash' | 'follow' | 'dutch' | 'rise' | 'drop' | 'whipin';
export type Loc =
	| 'office' | 'kitchen' | 'kitchenN' | 'classroom' | 'science' | 'cafeteria' | 'corridor' | 'lab' | 'road' | 'stage' | 'club' | 'studio' | 'city' | 'village'
	| 'living' | 'livingDim' | 'hospital' | 'porchBen' | 'porchAyva' | 'porchBenDusk' | 'bathroom' | 'field' | 'fieldSmoke' | 'hall' | 'black';
export type Beat = {
	loc: Loc;
	cam?: CamK;
	on?: number; // actor the camera works on
	on2?: number;
	z?: number;
	cy?: number; // camera y offset
	cast?: ActorB[];
	props?: PropB[];
	crowd?: Crowd[];
	fx?: Fx[];
	card?: string; // a full-frame motion-graphics card instead of a set
	whip?: boolean;
	smoke?: number;
	alarm?: number;
};

/* ------------------------------ locations ------------------------------- */
const LOCS: Record<Loc, {bg: string; light?: any; set: (f: number, b: Beat) => React.ReactNode; depth?: number}> = {
	office: {bg: '#2c4560', light: {x: 78, y: 20, o: 0.45}, set: (f) => <Office f={f} />},
	kitchen: {bg: '#f3e6c4', light: {x: 50, y: 15, o: 0.42}, set: () => <Kitchen />},
	kitchenN: {bg: '#2a2a48', light: {x: 50, y: 20, night: true, o: 0.4}, set: () => <Kitchen night />},
	classroom: {bg: '#e9dcb4', light: {x: 80, y: 20, o: 0.42}, set: (f) => <Classroom f={f} />},
	science: {bg: '#bfe0d4', light: {x: 80, y: 20, o: 0.42}, set: (f) => <Classroom f={f} science board="Биология" />},
	cafeteria: {bg: '#f7d9a8', light: {x: 20, y: 15, o: 0.4}, set: (f) => <Cafeteria f={f} />},
	corridor: {bg: '#f1e6c8', light: {x: 80, y: 15, o: 0.42}, set: (f) => <Corridor f={f} />},
	lab: {bg: '#cfe8ef', light: {x: 40, y: 10, o: 0.4}, set: (f) => <Lab f={f} />},
	road: {bg: '#7cc0ec', light: {x: 30, y: 10, o: 0.45}, set: (f) => <Road f={f} />},
	stage: {bg: '#20163a', light: {x: 50, y: 10, o: 0.5, c: '255,220,160'}, set: (f, b) => <BigStage f={f} smoke={b.smoke} alarm={b.alarm} />},
	hall: {bg: '#20163a', light: {x: 50, y: 10, o: 0.5, c: '255,220,160'}, set: (f, b) => <BigStage f={f} title="ВЫПУСКНОЙ ГОДА" smoke={b.smoke} alarm={b.alarm} />},
	club: {bg: '#3a1a18', light: {x: 50, y: 5, o: 0.55, c: '255,200,220'}, set: (f) => <Club f={f} />},
	studio: {bg: '#141a3a', light: {x: 60, y: 10, o: 0.5, c: '200,180,255'}, set: (f) => <Studio f={f} />},
	city: {bg: '#070b26', light: {x: 80, y: 10, night: true, o: 0.4}, set: (f) => <NightCity f={f} />},
	village: {bg: '#f0a050', light: {x: 75, y: 25, o: 0.5}, set: (f) => <Village f={f} />},
	living: {bg: '#d9c6a0', light: {x: 50, y: 20, o: 0.45}, set: (f) => <LivingRoom f={f} />},
	livingDim: {bg: '#5a5a6a', light: {x: 50, y: 20, o: 0.3, c: '200,210,255'}, set: (f) => <LivingRoom f={f} dim />},
	hospital: {bg: '#d6f0ec', light: {x: 50, y: 15, o: 0.4}, set: (f) => <Hospital f={f} />},
	porchBen: {bg: '#8fc6ec', light: {x: 30, y: 10, o: 0.45}, set: (f, b) => <Porch f={f} door="#2f8a5a" c="#e8d0b0" open={doorOpen(b, f)} />},
	porchBenDusk: {bg: '#f08a5a', light: {x: 20, y: 30, o: 0.5, c: '255,190,140'}, set: (f, b) => <Porch f={f} door="#2f8a5a" c="#e8d0b0" dusk open={doorOpen(b, f)} />},
	porchAyva: {bg: '#f08a5a', light: {x: 20, y: 30, o: 0.5, c: '255,190,140'}, set: (f, b) => <Porch f={f} door="#c64a7a" c="#f2e2c8" dusk open={doorOpen(b, f)} />},
	bathroom: {bg: '#1d2238', light: {x: 70, y: 5, o: 0.35, night: true}, set: (f) => <Bathroom f={f} />},
	field: {bg: '#7cc0ec', light: {x: 30, y: 10, o: 0.45}, set: (f, b) => <Field f={f} trucks={b.props?.some((p) => p.p === 'car') ? 0 : 0} />},
	fieldSmoke: {bg: '#f0a070', light: {x: 70, y: 10, o: 0.45}, set: (f, b) => <Field f={f} smoke={1} dusk trucks={(b as any).trucks ?? 0} />},
	black: {bg: '#06060c', light: false, set: () => null},
};
const doorOpen = (b: Beat, f: number) => {
	const d = b.props?.find((p) => p.p === 'door');
	return d ? (d.open ?? 1) * Math.min(1, Math.max(0, (f - (d.move ?? 0)) / 10)) : 0;
};

/* ------------------------------ hand items ------------------------------ */
const Item: React.FC<{i: ActorB['item']}> = ({i}) => {
	switch (i) {
		case 'mic':
			return (
				<g transform="rotate(-30)">
					<rect x={-5} y={-6} width={10} height={44} rx={4} fill="#2b2b30" />
					<circle cx={0} cy={-14} r={13} fill="#9aa3b5" />
					<circle cx={0} cy={-14} r={13} fill="none" stroke="#5a6278" strokeWidth={2} />
				</g>
			);
		case 'phone':
			return (
				<g>
					<rect x={-16} y={-46} width={32} height={58} rx={6} fill="#1b1e2a" />
					<rect x={-12} y={-40} width={24} height={44} rx={3} fill="#7ad0ff" />
				</g>
			);
		case 'pencil':
			return <g transform="rotate(30)"><rect x={-4} y={-40} width={8} height={56} fill="#f2b21c" /><path d="M-4,16 L0,26 L4,16 Z" fill="#333" /></g>;
		case 'clipboard':
			return (
				<g transform="rotate(-8)">
					<rect x={-30} y={-60} width={60} height={80} rx={4} fill="#a9805a" />
					<rect x={-24} y={-52} width={48} height={66} fill="#fff" />
					{[0, 1, 2, 3].map((k) => <line key={k} x1={-18} y1={-40 + k * 14} x2={18} y2={-40 + k * 14} stroke="#999" strokeWidth={3} />)}
				</g>
			);
		case 'note':
			return <g transform="rotate(-10)"><rect x={-26} y={-40} width={52} height={40} fill="#fff8b0" />{[0, 1].map((k) => <line key={k} x1={-18} y1={-28 + k * 12} x2={18} y2={-28 + k * 12} stroke="#5a5a8a" strokeWidth={3} />)}</g>;
		case 'cup':
			return <g><rect x={-14} y={-30} width={28} height={30} rx={5} fill="#f2f2f2" /><rect x={-14} y={-30} width={28} height={8} fill="#b0703a" /></g>;
		case 'ticket':
			return <g transform="rotate(-15)"><rect x={-34} y={-24} width={68} height={40} rx={4} fill="#ffe08a" stroke="#c94a3a" strokeWidth={3} /><text x={0} y={2} textAnchor="middle" fontSize={14} fontFamily={FONT} fill="#c94a3a">ШТРАФ</text></g>;
		case 'pizza':
			return <g><path d="M0,0 L-30,-60 Q0,-75 30,-60 Z" fill="#f2c45a" /><circle cx={-6} cy={-44} r={6} fill="#c62a2a" /><circle cx={8} cy={-30} r={5} fill="#c62a2a" /></g>;
		case 'tray':
			return <g><rect x={-50} y={-10} width={100} height={12} rx={4} fill="#f2a14a" /><ellipse cx={-14} cy={-14} rx={18} ry={7} fill="#a8643a" /></g>;
		case 'fruit':
			return <g><rect x={-40} y={-50} width={80} height={50} rx={10} fill="#c98a4a" /><circle cx={-18} cy={-56} r={16} fill="#ff6a3a" /><circle cx={8} cy={-60} r={15} fill="#7cc46a" /><circle cx={26} cy={-52} r={13} fill="#ffd34a" /></g>;
		case 'flower':
			return <g><line x1={0} y1={0} x2={0} y2={-50} stroke="#3a8a3a" strokeWidth={4} /><circle cx={0} cy={-56} r={12} fill="#ff6aa0" /></g>;
	}
	return null;
};

/* -------------------------------- icons ---------------------------------- */
export const IconG: React.FC<{i: Icon; s?: number}> = ({i, s = 1}) => {
	const c = (n: React.ReactNode) => <g transform={`scale(${s})`}>{n}</g>;
	switch (i) {
		case 'heart':
			return c(<path d="M0,30 C-60,-10 -40,-60 0,-30 C40,-60 60,-10 0,30 Z" fill="#ff4f6b" />);
		case 'fire':
			return c(<g><path d="M0,40 C-50,30 -40,-20 -10,-50 C-10,-20 10,-20 10,-40 C50,-10 50,30 0,40 Z" fill="#ff7a2a" /><path d="M0,40 C-24,30 -18,0 0,-14 C18,4 22,30 0,40 Z" fill="#ffd34a" /></g>);
		case 'phone':
			return c(<g><rect x={-30} y={-55} width={60} height={110} rx={10} fill="#1b1e2a" /><rect x={-24} y={-45} width={48} height={86} rx={4} fill="#7ad0ff" /></g>);
		case 'star':
			return c(<path d="M0,-50 L14,-16 L50,-14 L22,8 L32,44 L0,24 L-32,44 L-22,8 L-50,-14 L-14,-16 Z" fill="#ffd34a" />);
		case 'bulb':
			return c(<g><circle cx={0} cy={-10} r={36} fill="#ffe08a" /><rect x={-16} y={22} width={32} height={22} rx={4} fill="#9aa3b5" /></g>);
		case 'q':
			return c(<text y={30} textAnchor="middle" fontSize={110} fontFamily={FONT} fontWeight={900} fill="#ff2338">?</text>);
		case 'ex':
			return c(<text y={30} textAnchor="middle" fontSize={110} fontFamily={FONT} fontWeight={900} fill="#ffd34a">!</text>);
		case 'note':
			return c(<g><circle cx={-12} cy={24} r={14} fill="#fff" /><rect x={-1} y={-40} width={6} height={64} fill="#fff" /><path d="M5,-40 q30,10 26,34" stroke="#fff" strokeWidth={6} fill="none" /></g>);
		case 'skull':
			return c(<g><circle cx={0} cy={-8} r={36} fill="#f4f1e8" /><rect x={-20} y={18} width={40} height={20} rx={4} fill="#f4f1e8" /><circle cx={-13} cy={-8} r={9} fill="#222" /><circle cx={13} cy={-8} r={9} fill="#222" /></g>);
		case 'clock':
			return c(<g><circle r={44} fill="#fff" stroke="#333" strokeWidth={6} /><line x1={0} y1={0} x2={0} y2={-28} stroke="#222" strokeWidth={5} /><line x1={0} y1={0} x2={20} y2={8} stroke="#222" strokeWidth={5} /></g>);
		case 'ticket':
			return c(<g><rect x={-60} y={-34} width={120} height={68} rx={6} fill="#ffe08a" stroke="#c94a3a" strokeWidth={5} /><text y={10} textAnchor="middle" fontSize={26} fontFamily={FONT} fill="#c94a3a">ШТРАФ</text></g>);
		case 'tv':
			return c(<g><rect x={-60} y={-44} width={120} height={84} rx={10} fill="#2b2f3a" /><rect x={-50} y={-36} width={100} height={66} fill="#7ad0ff" /></g>);
		case 'brain':
			return c(<g><path d="M-40,10 C-60,-30 -20,-55 0,-40 C20,-55 60,-30 40,10 C40,40 -40,40 -40,10 Z" fill="#ff9ab8" /><path d="M0,-38 V30 M-24,-20 q10,10 0,24 M24,-20 q-10,10 0,24" stroke="#d96a8a" strokeWidth={4} fill="none" /></g>);
		case 'pizza':
			return c(<g><path d="M0,40 L-40,-40 Q0,-60 40,-40 Z" fill="#f2c45a" /><circle cx={-8} cy={-20} r={8} fill="#c62a2a" /><circle cx={12} cy={0} r={7} fill="#c62a2a" /></g>);
		case 'medal':
			return c(<g><path d="M-20,-50 L0,-10 L20,-50" stroke="#3d6fd6" strokeWidth={12} fill="none" /><circle cy={14} r={30} fill="#ffd34a" /><text y={24} textAnchor="middle" fontSize={30} fontFamily={FONT} fill="#a07a1a">1</text></g>);
		case 'eye':
			return c(<g><ellipse rx={50} ry={28} fill="#fff" /><circle r={16} fill="#2a2a3a" /></g>);
		case 'bell':
			return c(<g><path d="M-36,24 C-36,-30 36,-30 36,24 Z" fill="#ff3a3a" /><rect x={-44} y={22} width={88} height={10} rx={4} fill="#c62a2a" /></g>);
		case 'money':
			return c(<g><rect x={-60} y={-30} width={120} height={60} rx={6} fill="#7cc46a" /><text y={12} textAnchor="middle" fontSize={34} fontFamily={FONT} fill="#1d5a2a">$</text></g>);
		case 'dog':
			return c(<g><ellipse cx={0} cy={10} rx={46} ry={26} fill="#c98a4a" /><circle cx={40} cy={-14} r={24} fill="#c98a4a" /><ellipse cx={30} cy={-34} rx={8} ry={16} fill="#8a5a2a" /><circle cx={48} cy={-18} r={4} fill="#111" /></g>);
		case 'tea':
			return c(<g><rect x={-30} y={-20} width={60} height={50} rx={8} fill="#fff" /><path d="M30,-10 q20,0 20,14 q0,14 -20,14" stroke="#fff" strokeWidth={7} fill="none" /><path d="M-10,-30 q-10,-14 0,-28 M10,-30 q-10,-14 0,-28" stroke="#ccc" strokeWidth={4} fill="none" /></g>);
		case 'drop':
			return c(<path d="M0,-30 C20,0 20,20 0,24 C-20,20 -20,0 0,-30 Z" fill="#7ad0ff" />);
		case 'bone':
			return c(<g><rect x={-40} y={-8} width={80} height={16} rx={8} fill="#f4f1e8" />{[-40, 40].map((x) => <g key={x}><circle cx={x} cy={-10} r={12} fill="#f4f1e8" /><circle cx={x} cy={10} r={12} fill="#f4f1e8" /></g>)}</g>);
		case 'shoe':
			return c(<path d="M-50,10 L-50,-20 L-10,-20 L10,0 L50,6 L50,20 L-50,20 Z" fill="#c94a3a" />);
		case 'like':
			return c(<g><rect x={-44} y={-10} width={22} height={46} rx={4} fill="#3d6fd6" /><path d="M-18,-10 L0,-50 C14,-50 14,-30 10,-14 L40,-14 C50,-14 50,0 44,4 L40,36 L-18,36 Z" fill="#3d6fd6" /></g>);
		case 'fruit':
			return c(<g><rect x={-50} y={-20} width={100} height={50} rx={10} fill="#c98a4a" /><circle cx={-22} cy={-26} r={20} fill="#ff6a3a" /><circle cx={10} cy={-30} r={18} fill="#7cc46a" /><circle cx={32} cy={-22} r={15} fill="#ffd34a" /></g>);
	}
	return null;
};

/* ------------------------- action -> pose / face ------------------------- */
const LAUGHS = new Set<Act>(['laugh', 'laughBig', 'laughFloor']);
type Out = {pose: Pose; e?: ActorB['e']; m?: ActorB['m']; armOver?: boolean; rot?: number; lift?: number; squash?: number; look?: [number, number]; handF?: 'point' | 'fist' | 'snap'; lid?: number};
const actPose = (a: Act, base: Pose, f: number, k: number, D: number, gf: number): Out => {
	switch (a) {
		case 'talk': {
			const ph = Math.floor(f / 26) % 3;
			const g = (['presentF', 'point', 'shrug'] as const)[ph];
			const kk = k * env(f % 26, 2, 20, 6, 6);
			return {pose: gesture(g, {...base, head: base.head + Math.sin(f / 7) * 3}, kk, f), handF: g === 'point' && kk > 0.5 ? 'point' : undefined};
		}
		case 'laugh': {
			const bounce = Math.sin(f / 2.4);
			const p = {...base, lean: base.lean - 12 * k + bounce * 4 * k, head: base.head - 16 * k + bounce * 6 * k};
			return {pose: reach(reach(p, 'F', [26, -60], k), 'B', [20, -50], k), e: 'sleepy', m: 'open', lift: Math.abs(bounce) * 5 * k, look: [0, -0.6]};
		}
		case 'laughBig': {
			const ph = Math.sin(f / 5);
			const p = {...base, lean: base.lean + (ph > 0 ? 28 * ph : -16 * -ph) * k, head: base.head - 12 * k + Math.sin(f / 2.2) * 6 * k};
			return {pose: {...p, armF: [lerpN(base.armF[0], 60 + 50 * Math.abs(Math.sin(f / 3)), k), lerpN(base.armF[1], 90, k)], armB: [lerpN(base.armB[0], -30, k), lerpN(base.armB[1], 80, k)]}, e: 'sleepy', m: 'open', lift: Math.abs(Math.sin(f / 2.4)) * 7 * k};
		}
		case 'laughFloor': {
			const fallK = interpolate(f, [0, 14], [0, 1], {...clamp, easing: Easing.out(Easing.quad)});
			const roll = Math.sin(f / 3) * 6 * fallK;
			return {pose: {lean: 0, head: -10 + Math.sin(f / 2) * 8, armF: [70 + Math.sin(f / 2.5) * 40, 90], armB: [-60, 80], legF: [70 + Math.sin(f / 3) * 30, 60], legB: [40 - Math.sin(f / 3) * 30, 50]}, rot: -84 * fallK + roll, e: 'sleepy', m: 'open'};
		}
		case 'cry':
			return {pose: gesture('facepalm', {...base, head: base.head + 18 * k, lean: base.lean + 8 * k + Math.sin(f / 3) * 2 * k}, k, f), e: 'sad', m: 'frown', armOver: k > 0.5};
		case 'wipe':
			return {pose: gesture('touchFace', base, k, f), e: 'sad', m: 'smile', armOver: k > 0.5};
		case 'shrug':
			return {pose: gesture('shrug', base, k * env(f, 0, D - 10, 8, 10), f), m: 'smirk'};
		case 'think':
			return {pose: gesture('think', base, k, f), look: [0.5, -0.8], m: 'flat'};
		case 'facepalm':
			return {pose: gesture('facepalm', base, k, f), armOver: k > 0.5, e: 'sad'};
		case 'scratch':
			return {pose: gesture('scratch', base, k, f), look: [0.4, -0.6], m: 'flat'};
		case 'point':
			return {pose: gesture('point', base, k, f), handF: k > 0.5 ? 'point' : undefined};
		case 'wave':
			return {pose: gesture('wave', base, k, f), m: 'smile'};
		case 'shock':
			return {pose: gesture('handsOnHead', base, k, f), e: 'wide', m: 'open', squash: Math.max(0, 0.08 - f * 0.01)};
		case 'scared':
			return {pose: gesture('stop', {...base, lean: base.lean - 10 * k}, k, f), e: 'wide', m: 'open'};
		case 'cross':
			return {pose: gesture('armsCrossed', base, k, f), e: 'angry', m: 'flat'};
		case 'fist':
			return {pose: gesture('fist', base, k, f), e: 'angry', handF: 'fist'};
		case 'jump': {
			const ph = (f % 20) / 20;
			const h = Math.sin(ph * Math.PI) * 60 * k;
			return {pose: {...base, armF: [lerpN(base.armF[0], 165, k), 10], armB: [lerpN(base.armB[0], -160, k), 10], legF: [20 * k, 40 * k * (1 - Math.sin(ph * Math.PI))], legB: [-10 * k, 30 * k]}, lift: h, squash: ph < 0.1 ? 0.06 * k : 0, e: 'wide', m: 'open'};
		}
		case 'cheer': {
			const h = Math.abs(Math.sin(f / 4)) * 26 * k;
			return {pose: {...base, armF: [lerpN(base.armF[0], 160, k), 20], armB: [lerpN(base.armB[0], -155, k), 20]}, lift: h, m: 'open', e: 'wide'};
		}
		case 'dance': {
			const ph = f / 6;
			return {pose: {lean: Math.sin(ph) * 10, head: Math.sin(ph * 2) * 10, armF: [120 + Math.sin(ph) * 40, 30], armB: [-120 + Math.cos(ph) * 40, 30], legF: [10 + Math.sin(ph) * 18, 14], legB: [-10, 12]}, lift: Math.abs(Math.sin(ph)) * 10, m: 'smile'};
		}
		case 'conga': {
			const ph = f / 4;
			const kick = Math.max(0, Math.sin(ph / 2));
			return {pose: {lean: 6, head: Math.sin(ph) * 8, armF: [82, 12], armB: [74, 16], legF: [18 + 30 * kick, 10], legB: [-14, 8]}, lift: Math.abs(Math.sin(ph)) * 6, m: 'open', e: 'sleepy'};
		}
		case 'fall': {
			const fk = interpolate(f, [0, 10], [0, 1], {...clamp, easing: Easing.in(Easing.quad)});
			return {pose: {...base, armF: [120, 40], armB: [-140, 40], legF: [40 * fk, 10]}, rot: -88 * fk, e: 'wide', m: 'open'};
		}
		case 'pickup':
			return {pose: reach({...base, lean: base.lean + 42 * k, head: base.head + 10 * k, legF: [base.legF[0] + 18 * k, base.legF[1] + 30 * k], legB: [base.legB[0] - 6 * k, base.legB[1] + 20 * k]}, 'F', [70, 120], k)};
		case 'give':
			return {pose: reach({...base, lean: base.lean + 6 * k}, 'F', [100, -70], k), m: 'smile'};
		case 'hold':
			return {pose: reach(base, 'F', [60, -70], k)};
		case 'hug':
			return {pose: reach(reach({...base, lean: base.lean + 8 * k}, 'F', [70, -80], k), 'B', [70, -70], k), m: 'smile', e: 'sleepy'};
		case 'knock': {
			const kn = Math.abs(Math.sin(f / 2.2)) * env(f, 4, D * 0.5, 4, 4);
			return {pose: {...base, armF: [lerpN(base.armF[0], 90 + kn * 16, k), lerpN(base.armF[1], 70 - kn * 30, k)]}, handF: 'fist'};
		}
		case 'mic':
			return {pose: reach({...base, head: base.head + Math.sin(f / 9) * 3}, 'F', [38, -128], k), m: 'open'};
		case 'raise':
			return {pose: {...base, armF: [lerpN(base.armF[0], 172, k), lerpN(base.armF[1], 6, k)]}, m: 'flat', look: [0.6, -0.3]};
		case 'stare':
			return {pose: {...base, lean: base.lean + 10 * k, head: base.head + 6 * k}, e: 'angry', m: 'flat', look: [1, 0]};
		case 'sad':
			return {pose: {...base, head: base.head + 20 * k, lean: base.lean + 8 * k, armF: [4, 6], armB: [-4, 6]}, e: 'sad', m: 'frown', look: [0.3, 0.8]};
		case 'nod':
			return {pose: {...base, head: base.head + Math.sin(f / 4) * 10 * k}, m: 'smile'};
		case 'no':
			return {pose: {...base, head: base.head + Math.sin(f / 3) * 8 * k}, e: 'worried', m: 'frown', look: [Math.sin(f / 3), 0]};
		case 'tour':
			return {pose: {...base, armF: [lerpN(base.armF[0], 120 + Math.sin(f / 5) * 25, k), lerpN(base.armF[1], 20, k)]}, m: 'open'};
		case 'bow':
			return {pose: {...base, lean: base.lean + 40 * k, head: base.head + 10 * k}, m: 'smile'};
		case 'phone':
			return {pose: reach({...base, head: base.head + 14 * k}, 'F', [44, -86], k), look: [0.6, 0.6]};
		case 'write':
			return {pose: reach({...base, head: base.head + 18 * k, lean: base.lean + 10 * k}, 'F', [70 + Math.sin(f / 2) * 6, -40], k), look: [0.6, 0.9]};
		case 'snap':
			return {pose: gesture('point', base, k, f), handF: 'snap', m: 'smirk'};
		case 'run':
			return {pose: run(f * 0.45)};
		case 'idle':
		default:
			return {pose: base};
	}
};
const lerpN = (a: number, b: number, k: number) => a + (b - a) * k;

/* ------------------------- floating «ХА-ХА» -------------------------- */
const HaFx: React.FC<{x: number; y: number; f: number; s: number; seed: string; c?: string}> = ({x, y, f, s, seed, c = '#ffd34a'}) => (
	<g>
		{[0, 1, 2].map((i) => {
			const per = 22;
			const t = ((f + i * 8 + Math.floor(random(seed) * 10)) % per) / per;
			const side = (i % 2 ? 1 : -1) * (40 + 30 * random(seed + i));
			return (
				<text key={i} x={x + side * s + Math.sin(t * 6 + i) * 8} y={y - t * 120 * s} fontSize={(30 + 14 * (1 - t)) * s} fontFamily={FONT} fontWeight={900} fill={c} stroke="#1b1028" strokeWidth={5 * s} paintOrder="stroke" textAnchor="middle" opacity={Math.min(1, (1 - t) * 2)} transform={`rotate(${side > 0 ? 12 : -12} ${x + side * s} ${y - t * 120 * s})`}>
					ХА
				</text>
			);
		})}
	</g>
);
const Tears: React.FC<{x: number; y: number; f: number; s: number}> = ({x, y, f, s}) => (
	<g>
		{[-1, 1].map((d) =>
			[0, 1].map((i) => {
				const t = ((f + i * 9) % 18) / 18;
				return <path key={d + '' + i} d="M0,-10 C7,0 7,7 0,9 C-7,7 -7,0 0,-10 Z" fill="#7ad0ff" transform={`translate(${x + d * (26 + t * 40) * s},${y + t * t * 80 * s}) scale(${s * 1.3})`} opacity={1 - t} />;
			}),
		)}
	</g>
);

/* ------------------------------ an actor -------------------------------- */
const BeatActor: React.FC<{A: ActorB; i: number; D: number; floor: number; others: ActorB[]; badgeOk: boolean}> = ({A, i, D, floor: fl0, others, badgeOk}) => {
	const {f, gf} = useShot();
	if (A.hide || (A.until !== undefined && f > A.until * D)) return null;
	const s = A.s ?? (A.w === 'hero' ? 1 : 1);
	const floor = A.floor ?? fl0;
	let x = A.x;
	let base: Pose = idle(gf, i * 3 + A.x / 200);
	let vx = 0;
	let bob = 0;
	let facing: 1 | -1 = A.fc ?? 1;
	if (A.fc === undefined && others.length) {
		const ox = others.reduce((a, o) => a + o.x, 0) / others.length;
		facing = ox >= A.x ? 1 : -1;
	}
	const isRun = A.a === 'run';
	if (A.to !== undefined && A.to !== A.x) {
		const t0 = (A.t0 ?? 0.02) * D;
		const dist = Math.abs(A.to - A.x);
		const t1 = A.t1 !== undefined ? A.t1 * D : Math.min(D - 4, t0 + dist / (isRun ? 16 : 8));
		const w = walkTo(f, t0, t1, A.x, A.to, i, isRun ? 0.55 : 0.32);
		x = w.x;
		vx = w.vx;
		bob = w.bob;
		if (w.moving) {
			facing = w.facing;
			base = isRun ? blend(w.pose, run((f - t0) * 0.5), Math.min(1, Math.min(f - t0, t1 - f) / 4)) : w.pose;
		} else if (A.fc === undefined) facing = f >= t1 ? (A.fc ?? w.facing) : w.facing;
	}
	if (A.sit) base = {...SIT, head: Math.sin(gf / 31 + i) * 2.5, lean: -4 + Math.sin(gf / 23 + i) * 1.2};
	// actions: a until ab, then b
	const ab = (A.ab ?? 0.5) * D;
	const useB = A.b && f >= ab;
	const act: Act = (useB ? A.b : A.a) ?? 'idle';
	const kIn = useB ? env(f, ab, D + 99, 7, 1) : env(f, 2, A.b ? ab - 4 : D + 99, 7, 6);
	const moving = A.to !== undefined && Math.abs(vx) > 0.5;
	const o = act === 'run' || act === 'conga' || act === 'laughFloor' || act === 'fall' || act === 'jump' || act === 'dance' ? actPose(act, base, f, 1, D, gf) : actPose(act, base, f, moving && act !== 'tour' && act !== 'mic' ? 0 : kIn, D, gf);
	let pose = o.pose;
	if (A.sit && act !== 'laughFloor' && act !== 'fall') pose = {...pose, legF: SIT.legF, legB: SIT.legB};
	if (act === 'conga' && A.to !== undefined) {
		const ph = f / 4;
		pose = {...pose, legF: walk(ph).legF, legB: walk(ph).legB};
	}
	const seat = A.sit ? floor - 110 * s : undefined;
	const lift = (o.lift ?? 0) + bob;
	const rot = (o.rot ?? 0) * facing + (A.lie ? -86 * facing : 0);
	const expr = A.e ?? o.e;
	const mouth = A.m ?? o.m;
	const hipY = seat ?? floor - 157 * s;
	const headY = hipY - 164 * s - lift * s;
	const laughing = LAUGHS.has(act) && (kIn > 0.3 || act === 'laughFloor');
	const actor = (
		<Actor
			who={A.w}
			x={x}
			floor={floor}
			s={s}
			seat={seat}
			facing={facing}
			faceTurn={0.55}
			look={o.look ?? [0.7, 0]}
			pose={pose}
			vx={vx}
			bob={lift}
			expr={expr}
			mouth={A.say ? undefined : mouth}
			sp={A.say ? 'N' : 'MUTE'}
			armOver={o.armOver}
			handF={o.handF}
			squash={o.squash}
			handItem={A.item ? <Item i={A.item} /> : undefined}
			uid={`a${i}-${A.w}`}
			shadow={!A.lie}
		/>
	);
	const showBadge = A.w === 'hero' && (A.badge ?? badgeOk) && !A.lie && Math.abs(rot) < 10;
	return (
		<g>
			{A.sit && A.chair !== false ? <Chair x={x - 10 * facing} y={floor - 100} facing={facing} /> : null}
			{rot ? <g transform={`rotate(${rot} ${x} ${floor - 10})`}>{actor}</g> : actor}
			{laughing ? <HaFx x={x} y={rot ? floor - 120 : headY - 40 * s} f={f} s={s} seed={A.w + i} /> : null}
			{act === 'laughBig' || act === 'cry' ? <Tears x={x + 10 * facing} y={headY + 6 * s} f={f} s={s} /> : null}
			{showBadge ? <HeroBadge x={x} y={headY - 112 * s} s={0.78 * s} /> : null}
		</g>
	);
};

/* actor world head point for camera/fx */
export const actorAt = (A: ActorB, f: number, D: number, fl: number) => {
	let x = A.x;
	if (A.to !== undefined) {
		const t0 = (A.t0 ?? 0.02) * D;
		const dist = Math.abs(A.to - A.x);
		const t1 = A.t1 !== undefined ? A.t1 * D : Math.min(D - 4, t0 + dist / (A.a === 'run' ? 16 : 8));
		x = walkTo(f, t0, t1, A.x, A.to).x;
	}
	const s = A.s ?? 1;
	const floor = A.floor ?? fl;
	const hip = A.sit ? floor - 110 * s : floor - 157 * s;
	const y = A.lie ? floor - 60 : hip - 164 * s;
	return {x, y, s};
};

/* ------------------------------- crowd ---------------------------------- */
const CrowdG: React.FC<{c: Crowd; f: number; gf: number}> = ({c, f, gf}) => {
	const fl = c.floor ?? 900;
	const s = c.s ?? 0.8;
	return (
		<>
			{Array.from({length: c.n}).map((_, i) => {
				const r = random((c.seed ?? 'cr') + i);
				let x = c.x0 + ((c.x1 - c.x0) * (i + 0.5)) / c.n + (r - 0.5) * 30;
				let pose: Pose = idle(gf, i);
				let facing: 1 | -1 = r > 0.5 ? 1 : -1;
				let lift = 0;
				let expr: any;
				let mouth: any;
				let seat: number | undefined;
				const dir = c.dir ?? 1;
				if (c.mode === 'laugh' || c.mode === 'sitLaugh') {
					const b = Math.sin(gf / (2.2 + r) + i);
					pose = {...pose, lean: -10 + b * 5, head: -14 + b * 6, armF: [40 + 20 * b, 80], armB: [-20, 70]};
					expr = 'sleepy';
					mouth = 'open';
					lift = c.mode === 'laugh' ? Math.abs(b) * 5 : 0;
				}
				if (c.mode === 'sit' || c.mode === 'sitLaugh') {
					pose = {...pose, legF: SIT.legF, legB: SIT.legB};
					seat = fl - 110 * s;
				}
				if (c.mode === 'cheer') {
					pose = {...pose, armF: [160, 20], armB: [-150, 20]};
					lift = Math.abs(Math.sin(gf / 4 + i)) * 20;
					mouth = 'open';
				}
				if (c.mode === 'dance') {
					const ph = gf / 6 + r * 6;
					pose = {lean: Math.sin(ph) * 8, head: Math.sin(ph * 2) * 10, armF: [120 + Math.sin(ph) * 40, 30], armB: [-120 + Math.cos(ph) * 40, 30], legF: [10 + Math.sin(ph) * 15, 10], legB: [-10, 10]};
				}
				if (c.mode === 'conga') {
					facing = dir;
					const ph = gf / 4;
					x += dir * f * 4.2;
					x = ((x - c.x0 + 4000) % (c.x1 - c.x0 + 600)) + c.x0 - 300;
					pose = {lean: 6, head: Math.sin(ph + i) * 8, armF: [82, 12], armB: [74, 16], ...{legF: walk(ph + i).legF, legB: walk(ph + i).legB}};
					lift = Math.abs(Math.sin(ph + i)) * 5;
					expr = 'sleepy';
					mouth = 'open';
				}
				if (c.mode === 'run' || c.mode === 'panic') {
					facing = dir;
					x += dir * f * (6 + r * 3);
					pose = c.mode === 'panic' ? {...run(gf * 0.45 + r * 6), armF: [150, 20], armB: [-140, 20]} : run(gf * 0.45 + r * 6);
					expr = 'wide';
				}
				if (c.mode === 'walk') {
					facing = dir;
					x += dir * f * (2 + r);
					pose = walk(gf * 0.25 + r * 6);
				}
				const hipY = seat ?? fl - 157 * s;
				return (
					<g key={i}>
						<ellipse cx={x} cy={fl + 4} rx={60 * s} ry={10 * s} fill="#000" opacity={0.18} />
						<Stickman id={`cr${c.seed ?? ''}${i}`} x={x} y={hipY - lift * s} scale={s * (0.92 + r * 0.16)} facing={facing} pose={pose} blink={(gf + i * 17) % 97 < 4 ? 1 : 0} expr={expr} mouth={mouth} look={[facing * 0.4, 0]} {...crowdLook2(i, c.seed ?? 'cr')} />
						{(c.mode === 'laugh' || c.mode === 'sitLaugh' || c.mode === 'conga') && i % 3 === 0 ? <HaFx x={x} y={hipY - 230 * s} f={f + i * 5} s={s * 0.8} seed={'c' + i} c={i % 2 ? '#ffd34a' : '#fff'} /> : null}
					</g>
				);
			})}
		</>
	);
};
const COLS = ['#3d6fd6', '#3aa37a', '#8b5cf6', '#e86aa0', '#f08a3c', '#3fc1c9', '#9aa3b5', '#5b6bd6', '#f2b21c', '#7a5cc4'];
const HAIR = ['short', 'bun', 'ponytail', 'spiky', 'bob', 'cap', 'none', 'short'] as const;
const crowdLook2 = (i: number, seed: string) => ({
	color: COLS[Math.floor(random(seed + 'col' + i) * COLS.length)],
	hair: HAIR[Math.floor(random(seed + 'h' + i) * HAIR.length)] as any,
	hairColor: COLS[Math.floor(random(seed + 'hc' + i) * COLS.length)],
	rimW: 2,
});

/* -------------------------------- props --------------------------------- */
const PropG: React.FC<{p: PropB; f: number}> = ({p, f}) => {
	const x = p.x ?? 960;
	switch (p.p) {
		case 'desk':
			return <BigDesk x={x} />;
		case 'table':
			return <KitchenTable />;
		case 'lunch':
			return <LunchTable x0={x - 700} x1={x + 700} trays={p.xs ?? []} />;
		case 'desks':
			return <SchoolDesks xs={p.xs ?? [x]} />;
		case 'car':
			return <Svg><CarSide x={x} f={f} c={p.c ?? '#3d6fd6'} open={p.open} /></Svg>;
		case 'police':
			return <Svg><CarSide x={x} f={f} police /></Svg>;
		case 'armchair':
			return <Armchair x={x} c={p.c} front={p.front} />;
		case 'rat':
			return <Svg><Rat x={x} y={(p as any).y ?? 660} f={f} laugh={p.laugh ? 1 : 0} s={0.9} /></Svg>;
		case 'mic':
			return (
				<Svg>
					<line x1={x} y1={900} x2={x} y2={640} stroke="#2b2b30" strokeWidth={8} />
					<ellipse cx={x} cy={900} rx={50} ry={10} fill="#2b2b30" />
					<rect x={x - 8} y={612} width={16} height={36} rx={6} fill="#5a6278" />
				</Svg>
			);
		case 'bed':
			return (
				<Svg>
					<rect x={x - 230} y={790} width={460} height={60} rx={14} fill="#f4f6fa" />
					<rect x={x - 230} y={690} width={24} height={210} fill="#9aa3b5" />
					<rect x={x - 200} y={770} width={420} height={40} rx={14} fill={p.c ?? '#7fc0e8'} />
				</Svg>
			);
		case 'lamp':
			return <Svg><Lamp x={x} y={300} /></Svg>;
		default:
			return null;
	}
};

/* ---------------------------------- FX ---------------------------------- */
const TextPop: React.FC<{t: string; x: number; y: number; k: number; c?: string; size?: number; f: number}> = ({t, x, y, k, c = '#ffd34a', size = 90, f}) => {
	const rot = -6 + Math.sin(f / 9) * 3;
	return (
		<g transform={`translate(${x},${y + Math.sin(f / 11) * 6}) rotate(${rot}) scale(${k})`}>
			<text textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={900} fill={c} stroke="#1b1028" strokeWidth={size * 0.12} paintOrder="stroke" style={{letterSpacing: 2}}>
				{t}
			</text>
		</g>
	);
};
const Burst: React.FC<{x: number; y: number; f: number; c?: string}> = ({x, y, f, c = '#fff6c0'}) => (
	<g opacity={0.5}>
		{Array.from({length: 22}).map((_, i) => {
			const a = (i / 22) * Math.PI * 2 + f / 60;
			const r0 = 260 + 30 * Math.sin(f / 3 + i);
			return <line key={i} x1={x + Math.cos(a) * r0} y1={y + Math.sin(a) * r0} x2={x + Math.cos(a) * 1300} y2={y + Math.sin(a) * 1300} stroke={c} strokeWidth={14 + (i % 3) * 8} opacity={0.5} />;
		})}
	</g>
);
const Confetti: React.FC<{f: number}> = ({f}) => (
	<g>
		{Array.from({length: 70}).map((_, i) => {
			const x = random('cf' + i) * 2100 - 90 + Math.sin(f / 12 + i) * 30;
			const y = ((random('cy' + i) * 1200 + f * (5 + random('cs' + i) * 5)) % 1300) - 200;
			return <rect key={i} x={x} y={y} width={14} height={24} fill={COLS[i % COLS.length]} transform={`rotate(${f * 6 + i * 40} ${x} ${y})`} />;
		})}
	</g>
);
const Hearts: React.FC<{x: number; y: number; f: number}> = ({x, y, f}) => (
	<g>
		{Array.from({length: 6}).map((_, i) => {
			const t = ((f + i * 7) % 40) / 40;
			return (
				<g key={i} transform={`translate(${x + Math.sin(t * 6 + i) * 60 + (i - 3) * 20},${y - t * 220})`} opacity={1 - t}>
					<IconG i="heart" s={0.45 + 0.2 * (i % 2)} />
				</g>
			);
		})}
	</g>
);
const Sparkle: React.FC<{x: number; y: number; f: number}> = ({x, y, f}) => (
	<g>
		{Array.from({length: 8}).map((_, i) => {
			const a = (i / 8) * Math.PI * 2;
			const k = ((f / 14 + i * 0.13) % 1);
			return <path key={i} d="M0,-14 L4,-4 L14,0 L4,4 L0,14 L-4,4 L-14,0 L-4,-4 Z" fill="#fff6a0" transform={`translate(${x + Math.cos(a) * (80 + k * 60)},${y + Math.sin(a) * (80 + k * 60)}) scale(${1 - k})`} />;
		})}
	</g>
);
const SmokeFx: React.FC<{f: number; d: number}> = ({f, d}) => (
	<g opacity={d}>
		{Array.from({length: 16}).map((_, i) => (
			<ellipse key={i} cx={-300 + (i % 8) * 320 + Math.sin(f / 30 + i) * 70} cy={20 + Math.floor(i / 8) * 200 + (i % 3) * 60 + Math.sin(f / 25 + i) * 25} rx={320} ry={150} fill="#9a9aa6" opacity={0.55} style={{filter: 'blur(26px)'}} />
		))}
	</g>
);

/* ------------------------------ camera ---------------------------------- */
const AUTO: CamK[] = ['push', 'panR', 'close', 'pull', 'low', 'panL', 'two', 'push', 'dutch', 'rise'];

const camFor = (b: Beat, f: number, D: number, fl: number, idx: number): {cam: Cam; tilt: number; shake: number} => {
	const cast = (b.cast ?? []).filter((a) => !a.hide);
	const k = interpolate(f, [0, D], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
	const kind: CamK = b.cam ?? (cast.length ? AUTO[idx % AUTO.length] : 'wide');
	const on = cast[b.on ?? 0];
	const p = on ? actorAt(on, f, D, fl) : {x: 960, y: 560, s: 1};
	const tx = p.x;
	const ty = p.y + 40 + (b.cy ?? 0);
	const z = b.z ?? 1.35;
	let cam: Cam;
	let tilt = 0;
	let shake = 0;
	const o2 = cast[b.on2 ?? (b.on === 1 ? 0 : 1)];
	switch (kind) {
		case 'push':
			cam = mixCam(camOn(tx, ty + 30, z), camOn(tx, ty, z * 1.32), k);
			break;
		case 'pull':
			cam = mixCam(camOn(tx, ty, z * 1.4), camOn(tx, ty + 30, z * 0.95), k);
			break;
		case 'panR':
			cam = camOn(tx - 160 + 320 * k, ty + 20, z * 1.08);
			break;
		case 'panL':
			cam = camOn(tx + 160 - 320 * k, ty + 20, z * 1.08);
			break;
		case 'close':
			cam = mixCam(camOn(tx + 10, ty - 30, 2.05), camOn(tx - 10, ty - 36, 2.3), k);
			break;
		case 'wide':
			cam = mixCam(camOn(960, 560, 1.0), camOn(960, 545, 1.1), k);
			break;
		case 'low':
			cam = mixCam(camOn(tx, ty + 150, z * 1.05), camOn(tx, ty + 110, z * 1.22), k);
			break;
		case 'rise':
			cam = mixCam(camOn(tx, ty + 220, z * 1.1), camOn(tx, ty - 20, z * 1.25), k);
			break;
		case 'drop':
			cam = mixCam(camOn(tx, ty - 160, z * 1.1), camOn(tx, ty + 40, z * 1.2), k);
			break;
		case 'two':
		case 'orbit': {
			const q = o2 ? actorAt(o2, f, D, fl) : p;
			if (kind === 'orbit') {
				cam = mixCam(camOn(p.x, p.y + 20, 1.9), camOn(q.x, q.y + 20, 1.9), interpolate(f, [D * 0.35, D * 0.65], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)}));
			} else {
				const mx = (p.x + q.x) / 2;
				const zz = Math.max(1.05, Math.min(1.8, 1500 / (Math.abs(p.x - q.x) + 650)));
				cam = mixCam(camOn(mx - 40, (p.y + q.y) / 2 + 70, zz), camOn(mx + 40, (p.y + q.y) / 2 + 60, zz * 1.12), k);
			}
			break;
		}
		case 'crash': {
			const c = interpolate(f, [0, 6], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
			cam = mixCam(camOn(tx, ty + 40, 1.1), camOn(tx, ty - 10, 2.0 + 0.15 * k), c);
			shake = interpolate(f, [4, 14], [14, 0], clamp);
			break;
		}
		case 'follow':
			cam = camOn(tx + 60 * (on?.to !== undefined ? Math.sign(on.to - on.x) : 1), ty + 10, z * 1.1 + 0.08 * k);
			break;
		case 'dutch':
			cam = mixCam(camOn(tx, ty, z * 1.25), camOn(tx + 40, ty - 10, z * 1.42), k);
			tilt = (idx % 2 ? 1 : -1) * (4 - 1.5 * k);
			break;
		case 'whipin':
			cam = mixCam(camOn(tx + 500, ty, z), camOn(tx, ty, z * 1.2), interpolate(f, [0, 10], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)}));
			break;
	}
	return {cam: cam!, tilt, shake};
};

/* ------------------------------- the shot -------------------------------- */
export const BeatShot: React.FC<{b: Beat; idx: number; lineNo: number; cards: Record<string, React.FC<{b: Beat}>>}> = ({b, idx, lineNo, cards}) => {
	const {f, gf, dur} = useShot();
	const D = dur;
	if (b.card) {
		const C = cards[b.card];
		return (
			<AbsoluteFill>
				<C b={b} />
				<ScreenFx b={b} f={f} D={D} />
			</AbsoluteFill>
		);
	}
	const L = LOCS[b.loc];
	const FL = 900;
	const cast = (b.cast ?? []).filter((a) => !a.hide);
	const {cam, tilt, shake: s0} = camFor(b, f, D, FL, idx);
	let shake = s0;
	for (const x of b.fx ?? []) if (x.k === 'shake') shake = Math.max(shake, interpolate(f - (x.at ?? 0) * D, [0, 3, 16], [0, 18, 0], clamp));
	const sx = shake ? (random('sx' + gf) - 0.5) * shake : 0;
	const sy = shake ? (random('sy' + gf) - 0.5) * shake : 0;
	const badgeOk = lineNo >= 19;
	const behind = (b.props ?? []).filter((p) => !p.front);
	const front = (b.props ?? []).filter((p) => p.front);
	const crowdsBack = (b.crowd ?? []).filter((c) => (c.depth ?? 1.25) > 1);
	const crowdsFront = (b.crowd ?? []).filter((c) => (c.depth ?? 1.25) < 1);
	const crowdsMid = (b.crowd ?? []).filter((c) => (c.depth ?? 1.25) === 1);
	const at = (x: Fx) => (x.at ?? 0.1) * D;
	const live = (x: Fx) => f >= at(x) && f <= (x.to !== undefined ? x.to * D : D + 99);
	const head = (x: Fx) => {
		const a = cast[x.on ?? b.on ?? 0];
		return a ? actorAt(a, f, D, FL) : {x: 960, y: 500, s: 1};
	};
	return (
		<AbsoluteFill style={{transform: `translate(${sx}px,${sy}px) rotate(${tilt}deg) scale(${tilt ? 1.08 : 1})`}}>
			<Stage cam={cam} bg={L.bg} light={L.light}>
				<Layer depth={1.55}>{L.set(gf, b)}</Layer>
				{crowdsBack.map((c, i) => (
					<Layer depth={c.depth ?? 1.25} key={'cb' + i}>
						<Svg>
							<CrowdG c={c} f={f} gf={gf} />
						</Svg>
					</Layer>
				))}
				<Layer depth={1}>
					{behind.map((p, i) => (
						<PropG key={i} p={p.move ? {...p, x: (p.x ?? 960) + p.move * f} : p} f={gf} />
					))}
					<Svg>
						{(b.fx ?? []).filter((x) => x.k === 'burst' && live(x)).map((x, i) => {
							const h = head(x);
							return <Burst key={i} x={x.x ?? h.x} y={x.y ?? h.y} f={f} c={x.c} />;
						})}
						{crowdsMid.map((c, i) => (
							<CrowdG key={i} c={c} f={f} gf={gf} />
						))}
						{cast.map((A, i) => (
							<BeatActor key={i} A={A} i={i} D={D} floor={FL} others={cast.filter((_, j) => j !== i)} badgeOk={badgeOk} />
						))}
					</Svg>
					{front.map((p, i) => (
						<PropG key={i} p={p} f={gf} />
					))}
					<Svg>
						{(b.fx ?? []).map((x, i) => {
							if (!live(x)) return null;
							const t = f - at(x);
							const h = head(x);
							const k = spring({frame: t, fps: 30, config: {damping: 9, stiffness: 160}});
							switch (x.k) {
								case 'text':
									if (x.x !== undefined) return null;
									return <TextPop key={i} t={x.t ?? ''} x={h.x + 220} y={h.y - 80} k={k} c={x.c} size={x.size} f={f} />;
								case 'icon':
									return (
										<g key={i} transform={`translate(${x.x ?? h.x + 170},${(x.y ?? h.y - 110) + Math.sin(f / 8) * 8}) rotate(${Math.sin(f / 10) * 8}) scale(${k * (x.size ?? 1)})`}>
											<IconG i={x.i ?? 'star'} />
										</g>
									);
								case 'bubble':
									return (
										<g key={i} transform={`translate(${x.x ?? h.x + 170},${(x.y ?? h.y - 150) + Math.sin(f / 9) * 5}) scale(${k})`}>
											{x.t && !x.i ? <rect x={-Math.max(78, (x.t.length * 36 * 0.62) / 2 + 30)} y={-58} width={2 * Math.max(78, (x.t.length * 36 * 0.62) / 2 + 30)} height={116} rx={58} fill="#fbf8ef" /> : <circle r={78} fill="#fbf8ef" />}
											<circle cx={-70} cy={70} r={14} fill="#fbf8ef" />
											<circle cx={-96} cy={98} r={8} fill="#fbf8ef" />
											{x.i ? <IconG i={x.i} s={0.9} /> : <text y={13} textAnchor="middle" fontSize={x.t && x.t.length > 3 ? 36 : x.size ?? 60} fontFamily={FONT} fontWeight={900} fill="#1b1e2a">{x.t}</text>}
										</g>
									);
								case 'hearts':
									return <Hearts key={i} x={x.x ?? h.x} y={x.y ?? h.y - 60} f={t} />;
								case 'sparkle':
									return <Sparkle key={i} x={x.x ?? h.x} y={x.y ?? h.y} f={t} />;
								case 'tears':
									return <Tears key={i} x={h.x} y={h.y + 6} f={t} s={h.s} />;
								case 'sweat':
									return <g key={i} transform={`translate(${h.x + 55},${h.y - 30 + (t % 20)})`} opacity={1 - (t % 20) / 20}><IconG i="drop" s={0.6} /></g>;
								case 'milk': {
									const u = Math.min(1, t / 12);
									return <path key={i} d={`M${h.x + 30},${h.y + 10} q${60 * u},${-10} ${110 * u},${70 * u}`} stroke="#fff" strokeWidth={14} fill="none" strokeLinecap="round" />;
								}
								case 'zzz':
									return <text key={i} x={h.x + 60} y={h.y - 80 - (t % 30)} fontSize={50} fontFamily={FONT} fill="#fff" opacity={1 - (t % 30) / 30}>z</text>;
								case 'ha':
									return <HaFx key={i} x={x.x ?? h.x} y={x.y ?? h.y - 40} f={t} s={x.size ?? 1.3} seed={'fx' + i} />;
								case 'confetti':
									return <Confetti key={i} f={t} />;
								default:
									return null;
							}
						})}
					</Svg>
				</Layer>
				{crowdsFront.map((c, i) => (
					<Layer depth={c.depth ?? 0.7} key={'cf' + i}>
						<Svg>
							<CrowdG c={c} f={f} gf={gf} />
						</Svg>
					</Layer>
				))}
				{b.loc === 'stage' || b.loc === 'hall' || b.loc === 'club' ? (
					<Layer depth={0.72}>
						<Audience f={gf} laugh={(b as any).aud ?? 0} stand={(b as any).stand ?? 0} />
					</Layer>
				) : null}
				{(b.fx ?? []).some((x) => x.k === 'smoke') || b.smoke ? (
					<Layer depth={0.9}>
						<Svg>
							<SmokeFx f={gf} d={b.smoke ?? 0.8} />
						</Svg>
					</Layer>
				) : null}
			</Stage>
			<ScreenFx b={b} f={f} D={D} />
		</AbsoluteFill>
	);
};

/* screen-space: accents, flashes, alarm, REC frame, darkness */
const ScreenFx: React.FC<{b: Beat; f: number; D: number}> = ({b, f, D}) => (
	<>
		{(b.fx ?? []).map((x, i) => {
			const t0 = (x.at ?? 0.1) * D;
			const t1 = x.to !== undefined ? x.to * D : D;
			const t = f - t0;
			if (t < 0 || f > t1 + 2) return null;
			switch (x.k) {
				case 'acc':
					return <Accent key={i} text={x.t ?? ''} sub={x.sub} t={t} dur={t1 - t0} y={x.y ?? 880} c={x.c} />;
				case 'title': {
					const k = spring({frame: t, fps: 30, config: {damping: 12, stiffness: 150}});
					return (
						<AbsoluteFill key={i} style={{pointerEvents: 'none'}}>
							<div style={{position: 'absolute', top: x.y ?? 120, left: 40, right: 40, textAlign: 'center', transform: `scale(${0.6 + 0.4 * k}) rotate(${(1 - k) * -6}deg)`, opacity: Math.min(1, k * 1.5) * interpolate(f, [t1 - 8, t1], [1, 0], clamp)}}>
								{(x.t ?? '').split('|').map((w, j, arr) => (
									<div key={j} style={{fontFamily: FONT, fontWeight: 900, fontSize: x.size ?? 96, lineHeight: 1.08, color: j === arr.length - 1 ? x.c ?? '#ffd34a' : '#fff', WebkitTextStroke: '4px #120c20', paintOrder: 'stroke', textShadow: '0 10px 30px rgba(0,0,0,.55)'}}>
										{w}
									</div>
								))}
							</div>
						</AbsoluteFill>
					);
				}
				case 'text': {
					if (x.x === undefined) return null;
					const k = spring({frame: t, fps: 30, config: {damping: 9, stiffness: 160}});
					const sz = x.size ?? 90;
					return (
						<AbsoluteFill key={i} style={{pointerEvents: 'none'}}>
							<svg viewBox="0 0 1920 1080" width={1920} height={1080}>
								<TextPop t={x.t ?? ''} x={Math.min(1920 - (x.t ?? '').length * sz * 0.36 - 40, Math.max((x.t ?? '').length * sz * 0.36 + 40, x.x))} y={Math.max(sz + 20, x.y ?? 300)} k={k} c={x.c} size={sz} f={f} />
							</svg>
						</AbsoluteFill>
					);
				}
				case 'flash':
					return <AbsoluteFill key={i} style={{background: '#fff', opacity: interpolate(t, [0, 1, 7], [0, 0.85, 0], clamp)}} />;
				case 'alarm':
					return <AbsoluteFill key={i} style={{background: '#ff1a2a', opacity: Math.floor(f / 7) % 2 ? 0.22 : 0.04, mixBlendMode: 'multiply'}} />;
				case 'dark':
					return <AbsoluteFill key={i} style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 25%, rgba(0,0,10,0.75) 80%)'}} />;
				case 'rec':
					return (
						<AbsoluteFill key={i} style={{pointerEvents: 'none'}}>
							<div style={{position: 'absolute', inset: 40, border: '4px solid rgba(255,255,255,.8)', borderRadius: 18}} />
							<div style={{position: 'absolute', top: 64, left: 80, color: '#fff', fontFamily: FONT, fontSize: 38, fontWeight: 800, display: 'flex', alignItems: 'center', gap: 14}}>
								<div style={{width: 26, height: 26, borderRadius: 13, background: '#ff2a2a', opacity: Math.floor(f / 12) % 2 ? 1 : 0.2}} />
								REC
							</div>
							<div style={{position: 'absolute', top: 64, right: 80, color: '#fff', fontFamily: FONT, fontSize: 34}}>00:{String(Math.floor(f / 30) % 60).padStart(2, '0')}</div>
						</AbsoluteFill>
					);
				case 'count': {
					const [a0, a1] = x.n ?? [0, 100];
					const v = Math.round(interpolate(t, [0, Math.max(10, (t1 - t0) * 0.7)], [a0, a1], {...clamp, easing: Easing.out(Easing.cubic)}));
					const k = spring({frame: t, fps: 30, config: {damping: 11, stiffness: 160}});
					return (
						<AbsoluteFill key={i} style={{pointerEvents: 'none'}}>
							<div style={{position: 'absolute', top: x.y ?? 90, left: 0, right: 0, display: 'flex', justifyContent: 'center', transform: `scale(${k})`}}>
								<div style={{background: 'rgba(14,16,36,.9)', border: `5px solid ${x.c ?? '#ffd34a'}`, borderRadius: 30, padding: '10px 38px', fontFamily: FONT, color: '#fff', textAlign: 'center'}}>
									<div style={{fontSize: 30, color: x.c ?? '#ffd34a', fontWeight: 700}}>{x.sub ?? ''}</div>
									<div style={{fontSize: x.size ?? 96, fontWeight: 900, lineHeight: 1}}>
										{v.toLocaleString('ru-RU')}
										{x.t ?? ''}
									</div>
								</div>
							</div>
						</AbsoluteFill>
					);
				}
				default:
					return null;
			}
		})}
	</>
);

export {HAND};
