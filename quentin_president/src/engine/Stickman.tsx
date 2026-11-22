import React from 'react';
import {darken, lighten, mix} from './color';

/* Character renderer, "semi-real cartoon" style: tapered limbs, shaded cloth and skin,
   coloured hair, big expressive eyes, thin dark outline. The main hero (`hero`) keeps the
   channel's signature: a glossy black head with white eyes and a white mouth.
   The skeleton (RIG) and every exported helper are unchanged, so poses, IK, actions and
   the hard-coded floor offsets (hip = floor - 157 * scale) keep working. */

export type Expr = 'normal' | 'angry' | 'sad' | 'sleepy' | 'wide' | 'worried' | 'happy';
export type Hair = 'none' | 'spiky' | 'bun' | 'cap' | 'ponytail' | 'grey' | 'bob' | 'short' | 'long';
export type Outfit = 'hoodie' | 'suit' | 'gown' | 'dress' | 'coat' | 'apron' | 'tee';
export type Acc = 'headphones' | 'mustache' | 'glasses';
export type Mouth = 'line' | 'frown' | 'open' | 'smile' | 'flat' | 'smirk' | 'laugh' | 'none';
export type HandShape = 'fist' | 'point' | 'snap';
export type Build = 'm' | 'f' | 'k';

// Angles in degrees: 0 = limb points straight down, + = swings toward facing direction.
// Arm/leg pairs: [upper angle, joint bend]. Elbows bend forward, knees bend backward.
export type Pose = {
	lean: number;
	head: number;
	armB: [number, number];
	armF: [number, number];
	legB: [number, number];
	legF: [number, number];
};

export const POSES: Record<string, Pose> = {
	stand: {lean: 0, head: 0, armB: [-8, 10], armF: [8, 10], legB: [-4, 0], legF: [4, 0]},
	sit: {lean: -4, head: 0, armB: [25, 70], armF: [35, 65], legB: [88, 85], legF: [92, 90]},
};

const T = 125; // torso
const R = 50; // head (only for placement: the head centre is R * 0.78 above the neck)
const UA = 60;
const FA = 56;
const TH = 76;
const SH = 72;
const INK = '#1d1626';
const LN = 2.6; // outline half-width

type V = [number, number];
const rad = (a: number) => (a * Math.PI) / 180;
const dir = (a: number): V => [Math.sin(rad(a)), Math.cos(rad(a))];
const add = (a: V, b: V, k = 1): V => [a[0] + b[0] * k, a[1] + b[1] * k];

type Props = {
	x: number;
	y: number;
	scale?: number;
	facing?: 1 | -1;
	pose: Pose;
	id: string;
	/** hoodie / jacket colour */
	color: string;
	outfit?: Outfit;
	build?: Build; // m = broad shoulders, f = waist and hips, k = kid
	hair?: Hair;
	hairColor?: string;
	skin?: string;
	eye?: string; // iris colour
	lash?: boolean; // lashes (always on for build f)
	beard?: boolean;
	bag?: string; // backpack colour
	/** the signature hero: glossy black head, white eyes and mouth, black hands */
	hero?: boolean;
	expr?: Expr;
	look?: V;
	blink?: number;
	mouth?: Mouth;
	faceTurn?: number;
	rim?: string;
	rimW?: number;
	light?: V;
	shoe?: string;
	legColor?: string; // trousers colour
	handItem?: React.ReactNode;
	hideLegs?: boolean;
	hood?: boolean;
	handF?: HandShape;
	lidL?: number;
	lidR?: number;
	squash?: number;
	// 0 = sixteen, 1 = mid-thirties: wrinkles, eye bags
	age?: number;
	// 0..1 speech loudness; opens the mouth while the character talks
	talk?: number;
	acc?: Acc[];
	chestText?: string;
	// draw the front arm over the face (hand to cheek, facepalm, finger to lips)
	armOver?: boolean;
};

// tapered capsule from p (radius r1) to q (radius r2)
const cap = (p: V, q: V, r1: number, r2: number, key: string) => {
	const dx = q[0] - p[0];
	const dy = q[1] - p[1];
	const L = Math.hypot(dx, dy) || 1;
	const nx = -dy / L;
	const ny = dx / L;
	return (
		<g key={key}>
			<path d={`M${p[0] + nx * r1},${p[1] + ny * r1} L${q[0] + nx * r2},${q[1] + ny * r2} L${q[0] - nx * r2},${q[1] - ny * r2} L${p[0] - nx * r1},${p[1] - ny * r1} Z`} />
			<circle cx={p[0]} cy={p[1]} r={r1} />
			<circle cx={q[0]} cy={q[1]} r={r2} />
		</g>
	);
};
// outline pass + fill pass of the same shapes, so joints never show inner lines
const Solid: React.FC<{fill: string; children: React.ReactNode; w?: number}> = ({fill, children, w = LN}) => (
	<>
		<g fill={INK} stroke={INK} strokeWidth={w * 2} strokeLinejoin="round">
			{children}
		</g>
		<g fill={fill}>{children}</g>
	</>
);

