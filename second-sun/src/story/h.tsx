import React from 'react';
import {AbsoluteFill, interpolate, random, spring} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Gesture, env, gesture, idle, reach, run, walk} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {HeroBadge, Layer, Stage, Svg, clamp} from '../kit/kit';
import {FONT} from '../kit/ui';
import type {Cam} from '../engine/camera';
import {FarHouses, SKY, SkyDome, SkyMode, SpaceBG, Sun, Yard} from './places';

/* ---------- shared helpers for the shots of this video ---------- */

export const FL = 900;
export const headY = (s = 1, floor = FL) => floor - 157 * s - 164 * s;
export const badgeY = (s = 1, floor = FL) => headY(s, floor) - 108 * s;

/* a list of timed gestures on top of a base pose: [line, offset, length, gesture] */
export type Beat = [string, number, number, Gesture | Custom];
type Custom = 'cheer' | 'phoneUp' | 'shade' | 'carry' | 'clap' | 'armsOut' | 'sunscreen' | 'lookUp' | 'hug' | 'cover';
export const custom = (g: Custom, p: Pose, k: number, f: number): Pose => {
	if (k <= 0) return p;
	const L = (a: number, b: number) => a + (b - a) * k;
	switch (g) {
		case 'cheer':
			return {...p, head: L(p.head, -12), armF: [L(p.armF[0], 160 + Math.sin(f / 3) * 14), L(p.armF[1], 10)], armB: [L(p.armB[0], -160 - Math.sin(f / 3) * 14), L(p.armB[1], 10)]};
		case 'phoneUp':
			return {...p, head: L(p.head, -16), armF: [L(p.armF[0], 150), L(p.armF[1], 18)]};
		case 'shade':
			return reach({...p, head: L(p.head, -14)}, 'F', [44, -168], k);
		case 'carry':
			return {...p, armF: [L(p.armF[0], 62), L(p.armF[1], 40)], armB: [L(p.armB[0], 56), L(p.armB[1], 46)]};
		case 'clap': {
			const c = Math.abs(Math.sin(f / 2.2));
			return reach(reach(p, 'F', [40 + 10 * c, -90], k), 'B', [30 - 6 * c, -88], k);
		}
		case 'armsOut':
			return {...p, armF: [L(p.armF[0], 100), L(p.armF[1], 0)], armB: [L(p.armB[0], -100), L(p.armB[1], 0)]};
		case 'sunscreen':
			return reach(reach({...p, head: L(p.head, -8)}, 'F', [34 + Math.sin(f / 2.5) * 8, -150 + Math.cos(f / 2.5) * 10], k), 'B', [28 + Math.cos(f / 2.5) * 8, -142], k);
		case 'lookUp':
			return {...p, head: L(p.head, -22), lean: L(p.lean, -6)};
		case 'hug':
			return {...p, armF: [L(p.armF[0], 80), L(p.armF[1], 70)], armB: [L(p.armB[0], 76), L(p.armB[1], 76)]};
		case 'cover':
			return reach(reach({...p, head: L(p.head, 14)}, 'F', [36, -172], k), 'B', [30, -160], k);
	}
	return p;
};
const CUSTOM = ['cheer', 'phoneUp', 'shade', 'carry', 'clap', 'armsOut', 'sunscreen', 'lookUp', 'hug', 'cover'];
export const beats = (base: Pose, f: number, at: (n: string) => number, list: Beat[], inn = 8): Pose =>
	list.reduce((p, [l, o, len, g]) => {
		const k = env(f, at(l) + o, at(l) + o + len, inn, inn);
		return CUSTOM.includes(g) ? custom(g as Custom, p, k, f) : gesture(g as Gesture, p, k, f);
	}, base);
/* strength of a beat window (for hand shapes, expressions) */
export const on = (f: number, at: (n: string) => number, l: string, o: number, len: number) => env(f, at(l) + o, at(l) + o + len, 6, 6);

