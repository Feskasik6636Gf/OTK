import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Svg} from '../engine/camera';
import {Actor, } from '../kit/core';
import {CrowdRow} from '../kit/kit';
import {Cat} from './critters';
import {LOCS} from './places';
import {FONT} from '../kit/ui';

/* YouTube thumbnail 1920x1080: lion vs 100 men vs Max */
export const Thumb: React.FC = () => (
	<AbsoluteFill style={{background: '#3a0a14'}}>
		{LOCS.studio.far(0)}
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, rgba(255,60,80,0.35) 0%, rgba(0,0,0,0) 60%)'}} />
		<Svg>
			{/* light rays */}
			{Array.from({length: 14}).map((_, i) => (
				<path key={i} d={`M960,640 L${960 + Math.cos((i / 14) * Math.PI * 2) * 2400},${640 + Math.sin((i / 14) * Math.PI * 2) * 2400} L${960 + Math.cos(((i + 0.5) / 14) * Math.PI * 2) * 2400},${640 + Math.sin(((i + 0.5) / 14) * Math.PI * 2) * 2400} Z`} fill="#ff4a5e" opacity={0.07} />
			))}
			{/* crowd of 100 men in the middle */}
			<CrowdRow n={12} x0={800} x1={1330} floor={800} s={0.55} mode="stand" seed="thb2" />
			<CrowdRow n={13} x0={780} x1={1360} floor={880} s={0.7} mode="stand" seed="thb1" />
			{/* lion, roaring, left */}
			<Cat kind="lion" x={330} y={985} s={1.9} f={0} mode="stand" roar={0.95} shadow={false} />
			{/* Max, right, big */}
			<Actor who="max" x={1560} floor={1240} s={3.0} facing={-1} faceTurn={0.5} expr="normal" pose={{lean: 4, head: 6, armB: [-10, 12], armF: [-60, 40], legB: [-4, 0], legF: [4, 0]}} uid="thbmax" />
			{/* big VS discs */}
			<g transform="translate(960,560)">
				<circle r={86} fill="#ffd23a" stroke="#14060c" strokeWidth={12} />
				<text y={30} textAnchor="middle" fontSize={92} fontFamily={FONT} fontWeight={900} fill="#14060c">VS</text>
			</g>
			{/* 100 tag */}
			<g transform="translate(960,330) rotate(-4)">
				<rect x={-250} y={-72} width={500} height={144} rx={36} fill="#14060c" stroke="#8ae0ff" strokeWidth={10} />
				<text y={30} textAnchor="middle" fontSize={110} fontFamily={FONT} fontWeight={900} fill="#fff">100 MEN</text>
			</g>
		</Svg>
		{/* headline */}
		<div style={{position: 'absolute', left: 0, right: 0, bottom: 28, textAlign: 'center', transform: 'rotate(-2deg)'}}>
			<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 190, lineHeight: 1, color: '#ffd23a', WebkitTextStroke: '16px #14060c', paintOrder: 'stroke', textShadow: '0 14px 30px rgba(0,0,0,.6)', letterSpacing: 4}}>WHO SURVIVES?</div>
		</div>
		<div style={{position: 'absolute', left: 36, top: 28, fontFamily: FONT, fontWeight: 900, fontSize: 70, color: '#fff', WebkitTextStroke: '10px #14060c', paintOrder: 'stroke', transform: 'rotate(-3deg)'}}>30 DAYS · AMAZON</div>
	</AbsoluteFill>
);