const hairShapes = (h: Hair, c: string, id: string) => {
	const dk = darken(c, 0.35);
	const hl = lighten(c, 0.45);
	const fill = `url(#hg-${id})`;
	const S = {stroke: darken(c, 0.62), strokeWidth: 2.6, strokeLinejoin: 'round' as const};
	const strand = (d: string, o = 0.5) => <path d={d} stroke={dk} strokeWidth={1.8} fill="none" opacity={o} strokeLinecap="round" />;
	const shine = (d: string) => <path d={d} stroke={hl} strokeWidth={5} fill="none" opacity={0.55} strokeLinecap="round" />;
	const crown = <path d="M-43,-6 C-48,-66 48,-66 43,-6 Z" fill={fill} {...S} />;
	let back: React.ReactNode = null;
	if (h === 'long')
		back = (
			<g>
				<path d="M-44,-14 C-60,-60 -20,-62 0,-62 C28,-62 62,-50 46,-6 C54,40 50,90 56,120 C20,134 -30,132 -56,118 C-48,86 -52,40 -44,-14 Z" fill={fill} {...S} />
				{strand('M-30,0 C-34,50 -36,90 -40,118')}
				{strand('M30,0 C36,50 38,90 42,118')}
				{strand('M0,10 C-2,60 0,100 -2,126', 0.35)}
			</g>
		);
	if (h === 'bob')
		back = (
			<g>
				<path d="M-44,-14 C-58,-58 58,-58 46,-14 C52,10 50,36 46,50 C20,62 -22,62 -46,50 C-52,34 -50,8 -44,-14 Z" fill={fill} {...S} />
				{strand('M-30,0 C-34,20 -34,38 -34,52')}
				{strand('M30,0 C34,20 34,38 34,52')}
			</g>
		);
	if (h === 'ponytail')
		back = (
			<g>
				<path d="M-26,-40 C-82,-46 -92,30 -62,86 C-48,52 -44,14 -30,-4 Z" fill={fill} {...S} />
				{strand('M-46,-20 C-66,10 -64,50 -60,76')}
			</g>
		);
	let front: React.ReactNode = null;
	if (h === 'short')
		front = (
			<g>
				<path d="M-41,-8 C-48,-52 -8,-62 14,-56 C40,-52 52,-30 40,-6 C38,-24 28,-34 8,-32 C-8,-36 -26,-34 -41,-8 Z" fill={fill} {...S} />
				{shine('M-26,-46 C-12,-54 8,-54 22,-46')}
				{strand('M-34,-24 C-24,-34 -10,-40 6,-38')}
			</g>
		);
	if (h === 'spiky')
		front = (
			<g>
				<path d="M-42,-4 L-56,-26 L-36,-26 L-42,-58 L-22,-44 L-14,-72 L2,-48 L22,-70 L26,-44 L50,-52 L42,-24 L50,-4 C36,-28 -30,-30 -42,-4 Z" fill={fill} {...S} />
				{shine('M-24,-50 L-14,-62')}
			</g>
		);
	if (h === 'bun')
		front = (
			<g>
				<circle cx={-2} cy={-64} r={15} fill={fill} {...S} />
				<path d="M-41,-8 C-48,-56 48,-60 41,-8 C32,-32 -2,-40 -41,-8 Z" fill={fill} {...S} />
				{shine('M-22,-46 C-8,-54 10,-52 22,-44')}
			</g>
		);
	if (h === 'bob' || h === 'long')
		front = (
			<g>
				{crown}
				<path d="M-44,10 C-60,-60 60,-64 46,10 C44,-18 30,-34 10,-34 C-6,-26 -30,-24 -44,10 Z" fill={fill} {...S} />
				{shine('M-24,-48 C-8,-58 14,-56 26,-46')}
				{strand('M-38,-10 C-30,-30 -16,-36 0,-34')}
			</g>
		);
	if (h === 'ponytail')
		front = (
			<g>
				<path d="M-41,-8 C-48,-52 -8,-62 14,-56 C40,-52 52,-30 40,-6 C38,-24 28,-34 8,-32 C-8,-36 -26,-34 -41,-8 Z" fill={fill} {...S} />
				{shine('M-24,-46 C-10,-54 10,-54 22,-46')}
				<circle cx={-34} cy={-34} r={6} fill="#ff5c93" stroke={darken('#ff5c93', 0.5)} strokeWidth={2} />
			</g>
		);
	if (h === 'cap')
		front = (
			<g>
				<path d="M-42,-14 C-46,-66 46,-68 42,-14 Z" fill={c} {...S} />
				<path d="M18,-18 Q70,-24 76,-6 L22,-8 Z" fill={darken(c, 0.2)} {...S} />
				<circle cx={0} cy={-56} r={3.5} fill={darken(c, 0.3)} />
			</g>
		);
	if (h === 'grey')
		front = (
			<g>
				<path d="M-42,6 C-50,-26 -34,-32 -26,-22 C-30,-12 -34,-4 -38,10 Z" fill={fill} {...S} />
				<path d="M42,6 C50,-26 34,-32 26,-22 C30,-12 34,-4 38,10 Z" fill={fill} {...S} />
				<path d="M-30,-30 C-12,-44 14,-44 30,-30 C14,-38 -14,-38 -30,-30 Z" fill={fill} {...S} />
			</g>
		);
	return {back, front};
};