/* multi-stop walk: keys [frame, x]; walks between stops, idles at stops */
export const path = (f: number, keys: [number, number][], seed = 0, speed = 0.3, runK = 0) => {
	let i = 0;
	while (i + 1 < keys.length && f >= keys[i + 1][0]) i++;
	if (i + 1 >= keys.length || f < keys[0][0]) {
		const x = f < keys[0][0] ? keys[0][1] : keys[keys.length - 1][1];
		const prev = keys.length > 1 ? keys[keys.length - 1][1] - keys[keys.length - 2][1] : 1;
		return {x, pose: idle(f, seed), facing: (prev >= 0 ? 1 : -1) as 1 | -1, vx: 0, bob: 0, moving: false};
	}
	const [t0, x0] = keys[i];
	const [t1, x1] = keys[i + 1];
	if (x0 === x1) return {x: x0, pose: idle(f, seed), facing: (i > 0 && keys[i - 1][1] > x0 ? -1 : 1) as 1 | -1, vx: 0, bob: 0, moving: false};
	const u = (f - t0) / Math.max(1, t1 - t0);
	const e = u * u * (3 - 2 * u);
	const x = x0 + (x1 - x0) * e;
	const ph = (f - t0) * (runK ? 0.45 : speed * 1.15);
	const step = Math.min(1, Math.min(u, 1 - u) * 6);
	const base = runK ? run(ph) : walk(ph);
	const p0 = idle(f, seed);
	const pose: Pose = {
		lean: p0.lean + (base.lean - p0.lean) * step,
		head: p0.head + (base.head - p0.head) * step,
		armB: [p0.armB[0] + (base.armB[0] - p0.armB[0]) * step, p0.armB[1] + (base.armB[1] - p0.armB[1]) * step],
		armF: [p0.armF[0] + (base.armF[0] - p0.armF[0]) * step, p0.armF[1] + (base.armF[1] - p0.armF[1]) * step],
		legB: [p0.legB[0] + (base.legB[0] - p0.legB[0]) * step, p0.legB[1] + (base.legB[1] - p0.legB[1]) * step],
		legF: [p0.legF[0] + (base.legF[0] - p0.legF[0]) * step, p0.legF[1] + (base.legF[1] - p0.legF[1]) * step],
	};
	const vx = ((x1 - x0) * 6 * u * (1 - u)) / Math.max(1, t1 - t0);
	return {x, pose, facing: (x1 >= x0 ? 1 : -1) as 1 | -1, vx, bob: Math.abs(Math.sin(ph)) * (runK ? 10 : 4) * step, moving: true};
};

/* jump: returns lift (px) and squash for a hop at frame t0 */
export const hop = (f: number, t0: number, len = 16, h = 90) => {
	const u = (f - t0) / len;
	if (u < 0 || u > 1) return {lift: 0, squash: u > 1 && u < 1.25 ? 0.12 * (1 - (u - 1) * 4) : 0};
	return {lift: Math.sin(u * Math.PI) * h, squash: -0.06 * Math.sin(u * Math.PI)};
};
export const hops = (f: number, t0: number, t1: number, len = 16, h = 80) => {
	if (f < t0 || f > t1) return {lift: 0, squash: 0};
	return hop(f, t0 + Math.floor((f - t0) / len) * len, len, h);
};

/* the hero with the DAY badge over the head */
export const Hero: React.FC<Omit<React.ComponentProps<typeof Actor>, 'who'> & {badge?: boolean}> = ({badge = true, ...p}) => {
	const s = p.s ?? 1;
	const fl = p.floor ?? FL;
	return (
		<>
			<Actor {...p} who="hero" />
			{badge ? <HeroBadge x={p.x} y={(p.seat !== undefined ? p.seat - 164 * s - 108 * s : badgeY(s, fl)) - (p.bob ?? 0)} s={0.72 * s} /> : null}
		</>
	);
};

/* pop-in world text with outline and wobble */
export const PopText: React.FC<{t: number; x: number; y: number; text: string; size?: number; c?: string; rot?: number; out?: number; stroke?: string}> = ({t, x, y, text, size = 70, c = '#ffd34a', rot = -4, out = 9999, stroke = '#10132a'}) => {
	if (t < 0 || t > out + 10) return null;
	const k = spring({frame: t, fps: 30, config: {damping: 9, stiffness: 180}});
	const o = interpolate(t, [out, out + 10], [1, 0], clamp);
	const wob = Math.sin(t / 7) * 2;
	return (
		<g transform={`translate(${x},${y + Math.sin(t / 15) * 4}) rotate(${rot + wob}) scale(${k})`} opacity={o}>
			<text textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={900} fill={stroke} stroke={stroke} strokeWidth={size * 0.2} strokeLinejoin="round">
				{text}
			</text>
			<text textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={900} fill={c}>
				{text}
			</text>
		</g>
	);
};

