import React, {useMemo} from 'react';
import {AbsoluteFill, interpolate, spring, useVideoConfig} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Layer, Svg} from '../engine/camera';
import {blend, env, gesture, idle, walk, walkTo} from '../kit/actions';
import {Actor, L, LINES, TalkOverride, counterAt, talkOf, useShot, useSpeaking} from '../kit/core';
import {Bulb, Confetti, Exclaim, Glitch, ImpactText, LightningFlash, Pulse, Question, Rain, Shockwave, Smoke, Sparkles, Lightning, punch} from '../kit/fx';
import {CrowdRow, HeroBadge, Stage, camOn, ease, flash, mixCam} from '../kit/kit';
import {FONT} from '../kit/ui';
import {FX_RULES, GEST_CYCLE, GEST_RULES, Gest, Fx, Pop, clauses, popFor} from './rules';
import type {Cam} from '../engine/camera';

/* ============================== THE DIRECTOR ==============================
   A scene config says WHERE (background), WHO (cast with start slots) and a few options.
   The director then cuts every narration line into clauses (≈ every 2–3 s) and gives each
   clause: a new focus character, a gesture on the words, a walk to a new spot (every third
   clause), a new camera (wide / medium / close / pull-back / over the shoulder / low),
   plus an effect or number pop when the words ask for it. Nothing stands still. */

export type ActorCfg = {who: string; x: number; s?: number; face?: 1 | -1; enter?: 'L' | 'R'; sit?: number};
export type CrowdCfg = {n: number; x0: number; x1: number; s: number; mode: 'dance' | 'stand' | 'run' | 'walk' | 'panic'; seed: string; floor?: number; dir?: 1 | -1};
export type SceneCfg = {
	at: string;
	bg: (gf: number) => React.ReactNode;
	cast: ActorCfg[];
	crowd?: CrowdCfg[];
	front?: (gf: number, f: number) => React.ReactNode; // props between actors and camera (world space)
	names?: Record<string, RegExp>; // who is talked about (cast key -> regexp)
	night?: boolean;
	rain?: boolean;
	whip?: boolean;
	badge?: boolean; // show the approval badge over the hero
	bgc?: string;
	floor?: number;
	zoom?: number; // base zoom of the wide shot
	cy?: number;
	tone?: string; // overlay colour grade e.g. '255,120,60'
};

type Clause = {t0: number; t1: number; text: string; focus: number; gest: Gest; cam: number; fx?: {fx: Fx; text?: string}; pop?: Pop; dialog: boolean; idx: number};

const hashStr = (s: string) => [...s].reduce((a, c) => (a * 31 + c.charCodeAt(0)) >>> 0, 7);
const FLOOR = 900;
const NAMES: Record<string, RegExp> = {okafor: /Okafor|Chief of Staff/i, matias: /Matias/i, haddad: /Haddad|Leila/i, sunny: /Sunny/i, general: /general/i, econ: /economist/i, host: /host/i, kid: /\bkid\b/i, mom: /\bmom\b/i};
const SLOT_SHIFT = [0, -230, 170, -120, 240, -60, 200, -260];

export const sceneLines = (at: string, next?: string) => {
	const a = parseInt(at, 10);
	const b = next ? parseInt(next, 10) : 9999;
	return LINES.filter((l) => {
		const n = parseInt(l.id.slice(0, 3), 10);
		return n >= a && n < b;
	});
};