export const Stickman: React.FC<Props> = (p) => {
	const {pose, color, outfit: outfit0 = 'hoodie', build = 'm', expr = 'normal', look = [0.2, 0], faceTurn = 0.6, blink = 0, scale = 1, facing = 1, hero = false} = p;
	const outfit = outfit0 === 'gown' ? 'dress' : outfit0;
	const hairKind: Hair = p.hair ?? 'none';
	const f = build === 'f';
	const kid = build === 'k';
	const skin = hero ? '#0d0c10' : p.skin ?? '#f3cba8';
	const skinSh = hero ? '#07070a' : mix(skin, '#c0605a', 0.28);
	const hc = p.hairColor ?? (hairKind === 'grey' ? '#d9d9d9' : hairKind === 'cap' ? '#2f6fd8' : '#3b2a24');
	const eyeC = p.eye ?? '#4aa3d6';
	const pants = p.legColor ?? '#2d3a63';
	const shoe = p.shoe ?? '#f4f1ea';
	const rim = p.rim ?? '#f6d6a6';
	const rimW = p.rimW ?? 2.4;
	const light = p.light ?? [2, -1.5];
	const lash = p.lash ?? f;
	const mouth: Mouth = p.mouth ?? 'smile';
	const id = p.id;
	const lean = pose.lean;
	const up: V = [Math.sin(rad(lean)), -Math.cos(rad(lean))];
	const fwd: V = [Math.cos(rad(lean)), Math.sin(rad(lean))];
	const hip: V = [0, 0];
	const shoulder = add(add(hip, up, T - 18), fwd, 2);
	const shB = add(shoulder, fwd, -8);
	const headC = add(hip, up, T + R * 0.78);
	const arm = (s: V, a: [number, number]) => {
		const e = add(s, dir(a[0]), UA);
		return [s, e, add(e, dir(a[0] + a[1]), FA)] as V[];
	};
	const leg = (s: V, a: [number, number]) => {
		const k = add(s, dir(a[0]), TH);
		return [s, k, add(k, dir(a[0] - a[1]), SH)] as V[];
	};
	const aB = arm(shB, pose.armB);
	const aF = arm(shoulder, pose.armF);
	const lB = leg(add(hip, fwd, -6), pose.legB);
	const lF = leg(add(hip, fwd, 6), pose.legF);
	const sw = f ? 26 : kid ? 24 : 31;
	const ww = f ? 18 : kid ? 21 : 24;
	const hw = f ? 29 : kid ? 24 : 27;
	const top = -T - 2;
	const torso = `M${-sw},${top + 16} C${-sw},${top + 3} ${-sw + 12},${top} 0,${top} C${sw - 12},${top} ${sw},${top + 3} ${sw},${top + 16} C${sw + 1},${top + 56} ${ww + 3},-68 ${ww},-48 C${ww},-30 ${hw},-14 ${hw},10 L${-hw},10 C${-hw},-14 ${-ww},-30 ${-ww},-48 C${-ww - 3},-68 ${-sw - 1},${top + 56} ${-sw},${top + 16} Z`;
	const hi = lighten(color, 0.28);
	const sh = darken(color, 0.28);
	const age = p.age ?? 0;

	// ---- face ----
	const ex = faceTurn * 11;
	const wide = expr === 'wide';
	const erx = wide ? 10.5 : 9.2;
	const ery = wide ? 13 : 11.5;
	const baseLid = expr === 'sleepy' ? 0.5 : expr === 'sad' || expr === 'worried' ? 0.16 : expr === 'angry' ? 0.26 : 0;
	const lid = Math.max(baseLid, blink);
	const eL: V = [-15 + ex - 2, 4];
	const eR: V = [15 + ex + 1, 4];
	const eyeEl = (c: V, s: number, side: -1 | 1, lidv: number) => {
		const rx = erx * s;
		const ry = ery;
		const ir = rx * 0.86;
		const ix = c[0] + look[0] * (rx - ir * 0.7);
		const iy = c[1] + look[1] * 3;
		return (
			<g>
				<ellipse cx={c[0]} cy={c[1]} rx={rx} ry={ry} fill="#fff" />
				<g clipPath={`url(#ec-${id}-${side})`}>
					<ellipse cx={ix} cy={iy} rx={ir} ry={ir * 1.18} fill={`url(#ig-${id})`} />
					<ellipse cx={ix} cy={iy + 1} rx={ir * 0.45} ry={ir * 0.55} fill="#0d0a14" />
					<ellipse cx={ix - ir * 0.3} cy={iy - ir * 0.45} rx={ir * 0.3} ry={ir * 0.34} fill="#fff" />
					<circle cx={ix + ir * 0.35} cy={iy + ir * 0.4} r={ir * 0.14} fill="#fff" opacity={0.85} />
					<path d={`M${c[0] - rx},${c[1] - ry} h${rx * 2} v${ry * 0.9} q${-rx},${-ry * 0.5} ${-rx * 2},0 Z`} fill="#000" opacity={0.18} />
				</g>
				<path d={`M${c[0] - rx - 1.5},${c[1] - 1} Q${c[0]},${c[1] - ry * 1.55} ${c[0] + rx + 1.5},${c[1] - 1}`} stroke={INK} strokeWidth={lash ? 4.2 : 3.4} fill="none" strokeLinecap="round" />
				{lash ? <path d={`M${c[0] + (side === -1 ? -rx - 1 : rx + 1)},${c[1] - 1} l${side === -1 ? -5 : 5},-5`} stroke={INK} strokeWidth={3} strokeLinecap="round" /> : null}
				<path d={`M${c[0] - rx * 0.8},${c[1] + ry * 0.95} Q${c[0]},${c[1] + ry * 1.12} ${c[0] + rx * 0.8},${c[1] + ry * 0.95}`} stroke={skinSh} strokeWidth={1.8} fill="none" opacity={0.7} />
				{lidv > 0.01 ? (
					<g>
						<g clipPath={`url(#ec-${id}-${side})`}>
							<rect x={c[0] - rx - 2} y={c[1] - ry - 4} width={rx * 2 + 4} height={ry * 2 * lidv + 4} fill={skin} />
						</g>
						<path d={`M${c[0] - rx - 1},${c[1] - ry + ry * 2 * lidv} Q${c[0]},${c[1] - ry + ry * 2 * lidv + 6} ${c[0] + rx + 1},${c[1] - ry + ry * 2 * lidv}`} stroke={INK} strokeWidth={3.2} fill="none" strokeLinecap="round" />
					</g>
				) : null}
			</g>
		);
	};
	const brow = (c: V, side: -1 | 1) => {
		let a = 0;
		let rise = 0;
		if (expr === 'angry') a = 9;
		if (expr === 'sad' || expr === 'worried') a = -9;
		if (expr === 'wide') rise = 4;
		const y = c[1] - ery - 7 - rise;
		const inner = side === -1 ? c[0] + 9 : c[0] - 9;
		const outer = side === -1 ? c[0] - 11 : c[0] + 11;
		return <path d={`M${outer},${y - a * 0.5 + 1} Q${(outer + inner) / 2},${y - 4 - Math.abs(a) * 0.1} ${inner},${y + a * 0.7}`} stroke={darken(hc, 0.3)} strokeWidth={3.6} fill="none" strokeLinecap="round" />;
	};
	const mx = ex * 0.7;
	const my = 30;
	const lipC = f ? '#d9566a' : '#b8584f';
	const talk = p.talk ?? 0;
	const mouthEl = (() => {
		if (talk > 0.06) return <ellipse cx={mx} cy={my + 2} rx={6 + 2 * talk} ry={2.5 + 8 * Math.min(1, talk)} fill="#5b1a2a" stroke={INK} strokeWidth={2} />;
		switch (mouth) {
			case 'smile':
				return <path d={`M${mx - 9},${my - 2} Q${mx},${my + 7} ${mx + 9},${my - 2} Q${mx},${my + 1} ${mx - 9},${my - 2} Z`} fill={lipC} stroke={INK} strokeWidth={2.2} strokeLinejoin="round" />;
			case 'smirk':
				return <path d={`M${mx - 8},${my + 1} Q${mx + 3},${my + 4} ${mx + 10},${my - 5}`} stroke={INK} strokeWidth={3} fill="none" strokeLinecap="round" />;
			case 'frown':
				return <path d={`M${mx - 8},${my + 3} Q${mx},${my - 4} ${mx + 8},${my + 3}`} stroke={INK} strokeWidth={3} fill="none" strokeLinecap="round" />;
			case 'line':
			case 'flat':
				return <path d={`M${mx - 7},${my} h14`} stroke={INK} strokeWidth={3} strokeLinecap="round" />;
			case 'open':
				return (
					<g>
						<ellipse cx={mx} cy={my + 3} rx={7} ry={9} fill="#5b1a2a" stroke={INK} strokeWidth={2.4} />
						<ellipse cx={mx} cy={my + 8} rx={4.5} ry={3} fill="#e8707f" />
					</g>
				);
			case 'laugh':
				return (
					<g>
						<path d={`M${mx - 13},${my - 4} Q${mx},${my + 20} ${mx + 13},${my - 4} Z`} fill="#5b1a2a" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
						<path d={`M${mx - 11},${my - 3} h22 v4 q-11,3 -22,0 Z`} fill="#fff" />
					</g>
				);
			default:
				return null;
		}
	})();
	// hero face: white shapes on the glossy black head
	const heroFace = () => {
		const lidK = expr === 'wide' ? 0 : expr === 'angry' ? 0.45 : expr === 'sad' || expr === 'worried' ? 0.35 : expr === 'sleepy' ? 0.7 : 0.4;
		const slant = expr === 'angry' ? 5 : expr === 'sad' || expr === 'worried' ? -5 : 0;
		const E = (cx: number, side: number, lidv: number) => {
			const w = 11;
			const h = wide ? 13 : 10;
			const topY = 2 - h + 2 * h * Math.max(lidK, lidv, blink) * 0.55;
			return (
				<path
					d={`M${cx - w},${topY - slant * side} L${cx + w},${topY + slant * side} L${cx + w - 1},${2 + h * 0.5} Q${cx},${2 + h * 1.5} ${cx - w + 1},${2 + h * 0.5} Z`}
					fill="#fff"
					transform={`translate(${look[0] * 3},${look[1] * 3})`}
				/>
			);
		};
		const m2 = 28;
		const mh = ex * 0.7;
		const wm = (d: string, fill = false) => (fill ? <path d={d} fill="#fff" /> : <path d={d} stroke="#fff" strokeWidth={3.6} fill="none" strokeLinecap="round" />);
		let mEl: React.ReactNode;
		if (talk > 0.06) mEl = <ellipse cx={mh} cy={m2 + 2} rx={6 + 2 * talk} ry={2.5 + 8 * Math.min(1, talk)} fill="#fff" />;
		else if (mouth === 'open' || mouth === 'laugh') mEl = wm(`M${mh - 11},${m2 - 4} Q${mh},${m2 + 20} ${mh + 11},${m2 - 4} Z`, true);
		else if (mouth === 'frown') mEl = wm(`M${mh - 10},${m2 + 5} Q${mh},${m2 - 5} ${mh + 10},${m2 + 5}`);
		else if (mouth === 'flat' || mouth === 'line') mEl = wm(`M${mh - 8},${m2} h16`);
		else if (mouth === 'smirk') mEl = wm(`M${mh - 10},${m2 + 1} Q${mh + 2},${m2 + 8} ${mh + 11},${m2 - 4}`);
		else if (mouth === 'none') mEl = null;
		else mEl = wm(`M${mh - 11},${m2 - 2} Q${mh},${m2 + 10} ${mh + 11},${m2 - 2}`);
		return (
			<g>
				<circle r={46} fill={`url(#hh-${id})`} />
				<ellipse cx={-17} cy={-22} rx={11} ry={19} fill="#fff" opacity={0.16} transform="rotate(32 -17 -22)" />
				<g transform={`translate(${ex},0)`}>
					{E(-17, -1, p.lidL ?? 0)}
					{E(17, 1, p.lidR ?? 0)}
				</g>
				{mEl}
			</g>
		);
	};

	const {back, front} = hairShapes(hairKind, hc, id);
	const acc = p.acc ?? [];
	const sleeveF = [aF[0], aF[1], add(aF[1], dir(pose.armF[0] + pose.armF[1]), FA * 0.86)];
	const sleeveB = [aB[0], aB[1], add(aB[1], dir(pose.armB[0] + pose.armB[1]), FA * 0.86)];
	const hand = (pts: V[], ang: number, front: boolean, key: string) => {
		const d = dir(ang);
		const c = add(pts[2], d, 6);
		return (
			<g key={key} transform={`translate(${c[0]},${c[1]}) rotate(${-ang})`}>
				<Solid fill={front ? skin : skinSh} w={2.4}>
					<ellipse cx={0} cy={4} rx={7.5} ry={10} />
					<ellipse cx={8} cy={0} rx={3} ry={6} transform="rotate(-30 8 0)" />
				</Solid>
			</g>
		);
	};
	const shoeEl = (pt: V, c: string, key: string) => (
		<g key={key} transform={`translate(${pt[0] + 6},${pt[1] - 6})`}>
			<Solid fill={c} w={2.6}>
				<path d="M-13,-8 L6,-8 C20,-6 30,0 31,8 L31,10 L-14,10 Z" />
			</Solid>
			<path d="M-14,6 L31,6 L31,12 C31,15 -14,15 -14,12 Z" fill="#f6f2ea" stroke={INK} strokeWidth={2.6} strokeLinejoin="round" />
			<path d="M12,-4 q10,0 15,9" stroke={lighten(c, 0.5)} strokeWidth={3} fill="none" strokeLinecap="round" />
		</g>
	);
	const fid = 'rim-' + id;
	const frontAng = pose.armF[0] + pose.armF[1];
	const fh = hand(aF, frontAng, true, 'hf');
	return (
		<g transform={`translate(${p.x},${p.y}) scale(${scale * facing * (1 + (p.squash ?? 0))},${scale * (1 - (p.squash ?? 0))})`}>
			<defs>
				<filter id={fid} x="-40%" y="-40%" width="180%" height="180%">
					<feMorphology in="SourceAlpha" operator="dilate" radius={rimW} result="d" />
					<feOffset in="d" dx={light[0] * facing} dy={light[1]} result="o" />
					<feFlood floodColor={rim} />
					<feComposite in2="o" operator="in" result="r" />
					<feMerge>
						<feMergeNode in="r" />
						<feMergeNode in="SourceGraphic" />
					</feMerge>
				</filter>
				<linearGradient id={`sk-${id}`} x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor={lighten(skin, 0.18)} />
					<stop offset="0.6" stopColor={skin} />
					<stop offset="1" stopColor={skinSh} />
				</linearGradient>
				<linearGradient id={`hg-${id}`} x1="0" y1="0" x2="1" y2="1">
					<stop offset="0" stopColor={lighten(hc, 0.12)} />
					<stop offset="0.55" stopColor={hc} />
					<stop offset="1" stopColor={darken(hc, 0.4)} />
				</linearGradient>
				<linearGradient id={`cl-${id}`} x1="0" y1="0" x2="1" y2="0.4">
					<stop offset="0" stopColor={lighten(color, 0.16)} />
					<stop offset="0.55" stopColor={color} />
					<stop offset="1" stopColor={darken(color, 0.3)} />
				</linearGradient>
				<linearGradient id={`pn-${id}`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor={lighten(pants, 0.12)} />
					<stop offset="1" stopColor={darken(pants, 0.3)} />
				</linearGradient>
				<radialGradient id={`ig-${id}`} cx="0.5" cy="0.25" r="0.9">
					<stop offset="0" stopColor={darken(eyeC, 0.35)} />
					<stop offset="0.5" stopColor={eyeC} />
					<stop offset="1" stopColor={lighten(eyeC, 0.5)} />
				</radialGradient>
				<radialGradient id={`bl-${id}`}>
					<stop offset="0" stopColor="#ff6d7e" stopOpacity="0.55" />
					<stop offset="1" stopColor="#ff6d7e" stopOpacity="0" />
				</radialGradient>
				<radialGradient id={`hh-${id}`} cx="0.35" cy="0.3" r="0.9">
					<stop offset="0" stopColor="#262329" />
					<stop offset="0.6" stopColor="#0d0c10" />
					<stop offset="1" stopColor="#050507" />
				</radialGradient>
				<clipPath id={`tc-${id}`}>
					<path d={torso} />
				</clipPath>
				<clipPath id={`ec-${id}--1`}>
					<ellipse cx={eL[0]} cy={eL[1]} rx={erx} ry={ery} />
				</clipPath>
				<clipPath id={`ec-${id}-1`}>
					<ellipse cx={eR[0]} cy={eR[1]} rx={erx * 0.9} ry={ery} />
				</clipPath>
			</defs>
			<g filter={rimW > 0.05 ? `url(#${fid})` : undefined}>
				{back ? <g transform={`translate(${headC[0]},${headC[1]}) rotate(${pose.head + lean * 0.25})`}>{back}</g> : null}
				{/* back limbs */}
				{p.hideLegs ? null : (
					<>
						<Solid fill={darken(pants, 0.3)}>
							{cap(lB[0], lB[1], 15, 11, 'a')}
							{cap(lB[1], lB[2], 11, 8, 'b')}
						</Solid>
						{shoeEl(lB[2], darken(shoe, 0.25), 'sb')}
					</>
				)}
				<Solid fill={darken(color, 0.3)}>
					{cap(sleeveB[0], sleeveB[1], 11.5, 10, 'a')}
					{cap(sleeveB[1], sleeveB[2], 10, 8.6, 'b')}
				</Solid>
				{hand(aB, pose.armB[0] + pose.armB[1], false, 'hb')}
				{/* front leg */}
				{p.hideLegs ? null : (
					<>
						<Solid fill={`url(#pn-${id})`}>
							{cap(lF[0], lF[1], 15, 11, 'a')}
							{cap(lF[1], lF[2], 11, 8, 'b')}
						</Solid>
						<path d={`M${lF[0][0] + 12},${lF[0][1] + 6} L${lF[1][0] + 8},${lF[1][1]} L${lF[2][0] + 6},${lF[2][1] - 4}`} stroke={lighten(pants, 0.4)} strokeWidth={2} fill="none" opacity={0.7} strokeLinecap="round" />
						{shoeEl(lF[2], shoe, 'sf')}
					</>
				)}
				{/* torso */}
				<g transform={`rotate(${lean})`}>
					{p.bag ? (
						<Solid fill={p.bag}>
							<rect x={-sw - 13} y={top + 26} width={22} height={74} rx={10} />
						</Solid>
					) : null}
					{outfit === 'hoodie' ? (
						<Solid fill={darken(color, 0.22)}>
							<ellipse cx={-4} cy={top + 6} rx={36} ry={17} />
						</Solid>
					) : null}
					{outfit === 'dress' ? (
						<Solid fill={`url(#cl-${id})`}>
							<path d={`M${-ww - 2},-48 C${-ww - 14},-10 ${-hw - 22},30 ${-hw - 26},52 Q0,66 ${hw + 26},52 C${hw + 22},30 ${hw + 14},-10 ${ww + 2},-48 Z`} />
						</Solid>
					) : null}
					<Solid fill={`url(#cl-${id})`}>
						<path d={torso} />
					</Solid>
					<g clipPath={`url(#tc-${id})`}>
						<path d={`M${sw * 0.25},${top} L${sw + 4},${top} L${sw + 4},20 L${hw * 0.45},20 C${ww * 0.4},-20 ${ww * 0.4},-60 ${sw * 0.25},${top} Z`} fill={sh} opacity={0.35} />
						<path d={`M${-sw + 6},${top + 14} C${-sw + 8},-60 ${-ww + 4},-40 ${-hw + 6},4`} stroke={hi} strokeWidth={6} fill="none" opacity={0.5} strokeLinecap="round" />
						<path d={`M${-hw},6 H${hw}`} stroke={darken(color, 0.4)} strokeWidth={14} opacity={0.35} />
						<path d="M-14,-46 q10,14 6,34 M10,-54 q-8,16 -2,38 M-20,-80 q6,6 2,16" stroke={darken(color, 0.4)} strokeWidth={2} fill="none" opacity={0.45} strokeLinecap="round" />
					</g>
					{outfit === 'hoodie' ? (
						<>
							<Solid fill={darken(color, 0.08)} w={2.4}>
								<path d="M-22,-46 H22 L28,-14 H-28 Z" />
							</Solid>
							<path d={`M-12,${top + 8} q-1,34 -3,40 M12,${top + 8} q2,34 0,38`} stroke="#f4efe6" strokeWidth={3.4} fill="none" strokeLinecap="round" />
							<circle cx={-15} cy={top + 50} r={3} fill="#f4efe6" stroke={INK} strokeWidth={1.6} />
							<circle cx={12} cy={top + 48} r={3} fill="#f4efe6" stroke={INK} strokeWidth={1.6} />
						</>
					) : null}
					{outfit === 'tee' || outfit === 'dress' ? <path d={`M-16,${top + 1} Q0,${top + 22} 16,${top + 1}`} fill={skin} stroke={INK} strokeWidth={2.6} /> : null}
					{outfit === 'tee' ? <path d="M-8,-84 l4,9 10,1 -7,7 2,10 -9,-5 -9,5 2,-10 -7,-7 10,-1 Z" fill="#ffd84a" stroke={INK} strokeWidth={2.2} strokeLinejoin="round" /> : null}
					{outfit === 'dress' ? <path d={`M${-ww},-42 H${ww}`} stroke="#fff3d6" strokeWidth={8} /> : null}
					{outfit === 'suit' ? (
						<>
							<path d={`M-15,${top + 1} L15,${top + 1} L3,${top + 52} Z`} fill="#f7f3ea" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
							<path d={`M-2,${top + 8} h7 l3,38 -6,9 -6,-9 Z`} fill="#d9433f" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
							<path d={`M-17,${top + 1} L3,${top + 58} M21,${top + 1} L3,${top + 58}`} stroke={INK} strokeWidth={2.8} />
						</>
					) : null}
					{outfit === 'coat' ? (
						<>
							<path d={`M4,${top + 3} V14`} stroke={INK} strokeWidth={3} />
							<circle cx={-6} cy={-66} r={3} fill={INK} />
							<circle cx={-6} cy={-36} r={3} fill={INK} />
						</>
					) : null}
					{outfit === 'apron' ? (
						<>
							<rect x={-18} y={-66} width={44} height={74} rx={10} fill="#f4efe6" stroke={INK} strokeWidth={3} />
							<path d={`M-12,-62 L-6,${top + 8} M20,-62 L14,${top + 8}`} stroke="#f4efe6" strokeWidth={4} />
						</>
					) : null}
					{p.chestText ? (
						<g transform={`translate(4,${top + 40}) rotate(-4)`}>
							<rect x={-26} y={-10} width={52} height={20} rx={3} fill="#fbfaf4" stroke="#c94a3a" strokeWidth={2} />
							<text x={0} y={5} textAnchor="middle" fontSize={10} fontFamily="'Rubik', sans-serif" fontWeight={900} fill="#c94a3a">
								{p.chestText}
							</text>
						</g>
					) : null}
				</g>
				{/* neck */}
				<Solid fill={skinSh} w={2.4}>
					<path transform={`rotate(${lean * 0.6})`} d={`M-9,${-T + 4} L9,${-T + 4} L8,${-T - 26} L-8,${-T - 26} Z`} />
				</Solid>
				{/* front arm */}
				<Solid fill={`url(#cl-${id})`}>
					{cap(sleeveF[0], sleeveF[1], 11.5, 10, 'a')}
					{cap(sleeveF[1], sleeveF[2], 10, 8.6, 'b')}
				</Solid>
				<path d={`M${sleeveF[0][0] - 5},${sleeveF[0][1] + 6} L${sleeveF[1][0] - 4},${sleeveF[1][1]}`} stroke={hi} strokeWidth={3} opacity={0.6} strokeLinecap="round" />
				{p.handItem ? <g transform={`translate(${aF[2][0]},${aF[2][1]})`}>{p.handItem}</g> : null}
				{(() => {
					const h = aF[2];
					const dd = dir(frontAng);
					if (p.handF === 'point') return <line x1={h[0]} y1={h[1]} x2={h[0] + dd[0] * 26} y2={h[1] + dd[1] * 26} stroke={skin} strokeWidth={7} strokeLinecap="round" />;
					if (p.handF === 'snap')
						return (
							<>
								<line x1={h[0]} y1={h[1]} x2={h[0] + dd[0] * 21 - dd[1] * 3} y2={h[1] + dd[1] * 21 + dd[0] * 3} stroke={skin} strokeWidth={6} strokeLinecap="round" />
								<line x1={h[0]} y1={h[1]} x2={h[0] + dd[0] * 15 + dd[1] * 5} y2={h[1] + dd[1] * 15 - dd[0] * 5} stroke={skin} strokeWidth={6} strokeLinecap="round" />
							</>
						);
					return null;
				})()}
				{fh}
				{/* head */}
				<g transform={`translate(${headC[0]},${headC[1]}) rotate(${pose.head + lean * 0.25})`}>
					{p.hood ? (
						<>
							<Solid fill={sh}>
								<ellipse cx={-6} cy={-4} rx={58} ry={56} />
							</Solid>
						</>
					) : null}
					{hero ? (
						heroFace()
					) : (
						<>
							<Solid fill={skinSh} w={2.4}>
								<ellipse cx={-38} cy={6} rx={6} ry={9} />
							</Solid>
							<Solid fill={`url(#sk-${id})`}>
								<path d="M-38,-8 C-42,-52 42,-52 38,-8 C38,18 22,46 0,46 C-22,46 -38,18 -38,-8 Z" />
							</Solid>
							<path d="M24,-12 C40,6 28,34 6,46 C26,36 44,14 24,-12 Z" fill={skinSh} opacity={0.35} />
							<ellipse cx={eL[0] - 2} cy={19} rx={10} ry={6} fill={`url(#bl-${id})`} />
							<ellipse cx={eR[0] + 1} cy={19} rx={10} ry={6} fill={`url(#bl-${id})`} />
							{p.beard ? <path d="M-37,8 C-40,44 -14,56 0,56 C14,56 40,44 37,8 C28,30 14,34 0,34 C-14,34 -28,30 -37,8 Z" fill={`url(#hg-${id})`} stroke={darken(hc, 0.6)} strokeWidth={2.4} strokeLinejoin="round" /> : null}
							{eyeEl(eL, 1, -1, Math.max(lid, p.lidL ?? 0))}
							{eyeEl(eR, 0.9, 1, Math.max(lid, p.lidR ?? 0))}
							{brow(eL, -1)}
							{brow(eR, 1)}
							<path d={`M${ex * 0.85},12 q3,6 -1,10`} stroke={skinSh} strokeWidth={2.6} fill="none" strokeLinecap="round" />
							{mouthEl}
							{age > 0.05 ? <path d={`M${-20 + ex},-26 q20,-6 40,0 M${eL[0] - 8},${eL[1] + 16} q8,5 16,0 M${eR[0] - 8},${eR[1] + 16} q8,5 16,0`} stroke={skinSh} strokeWidth={2} fill="none" opacity={Math.min(1, age * 1.4)} strokeLinecap="round" /> : null}
							{acc.includes('mustache') ? <path d={`M${mx - 13},${my - 8} q6,-7 13,-2 q7,-5 13,2 q-6,3 -13,1 q-7,2 -13,-1 z`} fill={lighten(hc, 0.2)} stroke={darken(hc, 0.5)} strokeWidth={1.6} /> : null}
							{front}
							{acc.includes('glasses') ? (
								<g stroke={INK} strokeWidth={2.8} fill="#cfeaff" fillOpacity={0.22}>
									<circle cx={eL[0]} cy={eL[1]} r={erx + 5} />
									<circle cx={eR[0]} cy={eR[1]} r={erx + 5} />
									<line x1={eL[0] + erx + 5} y1={eL[1]} x2={eR[0] - erx - 5} y2={eR[1]} />
								</g>
							) : null}
						</>
					)}
					{acc.includes('headphones') ? (
						<>
							<path d="M-46,4 C-52,-62 52,-62 46,4" stroke="#2b2f3a" strokeWidth={7} fill="none" />
							<rect x={-54} y={-8} width={16} height={28} rx={7} fill="#e9e4f5" stroke={INK} strokeWidth={2.4} />
						</>
					) : null}
				</g>
			</g>
			{p.armOver ? (
				<g>
					<Solid fill={`url(#cl-${id})`}>
						{cap(sleeveF[0], sleeveF[1], 11.5, 10, 'a')}
						{cap(sleeveF[1], sleeveF[2], 10, 8.6, 'b')}
					</Solid>
					{fh}
				</g>
			) : null}
		</g>
	);
};

// World-space position of the front hand, for attaching FX to it.
export const frontHand = (pose: Pose, x: number, y: number, scale: number, facing: 1 | -1): V => {
	const up: V = [Math.sin(rad(pose.lean)), -Math.cos(rad(pose.lean))];
	const fwd: V = [Math.cos(rad(pose.lean)), Math.sin(rad(pose.lean))];
	const sh = add(add([0, 0], up, T - 18), fwd, 2);
	const e = add(sh, dir(pose.armF[0]), UA);
	const h = add(e, dir(pose.armF[0] + pose.armF[1]), FA);
	return [x + h[0] * scale * facing, y + h[1] * scale];
};

/* ---------------------------- skeleton & arm IK ----------------------------
   Local rig space: hip at the origin, +x toward the facing direction, +y down,
   unscaled. Shots convert world targets with toLocal(). */
export const RIG = {T, R, UA, FA, TH, SH};
export const rigPoints = (pose: Pose) => {
	const up: V = [Math.sin(rad(pose.lean)), -Math.cos(rad(pose.lean))];
	const fwd: V = [Math.cos(rad(pose.lean)), Math.sin(rad(pose.lean))];
	const shF = add(add([0, 0], up, T - 18), fwd, 2);
	const shB = add(shF, fwd, -8);
	const head = add([0, 0], up, T + R * 0.78);
	return {shF, shB, head, up, fwd};
};
/* two-bone solve: upper angle + elbow bend that put the hand at t (elbow bends forward) */
export const ikArm = (s: V, t: V): [number, number] => {
	const dx = t[0] - s[0];
	const dy = t[1] - s[1];
	const d = Math.max(Math.abs(UA - FA) + 1, Math.min(UA + FA - 0.5, Math.hypot(dx, dy)));
	const th = (Math.atan2(dx, dy) * 180) / Math.PI;
	const B = (Math.acos((UA * UA + d * d - FA * FA) / (2 * UA * d)) * 180) / Math.PI;
	const C = (Math.acos((UA * UA + FA * FA - d * d) / (2 * UA * FA)) * 180) / Math.PI;
	return [th - B, 180 - C];
};
/* world point -> rig-local point of a figure at (x, y) with scale/facing */
export const toLocal = (wx: number, wy: number, x: number, y: number, scale: number, facing: 1 | -1): V => [((wx - x) / scale) * facing, (wy - y) / scale];