/* pill label in world space */
export const Pill: React.FC<{t: number; x: number; y: number; text: string; c?: string; size?: number; out?: number}> = ({t, x, y, text, c = '#ff8a2a', size = 34, out = 9999}) => {
	if (t < 0 || t > out + 8) return null;
	const k = spring({frame: t, fps: 30, config: {damping: 11, stiffness: 170}});
	const o = interpolate(t, [out, out + 8], [1, 0], clamp);
	const w = text.length * size * 0.68 + 48;
	return (
		<g transform={`translate(${x},${y}) scale(${k})`} opacity={o}>
			<rect x={-w / 2} y={-size * 0.95} width={w} height={size * 1.9} rx={size * 0.95} fill="#11142c" stroke={c} strokeWidth={4} />
			<text x={0} y={size * 0.36} textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={800} fill="#fff">
				{text}
			</text>
		</g>
	);
};

/* big screen-space title that punches in (for hooks and key words) */
export const Punch: React.FC<{t: number; text: string; sub?: string; out?: number; c?: string; top?: number; size?: number}> = ({t, text, sub, out = 60, c = '#ffd34a', top = 120, size = 110}) => {
	if (t < 0 || t > out + 8) return null;
	const k = spring({frame: t, fps: 30, config: {damping: 10, stiffness: 200}});
	const o = interpolate(t, [out, out + 8], [1, 0], clamp);
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top, left: 0, right: 0, textAlign: 'center', opacity: o, transform: `scale(${0.6 + 0.4 * k}) rotate(${(1 - k) * -6}deg)`}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: size, color: c, WebkitTextStroke: '6px #0b0d1e', paintOrder: 'stroke', textShadow: '0 10px 30px rgba(0,0,0,.55)', letterSpacing: 2}}>{text}</div>
				{sub ? <div style={{fontFamily: FONT, fontWeight: 800, fontSize: size * 0.36, color: '#fff', WebkitTextStroke: '3px #0b0d1e', paintOrder: 'stroke', marginTop: 4}}>{sub}</div> : null}
			</div>
		</AbsoluteFill>
	);
};

/* white flash overlay */
export const Flash: React.FC<{f: number; at: number; len?: number; c?: string}> = ({f, at, len = 8, c = '#fff'}) => {
	const o = interpolate(f, [at, at + 1, at + len], [0, 0.85, 0], clamp);
	return o > 0 ? <AbsoluteFill style={{background: c, opacity: o, pointerEvents: 'none'}} /> : null;
};

/* screen shake offset applied to a camera */
export const shake = (cam: Cam, f: number, at: number, len = 14, amp = 18): Cam => {
	const k = interpolate(f, [at, at + len], [1, 0], clamp) * (f >= at ? 1 : 0);
	return {...cam, x: cam.x + Math.sin(f * 3.1) * amp * k, y: cam.y + Math.cos(f * 2.3) * amp * k};
};

/* outdoor stage: sky (far), houses (mid), yard (subject plane), cast in children */
export const Outdoor: React.FC<{
	cam: Cam;
	mode: SkyMode;
	suns?: Sun[];
	stars?: number;
	milky?: number;
	yard?: Partial<React.ComponentProps<typeof Yard>> | false;
	houses?: boolean;
	lit?: number;
	children?: React.ReactNode;
	front?: React.ReactNode;
	mid?: React.ReactNode;
	id: string;
	tint?: string;
}> = ({cam, mode, suns, stars, milky, yard, houses = true, lit, children, front, mid, id, tint}) => {
	const {gf} = useShot();
	const p = SKY[mode];
	return (
		<Stage cam={cam} bg={p.top} light={{x: 30, y: 10, o: 0.4, c: hexRgb(p.amb), night: mode === 'night' || mode === 'dark'}}>
			<Layer depth={4}>
				<SkyDome id={id} mode={mode} f={gf} suns={suns} stars={stars} milky={milky} />
			</Layer>
			{houses ? (
				<Layer depth={1.9}>
					<FarHouses mode={mode} lit={lit} />
				</Layer>
			) : null}
			{mid ? <Layer depth={1.4}>{mid}</Layer> : null}
			{yard !== false ? (
				<Layer depth={1}>
					<Yard {...(yard ?? {})} mode={mode} f={gf} />
				</Layer>
			) : null}
			<Layer depth={1}>
				<Svg>{children}</Svg>
			</Layer>
			{front ? (
				<Layer depth={0.7}>
					<Svg>{front}</Svg>
				</Layer>
			) : null}
			{tint ? <AbsoluteFill style={{background: tint, mixBlendMode: 'soft-light', pointerEvents: 'none'}} /> : null}
		</Stage>
	);
};
export const hexRgb = (h: string) => {
	const n = parseInt(h.slice(1), 16);
	return `${(n >> 16) & 255},${(n >> 8) & 255},${n & 255}`;
};

