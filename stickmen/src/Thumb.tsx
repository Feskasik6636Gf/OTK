import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Actor} from './kit/core';
import {Stage, Layer, Svg, camOn} from './kit/kit';
import {PLACES} from './story/places';
import {FONT} from './kit/ui';
import {ICONS} from './story/icons';
import type {Pose} from './engine/Stickman';

const shock: Pose = {lean: -4, head: 0, armB: [-150, 20], armF: [150, 20], legB: [-6, 0], legF: [6, 0]};
const hold: Pose = {lean: 0, head: 0, armB: [-8, 10], armF: [8, 10], legB: [-4, 0], legF: [4, 0]};

export const Thumb: React.FC = () => {
	const Void = PLACES.void;
	return (
		<AbsoluteFill style={{background: '#12040a'}}>
			<Stage cam={camOn(960, 600, 1.0)} still bg="#12040a" light={false} grain={0.06} vig={0.5}>
				<Layer depth={1.6}>
					<Void f={0} />
				</Layer>
				<Layer depth={1}>
					<Svg>
						<Actor who="heroKid" x={430} floor={960} s={0.8} pose={hold} faceTurn={0.5} expr="wide" lidL={0} lidR={0} blink={0} mouth="open" uid="k" />
						<Actor who="heroKid" x={960} floor={1010} s={1.3} pose={shock} faceTurn={0.3} expr="wide" lidL={0} lidR={0} blink={0} mouth="open" uid="h" />
						<Actor who="heroOld" x={1510} floor={960} s={1.15} pose={hold} faceTurn={0.5} expr="wide" lidL={0} lidR={0} blink={0} mouth="open" uid="o" handItem={ICONS.cane(1.2)} />
						{[['6', 430, 560], ['16', 960, 420], ['83', 1510, 480]].map(([t, x, y]) => (
							<g key={t as string} transform={`translate(${x},${y})`}>
								<rect x={-92} y={-52} width={184} height={104} rx={30} fill="#11142c" stroke="#ffc94a" strokeWidth={6} />
								<text textAnchor="middle" y={26} fontSize={78} fontFamily={FONT} fontWeight={900} fill="#fff">
									{t}
								</text>
							</g>
						))}
					</Svg>
				</Layer>
			</Stage>
			<AbsoluteFill style={{alignItems: 'center', justifyContent: 'flex-start', paddingTop: 36}}>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 140, color: '#fff', letterSpacing: 3, textShadow: '0 8px 0 #b3142a, 0 0 40px rgba(255,35,64,0.8)', WebkitTextStroke: '10px #12060a', paintOrder: 'stroke fill', lineHeight: 1}}>EVERY AGE</div>
				<div style={{fontFamily: FONT, fontWeight: 900, fontSize: 84, color: '#ffc94a', letterSpacing: 2, WebkitTextStroke: '8px #12060a', paintOrder: 'stroke fill', marginTop: 6}}>FOR 100 DAYS</div>
			</AbsoluteFill>
		</AbsoluteFill>
	);
};
