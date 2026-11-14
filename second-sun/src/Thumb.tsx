import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Layer, Stage, Svg, camOn} from './kit/kit';
import {AgeBadge, FONT} from './kit/ui';
import {FarHouses, ORANGE_SUN, SkyDome, WHITE_SUN, Yard} from './story/places';
import {Hero, custom, idle} from './story/h';

/* YouTube thumbnail: hero at 2 AM under two suns */
export const Thumb: React.FC = () => (
	<AbsoluteFill>
		<Stage cam={camOn(1080, 520, 1.55)} bg="#2f7fe6" light={{x: 70, y: 10, o: 0.4}} still>
			<Layer depth={4}>
				<SkyDome id="th" mode="blue" f={0} suns={[{x: 1700, y: 180, r: 80, c: WHITE_SUN}, {x: 1420, y: 230, r: 60, c: ORANGE_SUN, glow: 1.6}]} />
			</Layer>
			<Layer depth={1.9}>
				<FarHouses mode="blue" />
			</Layer>
			<Layer depth={1}>
				<Yard mode="blue" f={0} hoop={false} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					<Hero x={1180} s={1.1} badge={false} pose={{...custom('lookUp', idle(0, 1), 1, 0), armF: [150, 10]}} handF="point" look={[0.3, -1]} expr="worried" mouth="smirk" uid="thumb" />
					<AgeBadge x={1180} y={355} value={41} s={0.85} label="DAY" c="#ff8a2a" />
				</Svg>
			</Layer>
		</Stage>
		<div style={{position: 'absolute', left: 70, top: 120, fontFamily: FONT, fontWeight: 900, fontSize: 230, color: '#fff', WebkitTextStroke: '12px #0b0d1e', paintOrder: 'stroke', lineHeight: 1, transform: 'rotate(-4deg)'}}>2:00 AM</div>
		<div style={{position: 'absolute', left: 90, top: 360, fontFamily: FONT, fontWeight: 900, fontSize: 130, color: '#ffd34a', WebkitTextStroke: '9px #0b0d1e', paintOrder: 'stroke', transform: 'rotate(-4deg)'}}>NO NIGHT?!</div>
	</AbsoluteFill>
);