/* space stage: starfield far, subjects at depth 1 */
export const SpaceStage: React.FC<{cam: Cam; tint?: string; children: React.ReactNode; still?: boolean}> = ({cam, tint, children, still}) => {
	const {gf} = useShot();
	return (
		<Stage cam={cam} bg="#04040f" light={false} still={still}>
			<Layer depth={3}>
				<SpaceBG f={gf} tint={tint} />
			</Layer>
			<Layer depth={1} sharp>
				<Svg>{children}</Svg>
			</Layer>
		</Stage>
	);
};

/* interior stage: one set component + cast */
export const Inside: React.FC<{cam: Cam; set: React.ReactNode; children?: React.ReactNode; front?: React.ReactNode; bg?: string; light?: React.ComponentProps<typeof Stage>['light']; tint?: string}> = ({cam, set, children, front, bg = '#1a1a2a', light, tint}) => (
	<Stage cam={cam} bg={bg} light={light ?? {x: 70, y: 15, o: 0.4}}>
		<Layer depth={1.25}>{set}</Layer>
		<Layer depth={1}>
			<Svg>{children}</Svg>
		</Layer>
		{front ? (
			<Layer depth={0.7}>
				<Svg>{front}</Svg>
			</Layer>
		) : null}
		{tint ? <AbsoluteFill style={{background: tint, mixBlendMode: 'soft-light', pointerEvents: 'none'}} /> : null}
	</Stage>
);

/* little confetti / sparks burst in world space */
export const Burst: React.FC<{t: number; x: number; y: number; n?: number; c?: string[]; r?: number; seed?: string}> = ({t, x, y, n = 18, c = ['#ffd34a', '#ff5a6a', '#5ad0ff', '#9ff0b0'], r = 220, seed = 'b'}) => {
	if (t < 0 || t > 40) return null;
	const u = t / 40;
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const a = (i / n) * Math.PI * 2 + random(seed + i) * 0.5;
				const d = r * (0.4 + random(seed + 'd' + i) * 0.6) * Math.sqrt(u);
				return <rect key={i} x={x + Math.cos(a) * d} y={y + Math.sin(a) * d + u * u * 120} width={10} height={16} fill={c[i % c.length]} opacity={1 - u} transform={`rotate(${t * 12 + i * 40} ${x + Math.cos(a) * d} ${y + Math.sin(a) * d + u * u * 120})`} />;
			})}
		</g>
	);
};

/* "Zzz" floating up */
export const Zzz: React.FC<{f: number; x: number; y: number; s?: number; c?: string}> = ({f, x, y, s = 1, c = '#fff'}) => (
	<g>
		{[0, 1, 2].map((i) => {
			const u = ((f / 40 + i / 3) % 1);
			return (
				<text key={i} x={x + u * 60 * s + i * 6} y={y - u * 120 * s} fontSize={(26 + i * 10) * s} fontFamily={FONT} fontWeight={900} fill={c} opacity={Math.sin(u * Math.PI)}>
					Z
				</text>
			);
		})}
	</g>
);

/* the red question mark from the hero's portrait */
export const QMark: React.FC<{t: number; x: number; y: number; s?: number}> = ({t, x, y, s = 1}) => {
	if (t < 0) return null;
	const k = spring({frame: t, fps: 30, config: {damping: 8, stiffness: 160}});
	return (
		<g transform={`translate(${x},${y + Math.sin(t / 10) * 6}) rotate(${12 + Math.sin(t / 13) * 6}) scale(${k * s})`}>
			<text textAnchor="middle" fontSize={190} fontFamily={FONT} fontWeight={900} fill="#ff2a3c" stroke="#3a0008" strokeWidth={6}>
				?
			</text>
		</g>
	);
};

/* lerp helper on frames */
export const tw = (f: number, a: number, b: number, v0: number, v1: number) => interpolate(f, [a, b], [v0, v1], clamp);
export {idle, env};
