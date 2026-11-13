import React from 'react';
import {AbsoluteFill, Easing, interpolate, spring, useVideoConfig} from 'remotion';
import {Bubble} from '../kit/ui';
import {FONT} from '../kit/ui';
import {clamp} from '../kit/kit';
import {hudKeys, valueAt} from './hud';

/* Screen-space graphics: title slams, stat pills, round banners and the HUD. */

export const Slam: React.FC<{t: number; dur: number; text: string; sub?: string; c?: string; y?: number; size?: number; rot?: number; strike?: boolean}> = ({t, dur, text, sub, c = '#ffd23a', y = 60, size = 120, rot = -3, strike}) => {
	const {fps} = useVideoConfig();
	if (t < 0 || t > dur) return null;
	const k = spring({frame: t, fps, config: {damping: 9, stiffness: 190, mass: 0.7}});
	const o = Math.min(interpolate(t, [0, 3], [0, 1], clamp), interpolate(t, [dur - 8, dur], [1, 0], clamp));
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', left: 0, right: 0, top: y, textAlign: 'center', opacity: o, transform: `rotate(${rot}deg) scale(${0.4 + 0.6 * k})`}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1.02, color: c, WebkitTextStroke: '10px #12040a', paintOrder: 'stroke', textShadow: '0 12px 30px rgba(0,0,0,.55)', letterSpacing: 2, textDecoration: strike ? 'line-through' : undefined, textDecorationColor: '#ff2340', textDecorationThickness: '14px'}}>{text}</div>
				{sub ? <div style={{marginTop: 6, fontFamily: FONT, fontWeight: 800, fontSize: size * 0.4, color: '#fff', WebkitTextStroke: '6px #12040a', paintOrder: 'stroke'}}>{sub}</div> : null}
			</div>
		</AbsoluteFill>
	);
};

/* big number with a small label; slides in from a side */
export const Stat: React.FC<{t: number; dur: number; big: string; label?: string; side?: 'l' | 'r' | 'c'; y?: number; c?: string; size?: number}> = ({t, dur, big, label, side = 'r', y = 230, c = '#ffd23a', size = 120}) => {
	const {fps} = useVideoConfig();
	if (t < 0 || t > dur) return null;
	const k = spring({frame: t, fps, config: {damping: 11, stiffness: 150}});
	const o = Math.min(interpolate(t, [0, 4], [0, 1], clamp), interpolate(t, [dur - 8, dur], [1, 0], clamp));
	const dx = side === 'c' ? 0 : (side === 'r' ? 1 : -1) * (1 - k) * 400;
	const pos: React.CSSProperties = side === 'c' ? {left: 0, right: 0, textAlign: 'center'} : side === 'r' ? {right: 70, textAlign: 'right'} : {left: 70, textAlign: 'left'};
	return (
		<AbsoluteFill style={{pointerEvents: 'none'}}>
			<div style={{position: 'absolute', top: y, ...pos, opacity: o, transform: `translateX(${dx}px) scale(${0.85 + 0.15 * k})`}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: size, lineHeight: 1, color: c, WebkitTextStroke: '8px #12040a', paintOrder: 'stroke', textShadow: '0 10px 26px rgba(0,0,0,.5)'}}>{big}</div>
				{label ? <div style={{marginTop: 4, display: 'inline-block', background: 'rgba(12,4,10,.82)', border: `3px solid ${c}`, borderRadius: 16, padding: '6px 22px', fontFamily: FONT, fontWeight: 800, fontSize: size * 0.3, color: '#fff'}}>{label}</div> : null}
			</div>
		</AbsoluteFill>
	);
};

/* count-up stat: number rolls from `from` to `to` */
export const CountUp: React.FC<{t: number; dur: number; from?: number; to: number; roll?: number; label?: string; side?: 'l' | 'r' | 'c'; y?: number; c?: string; size?: number; suffix?: string; fmt?: boolean}> = ({t, dur, from = 0, to, roll = 24, suffix = '', fmt = true, ...rest}) => {
	const v = Math.round(interpolate(t, [4, 4 + roll], [from, to], {...clamp, easing: Easing.out(Easing.cubic)}));
	return <Stat t={t} dur={dur} big={(fmt ? v.toLocaleString('en-US') : String(v)) + suffix} {...rest} />;
};

