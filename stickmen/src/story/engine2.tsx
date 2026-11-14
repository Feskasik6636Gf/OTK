import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Pose as P2} from '../engine/Stickman';
import {blend, env, gesture, Gesture, idle, run, SIT, walk, walkTo} from '../kit/actions';
import {Actor, counterAt, useShot} from '../kit/core';
import type {ShotDef} from '../kit/coverage';
import {HeroBadge, Layer, Stage, Svg, camOn, mixCam, clamp} from '../kit/kit';
import {Onoma} from '../reference/PauseTime';
import {Bubble, FONT} from '../kit/ui';
import {Grain} from '../engine/camera';
import {ICONS} from './icons';
import {PLACES, PlaceKey} from './places';
import {id3} from './config';

/* ============================== tiny scene DSL ==============================
   A beat is a string:  "<line>[+offset] <kind> [args]"  — <line> is the 0-based index of the
   voice line (the transcript listing); times are measured from the start of that line.
   Track kinds : walk X | run X | face L|R | sit | stand | expr NAME | mouth NAME | item NAME | hide | show
                 gestures (touchFace rubChin facepalm scratch shrug point handsOnHead wave armsCrossed think
                 fist presentF stop) , jump, shake (head no), nod, sob, laugh, cheer, slump, hug, hop, spin
                 any beat may end with /N = duration in frames
   Fx kinds    : onoma TEXT [x y color] | bubble WHO TEXT | think WHO TEXT | title TEXT | stat BIG SMALL
                 flash | shake [amp] | icon NAME x y [scale] | zoomhit
   Underscore in text = space. */

export type TrackSpec = {
	who: string;
	x: number;
	s?: number;
	floor?: number;
	face?: 1 | -1;
	seat?: number; // y of the hip when sitting
	expr?: string;
	mouth?: string;
	hero?: boolean;
	badge?: boolean;
	hidden?: boolean;
	item?: string;
	beats?: string[];
	look?: [number, number];
	depth?: number; // layer depth of this track (default 1)
	age?: number;
};
export type CrowdSpec = {n: number; x0: number; x1: number; floor?: number; s?: number; mode?: 'dance' | 'stand' | 'run' | 'walk' | 'panic'; seed?: string; depth?: number};
export type ShotSpec = {
	at: number;
	place: PlaceKey;
	night?: boolean;
	cam: string[]; // first = start "x y z", then "idx x y z" keyframes; x may be F (follow hero) or F:who
	tracks: TrackSpec[];
	fx?: string[];
	whip?: boolean;
	crowd?: CrowdSpec[];
	light?: {x?: number; y?: number; o?: number; c?: string; night?: boolean};
	dust?: string;
	fg?: boolean;
	pv?: Record<string, number | string>; // extra place props
	floor?: number;
};

const FL = 900;
const num = (s: string | undefined, d: number) => (s === undefined || s === '' || isNaN(+s) ? d : +s);

type Beat = {line: string; off: number; kind: string; a: string[]; dur?: number};
const parse = (b: string): Beat => {
	const m = b.trim().match(/^(\d+)(?:\+(-?\d+))?\s+(\S+)(?:\s+(.*))?$/);
	if (!m) throw new Error('bad beat: ' + b);
	let kind = m[3];
	let dur: number | undefined;
	let args = (m[4] ?? '').trim();
	const dm = kind.match(/^(\w+)\/(\d+)$/);
	if (dm) {
		kind = dm[1];
		dur = +dm[2];
	}
	const dm2 = args.match(/^(.*?)\/(\d+)$/);
	if (dm2) {
		args = dm2[1].trim();
		dur = +dm2[2];
	}
	return {line: id3(+m[1]), off: m[2] ? +m[2] : 0, kind, a: args ? args.split(/\s+/) : [], dur};
};

export const heroScale = (gf: number) => {
	const c = counterAt(gf);
	return c >= 16 ? 1 : 0.4 + 0.6 * Math.max(0, c / 16);
};

const GEST = new Set(['touchFace', 'rubChin', 'facepalm', 'scratch', 'shrug', 'point', 'handsOnHead', 'wave', 'armsCrossed', 'think', 'fist', 'presentF', 'stop']);
const OVER = new Set(['touchFace', 'rubChin', 'facepalm', 'scratch', 'handsOnHead', 'think']);
const lerp = (a: number, b: number, k: number) => a + (b - a) * k;

