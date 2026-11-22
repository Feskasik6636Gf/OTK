import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {blend, env, gesture, idle, walkTo} from '../kit/actions';
import {Actor, ShotCtx} from '../kit/core';
import {Layer, Stage, Svg, camOn, usePush} from '../kit/kit';
import {WORLD} from '../kit/world';

/* REFERENCE: the world library in one reel (5 places x 5 s). Each place is a living
   background (check the details: leaves, waves, stars, cars, tumbleweed) with the hero and
   a friend who never stand still. Render it to see what "our level" means for locations:
     node tools/render.mjs World   (or: remotion still src/index.ts World out/w.png --frame=75) */
const PER = 150;
const PLAN = ['forest', 'beach', 'moon', 'city', 'desert'];

const Place: React.FC<{id: string; f: number; gf: number}> = ({id, f, gf}) => {
	const w = WORLD.find((x) => x.id === id)!;
	const cam = usePush(camOn(900, 560, 1.12), camOn(1000, 540, 1.3));
	const hero = walkTo(f, 6, 70, 420, 900, 1, 0.34);
	const friend = walkTo(f, 14, 78, -120, 560, 2, 0.34);
	const hp = blend(hero.pose, gesture('wave', hero.pose, env(f, 80, 140, 8, 10), f), 1);
	const fp = gesture('shrug', friend.pose, env(f, 90, 140, 8, 10), f);
	return (
		<ShotCtx.Provider value={{f, gf, dur: PER, start: gf - f, at: () => 0, end: () => 0}}>
			<Stage cam={cam} bg="#101225" light={{x: 20, y: 10, o: 0.25}}>
				<Layer depth={1.6}>{w.make(gf)}</Layer>
				<Layer depth={1}>
					<Svg>
						<Actor who="girl" x={friend.x} floor={900} s={1.05} facing={friend.facing} pose={fp} vx={friend.vx} bob={friend.bob} expr={f > 90 ? 'wide' : 'happy'} mouth={f > 90 ? 'open' : 'smile'} uid={'wf' + id} />
						<Actor who="hero" x={hero.x} floor={900} s={1.15} facing={hero.facing} pose={hp} vx={hero.vx} bob={hero.bob} expr={f > 80 ? 'happy' : 'normal'} mouth={f > 80 ? 'laugh' : 'smirk'} uid={'wh' + id} />
					</Svg>
				</Layer>
			</Stage>
		</ShotCtx.Provider>
	);
};

export const WorldTour: React.FC = () => {
	const gf = useCurrentFrame();
	const i = Math.min(PLAN.length - 1, Math.floor(gf / PER));
	return (
		<AbsoluteFill style={{background: '#000'}}>
			<Place id={PLAN[i]} f={gf - i * PER} gf={gf} />
		</AbsoluteFill>
	);
};
export const WORLD_TOUR_FRAMES = PER * PLAN.length;
