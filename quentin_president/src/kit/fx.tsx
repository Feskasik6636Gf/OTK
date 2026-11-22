import React from 'react';
import {AbsoluteFill, interpolate, random} from 'remotion';
import {Pop, clamp} from './kit';
import {FONT} from './ui';

/* ------------------------------- effects library -------------------------------
   Short, loud, readable effects for key beats. Every effect has a matching sound
   (FX_SOUND below, details in references/effects.md): put the sfx in sound.json on the
   SAME line and frame as the effect. `f` is the local frame, `t0` the frame it starts on.
   World effects go inside <Svg> (they move with the camera); screen effects (Glitch,
   LightningFlash, Pulse, Rain, Snow) are overlays: render them next to <Stage>. */

const INK = '#1d1626';
const env = (f: number, t0: number, len: number) => interpolate(f, [t0, t0 + 2, t0 + len * 0.55, t0 + len], [0, 1, 1, 0], clamp);

/* effect -> sound.json type(s), so the picture never plays silently */
export const FX_SOUND: Record<string, string> = {
	Shockwave: 'impact',
	ImpactText: 'impact',
	SpeedLines: 'whoosh',
	Sparkles: 'sparkle',
	Smoke: 'swoosh',
	Confetti: 'success',
	Lightning: 'thunder',
	LightningFlash: 'thunder',
	Glitch: 'glitch',
	Pulse: 'heartbeat',
	Exclaim: 'pop',
	Question: 'pop',
	Bulb: 'ding',
	Rain: 'ambience rain',
	Snow: 'ambience wind',
	punch: 'thud',
	flash: 'flashbang',
};

/* camera punch: multiply the camera zoom by (1 + punch(f, t0)) for a beat hit */
export const punch = (f: number, t0: number, amp = 0.09, len = 12) => (f < t0 ? 0 : amp * Math.exp(-(f - t0) / (len / 3)) * Math.cos(((f - t0) / len) * Math.PI * 0.5));

/* anime speed lines around a point: run, fall, shock, a fast move */
export const SpeedLines: React.FC<{f: number; t0: number; t1: number; x?: number; y?: number; c?: string; n?: number}> = ({f, t0, t1, x = 960, y = 540, c = '#ffffff', n = 46}) => {
	if (f < t0 || f > t1) return null;
	const o = interpolate(f, [t0, t0 + 4, t1 - 4, t1], [0, 1, 1, 0], clamp);
	return (
		<g opacity={o * 0.85}>
			{Array.from({length: n}).map((_, i) => {
				const a = (i / n) * Math.PI * 2 + random('sl' + i) * 0.2;
				const r0 = 380 + random('s0' + i) * 260 + Math.sin(f * 1.3 + i) * 30;
				const r1 = r0 + 260 + random('s1' + i) * 520;
				return <line key={i} x1={x + Math.cos(a) * r0} y1={y + Math.sin(a) * r0} x2={x + Math.cos(a) * r1} y2={y + Math.sin(a) * r1} stroke={c} strokeWidth={3 + random('sw' + i) * 7} strokeLinecap="round" />;
			})}
		</g>
	);
};

/* expanding ring + flash + sparks: a hit, an explosion, a landing */
export const Shockwave: React.FC<{f: number; t0: number; x: number; y: number; c?: string; r?: number}> = ({f, t0, x, y, c = '#ffe08a', r = 420}) => {
	const k = (f - t0) / 22;
	if (k < 0 || k > 1) return null;
	const e = 1 - Math.pow(1 - k, 3);
	return (
		<g opacity={1 - k * k}>
			<circle cx={x} cy={y} r={r * e * 0.45} fill="#fff" opacity={Math.max(0, 1 - k * 3)} />
			<circle cx={x} cy={y} r={r * e} fill="none" stroke={c} strokeWidth={26 * (1 - k)} />
			<circle cx={x} cy={y} r={r * e * 0.7} fill="none" stroke="#fff" strokeWidth={10 * (1 - k)} />
			{Array.from({length: 14}).map((_, i) => {
				const a = (i / 14) * Math.PI * 2;
				return <line key={i} x1={x + Math.cos(a) * r * e * 0.8} y1={y + Math.sin(a) * r * e * 0.8} x2={x + Math.cos(a) * r * (e + 0.32)} y2={y + Math.sin(a) * r * (e + 0.32)} stroke={c} strokeWidth={9 * (1 - k)} strokeLinecap="round" />;
			})}
		</g>
	);
};

/* comic burst with a word: «БАХ!», «ЩЁЛК!», «ЧТО?!» */
export const ImpactText: React.FC<{f: number; t0: number; x: number; y: number; text: string; c?: string; s?: number}> = ({f, t0, x, y, text, c = '#ffd84a', s = 1}) => {
	if (f < t0 || f > t0 + 40) return null;
	const o = interpolate(f, [t0 + 28, t0 + 40], [1, 0], clamp);
	const pts = Array.from({length: 24}).map((_, i) => {
		const a = (i / 24) * Math.PI * 2;
		const r = i % 2 ? 150 : 230;
		return `${Math.cos(a) * r},${Math.sin(a) * r * 0.78}`;
	});
	return (
		<g opacity={o}>
			<Pop t={f - t0} x={x} y={y} s={s}>
				<g transform={`rotate(${-8 + Math.sin(f * 1.4) * 2})`}>
					<polygon points={pts.join(' ')} fill={c} stroke={INK} strokeWidth={8} strokeLinejoin="round" />
					<text y={28} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill="#fff" stroke={INK} strokeWidth={10} paintOrder="stroke">{text}</text>
				</g>
			</Pop>
		</g>
	);
};

