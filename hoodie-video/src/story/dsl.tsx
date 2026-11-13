import React from 'react';
import {AbsoluteFill, Easing, interpolate} from 'remotion';
import {Pose, Stickman} from '../engine/Stickman';
import {CAST} from '../story/cast';
import {Gesture, blend, env, gesture, idle, run, walkTo} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import type {ShotDef} from '../kit/coverage';
import {Layer, Stage, Svg, camOn, usePush} from '../kit/kit';
import {LOCS, LocKey} from './places';

export type Ctx = {f: number; gf: number; dur: number; at: (n: string) => number; end: (n: string) => number};
export type Cam = [number, number, number];
/* gesture, line id, frames from the line start (on, off) */
export type G = [Gesture, string, number, number];

export type AS = {
	who: string;
	x: number;
	to?: number; // walk (or run) to this x
	w?: [string, number, number]; // walk window: line id, frames from its start (begin, end)
	run?: boolean;
	s?: number;
	face?: 1 | -1;
	floor?: number;
	g?: G[];
	seed?: number;
	rot?: number; // lie down / tilt about the feet
	pose?: (p: Pose, c: Ctx) => Pose;
	hide?: boolean;
	[k: string]: any;
};

/* an actor placed in a shot: walks / runs between two x, gestures timed to words */
export const man = (c: Ctx, a: AS): React.ReactNode => {
	const {who, x, to, w, run: running, s = 1, face, floor = 900, g = [], seed = 0, rot, pose: pf, hide, ...rest} = a;
	if (hide) return null;
	let px = x;
	let pose: Pose = idle(c.gf, seed + x / 100);
	let vx = 0;
	let bob = 0;
	let facing: 1 | -1 = face ?? 1;
	if (to !== undefined && w) {
		const t0 = c.at(w[0]) + w[1];
		const t1 = c.at(w[0]) + w[2];
		const r = walkTo(c.f, t0, t1, x, to, seed, running ? 0.55 : 0.3);
		px = r.x;
		vx = r.vx;
		bob = r.bob;
		const u = Math.max(0, Math.min(1, (c.f - t0) / Math.max(1, t1 - t0)));
		const step = c.f > t0 && c.f < t1 ? Math.min(1, Math.min(u, 1 - u) * 6) : 0;
		pose = running ? blend(idle(c.f, seed), run((c.f - t0) * 0.55), step) : r.pose;
		if (face === undefined && (c.f > t0 - 2)) facing = to >= x ? 1 : -1;
		if (face === undefined && c.f <= t0 - 2) facing = to >= x ? 1 : -1;
	}
	for (const [n, line, o0, o1] of g) pose = gesture(n, pose, env(c.f, c.at(line) + o0, c.at(line) + o1, 8, 8), c.f);
	if (pf) pose = pf(pose, c);
	const el = <Actor who={who} x={px} floor={floor} s={s} facing={facing} faceTurn={0.5} pose={pose} vx={vx} bob={bob} seed={seed} uid={`${who}${seed}`} {...rest} />;
	return rot ? <g transform={`rotate(${rot} ${px} ${floor})`}>{el}</g> : el;
};

/* a lying figure (sick, asleep): rotate about the feet */
export const lying = (c: Ctx, who: string, x: number, floor: number, rest: Record<string, any> = {}) =>
	man(c, {who, x, floor, rot: -84, face: 1, pose: () => ({lean: 0, head: -6 + Math.sin(c.gf / 25) * 3, armB: [4, 10], armF: [10, 14], legB: [0, 0], legF: [3, 0]}), ...rest});

export type Opts = {
	whip?: boolean;
	back?: (c: Ctx) => React.ReactNode; // behind the actors (depth 1.15), world svg
	fg?: (c: Ctx) => React.ReactNode; // in front of the actors (depth 0.8), world svg
	over?: (c: Ctx) => React.ReactNode; // screen space overlay
	dust?: string | false;
	light?: any;
	noFront?: boolean;
	noMid?: boolean;
	grain?: number;
	still?: boolean;
	shake?: (c: Ctx) => number; // px amplitude
	flash?: (c: Ctx) => number; // 0..1 white
	tint?: (c: Ctx) => string | null; // colour wash
};

/* One shot: location + camera push + world svg body + overlays. */
export const S = (at: string, loc: LocKey, a: Cam, b: Cam | null, body: (c: Ctx) => React.ReactNode, o: Opts = {}): ShotDef => {
	const C: React.FC = () => {
		const sh = useShot();
		const bb: Cam = b ?? [a[0] + 24, a[1] - 6, a[2] * 1.07];
		const cam = usePush(camOn(a[0], a[1], a[2]), camOn(bb[0], bb[1], bb[2]));
		const L = LOCS[loc];
		const c: Ctx = {f: sh.f, gf: sh.gf, dur: sh.dur, at: sh.at, end: sh.end};
		const sk = o.shake ? o.shake(c) : 0;
		const fl = o.flash ? o.flash(c) : 0;
		const tn = o.tint ? o.tint(c) : null;
		return (
			<>
				<AbsoluteFill style={sk > 0.1 ? {transform: `translate(${Math.sin(c.gf * 2.7) * sk}px, ${Math.cos(c.gf * 3.3) * sk}px)`} : undefined}>
				<Stage cam={cam} bg={L.bg} light={o.light ?? L.light} dust={o.dust === false ? undefined : o.dust ?? L.dust} grain={o.grain} still={o.still}>
					<Layer depth={2}>{L.far(c.gf)}</Layer>
					{o.noMid ? null : <Layer depth={1.35}>{L.mid(c.gf)}</Layer>}
					{o.back ? (
						<Layer depth={1.15}>
							<Svg>{o.back(c)}</Svg>
						</Layer>
					) : null}
					<Layer depth={1}>
						{L.ground(c.gf)}
						<Svg>{body(c)}</Svg>
					</Layer>
					{o.fg ? (
						<Layer depth={0.8}>
							<Svg>{o.fg(c)}</Svg>
						</Layer>
					) : null}
					{o.noFront ? null : <Layer depth={0.6}>{L.front(c.gf)}</Layer>}
				</Stage>
				</AbsoluteFill>
				{tn ? <AbsoluteFill style={{background: tn, pointerEvents: 'none'}} /> : null}
				{fl > 0.01 ? <AbsoluteFill style={{background: '#fff', opacity: fl, pointerEvents: 'none'}} /> : null}
				{o.over ? o.over(c) : null}
			</>
		);
	};
	return {at, C, whip: o.whip};
};

export const FL = 900;
export const hy = (s: number) => FL - 157 * s - 164 * s; // head centre y of a standing figure

export const clampO = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
/* spring-ish pop 0→1 (overshoot) starting at frame t */
export const pop = (f: number, t: number, d = 10) => interpolate(f, [t, t + d], [0, 1], {...clampO, easing: Easing.out(Easing.back(2.2))});
/* scale a group about (x,y) */
export const sc = (k: number, x: number, y: number, ch: React.ReactNode) => (
	<g transform={`translate(${x},${y}) scale(${Math.max(0.0001, k)}) translate(${-x},${-y})`}>{ch}</g>
);
/* frames since line `n` + off (negative = not yet) */
export const rel = (c: Ctx, n: string, off = 0) => c.f - c.at(n) - off;
/* ease 0..1 over [t0,t1] in shot frames */
export const lerpF = (f: number, t0: number, t1: number, a: number, b: number) => interpolate(f, [t0, t1], [a, b], {...clampO, easing: Easing.inOut(Easing.cubic)});
