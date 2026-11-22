import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Svg} from '../engine/camera';
import {Bulb, Confetti, Exclaim, Glitch, ImpactText, Lightning, LightningFlash, Pulse, Question, Rain, Shockwave, Smoke, Snow, SpeedLines, Sparkles, FX_SOUND} from '../kit/fx';
import {FONT} from '../kit/ui';

/* REFERENCE: every effect of the library, 1.5 s each, with the sound it needs.
   Render a still of it (remotion still src/index.ts Fx --frame=70) to see what each looks like. */
const EFFECTS: {name: string; run: (f: number) => React.ReactNode}[] = [
	{name: 'Shockwave', run: (f) => <Shockwave f={f} t0={4} x={960} y={540} />},
	{name: 'ImpactText', run: (f) => <ImpactText f={f} t0={4} x={960} y={540} text="БАХ!" />},
	{name: 'SpeedLines', run: (f) => <SpeedLines f={f} t0={2} t1={44} />},
	{name: 'Sparkles', run: (f) => <Sparkles f={f} t0={4} x={960} y={540} />},
	{name: 'Smoke', run: (f) => <Smoke f={f} t0={4} x={960} y={600} s={1.4} />},
	{name: 'Confetti', run: (f) => <Confetti f={f} t0={2} />},
	{name: 'Lightning', run: (f) => <Lightning f={f} t0={6} x={960} />},
	{name: 'Exclaim', run: (f) => <Exclaim f={f} t0={4} x={960} y={500} />},
	{name: 'Question', run: (f) => <Question f={f} t0={4} x={960} y={500} />},
	{name: 'Bulb', run: (f) => <Bulb f={f} t0={4} x={960} y={500} />},
];
const PER = 45;
export const FxReel: React.FC = () => {
	const gf = useCurrentFrame();
	const i = Math.min(EFFECTS.length + 3, Math.floor(gf / PER));
	const f = gf - i * PER;
	const overlay = i === EFFECTS.length ? <Glitch f={f} t0={2} len={30} /> : i === EFFECTS.length + 1 ? <Pulse f={f} /> : i === EFFECTS.length + 2 ? <Rain f={f} /> : i === EFFECTS.length + 3 ? <Snow f={f} /> : null;
	const name = i < EFFECTS.length ? EFFECTS[i].name : ['Glitch', 'Pulse', 'Rain', 'Snow'][i - EFFECTS.length];
	return (
		<AbsoluteFill style={{background: i === 6 || i === EFFECTS.length + 2 ? '#1a2142' : '#2a3355'}}>
			<Svg>{i < EFFECTS.length ? EFFECTS[i].run(f) : null}</Svg>
			{i === 6 ? <LightningFlash f={f} t0={6} /> : null}
			{overlay}
			<div style={{position: 'absolute', left: 40, top: 30, fontFamily: FONT, fontWeight: 900, fontSize: 56, color: '#fff'}}>{name} <span style={{fontSize: 34, color: '#ffd84a'}}>→ {FX_SOUND[name]}</span></div>
		</AbsoluteFill>
	);
};
export const FX_REEL_FRAMES = PER * (EFFECTS.length + 4);
