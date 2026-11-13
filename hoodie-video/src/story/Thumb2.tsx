import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Svg} from '../engine/camera';
import {Actor} from '../kit/core';
import {CrowdRow} from '../kit/kit';
import {Cat} from './critters';
import {LOCS} from './places';
import {FONT} from '../kit/ui';

/* Thumbnail v2 — "American style": giant faces, low angle, cold background, warm rim light, glow, grade, grain */
export const Thumb2: React.FC = () => (
	<AbsoluteFill style={{background: '#06121c'}}>
		{/* blurred cold jungle */}
		<AbsoluteFill style={{filter: 'blur(9px) saturate(0.85)', transform: 'scale(1.08)'}}>
			{LOCS.jn.far(30)}
			{LOCS.jn.mid(30)}
		</AbsoluteFill>
		<AbsoluteFill style={{background: 'linear-gradient(100deg, rgba(10,70,110,0.55) 0%, rgba(10,30,60,0.15) 50%, rgba(120,10,30,0.55) 100%)', mixBlendMode: 'color'}} />
		{/* god rays */}
		<Svg>
			{Array.from({length: 9}).map((_, i) => (
				<path key={i} d={`M${700 + i * 70},-80 L${300 + i * 210},1180 L${380 + i * 210},1180 Z`} fill="#bfe6ff" opacity={0.06} />
			))}
		</Svg>
		<AbsoluteFill style={{transform: 'rotate(-3deg) scale(1.06)'}}>
			<Svg>
				{/* small crowd far below, between the giants */}
				<CrowdRow n={9} x0={700} x1={1250} floor={880} s={0.5} mode="panic" seed="thc" dir={-1} t={0} />
				{/* roaring lion, head huge, left */}
				<Cat kind="lion" x={60} y={1120} s={3.7} f={0} mode="stand" roar={1} shadow={false} />
				{/* warm rim glow behind Max */}
				<defs>
					<radialGradient id="maxglow">
						<stop offset="0" stopColor="#ff2340" stopOpacity="0.75" />
						<stop offset="1" stopColor="#ff2340" stopOpacity="0" />
					</radialGradient>
				</defs>
				<circle cx={1500} cy={470} r={470} fill="url(#maxglow)" />
				<Actor who="max" x={1500} floor={1560} s={3.5} facing={-1} faceTurn={0.45} expr="normal" look={[-0.6, 0.1]} pose={{lean: 0, head: -4, armB: [-10, 12], armF: [-70, 40], legB: [-4, 0], legF: [4, 0]}} uid="th2max" />
			</Svg>
		</AbsoluteFill>
		{/* headline */}
		<div style={{zIndex: 5, position: 'absolute', left: 40, right: 40, bottom: 34, textAlign: 'center', transform: 'rotate(-2deg)'}}>
			<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 120, whiteSpace: 'nowrap', lineHeight: 1, color: '#fff', WebkitTextStroke: '15px #0a0206', paintOrder: 'stroke', textShadow: '0 14px 34px rgba(0,0,0,.7)', letterSpacing: 3}}>
				<span style={{color: '#ffd23a'}}>1</span> LION · <span style={{color: '#8ae0ff'}}>100</span> MEN · <span style={{color: '#ff4a62'}}>MAX</span>
			</div>
		</div>
		<div style={{zIndex: 5, position: 'absolute', left: 44, top: 30, fontFamily: FONT, fontWeight: 900, fontSize: 84, color: '#ffd23a', WebkitTextStroke: '12px #0a0206', paintOrder: 'stroke', transform: 'rotate(-3deg)'}}>WHO SURVIVES?</div>
		{/* grade + vignette + grain */}
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.55) 100%)'}} />
		<AbsoluteFill style={{background: 'linear-gradient(to bottom, rgba(255,255,255,0.06), rgba(0,0,0,0.0) 40%)', mixBlendMode: 'soft-light'}} />
	</AbsoluteFill>
);