/* four-point stars bursting out: a find, magic, a win, a clean result */
export const Sparkles: React.FC<{f: number; t0: number; x: number; y: number; n?: number; c?: string}> = ({f, t0, x, y, n = 12, c = '#fff3a0'}) => {
	const k = (f - t0) / 36;
	if (k < 0 || k > 1) return null;
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const a = (i / n) * Math.PI * 2 + random('sp' + i);
				const d = 60 + (80 + random('sd' + i) * 160) * (1 - Math.pow(1 - k, 2));
				const sz = (14 + random('ss' + i) * 22) * Math.sin(Math.min(1, k * 1.2) * Math.PI);
				return <path key={i} transform={`translate(${x + Math.cos(a) * d},${y + Math.sin(a) * d}) rotate(${k * 90})`} d={`M0,${-sz} Q${sz * 0.12},${-sz * 0.12} ${sz},0 Q${sz * 0.12},${sz * 0.12} 0,${sz} Q${-sz * 0.12},${sz * 0.12} ${-sz},0 Q${-sz * 0.12},${-sz * 0.12} 0,${-sz} Z`} fill={c} stroke={INK} strokeWidth={2.4} opacity={1 - k * k} />;
			})}
		</g>
	);
};

/* a puff of smoke: landing, a crash, a disappearing act, steam */
export const Smoke: React.FC<{f: number; t0: number; x: number; y: number; s?: number; c?: string}> = ({f, t0, x, y, s = 1, c = '#d9d6e6'}) => {
	const k = (f - t0) / 50;
	if (k < 0 || k > 1) return null;
	return (
		<g opacity={1 - k * k}>
			{Array.from({length: 9}).map((_, i) => {
				const a = (i / 9) * Math.PI * 2;
				const d = (30 + 90 * k) * s;
				return <circle key={i} cx={x + Math.cos(a) * d * 1.3} cy={y + Math.sin(a) * d * 0.55 - k * 90 * s} r={(30 + 50 * k) * s * (0.7 + random('sm' + i) * 0.6)} fill={c} stroke={INK} strokeWidth={3} />;
			})}
		</g>
	);
};

/* confetti over the whole world: victory, a record, a birthday, a solved riddle */
export const Confetti: React.FC<{f: number; t0: number; n?: number}> = ({f, t0, n = 90}) => {
	const k = (f - t0) / 80;
	if (k < 0 || k > 1) return null;
	const cols = ['#ff2540', '#ffd84a', '#3d6fe0', '#52bd80', '#ff8a5b', '#b58cff'];
	return (
		<g opacity={1 - Math.max(0, k - 0.75) * 4}>
			{Array.from({length: n}).map((_, i) => {
				const x = -100 + random('cx' + i) * 2120 + Math.sin(f * 0.15 + i) * 40;
				const y = -80 + (random('cy' + i) * 0.3 + k * (0.9 + random('cv' + i) * 0.5)) * 1300;
				return <rect key={i} x={x} y={y} width={16} height={9} fill={cols[i % 6]} stroke={INK} strokeWidth={1.6} transform={`rotate(${f * (4 + (i % 5) * 3)} ${x} ${y})`} />;
			})}
		</g>
	);
};

/* a bolt of lightning (world) */
export const Lightning: React.FC<{f: number; t0: number; x: number}> = ({f, t0, x}) => {
	if (f < t0 || f > t0 + 10) return null;
	let px = x;
	let py = -80;
	const pts = [[px, py]];
	for (let i = 0; i < 9; i++) {
		px += (random('lx' + i) - 0.5) * 150;
		py += 120;
		pts.push([px, py]);
	}
	const d = pts.map((p) => p.join(',')).join(' ');
	return (
		<g opacity={f < t0 + 4 ? 1 : 0.5}>
			<polyline points={d} fill="none" stroke="#bfe6ff" strokeWidth={26} strokeLinejoin="round" opacity={0.5} />
			<polyline points={d} fill="none" stroke="#fff" strokeWidth={10} strokeLinejoin="round" />
		</g>
	);
};
export const LightningFlash: React.FC<{f: number; t0: number}> = ({f, t0}) => <AbsoluteFill style={{background: '#dff0ff', opacity: Math.max(env(f, t0, 8), 0.7 * env(f, t0 + 9, 10)) * 0.85, pointerEvents: 'none'}} />;