/* ROUND n banner with the winner */
export const Round: React.FC<{t: number; dur: number; n: number; title: string; winner: string; c?: string}> = ({t, dur, n, title, winner, c = '#ffd23a'}) => {
	const {fps} = useVideoConfig();
	if (t < 0 || t > dur) return null;
	const k = spring({frame: t, fps, config: {damping: 12, stiffness: 140}});
	const k2 = spring({frame: t - 14, fps, config: {damping: 8, stiffness: 200}});
	const o = Math.min(interpolate(t, [0, 3], [0, 1], clamp), interpolate(t, [dur - 8, dur], [1, 0], clamp));
	return (
		<AbsoluteFill style={{pointerEvents: 'none', alignItems: 'center', justifyContent: 'center'}}>
			<div style={{opacity: o, transform: `translateY(${(1 - k) * -120}px) scale(${0.8 + 0.2 * k})`, textAlign: 'center'}}>
				<div style={{display: 'inline-block', background: 'rgba(18,4,10,.9)', border: `6px solid ${c}`, borderRadius: 30, padding: '14px 54px', boxShadow: '0 20px 60px rgba(0,0,0,.6)'}}>
					<div style={{fontFamily: FONT, fontWeight: 800, fontSize: 40, color: '#ff8a98', letterSpacing: 10}}>ROUND {n}</div>
					<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 112, color: '#fff', lineHeight: 1.05}}>{title}</div>
				</div>
				<div style={{marginTop: 18, transform: `scale(${Math.max(0, k2)}) rotate(-4deg)`, display: 'inline-block', background: c, color: '#12040a', fontFamily: FONT, fontWeight: 900, fontSize: 70, padding: '6px 40px', borderRadius: 24}}>{winner}</div>
			</div>
		</AbsoluteFill>
	);
};

/* screen HUD: day, men left and the round score */
export const Hud: React.FC<{f: number}> = ({f}) => {
	const K = hudKeys();
	if (f < K.from || f > K.to) return null;
	const day = valueAt(K.days, f);
	const men = valueAt(K.men, f);
	const sc = valueAt(K.score, f);
	const fadeIn = interpolate(f, [K.from, K.from + 12], [0, 1], clamp);
	const popD = 1 + 0.35 * Math.exp(-Math.max(0, day.ago) / 5);
	const popM = 1 + 0.35 * Math.exp(-Math.max(0, men.ago) / 5);
	const popS = 1 + 0.25 * Math.exp(-Math.max(0, sc.ago) / 5);
	const pill: React.CSSProperties = {background: 'rgba(14,4,10,.78)', border: '3px solid #ff3a52', borderRadius: 18, padding: '4px 18px', fontFamily: FONT, color: '#fff', display: 'flex', alignItems: 'baseline', gap: 10};
	return (
		<AbsoluteFill style={{pointerEvents: 'none', opacity: fadeIn}}>
			<div style={{position: 'absolute', left: 36, top: 30, ...pill, transform: `scale(${popD})`, transformOrigin: 'left top'}}>
				<span style={{fontWeight: 700, fontSize: 24, color: '#ff8a98', letterSpacing: 4}}>DAY</span>
				<span style={{fontWeight: 900, fontSize: 50}}>{day.v}</span>
			</div>
			<div style={{position: 'absolute', right: 36, top: 30, ...pill, transform: `scale(${popM})`, transformOrigin: 'right top'}}>
				<span style={{fontWeight: 700, fontSize: 24, color: '#ff8a98', letterSpacing: 4}}>MEN</span>
				<span style={{fontWeight: 900, fontSize: 50, color: men.v < 50 ? '#ffd23a' : '#fff'}}>{men.v}</span>
			</div>
			<div style={{position: 'absolute', right: 36, top: 104, ...pill, padding: '2px 14px', transform: `scale(${popS})`, transformOrigin: 'right top', fontSize: 22, fontWeight: 800, gap: 16}}>
				<span>LION <b style={{color: '#ffd23a'}}>{sc.v[0]}</b></span>
				<span>MEN <b style={{color: '#ffd23a'}}>{sc.v[1]}</b></span>
				<span>MAX <b style={{color: '#ffd23a'}}>{sc.v[2]}</b></span>
			</div>
		</AbsoluteFill>
	);
};

/* a comic speech bubble with one line of text, in world space (use inside <Svg>) */
export const Say: React.FC<{t: number; x: number; y: number; text: string; w?: number; tail?: [number, number]; size?: number; fill?: string}> = ({t, x, y, text, w, tail = [20, 70], size = 44, fill}) => {
	const ww = w ?? text.length * size * 0.62 + 56;
	return (
		<Bubble x={x} y={y} w={ww} h={size * 1.9} t={t} tail={tail} fill={fill}>
			<text x={0} y={size * 0.34} textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={900} fill="#14151c">
				{text}
			</text>
		</Bubble>
	);
};