type TrackOut = {x: number; y: number; s: number; pose: Pose; facing: 1 | -1; vx: number; bob: number; props: Record<string, any>; hidden: boolean; seat?: number; item?: string; moving: boolean};

export const evalTrack = (tr: TrackSpec, f: number, gf: number, at: (n: string) => number, endOf: (n: string) => number): TrackOut => {
	const beats = (tr.beats ?? []).map(parse);
	const T = (b: Beat) => at(b.line) + b.off;
	const sorted = beats.map((b) => ({b, t: T(b)})).sort((p, q) => p.t - q.t);
	const baseS = (tr.s ?? 1) * (tr.hero ? heroScale(gf) : 1);
	const c = tr.hero ? counterAt(gf) : 0;
	const old = tr.hero && c >= 60;
	const speed = (old ? 4.5 : 7) * (tr.hero ? Math.max(0.6, Math.sqrt(heroScale(gf))) : 1) * 1; // px per frame
	// --- horizontal movement segments
	let cur = tr.x;
	let facing: 1 | -1 = tr.face ?? 1;
	let seg: {t0: number; t1: number; x0: number; x1: number; run: boolean} | null = null;
	let lastSeg: {t0: number; t1: number; x0: number; x1: number; run: boolean} | null = null;
	let sitting = false;
	let hidden = !!tr.hidden;
	let expr = tr.expr as string | undefined;
	let mouth = tr.mouth as string | undefined;
	let item = tr.item;
	let glasses = false;
	for (const {b, t} of sorted) {
		if (t > f) break;
		if (b.kind === 'walk' || b.kind === 'run') {
			const x1 = num(b.a[0], cur);
			const sp = b.kind === 'run' ? speed * 2.1 : speed * (b.a[1] ? +b.a[1] : 1);
			const t1 = t + Math.max(14, Math.round(Math.abs(x1 - cur) / sp));
			const s = {t0: t, t1, x0: cur, x1, run: b.kind === 'run'};
			if (f < t1) seg = s;
			else lastSeg = s;
			if (x1 !== cur) facing = x1 > cur ? 1 : -1;
			cur = f < t1 ? cur : x1;
			if (f < t1) break;
		} else if (b.kind === 'face') facing = b.a[0] === 'L' ? -1 : 1;
		else if (b.kind === 'sit') sitting = true;
		else if (b.kind === 'stand') sitting = false;
		else if (b.kind === 'expr') expr = b.a[0] === 'none' ? undefined : b.a[0];
		else if (b.kind === 'mouth') mouth = b.a[0];
		else if (b.kind === 'item') item = b.a[0] === 'none' ? undefined : b.a[0];
		else if (b.kind === 'glasses') glasses = true;
		else if (b.kind === 'hide') hidden = true;
		else if (b.kind === 'show') hidden = false;
	}
	// state kinds after a moving segment (e.g. 'sit' scheduled while walking) are rare; ignore
	let x = cur;
	let pose: Pose = idle(gf, tr.x / 91);
	let vx = 0;
	let bob = 0;
	let moving = false;
	if (seg) {
		const w = walkTo(f, seg.t0, seg.t1, seg.x0, seg.x1, tr.x / 91, seg.run ? 0.55 : 0.3);
		x = w.x;
		vx = w.vx;
		bob = w.bob;
		moving = true;
		pose = w.pose;
		if (seg.run) {
			const u = Math.max(0, Math.min(1, (f - seg.t0) / Math.max(1, seg.t1 - seg.t0)));
			const ph = (f - seg.t0) * 0.62;
			pose = blend(idle(gf, 1), run(ph), Math.min(1, Math.min(u, 1 - u) * 6));
			bob = Math.abs(Math.sin(ph)) * 8;
		}
	} else if (lastSeg) {
		x = lastSeg.x1;
	}
	let seatY: number | undefined;
	if (sitting) {
		pose = {...SIT, head: Math.sin(gf / 31) * 2, lean: -4 + Math.sin(gf / 23)};
		seatY = tr.seat ?? 800;
	}
	if (old && !sitting) pose = {...pose, lean: pose.lean + 9, head: pose.head + 7};
	// --- gestures and specials
	let armOver = false;
	let handF: 'point' | 'fist' | 'snap' | undefined;
	let faceTurnAdd = 0;
	let hop = 0;
	let squash = 0;
	let eMouth: string | undefined;
	for (const {b, t} of sorted) {
		const d = b.dur ?? (b.kind === 'jump' || b.kind === 'hop' ? 16 : b.kind === 'spin' ? 24 : 70);
		if (f < t - 2 || f > t + d + 12) continue;
		const k = env(f, t, t + d, 7, 9);
		if (GEST.has(b.kind)) {
			pose = gesture(b.kind as Gesture, pose, k, f - t);
			if (OVER.has(b.kind) && k > 0.55) armOver = true;
			if (b.kind === 'point' && k > 0.4) handF = 'point';
			if (b.kind === 'fist' && k > 0.4) handF = 'fist';
		} else if (b.kind === 'jump' || b.kind === 'hop') {
			const u = Math.max(0, Math.min(1, (f - t) / d));
			const h = b.kind === 'jump' ? 90 : 38;
			hop = Math.max(hop, h * Math.sin(Math.PI * u));
			if (u > 0 && u < 1) {
				pose = {...pose, armF: [lerp(pose.armF[0], 150, 0.8), 20], armB: [lerp(pose.armB[0], -150, 0.8), 20], legB: [-20, 40], legF: [20, 40]};
			}
			squash = Math.max(squash, u < 0.12 ? 0.12 : u > 0.9 ? 0.1 : 0);
		} else if (b.kind === 'shake') {
			pose = {...pose, head: pose.head + 16 * k * Math.sin((f - t) * 0.95)};
			eMouth ??= 'flat';
		} else if (b.kind === 'nod') {
			pose = {...pose, head: pose.head + 11 * k * Math.sin((f - t) * 0.6)};
		} else if (b.kind === 'sob') {
			pose = gesture('facepalm', pose, k, f - t);
			pose = {...pose, lean: pose.lean + 3 * k * Math.sin((f - t) * 0.8), head: pose.head + 2 * k * Math.sin((f - t) * 1.3)};
			if (k > 0.5) armOver = true;
			eMouth = 'frown';
		} else if (b.kind === 'laugh') {
			pose = {...pose, lean: pose.lean - 12 * k + 3 * k * Math.sin((f - t) * 0.9), head: pose.head - 6 * k, armF: [lerp(pose.armF[0], 25, k), lerp(pose.armF[1], 70, k)]};
			bob = Math.max(bob, k * Math.abs(Math.sin((f - t) * 0.5)) * 7);
			eMouth = 'open';
		} else if (b.kind === 'cheer') {
			pose = {...pose, armF: [lerp(pose.armF[0], 160, k), lerp(pose.armF[1], 12, k)], armB: [lerp(pose.armB[0], -160, k), lerp(pose.armB[1], 12, k)]};
			bob = Math.max(bob, k * Math.abs(Math.sin((f - t) * 0.45)) * 18);
			eMouth = 'open';
		} else if (b.kind === 'slump') {
			pose = {...pose, lean: pose.lean + 12 * k, head: pose.head + 18 * k, armF: [lerp(pose.armF[0], 4, k), lerp(pose.armF[1], 6, k)], armB: [lerp(pose.armB[0], -4, k), 6]};
		} else if (b.kind === 'hug') {
			pose = {...pose, lean: pose.lean + 6 * k, armF: [lerp(pose.armF[0], 92, k), lerp(pose.armF[1], 26, k)], armB: [lerp(pose.armB[0], 88, k), lerp(pose.armB[1], 24, k)]};
		} else if (b.kind === 'spin') {
			faceTurnAdd = k;
		} else if (b.kind === 'lean') {
			pose = {...pose, lean: pose.lean + num(b.a[0], 10) * k};
		} else if (b.kind === 'reach') {
			pose = {...pose, armF: [lerp(pose.armF[0], 100, k), lerp(pose.armF[1], 6, k)], lean: pose.lean + 6 * k};
		} else if (b.kind === 'stumble') {
			pose = {...pose, lean: pose.lean + 18 * k * Math.sin((f - t) * 0.5), armF: [lerp(pose.armF[0], 70, k), 20], armB: [lerp(pose.armB[0], -70, k), 20]};
		}
	}
	const props: Record<string, any> = {};
	if (expr) props.expr = expr;
	if (glasses) props.acc = ['glasses'];
	if (tr.age !== undefined) props.age = tr.age;
	const m = eMouth ?? mouth;
	if (m) props.mouth = m;
	if (armOver) props.armOver = true;
	if (handF) props.handF = handF;
	if (squash) props.squash = squash;
	if (tr.look) props.look = tr.look;
	if (expr === 'wide') {
		props.lidL = 0;
		props.lidR = 0;
	}
	if (faceTurnAdd) props.faceTurn = 0.6;
	return {x, y: 0, s: baseS, pose, facing, vx, bob: bob + hop, props, hidden, seat: seatY, item, moving};
};