export const buildClauses = (cfg: SceneCfg, lines: typeof LINES, start: number): Clause[] => {
	const out: Clause[] = [];
	let lastFx = '';
	let lastFocus = -1;
	let lastCam = -1;
	let lastGest = '';
	let k = 0;
	for (const l of lines) {
		const cs = clauses(l.text);
		const tot = cs.reduce((a, c) => a + c.length + 6, 0);
		let acc = 0;
		for (const text of cs) {
			const w = (text.length + 6) / tot;
			const t0 = l.from - start + Math.round(acc * l.dur);
			acc += w;
			const t1 = l.from - start + Math.round(acc * l.dur);
			const h = hashStr(l.id + text);
			// focus: a named character, else the hero (you), rotating to others so everybody acts
			let focus = -1;
			for (const [who, re] of Object.entries(cfg.names ?? NAMES)) if (re.test(text)) {
				const ix = cfg.cast.findIndex((c) => c.who === who);
				if (ix >= 0) focus = ix;
			}
			if (focus < 0) {
				const hero = cfg.cast.findIndex((c) => c.who === 'hero');
				const others = cfg.cast.map((_, i) => i).filter((i) => i !== hero);
				focus = /\byou|your\b/i.test(text) && hero >= 0 ? hero : others.length && (k % 2 === 1 || hero < 0) ? others[(k >> 1) % others.length] : hero >= 0 ? hero : 0;
			}
			if (focus === lastFocus && cfg.cast.length > 1 && k % 3 === 0) focus = (focus + 1) % cfg.cast.length;
			let g: Gest = GEST_CYCLE[(h + k * 3) % GEST_CYCLE.length];
			for (const r of GEST_RULES) if (r.re.test(text)) {
				g = r.g;
				break;
			}
			if (g === lastGest) g = GEST_CYCLE[(h + k * 7 + 1) % GEST_CYCLE.length];
			lastGest = g;
			let cam = (h + k * 5) % 7;
			if (cam === lastCam) cam = (cam + 3) % 7;
			lastCam = cam;
			let fx: Clause['fx'];
			for (const r of FX_RULES) if (r.re.test(text) && r.fx !== lastFx) {
				fx = {fx: r.fx, text: r.text};
				lastFx = r.fx;
				break;
			}
			if (!fx) lastFx = '';
			out.push({t0, t1, text, focus, gest: g, cam, fx, pop: popFor(text) ?? undefined, dialog: /\bsays?\b|\basks?\b|\?|"|“|\bmoved\b|\bcalls\b/.test(text), idx: k});
			lastFocus = focus;
			k++;
		}
	}
	return out;
};

/* actor paths: entrance + a walk to a new spot every third clause, by the focus character */
type Seg = {t0: number; t1: number; x0: number; x1: number};
const buildPaths = (cfg: SceneCfg, cl: Clause[]): Seg[][] => {
	const paths: Seg[][] = cfg.cast.map((c) => {
		if (c.enter) return [{t0: 0, t1: 38, x0: c.enter === 'L' ? -260 : 2200, x1: c.x}];
		return [];
	});
	const cur = cfg.cast.map((c) => c.x);
	cl.forEach((c, i) => {
		if (i === 0) return;
		if (i % 3 !== 1) return;
		const a = cfg.cast[c.focus];
		if (!a || a.sit !== undefined) return;
		let x1 = a.x + SLOT_SHIFT[(i + c.focus) % SLOT_SHIFT.length];
		x1 = Math.max(260, Math.min(1660, x1));
		if (Math.abs(x1 - cur[c.focus]) < 80) x1 = Math.max(260, Math.min(1660, cur[c.focus] + 200));
		paths[c.focus].push({t0: c.t0 + 6, t1: Math.min(c.t1 - 4, c.t0 + 6 + Math.max(24, Math.abs(x1 - cur[c.focus]) / 7)), x0: cur[c.focus], x1});
		cur[c.focus] = x1;
	});
	return paths;
};
const posAt = (c: ActorCfg, path: Seg[], f: number) => {
	let x = path.length && path[0].t0 === 0 && c.enter ? path[0].x0 : c.x;
	let seg: Seg | null = null;
	for (const s of path) {
		if (f >= s.t0 && f <= s.t1) seg = s;
		if (f > s.t1) x = s.x1;
	}
	return {x, seg};
};

const PopText: React.FC<{f: number; t0: number; pop: Pop; alt: number}> = ({f, t0, pop, alt}) => {
	const {fps} = useVideoConfig();
	const d = f - t0;
	if (d < 0 || d > 70) return null;
	const sc = spring({frame: d, fps, config: {damping: 11, stiffness: 160}});
	const o = interpolate(d, [0, 4, 56, 70], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	if (pop.kind === 'day') {
		const x = interpolate(d, [0, 10], [-700, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
		return (
			<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
				<div style={{position: 'absolute', left: 0, top: 150, transform: `translateX(${x}px) rotate(-2deg)`, background: '#d9433d', color: '#fff', fontFamily: FONT, fontWeight: 900, fontSize: 120, padding: '10px 70px 10px 50px', borderRadius: '0 70px 70px 0', border: '6px solid #fff', boxShadow: '0 12px 0 rgba(0,0,0,.35)', letterSpacing: 4}}>{pop.text}</div>
			</AbsoluteFill>
		);
	}
	const left = alt % 2 === 0;
	return (
		<AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: 120, [left ? 'left' : 'right']: 120, transform: `scale(${0.4 + 0.6 * sc}) rotate(${left ? -4 : 4}deg)`, color: '#ffe05a', fontFamily: FONT, fontWeight: 900, fontSize: 190, WebkitTextStroke: '10px #1a1a2e', paintOrder: 'stroke fill', textShadow: '0 10px 0 rgba(0,0,0,.45)'}}>{pop.text}</div>
		</AbsoluteFill>
	);
};

const camFor = (c: Clause, ax: number, cx: number, zoom: number, cy: number, dir: number): Cam => {
	switch (c.cam) {
		case 0:
			return camOn(cx, cy, zoom);
		case 1:
			return camOn(ax, 600, 1.5);
		case 2:
			return camOn(ax, 570, 2.05, {farBlur: 8});
		case 3:
			return camOn(cx, cy - 20, zoom * 0.9);
		case 4:
			return camOn(ax + 170 * dir, 620, 1.3);
		case 5:
			return camOn(ax, 640, 1.15);
		default:
			return camOn(ax, 700, 1.75, {farBlur: 8});
	}
};

export const makeScene = (cfg: SceneCfg, lineIds: string[], nextAt: string | undefined): React.FC => {
	const Scene: React.FC = () => {
		const {f, gf, start} = useShot();
		const lines = useMemo(() => sceneLines(cfg.at, nextAt), []);
		const cl = useMemo(() => buildClauses(cfg, lines, start), [lines, start]);
		const paths = useMemo(() => buildPaths(cfg, cl), [cl]);
		const zoom = cfg.zoom ?? 1.0;
		const cy = cfg.cy ?? 560;
		const cx = cfg.cast.length ? cfg.cast.reduce((a, c) => a + c.x, 0) / cfg.cast.length : 960;
		const ki = Math.max(0, cl.findIndex((c) => f < c.t1));
		const k = cl.length && f >= cl[cl.length - 1].t1 ? cl.length - 1 : ki;
		const cur = cl[k];
		const prev = cl[Math.max(0, k - 1)];
		const pos = cfg.cast.map((c, i) => posAt(c, paths[i], f));
		const dirOf = (i: number) => (pos[i].x < cx ? 1 : -1);
		const camA = prev ? camFor(prev, pos[prev.focus].x, cx, zoom, cy, dirOf(prev.focus)) : camOn(cx, cy, zoom);
		const camB = cur ? camFor(cur, pos[cur.focus].x, cx, zoom, cy, dirOf(cur.focus)) : camA;
		const u = cur ? interpolate(f, [cur.t0, cur.t0 + 20], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease}) : 1;
		let cam: Cam = k === 0 ? mixCam(camOn(cx, cy, zoom * 1.12), camB, u) : mixCam(camA, camB, u);
		// beat hit: the camera punches on every effect
		if (cur?.fx) cam = {...cam, zoom: cam.zoom * (1 + punch(f, cur.t0 + 8, 0.05, 10))};
		// slow creep inside the clause so it never rests
		const creep = cur ? (f - cur.t0) / Math.max(30, cur.t1 - cur.t0) : 0;
		cam = {...cam, zoom: cam.zoom * (1 + 0.04 * creep), x: cam.x * (1 + 0.04 * creep) + Math.sin(gf / 31) * 6};
		const speaking = useSpeaking(gf);
		void speaking;
		const heroIdx = cfg.cast.findIndex((c) => c.who === 'hero');
		const showBadge = cfg.badge !== false && gf >= L('023').from + 20 && heroIdx >= 0;
		const flashK = cur?.fx && (cur.fx.fx === 'flash' || cur.fx.fx === 'lightning') ? flash(f, cur.t0 + 8, 8) : 0;
		const shake = cur?.fx && (cur.fx.fx === 'impact' || cur.fx.fx === 'lightning') && f - cur.t0 < 16 ? Math.sin(f * 7) * (10 - (f - cur.t0) * 0.5) : 0;
		return (
			<TalkOverride.Provider value={(sp, g) => (sp === 'N' ? talkOf('N', g) : 0)}>
				<div style={{position: 'absolute', inset: 0, transform: `translate(${shake}px, ${shake * 0.6}px)`}}>
					<Stage cam={cam} bg={cfg.bgc ?? '#101225'} light={{x: 22, y: 8, o: cfg.night ? 0.3 : 0.4, night: cfg.night}} dust={cfg.night ? '#aab8ff' : '#fff3d0'}>
						{cfg.bg(gf)}
						<Layer depth={1}>
							<Svg>
								{cfg.crowd?.map((c, i) => (
									<CrowdRow key={i} n={c.n} x0={c.x0} x1={c.x1} floor={c.floor ?? FLOOR - 20} s={c.s} mode={c.mode} seed={c.seed} dir={c.dir} t={gf % 4000} />
								))}
							</Svg>
						</Layer>
						<Layer depth={1}>
							<Svg>
								{cfg.cast.map((a, i) => {
									const p = pos[i];
									const isFocus = cur && cur.focus === i;
									const lookX = (cur ? pos[cur.focus].x : cx) - p.x;
									let facing: 1 | -1 = a.face ?? (lookX >= 0 ? 1 : -1);
									if (!a.face || p.seg) facing = p.seg ? (p.seg.x1 >= p.seg.x0 ? 1 : -1) : lookX >= 0 ? 1 : -1;
									if (a.sit !== undefined) facing = a.face ?? (lookX >= 0 ? 1 : -1);
									const seed = i * 3 + 1;
									const wk = p.seg ? walkTo(f, p.seg.t0, p.seg.t1, p.seg.x0, p.seg.x1, seed, 0.3) : null;
									let pose: Pose = wk ? wk.pose : idle(gf, seed);
									// the focus character acts on his clause; the others react in the gaps
									if (isFocus && cur && !wk) pose = gesture(cur.gest, pose, env(f, cur.t0 + 3, cur.t1 - 2, 8, 10), f);
									else if (!isFocus && cur && !wk && cl.length) {
										const r = cl[(k + i) % cl.length];
										const react: Gest = (['think', 'shrug', 'touchFace', 'armsCrossed', 'rubChin', 'scratch'] as Gest[])[(i + k) % 6];
										if (r) pose = gesture(react, pose, env(f, cur.t0 + 10, cur.t1 - 6, 10, 10) * 0.9, f);
									}
									const talking = isFocus && cur?.dialog;
									const s = a.s ?? 1;
									return (
										<Actor
											key={a.who + i}
											who={a.who}
											x={p.x}
											floor={cfg.floor ?? FLOOR}
											s={s}
											facing={facing}
											faceTurn={0.45}
											pose={pose}
											vx={wk ? wk.vx : 0}
											bob={wk ? wk.bob : 0}
											seat={a.sit}
											sp={talking ? 'N' : '__'}
											expr={cur && /storm|disaster|wrong|panic|died|water|shak|cry|coward/i.test(cur.text) ? (isFocus ? 'worried' : 'wide') : isFocus && cur && /laugh|smile|grin|best|great|91|love/i.test(cur.text) ? 'normal' : undefined}
											mouth={isFocus && cur && /smile|grin|laugh|joke/i.test(cur.text) ? 'smile' : undefined}
											armOver={isFocus && cur ? (['facepalm', 'touchFace', 'rubChin', 'think', 'handsOnHead'] as Gest[]).includes(cur.gest) && env(f, cur.t0 + 3, cur.t1 - 2, 8, 10) > 0.5 : false}
											handF={isFocus && cur && cur.gest === 'point' ? 'point' : undefined}
											look={[lookX > 0 ? 0.7 : -0.7, isFocus ? 0 : -0.1]}
											uid={`${cfg.at}-${i}`}
										/>
									);
								})}
								{cfg.front ? cfg.front(gf, f) : null}
								{showBadge && heroIdx >= 0 ? <HeroBadge x={pos[heroIdx].x} y={FLOOR - 157 * (cfg.cast[heroIdx].s ?? 1) - 164 * (cfg.cast[heroIdx].s ?? 1) - 115} s={0.7} /> : null}
								{cur?.fx ? <FxWorld f={f} t0={cur.t0 + 8} fx={cur.fx} x={pos[cur.focus]?.x ?? cx} s={cfg.cast[cur.focus]?.s ?? 1} /> : null}
							</Svg>
						</Layer>
					</Stage>
				</div>
				{cfg.rain ? <Rain f={gf} /> : null}
				{cur?.fx?.fx === 'lightning' ? <LightningFlash f={f} t0={cur.t0 + 8} /> : null}
				{cur?.fx?.fx === 'pulse' ? <Pulse f={f} /> : null}
				{cur?.fx?.fx === 'glitch' ? <Glitch f={f} t0={cur.t0 + 8} len={18} /> : null}
				{flashK > 0 ? <AbsoluteFill style={{background: '#fff', opacity: flashK * 0.8, pointerEvents: 'none'}} /> : null}
				{cfg.tone ? <AbsoluteFill style={{background: `rgba(${cfg.tone},0.16)`, mixBlendMode: 'multiply', pointerEvents: 'none'}} /> : null}
				{cl.map((c, i) => (c.pop ? <PopText key={i} f={f} t0={c.t0 + 8} pop={c.pop} alt={c.idx} /> : null))}
			</TalkOverride.Provider>
		);
	};
	return Scene;
};

const FxWorld: React.FC<{f: number; t0: number; fx: {fx: Fx; text?: string}; x: number; s: number}> = ({f, t0, fx, x, s}) => {
	const hy = FLOOR - 157 * s - 164 * s;
	switch (fx.fx) {
		case 'impact':
			return (
				<>
					<Shockwave f={f} t0={t0} x={x} y={hy + 60} r={300} />
					<ImpactText f={f} t0={t0} x={x} y={hy - 150} text={fx.text ?? 'BAM!'} s={0.9} />
				</>
			);
		case 'sparkle':
			return <Sparkles f={f} t0={t0} x={x} y={hy - 40} n={14} />;
		case 'exclaim':
			return <Exclaim f={f} t0={t0} x={x + 60} y={hy - 140} />;
		case 'question':
			return <Question f={f} t0={t0} x={x + 60} y={hy - 140} />;
		case 'bulb':
			return <Bulb f={f} t0={t0} x={x + 20} y={hy - 150} />;
		case 'smoke':
			return <Smoke f={f} t0={t0} x={x} y={FLOOR - 60} s={0.8} />;
		case 'confetti':
			return <Confetti f={f} t0={t0} n={50} />;
		case 'lightning':
			return <Lightning f={f} t0={t0} x={x + 500} />;
		case 'phone':
			return (
				<g transform={`translate(${x + 110},${hy + 80 + Math.sin(f * 2) * 3}) rotate(${Math.sin(f * 3) * 8})`} opacity={f - t0 < 40 ? 1 : 0}>
					<rect x={-26} y={-46} width={52} height={92} rx={10} fill="#222" stroke="#fff" strokeWidth={3} />
					<rect x={-20} y={-38} width={40} height={74} rx={5} fill="#6ac0ff" />
					<text y={10} textAnchor="middle" fontSize={22} fontFamily={FONT} fontWeight={800} fill="#fff">BZZT</text>
				</g>
			);
		default:
			return null;
	}
};
void blend;
void walk;
void counterAt;