/* screen-level: RGB-split glitch strips + scanlines: tech, a lie, a broken thing, time skip */
export const Glitch: React.FC<{f: number; t0: number; len?: number}> = ({f, t0, len = 14}) => {
	if (f < t0 || f > t0 + len) return null;
	const o = env(f, t0, len);
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: o, mixBlendMode: 'screen'}}>
			{Array.from({length: 9}).map((_, i) => {
				const top = random('gt' + i + f) * 1000;
				const h = 14 + random('gh' + i + f) * 90;
				const dx = (random('gx' + i + f) - 0.5) * 160;
				return <div key={i} style={{position: 'absolute', left: dx, right: -dx, top, height: h, background: ['#00ffe5', '#ff00aa', '#ffee00'][i % 3], opacity: 0.35}} />;
			})}
			<div style={{position: 'absolute', inset: 0, background: 'repeating-linear-gradient(0deg, rgba(0,0,0,.35) 0 2px, transparent 2px 5px)'}} />
		</AbsoluteFill>
	);
};

/* red vignette that beats like a heart: danger, panic, tension */
export const Pulse: React.FC<{f: number; period?: number; c?: string; o?: number}> = ({f, period = 30, c = '255,30,50', o = 0.5}) => {
	const k = Math.pow(Math.max(0, Math.sin((f / period) * Math.PI * 2)), 3);
	return <AbsoluteFill style={{pointerEvents: 'none', background: `radial-gradient(ellipse at 50% 50%, rgba(${c},0) 45%, rgba(${c},${o * (0.35 + 0.65 * k)}) 100%)`}} />;
};

/* weather overlays (continuous) */
export const Rain: React.FC<{f: number; o?: number; n?: number}> = ({f, o = 0.5, n = 110}) => (
	<AbsoluteFill style={{pointerEvents: 'none'}}>
		<svg width="100%" height="100%" viewBox="0 0 1920 1080">
			{Array.from({length: n}).map((_, i) => {
				const x = random('rx' + i) * 2100 - 100;
				const y = ((random('ry' + i) * 1300 + f * (34 + (i % 5) * 7)) % 1300) - 110;
				return <line key={i} x1={x} y1={y} x2={x - 26} y2={y + 80} stroke="#cfe6ff" strokeWidth={2.4} opacity={o * (0.4 + random('ro' + i) * 0.6)} strokeLinecap="round" />;
			})}
		</svg>
	</AbsoluteFill>
);
export const Snow: React.FC<{f: number; o?: number; n?: number}> = ({f, o = 0.9, n = 90}) => (
	<AbsoluteFill style={{pointerEvents: 'none'}}>
		<svg width="100%" height="100%" viewBox="0 0 1920 1080">
			{Array.from({length: n}).map((_, i) => {
				const x = random('nx' + i) * 1920 + Math.sin(f / 30 + i) * 40;
				const y = (random('ny' + i) * 1200 + f * (2 + (i % 4))) % 1200;
				return <circle key={i} cx={x} cy={y - 60} r={2 + (i % 4)} fill="#fff" opacity={o * (0.5 + random('no' + i) * 0.5)} />;
			})}
		</svg>
	</AbsoluteFill>
);

/* emotes above a head: «!», «?», an idea */
export const Exclaim: React.FC<{f: number; t0: number; x: number; y: number; s?: number}> = ({f, t0, x, y, s = 1}) => (
	<Pop t={f - t0} x={x} y={y} s={s}>
		<g transform={`rotate(${Math.sin(f * 0.6) * 6})`}>
			<text textAnchor="middle" y={40} fontFamily={FONT} fontWeight={900} fontSize={140} fill="#ff5a4a" stroke={INK} strokeWidth={10} paintOrder="stroke">!</text>
		</g>
	</Pop>
);
export const Question: React.FC<{f: number; t0: number; x: number; y: number; s?: number}> = ({f, t0, x, y, s = 1}) => (
	<Pop t={f - t0} x={x} y={y} s={s}>
		<g transform={`rotate(${Math.sin(f * 0.5) * 8})`}>
			<text textAnchor="middle" y={40} fontFamily={FONT} fontWeight={900} fontSize={140} fill="#ffd84a" stroke={INK} strokeWidth={10} paintOrder="stroke">?</text>
		</g>
	</Pop>
);
export const Bulb: React.FC<{f: number; t0: number; x: number; y: number; s?: number}> = ({f, t0, x, y, s = 1}) => (
	<Pop t={f - t0} x={x} y={y} s={s}>
		<g>
			{Array.from({length: 7}).map((_, i) => {
				const a = (-70 - i * 33) * (Math.PI / 180);
				return <line key={i} x1={Math.cos(a) * 62} y1={Math.sin(a) * 62 - 6} x2={Math.cos(a) * 92} y2={Math.sin(a) * 92 - 6} stroke="#ffd84a" strokeWidth={7} strokeLinecap="round" opacity={0.6 + 0.4 * Math.sin(f * 0.7 + i)} />;
			})}
			<circle cy={-6} r={44} fill="#fff3a0" stroke={INK} strokeWidth={6} />
			<rect x={-18} y={38} width={36} height={26} rx={6} fill="#c9cfe0" stroke={INK} strokeWidth={5} />
			<path d="M-14,-6 q14,-26 28,0" stroke="#ffb02e" strokeWidth={5} fill="none" />
		</g>
	</Pop>
);