/* ------------------------------- fx ------------------------------- */
type Fx = {t: number; kind: string; a: string[]; d?: number};
const parseFx = (s: string, at: (n: string) => number): Fx => {
	const b = parse(s);
	return {t: at(b.line) + b.off, kind: b.kind, a: b.a.map((x) => x.replace(/_/g, ' ')), d: b.dur};
};

const Title: React.FC<{t: number; text: string; d: number}> = ({t, text, d}) => {
	const {fps} = useVideoConfig();
	if (t < 0 || t > d) return null;
	const k = spring({frame: t, fps, config: {damping: 9, stiffness: 190, mass: 0.7}});
	const out = interpolate(t, [d - 8, d], [1, 0], clamp);
	return (
		<AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', pointerEvents: 'none', opacity: out}}>
			<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 230, color: '#fff', letterSpacing: 4, transform: `scale(${0.4 + 0.6 * k}) rotate(${(1 - k) * -6}deg)`, textShadow: '0 10px 0 #b3142a, 0 0 60px rgba(255,35,64,0.7), 0 0 8px #000', WebkitTextStroke: '8px #12060a', paintOrder: 'stroke fill'}}>{text}</div>
		</AbsoluteFill>
	);
};

const Stat: React.FC<{t: number; big: string; small: string; d: number}> = ({t, big, small, d}) => {
	const {fps} = useVideoConfig();
	if (t < 0 || t > d) return null;
	const k = spring({frame: t, fps, config: {damping: 11, stiffness: 150}});
	const out = interpolate(t, [d - 10, d], [1, 0], clamp);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: out}}>
			<div style={{position: 'absolute', left: 70, top: 120, transform: `translateX(${(1 - k) * -520}px) rotate(-2deg)`, background: 'rgba(18,8,12,0.9)', border: '4px solid #ff2340', borderRadius: 26, padding: '18px 38px', boxShadow: '0 12px 0 #5c0d1a'}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 112, color: '#fff', lineHeight: 1}}>{big}</div>
				<div style={{fontFamily: FONT, fontWeight: 600, fontSize: 40, color: '#ffc4cc', marginTop: 6}}>{small}</div>
			</div>
		</AbsoluteFill>
	);
};

/* ------------------------------ camera ------------------------------ */
type CamKey = {t: number; x: string; y: number; z: number};

/* ------------------------------ the shot ------------------------------ */
export const makeShot = (spec: ShotSpec): ShotDef => {
	const C: React.FC = () => {
		const {f, gf, at, end, dur} = useShot();
		const {fps} = useVideoConfig();
		const Place = PLACES[spec.place];
		// ---- tracks
		const outs = spec.tracks.map((tr) => ({tr, o: evalTrack(tr, f, gf, at, end)}));
		const hero = outs.find((o) => o.tr.hero);
		const whoX = (w: string) => outs.find((o) => o.tr.who === w)?.o.x ?? 960;
		// ---- camera keyframes
		const first = spec.cam[0].split(/\s+/);
		const keys: CamKey[] = [{t: 0, x: first[0], y: +first[1], z: +first[2]}];
		for (const k of spec.cam.slice(1)) {
			const p = k.trim().split(/\s+/);
			const mm = p[0].split('+');
			keys.push({t: at(id3(+mm[0])) + (mm[1] ? +mm[1] : -4), x: p[1], y: +p[2], z: +p[3]});
		}
		const camAt = (kk: CamKey) => {
			let X = 960;
			if (kk.x.startsWith('F')) {
				const w = kk.x.includes(':') ? kk.x.split(':')[1] : spec.tracks.find((t) => t.hero)?.who ?? spec.tracks[0].who;
				X = whoX(w);
			} else X = +kk.x;
			return {X, Y: kk.y, Z: kk.z};
		};
		let ki = 0;
		while (ki + 1 < keys.length && f >= keys[ki + 1].t) ki++;
		const kA = keys[ki];
		const kPrev = keys[Math.max(0, ki - 1)];
		const tIn = interpolate(f, [kA.t, kA.t + 22], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
		const cA = camAt(kA);
		const cP = ki > 0 ? camAt(kPrev) : cA;
		// slow creep forward inside each key
		const creep = 1 + 0.035 * interpolate(f, [kA.t, (keys[ki + 1]?.t ?? dur)], [0, 1], clamp);
		const camX = lerp(cP.X, cA.X, ki > 0 ? tIn : 1);
		const camY = lerp(cP.Y, cA.Y, ki > 0 ? tIn : 1);
		const camZ = lerp(cP.Z, cA.Z, ki > 0 ? tIn : 1) * creep;
		const cam = camOn(camX, camY, camZ, {farBlur: camZ > 1.6 ? 6 : 3});
		// ---- fx
		const fxs = (spec.fx ?? []).map((s) => parseFx(s, at));
		let shake = 0;
		let flashK = 0;
		for (const x of fxs) {
			if (x.kind === 'shake') {
				const amp = num(x.a[0], 14);
				const d = x.d ?? 18;
				if (f >= x.t && f < x.t + d) shake = Math.max(shake, amp * (1 - (f - x.t) / d));
			}
			if (x.kind === 'flash') flashK = Math.max(flashK, f >= x.t && f < x.t + 8 ? 1 - (f - x.t) / 8 : 0);
			if (x.kind === 'zoomhit') {
				/* handled via camera creep: small punch */
			}
		}
		const sh = shake ? `translate(${Math.sin(f * 7.1) * shake}px, ${Math.cos(f * 9.3) * shake}px)` : undefined;
		const hs = hero ? hero.o.s : 1;
		return (
			<AbsoluteFill style={{transform: sh}}>
				<Stage cam={cam} bg="#101225" light={spec.light ?? (spec.night ? {night: true, o: 0.3} : {x: 25, y: 10, o: 0.4})} dust={spec.dust} grain={0.1}>
					<Layer depth={1.6}>
						<Place f={gf} night={!!spec.night} {...(spec.pv ?? {})} />
					</Layer>
					{(spec.crowd ?? []).map((cr, i) => (
						<Layer depth={cr.depth ?? 1.25} key={'cr' + i}>
							<Svg>
								<CrowdMini {...cr} f={gf} />
							</Svg>
						</Layer>
					))}
					<Layer depth={1}>
						<Svg>
							{outs.map(({tr, o}, i) =>
								o.hidden ? null : (
									<g key={i} opacity={1}>
										<Actor
											who={tr.who}
											x={o.x}
											floor={tr.floor ?? FL}
											s={o.s}
											facing={o.facing}
											faceTurn={o.moving ? 0.55 : 0.35}
											pose={o.pose}
											vx={o.vx}
											bob={o.bob}
											seat={o.seat}
											uid={tr.who + i}
											handItem={o.item && ICONS[o.item] ? ICONS[o.item](1) : undefined}
											{...o.props}
										/>
									</g>
								),
							)}
							{hero && hero.tr.badge !== false && !hero.o.hidden ? <HeroBadge x={hero.o.x} y={(hero.o.seat ?? ((hero.tr.floor ?? FL) - 157 * hs)) - 164 * hs - 105 - hero.o.bob * hs} s={0.8} /> : null}
							{fxs.map((x, i) => {
								const t = f - x.t;
								if (x.kind === 'onoma') {
									const px = x.a[1] ? +x.a[1] : whoX(spec.tracks[0].who);
									return <Onoma key={i} x={px} y={x.a[2] ? +x.a[2] : 420} text={x.a[0]} t={t} c={x.a[3] ?? '#ffcf3f'} rot={((i * 7) % 15) - 7} size={x.d ?? 72} />;
								}
								if (x.kind === 'bubble' || x.kind === 'think') {
									const d = x.d ?? 80;
									if (t < 0 || t > d) return null;
									const wx = whoX(x.a[0]);
									const tw = x.a.slice(1).join(' ');
									const w = Math.max(160, Math.min(760, tw.length * 21 + 70));
									const lines = tw.length > 28 ? 2 : 1;
									const tr = spec.tracks.find((q) => q.who === x.a[0]);
									const sc = (tr?.hero ? hs : tr?.s ?? 1) * 1;
									const topY = (tr?.floor ?? FL) - 330 * sc - (tr?.hero ? 100 : 40) - (lines === 2 ? 30 : 0);
									const op = interpolate(t, [d - 8, d], [1, 0], clamp);
									const words = lines === 2 ? [tw.slice(0, Math.ceil(tw.length / 2)).replace(/\s\S*$/, ''), ''] : [tw];
									let l1 = tw;
									let l2 = '';
									if (lines === 2) {
										const mid = tw.lastIndexOf(' ', Math.ceil(tw.length / 2) + 4);
										l1 = tw.slice(0, mid > 0 ? mid : Math.ceil(tw.length / 2));
										l2 = tw.slice(l1.length).trim();
									}
									void words;
									const bw = lines === 2 ? Math.max(l1.length, l2.length) * 21 + 70 : w;
									return (
										<g key={i} opacity={op}>
											<Bubble x={Math.max(bw / 2 + 20, Math.min(1900 - bw / 2, wx + 40))} y={topY} w={bw} h={lines === 2 ? 118 : 78} t={t} thought={x.kind === 'think'} tail={[-30, 70]}>
												<text x={0} y={lines === 2 ? -10 : 12} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={34} fill="#14162a">
													{l1}
												</text>
												{lines === 2 ? (
													<text x={0} y={34} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={34} fill="#14162a">
														{l2}
													</text>
												) : null}
											</Bubble>
										</g>
									);
								}
								if (x.kind === 'icon') {
									const d = x.d ?? 90;
									if (t < 0 || t > d) return null;
									const k = spring({frame: t, fps, config: {damping: 9, stiffness: 160, mass: 0.7}});
									const o2 = interpolate(t, [d - 8, d], [1, 0], clamp);
									const sc = (x.a[3] ? +x.a[3] : 1) * k;
									const ix = x.a[1] === 'W' ? whoX(spec.tracks[0].who) : +x.a[1];
									return (
										<g key={i} transform={`translate(${ix},${+x.a[2] + Math.sin(t / 14) * 6}) scale(${sc})`} opacity={o2}>
											{ICONS[x.a[0]] ? ICONS[x.a[0]](2) : null}
										</g>
									);
								}
								return null;
							})}
						</Svg>
					</Layer>
					{spec.fg ? (
						<Layer depth={0.7}>
							<Svg>
								<rect x={-200} y={1010} width={2400} height={200} fill="#05050c" opacity={0.55} />
							</Svg>
						</Layer>
					) : null}
				</Stage>
				{fxs.map((x, i) => {
					const t = f - x.t;
					if (x.kind === 'stat') {
						// only the newest card is shown
						const newer = fxs.some((y, j) => j !== i && y.kind === 'stat' && y.t > x.t && f >= y.t);
						if (newer) return null;
					}
					if (x.kind === 'title') return <Title key={i} t={t} text={x.a.join(' ')} d={x.d ?? 54} />;
					if (x.kind === 'stat') return <Stat key={i} t={t} big={x.a[0]} small={x.a.slice(1).join(' ')} d={x.d ?? 120} />;
					return null;
				})}
				{flashK > 0 ? <AbsoluteFill style={{background: '#fff', opacity: flashK * 0.8, pointerEvents: 'none'}} /> : null}
			</AbsoluteFill>
		);
	};
	return {at: id3(spec.at), C, whip: spec.whip};
};

/* a handful of simple background people */
import {CrowdRow} from '../kit/kit';
const CrowdMini: React.FC<CrowdSpec & {f: number}> = ({n, x0, x1, floor = FL, s = 0.9, mode = 'stand', seed = 'cm', f}) => <CrowdRow n={n} x0={x0} x1={x1} floor={floor} s={s} mode={mode} seed={seed} t={f} />;
void mixCam;
void walk;
void Grain;
export type {P2};
