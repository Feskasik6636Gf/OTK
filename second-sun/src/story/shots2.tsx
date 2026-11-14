import React from 'react';
import {AbsoluteFill, interpolate, random} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Chair} from '../engine/props';
import {env, gesture, idle, walk} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {CrowdRow, Extra, Layer, Sleeper, Stage, Svg, camOn, mixCam, usePush} from '../kit/kit';
import {Bedroom, Blanket, Kitchen, KitchenTable} from '../kit/sets';
import {Board, Bubble, FONT, HAND} from '../kit/ui';
import {Callout} from '../kit/graphics';
import type {ShotDef} from '../kit/coverage';
import {Ball, Bathroom, Beach, Bird, Farm, Hospital, Living, ORANGE_SUN, Owl, Planet, School, Star, Store, Telescope, Tree, Tub, Turtle, WHITE_SUN, Woods} from './places';
import {Burst, FL, Flash, Hero, Inside, Outdoor, Pill, PopText, Punch, QMark, SpaceStage, Zzz, beats, headY, hops, on, path, shake, tw} from './h';

const SUNS_HOT = [
	{x: 1450, y: 160, r: 74, c: WHITE_SUN, glow: 1.3},
	{x: 520, y: 200, r: 42, c: ORANGE_SUN, glow: 1.6},
];

/* a simple thermometer in world space */
const Thermo: React.FC<{x: number; y: number; v: number; s?: number; label?: string}> = ({x, y, v, s = 1, label}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-34} y={-360} width={68} height={380} rx={34} fill="#f4f4f4" stroke="#2a2a3a" strokeWidth={8} />
		<circle cx={0} cy={40} r={56} fill="#e23a2a" stroke="#2a2a3a" strokeWidth={8} />
		<rect x={-16} y={30 - 360 * v} width={32} height={360 * v} rx={16} fill="#e23a2a" />
		{label ? (
			<text x={80} y={30 - 360 * v + 16} fontSize={64} fontFamily={FONT} fontWeight={900} fill="#fff" stroke="#10132a" strokeWidth={10} paintOrder="stroke">
				{label}
			</text>
		) : null}
	</g>
);

/* 063-067: two suns on opposite sides — no real night */
const S063: React.FC = () => {
	const {f, gf, at} = useShot();
	const rot = gf / 24;
	const cam = usePush(camOn(960, 540, 0.95), camOn(960, 540, 1.25));
	return (
		<SpaceStage cam={cam}>
			<Star x={180} y={540} r={110} c={WHITE_SUN} f={gf} id="w63" />
			<Star x={1760} y={540} r={70} c={ORANGE_SUN} f={gf} id="o63" />
			<line x1={300} y1={540} x2={820} y2={540} stroke={WHITE_SUN} strokeWidth={6} strokeDasharray="14 12" opacity={0.6} />
			<line x1={1660} y1={540} x2={1100} y2={540} stroke={ORANGE_SUN} strokeWidth={6} strokeDasharray="14 12" opacity={0.6} />
			<Planet x={960} y={540} r={150} f={rot * 20} />
			<path d="M960,390 A150,150 0 0 0 960,690 Z" fill="#fff8d0" opacity={0.18} />
			<path d="M960,390 A150,150 0 0 1 960,690 Z" fill="#ff8a2a" opacity={0.25} />
			{/* a tiny person riding the rotation */}
			<g transform={`rotate(${(rot * 57) % 360} 960 540)`}>
				<circle cx={960} cy={372} r={10} fill="#000" />
				<rect x={954} y={380} width={12} height={20} fill="#ff2a3c" />
			</g>
			<PopText t={f - at('064') - 20} x={500} y={300} text="SETS" size={50} c="#fff" out={70} />
			<PopText t={f - at('064') - 50} x={1440} y={300} text="RISES" size={50} c="#ff8a2a" out={70} />
			<Pill t={f - at('065') - 4} x={960} y={150} text="NO REAL NIGHT" c="#5ad0ff" size={48} out={at('066') - at('065')} />
			<Pill t={f - at('066') - 4} x={960} y={150} text="A FEW HOURS OF ORANGE EVENING" c="#ff8a2a" size={40} out={at('067') - at('066') - 4} />
			<PopText t={f - at('067') - 2} x={960} y={170} text="LIGHT AGAIN" size={80} />
		</SpaceStage>
	);
};

/* 068: and your body hates it */
const S068: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const cam = usePush(camOn(1500, 620, 1.6), camOn(1600, 610, 2.3));
	const toss = Math.sin(f / 5) * 6;
	return (
		<Stage cam={shake(cam, f, at('068') + 20, 20, 6)} bg="#a9cfe0" light={{x: 50, y: 20, o: 0.5, c: '255,200,120'}}>
			<Layer depth={1.2}>
				<Bedroom f={gf} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					<g transform={`rotate(${toss} 1560 640)`}>
						<Sleeper x={1560} y={640} s={0.9} expr="angry" />
					</g>
				</Svg>
			</Layer>
			<Layer depth={1}>
				<Blanket f={gf} lift={Math.abs(toss) * 2} />
			</Layer>
			<Punch t={f - at('068') - 6} text="YOUR BODY HATES IT" top={80} size={90} c="#ff5a6a" out={dur} />
		</Stage>
	);
};

/* 069-072: the brain clock, melatonin, light blocks it */
const S069: React.FC = () => {
	const {f, gf, at} = useShot();
	const dark = env(f, at('070'), at('072'), 12, 12);
	const block = tw(f, at('072'), at('072') + 20, 0, 1);
	return (
		<Board tint={dark > 0.5 ? '#0a0c24' : '#1a2150'}>
			<g transform={`translate(760,560) scale(${1 + 0.02 * Math.sin(f / 10)})`}>
				<path d="M-260,40 C-300,-160 -120,-280 20,-250 C180,-300 330,-160 290,0 C330,140 160,240 40,210 C-80,260 -260,200 -260,40 Z" fill="#ff9ab8" stroke="#c8507a" strokeWidth={10} />
				<path d="M-150,-120 q60,40 0,90 M40,-180 q-40,60 30,100 M150,-60 q-60,50 10,110 M-60,60 q60,-10 90,60" stroke="#c8507a" strokeWidth={8} fill="none" />
				<g transform="translate(20,-20)" opacity={tw(f, at('069') + 30, at('069') + 50, 0, 1)}>
					<circle r={78} fill="#fff" stroke="#2a2a3a" strokeWidth={8} />
					<line x1={0} y1={0} x2={Math.sin(gf / 10) * 54} y2={-Math.cos(gf / 10) * 54} stroke="#c8102e" strokeWidth={6} strokeLinecap="round" />
					<line x1={0} y1={0} x2={0} y2={-36} stroke="#2a2a3a" strokeWidth={8} strokeLinecap="round" />
				</g>
			</g>
			<Callout f={f} t0={at('069') + 50} t1={at('070')} from={[780, 540]} to={[1300, 300]} text="TINY CLOCK" />
			{/* melatonin bubbles */}
			{Array.from({length: 14}).map((_, i) => {
				const u = ((f - at('070')) / 60 + i / 14) % 1;
				const show = f > at('070') + 10 && f < at('072') + 30;
				return show ? (
					<g key={i} transform={`translate(${900 + i * 50 + Math.sin(u * 6 + i) * 30},${600 - u * 420})`} opacity={(1 - u) * (1 - block)}>
						<circle r={22} fill="#8a7aff" />
						<text y={9} textAnchor="middle" fontSize={24} fontFamily={FONT} fontWeight={900} fill="#fff">
							z
						</text>
					</g>
				) : null;
			})}
			<PopText t={f - at('070') - 50} x={1400} y={200} text="MELATONIN" size={70} c="#a99aff" out={at('072') - at('070') - 40} />
			<PopText t={f - at('071') - 6} x={1400} y={760} text="TIME TO SLEEP" size={56} c="#fff" out={at('072') - at('071')} />
			{block > 0 ? (
				<g>
					<path d={`M1920,0 L${1920 - 900 * block},${560 * block} L${1920 - 860 * block},${640 * block} Z`} fill="#fff6c0" opacity={0.7} />
					<PopText t={f - at('072') - 10} x={1200} y={900} text="LIGHT BLOCKS IT" size={64} c="#ff5a6a" />
					<g opacity={block} stroke="#ff2a3c" strokeWidth={26} strokeLinecap="round">
						<line x1={560} y1={360} x2={960} y2={760} />
						<line x1={960} y1={360} x2={560} y2={760} />
					</g>
				</g>
			) : null}
			<Flash f={f} at={at('072') + 2} c="#fff6c0" />
		</Board>
	);
};

/* 073: don't scroll your phone in bed */
const S073: React.FC = () => {
	const {f, gf, at} = useShot();
	const no = env(f, at('073') + 50, 9999, 8, 1);
	const sc = path(f, [[0, 2300], [at('073') + 40, 1180]], 3, 0.3, 1);
	const cam = usePush(camOn(900, 600, 1.7), camOn(980, 580, 1.35));
	const hp: Pose = {...idle(f, 1), legB: [88, 85], legF: [92, 90], armF: [40, 110], armB: [30, 110], head: 16};
	return (
		<Stage cam={cam} bg="#101225" light={{x: 40, y: 40, o: 0.45, c: '150,200,255'}}>
			<Layer depth={1.2}>
				<Bedroom night f={gf} />
			</Layer>
			<Layer depth={1}>
				<Svg>
					<rect x={700} y={790} width={300} height={100} rx={20} fill="#3a3050" />
					<Hero x={850} seat={780} pose={hp} look={[0.4, 0.8]} expr="sleepy" badge={false} uid="h73" />
					<g transform={`translate(${900},${640})`}>
						<rect x={-24} y={-40} width={48} height={80} rx={8} fill="#1a1a22" />
						<rect x={-20} y={-34} width={40} height={68} rx={4} fill="#9fd8ff" />
						{[0, 1, 2].map((i) => (
							<rect key={i} x={-14} y={-26 + ((i * 22 - f * 2) % 66 + 66) % 66} width={28} height={14} rx={3} fill="#fff" opacity={0.8} />
						))}
					</g>
					<circle cx={880} cy={560} r={160} fill="#9fd8ff" opacity={0.12} />
					<Actor who="scientist" x={sc.x} pose={gesture('stop', sc.pose, no, f)} facing={-1} vx={sc.vx} bob={sc.bob} expr="angry" look={[-0.8, 0]} uid="sc73" />
					{no > 0 ? (
						<g transform={`translate(${sc.x - 170},${520}) scale(${no}) rotate(-6)`}>
							<rect x={-130} y={-50} width={260} height={100} rx={16} fill="#c8102e" />
							<text x={0} y={18} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#fff">
								NO PHONE!
							</text>
						</g>
					) : null}
				</Svg>
			</Layer>
		</Stage>
	);
};

/* 074-076: the whole sky as a phone screen. All night. Every night. */
const S074: React.FC = () => {
	const {f, at, dur} = useShot();
	const k = tw(f, at('074') + 10, at('074') + 40, 0, 1);
	const cam = usePush(camOn(960, 300, 0.85), camOn(960, 500, 1.15));
	return (
		<>
			<Outdoor id="s74" cam={cam} mode="hot" suns={SUNS_HOT} lit={1} yard={{hoop: true}}>
				<g opacity={k}>
					<rect x={160} y={-260} width={1600} height={860} rx={90} fill="none" stroke="#14141c" strokeWidth={60} />
					<rect x={760} y={-240} width={400} height={40} rx={20} fill="#14141c" />
					<text x={300} y={-150} fontSize={44} fontFamily={FONT} fontWeight={800} fill="#14141c">
						3:12 AM
					</text>
					<rect x={1460} y={-180} width={120} height={50} rx={10} fill="none" stroke="#14141c" strokeWidth={6} />
					<rect x={1468} y={-172} width={100} height={34} fill="#14141c" />
				</g>
				<Sleeperless f={f} />
			</Outdoor>
			<Punch t={f - at('075') + 2} text="ALL NIGHT" top={720} c="#fff" out={at('076') - at('075') - 2} />
			<Punch t={f - at('076') + 2} text="EVERY NIGHT" top={720} c="#ff5a6a" out={dur} />
		</>
	);
};
const Sleeperless: React.FC<{f: number}> = ({f}) => (
	<g>
		<rect x={760} y={660} width={240} height={120} fill="#ffcf6a" opacity={0.5 + 0.2 * Math.sin(f / 9)} />
	</g>
);

/* 077-078: Day 9 — blackout curtains sell out everywhere */
const S077: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 520, 1.0), camOn(1000, 560, 1.4));
	const w = path(f, [[at('078'), -200], [at('078') + 50, 900]], 2, 0.3, 1);
	return (
		<>
			<Inside cam={shake(cam, f, at('078') + 10, 16, 8)} set={<Store f={gf} sold={tw(f, at('078'), at('078') + 40, 0, 1)} />} light={{x: 50, y: 10, o: 0.35}}>
				<CrowdRow n={7} x0={-400} x1={900} floor={FL + 20} s={0.95} mode="panic" seed="shop" t={Math.max(0, f - at('078'))} />
				<Hero x={w.x} pose={beats(w.pose, f, at, [['078', 60, 999, 'handsOnHead']])} facing={1} vx={w.vx} bob={w.bob} expr="worried" uid="h77" />
				<PopText t={f - at('078') - 20} x={960} y={420} text="BLACKOUT CURTAINS" size={52} c="#10132a" stroke="#fff" />
			</Inside>
			<Punch t={f - at('077') + 2} text="DAY 9" size={150} c="#ff8a2a" out={at('078') - at('077') + 10} top={300} />
		</>
	);
};

/* 079: people tape aluminium foil over their windows */
const S079: React.FC = () => {
	const {f, gf, at} = useShot();
	const pieces = Array.from({length: 8});
	const cam = usePush(camOn(1300, 470, 1.5), camOn(1440, 420, 1.85));
	const hp = beats(idle(f, 2), f, at, [['079', 0, 999, 'phoneUp']]);
	return (
		<Inside cam={cam} set={<Living f={gf} glow="#fff2c0" />} light={{x: 80, y: 20, o: 0.5}}>
			{pieces.map((_, i) => {
				const k = tw(f, at('079') + 6 + i * 9, at('079') + 14 + i * 9, 0, 1);
				const x = 1250 + (i % 4) * 112;
				const y = 190 + Math.floor(i / 4) * 186;
				return k > 0 ? (
					<g key={i} transform={`translate(${x + 56},${y + 93}) scale(${k}) rotate(${(random('foil' + i) - 0.5) * 6})`}>
						<rect x={-58} y={-95} width={116} height={190} fill="#c8ccd8" />
						<path d="M-50,-80 l30,40 l-20,30 l40,40 M10,-90 l20,60 l-30,50" stroke="#fff" strokeWidth={4} fill="none" opacity={0.7} />
						<rect x={-60} y={-100} width={30} height={14} fill="#e8d8a0" />
					</g>
				) : null;
			})}
			<Hero x={1180} s={1.05} pose={{...hp, armF: [hp.armF[0] + Math.sin(f / 3) * 10, hp.armF[1]]}} facing={1} look={[0.6, -0.6]} uid="h79" />
			<PopText t={f - at('079') - 30} x={1470} y={150} text="SCRITCH" size={44} c="#fff" out={40} />
		</Inside>
	);
};

/* 080: dad sleeps in the bathtub with a towel over his head */
const S080: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(860, 640, 1.1), camOn(760, 660, 1.6));
	return (
		<Inside cam={cam} set={<Bathroom f={gf} />} light={{x: 80, y: 20, o: 0.4}}>
			<g transform={`translate(860,690) rotate(-78)`}>
				<Actor who="dad" x={0} seat={0} s={1} pose={{...idle(f, 4), legB: [80, 20], legF: [84, 22]}} faceTurn={0.2} expr="sleepy" shadow={false} uid="d80" />
			</g>
			<Tub />
			<path d={`M640,${590 + Math.sin(f / 20) * 3} q100,-60 200,0 l10,80 q-110,30 -220,0 Z`} fill="#3ac0c0" />
			<path d="M650,600 l0,70 M700,590 l0,80 M760,588 l0,80 M820,594 l0,74" stroke="#2a9a9a" strokeWidth={4} />
			<Zzz f={f} x={820} y={520} s={1.3} c="#2a4a6a" />
			<Pill t={f - at('080') - 40} x={1100} y={420} text="DAD" c="#4a9a4a" />
		</Inside>
	);
};

/* 081: Sam awake for 22 hours, then asleep in his cereal */
const S081: React.FC = () => {
	const {f, at, dur} = useShot();
	const hrs = Math.floor(tw(f, at('081'), at('081') + 70, 0, 22));
	const fall = tw(f, at('081') + 80, at('081') + 92, 0, 1);
	const cam = mixCam(camOn(960, 560, 1.5), camOn(960, 640, 2.1), tw(f, at('081') + 76, at('081') + 90, 0, 1));
	const sp: Pose = {...idle(f, 5), legB: [88, 85], legF: [92, 90], armF: [60, 60], armB: [50, 60], head: 40 * fall, lean: 34 * fall};
	return (
		<Inside cam={shake(cam, f, at('081') + 92, 10, 10)} set={<Kitchen />} light={{x: 60, y: 20, o: 0.4}}>
			<Chair x={900} y={800} />
			<Actor who="sam" x={900} seat={790 - 157 * 0.78 + 157 * 0.78} s={0.78} pose={sp} expr={fall > 0.5 ? 'sleepy' : 'wide'} lidL={fall < 0.5 ? Math.abs(Math.sin(f / 7)) * 0.5 : 0} look={[0.2, 0.2]} uid="sam81" />
			<KitchenTableX />
			<g transform="translate(1040,680)">
				<path d="M-70,0 L70,0 Q60,56 0,58 Q-60,56 -70,0 Z" fill="#f2f2f2" />
				{Array.from({length: 8}).map((_, i) => (
					<circle key={i} cx={-50 + i * 14} cy={-4 - (fall >= 1 && f < at('081') + 110 ? (f - at('081') - 92) * (3 + (i % 3)) * Math.sin(i) : 0)} r={7} fill="#f2b21c" />
				))}
			</g>
			<Pill t={f - at('081') - 6} x={600} y={300} text={`AWAKE: ${hrs} H`} c="#5ad0ff" size={44} out={at('081') + 90 - (at('081') + 6)} />
			{fall >= 1 ? <PopText t={f - at('081') - 92} x={1040} y={520} text="SPLOSH!" size={70} c="#fff" /> : null}
			{fall >= 1 ? <Zzz f={f} x={1080} y={540} /> : null}
			{dur < 0 ? null : null}
		</Inside>
	);
};
const KitchenTableX: React.FC = () => (
	<g>
		<rect x={760} y={680} width={520} height={22} rx={6} fill="#b98a5a" />
		<rect x={790} y={700} width={16} height={190} fill="#8a6a44" />
		<rect x={1230} y={700} width={16} height={190} fill="#8a6a44" />
	</g>
);

/* 082-083: mom is a nurse; the hospital is full of sleepless people */
const S082: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const w = path(f, [[0, -200], [60, 400], [at('083') + 10, 400], [at('083') + 90, 1300]], 4, 0.34, 1);
	const cam = camOn(Math.max(700, Math.min(1300, w.x + 120)), 560, 1.3);
	return (
		<Inside cam={cam} set={<Hospital f={gf} />} light={{x: 50, y: 10, o: 0.35}}>
			{[-30, 650, 1330].map((x, i) => (
				<g key={x} transform={`translate(${x + 60},${670}) rotate(-84)`}>
					<Extra i={i + 70} x={0} floor={157} s={0.8} seed="pat" expr="sleepy" pose={idle(f, i)} />
				</g>
			))}
			<Actor who="mom" x={w.x} pose={beats(w.pose, f, at, [['082', 64, 50, 'wave']])} facing={w.facing} vx={w.vx} bob={w.bob} look={[0.6, 0]} uid="mom82" />
			<Pill t={f - at('082') - 30} x={400} y={250} text="MOM • NURSE" c="#3fbfb0" out={at('083') - at('082')} />
			<PopText t={f - at('083') - 20} x={960} y={300} text="NO SLEEP FOR DAYS" size={60} c="#fff" />
			{dur < 0 ? null : null}
		</Inside>
	);
};

/* 084-085: car crashes up, tempers up */
const S084: React.FC = () => {
	const {f, at} = useShot();
	const b1 = tw(f, at('084') + 6, at('084') + 40, 0, 1);
	const b2 = tw(f, at('085') + 2, at('085') + 30, 0, 1);
	return (
		<Board tint="#2a1030">
			{[[560, b1, '#ff8a2a', 'CAR CRASHES'], [1360, b2, '#ff2a3c', 'TEMPERS']].map(([x, b, c, t], i) => (
				<g key={i}>
					<rect x={(x as number) - 150} y={860 - 560 * (b as number)} width={300} height={560 * (b as number)} rx={16} fill={c as string} />
					<path d={`M${x},${780 - 560 * (b as number)} l-70,90 l140,0 Z`} fill="#fff" opacity={b as number} />
					<text x={x as number} y={960} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill="#fff">
						{t as string}
					</text>
				</g>
			))}
			<PopText t={f - at('084') - 30} x={560} y={200} text="UP" size={90} c="#ff8a2a" />
			<PopText t={f - at('085') - 24} x={1360} y={200} text="UP" size={90} c="#ff2a3c" />
		</Board>
	);
};

/* 086-087: everyone is tired, all the time */
const S086: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 560, 1.0), camOn(960, 600, 1.4));
	return (
		<Outdoor id="s86" cam={cam} mode="hot" suns={SUNS_HOT} yard={{hoop: false}}>
			{Array.from({length: 7}).map((_, i) => {
				const x = 200 + i * 250;
				const yawn = env(f, at('086') + i * 9, at('086') + i * 9 + 50, 8, 8);
				const p = gesture('facepalm', {...idle(f, i), lean: 8 + Math.sin(f / 20 + i) * 4, head: 18}, env(f, at('087') + i * 5, 9999, 8, 1), f);
				return i === 3 ? <Hero key={i} x={x} pose={p} expr="sleepy" mouth={yawn > 0.5 ? 'open' : 'flat'} armOver uid="h86" /> : <Extra key={i} i={i + 90} x={x} floor={FL + (i % 2) * 14} s={0.95} seed="tired" pose={p} expr="sleepy" />;
			})}
			<Zzz f={f} x={300} y={300} />
			<Zzz f={f + 20} x={1500} y={320} />
			<PopText t={f - at('087') - 6} x={960} y={200} text="ALL. THE. TIME." size={84} c="#fff" />
		</Outdoor>
	);
};

/* 088-089: animals get confused; birds sing at 3 am */
const S088: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(820, 420, 1.2), camOn(820, 380, 1.6));
	return (
		<Outdoor id="s88" cam={cam} mode="gold" suns={SUNS_HOT} houses={false} yard={false} mid={<Woods f={gf} mode="gold" />}>
			{[620, 760, 900, 1040].map((x, i) => (
				<g key={x} transform={`translate(${x},${385 - Math.abs(Math.sin(f / 6 + i)) * 6})`}>
					<ellipse cx={0} cy={-20} rx={30} ry={24} fill={['#5ad0ff', '#ff8a2a', '#ffd34a', '#9ff0b0'][i]} />
					<circle cx={22} cy={-40} r={16} fill={['#5ad0ff', '#ff8a2a', '#ffd34a', '#9ff0b0'][i]} />
					<circle cx={28} cy={-44} r={4} fill="#111" />
					<path d={`M36,-40 l16,${-4 - Math.abs(Math.sin(f / 3 + i)) * 6} l-16,10 Z`} fill="#f2b21c" />
				</g>
			))}
			{Array.from({length: 10}).map((_, i) => (
				<text key={i} x={700 + i * 50 + Math.sin(f / 9 + i) * 30} y={340 - ((f * 2.5 + i * 30) % 260)} fontSize={44} fill="#fff" opacity={0.85}>
					♪
				</text>
			))}
			<Pill t={f - at('089') - 4} x={1300} y={200} text="3:00 AM" c="#5ad0ff" size={50} />
			<QMark t={f - at('088') - 20} x={1400} y={500} s={0.6} />
		</Outdoor>
	);
};

/* 090: bats don't come out: no dark to hunt in */
const S090: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(820, 520, 1.6), camOn(820, 500, 2.0));
	return (
		<Outdoor id="s90" cam={cam} mode="gold" suns={SUNS_HOT} houses={false} yard={false} mid={<Woods f={gf} mode="gold" />}>
			{[640, 780, 920].map((x, i) => (
				<g key={x} transform={`translate(${x},${420}) rotate(${Math.sin(f / 15 + i) * 6})`}>
					<line x1={0} y1={0} x2={0} y2={20} stroke="#2a2a2a" strokeWidth={4} />
					<path d="M-40,30 q20,60 40,70 q20,-10 40,-70 q-40,20 -80,0 Z" fill="#2a2a3a" />
					<circle cx={0} cy={110} r={22} fill="#2a2a3a" />
					<path d="M-14,130 l6,10 l6,-10 M2,130 l6,10 l6,-10" fill="#2a2a3a" />
					<path d="M-10,108 l8,4 M10,108 l-8,4" stroke="#fff" strokeWidth={3} />
					<circle cx={-8} cy={116} r={3} fill="#fff" />
					<circle cx={8} cy={116} r={3} fill="#fff" />
				</g>
			))}
			<PopText t={f - at('090') - 30} x={780} y={760} text="NO DARK = NO HUNT" size={56} c="#fff" />
		</Outdoor>
	);
};

/* 091: owls blinking, waiting for a night that never comes */
const S091: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(800, 340, 1.5), camOn(820, 330, 2.0));
	return (
		<Outdoor id="s91" cam={cam} mode="gold" suns={SUNS_HOT} houses={false} yard={false} mid={<Woods f={gf} mode="gold" />}>
			{[700, 940].map((x, i) => {
				const t = (f + i * 13) % 50;
				const blink = t < 6 ? Math.sin((t / 6) * Math.PI) : 0;
				return <Owl key={x} x={x} y={410} s={0.9} blink={blink} look={Math.sin(f / 30 + i)} />;
			})}
			<Bubble x={1220} y={220} w={260} h={110} t={f - at('091') - 40} thought tail={[-140, 120]}>
				<circle cx={-60} cy={0} r={30} fill="#1a2350" />
				<circle cx={-48} cy={-8} r={24} fill="#fbf8ef" />
				<text x={40} y={14} textAnchor="middle" fontSize={40} fontFamily={FONT} fontWeight={900} fill="#222">
					…?
				</text>
			</Bubble>
		</Outdoor>
	);
};

/* 092-095: baby turtles hatch and crawl to the brightest horizon — the wrong way */
const S092: React.FC = () => {
	const {f, gf, at} = useShot();
	const wrong = f > at('094');
	const cam = mixCam(camOn(960, 860, 1.6), camOn(960, 820, 1.35), tw(f, at('093'), at('093') + 40, 0, 1));
	return (
		<Outdoor
			id="s92"
			cam={cam}
			mode="dusk"
			houses={false}
			yard={false}
			suns={[{x: 960, y: 640, r: 40, c: WHITE_SUN, glow: 0.6}, ...(wrong ? [{x: 1700, y: 760 - 140 * tw(f, at('094'), at('094') + 40, 0, 1), r: 46, c: ORANGE_SUN, glow: 2}] : [])]}
			mid={<Beach f={gf} mode="dusk" />}
		>
			{wrong ? <path d="M1300,860 q200,-90 600,-60 L2600,800 L2600,1300 L1300,1300 Z" fill="#c89a6a" /> : null}
			<ellipse cx={960} cy={1000} rx={120} ry={30} fill="#a07a50" />
			{Array.from({length: 14}).map((_, i) => {
				const hatch = tw(f, at('092') + 10 + i * 3, at('092') + 20 + i * 3, 0, 1);
				const go = Math.max(0, f - at('093') - i * 2);
				const turn = wrong ? tw(f, at('094') + 30, at('095') + 10, 0, 1) : 0;
				const toSea = Math.min(go * 1.4, 120) * (1 - turn);
				const away = Math.max(0, f - at('095')) * 2.5 * turn;
				const bx = 900 + (i % 7) * 22 - 60 + (i % 3) * 4;
				const by = 1000 + Math.floor(i / 7) * 16;
				return hatch > 0 ? <Turtle key={i} x={bx + (i - 7) * toSea * 0.12 + away * (0.8 + (i % 4) * 0.2)} y={by - toSea + away * 0.1} s={0.95 * hatch} f={gf} dir={turn > 0.5 ? 1 : i % 2 ? 1 : -1} seed={i} /> : null;
			})}
			{f > at('092') && f < at('094') ? <PopText t={f - at('092') - 30} x={960} y={600} text="HATCH!" size={60} c="#9ff0b0" out={60} /> : null}
			<Callout f={f} t0={at('093') + 30} t1={at('094')} from={[960, 640]} to={[1300, 420]} text="BRIGHTEST = OCEAN" c="#5ad0ff" />
			<Callout f={f} t0={at('094') + 40} t1={9999} from={[1700, 650]} to={[1350, 420]} text="ORANGE SUN" c="#ff8a2a" />
			{f > at('095') ? <PopText t={f - at('095') - 10} x={960} y={300} text="WRONG WAY!" size={84} c="#ff5a6a" /> : null}
		</Outdoor>
	);
};

/* 096-098: volunteers carry them by hand; you and Nia carry 400 in one night */
const S096: React.FC = () => {
	const {f, gf, at} = useShot();
	const n = Math.floor(tw(f, at('098'), at('098') + 70, 1, 400));
	const loop = (seed: number) => {
		const t = (f + seed * 40) % 120;
		return t < 60 ? {x: 1300 - t * 9, dir: -1 as const, carry: 1} : {x: 760 + (t - 60) * 9, dir: 1 as const, carry: 0};
	};
	const h = loop(0);
	const n2 = loop(1);
	const cam = usePush(camOn(1000, 560, 1.15), camOn(980, 560, 1.4));
	const mk = (L: ReturnType<typeof loop>, seed: number) => {
		const p = walk(f * 0.36 + seed);
		return L.carry ? {...p, armF: [62, 40] as [number, number], armB: [56, 46] as [number, number]} : p;
	};
	return (
		<Outdoor id="s96" cam={cam} mode="orange" houses={false} yard={false} suns={[{x: 1600, y: 260, r: 40, c: ORANGE_SUN, glow: 1.8}]} mid={<Beach f={gf} mode="orange" />}>
			<Extra i={11} x={300 + Math.sin(f / 30) * 40} floor={FL - 10} s={0.8} seed="vol" pose={{...walk(f * 0.3), armF: [62, 40], armB: [56, 46]}} facing={-1} />
			<Extra i={13} x={1600 - Math.sin(f / 30) * 40} floor={FL - 6} s={0.8} seed="vol" pose={{...walk(f * 0.3 + 2), armF: [62, 40], armB: [56, 46]}} facing={-1} />
			<Hero x={h.x} pose={mk(h, 0)} facing={h.dir} bob={Math.abs(Math.sin(f * 0.36)) * 4} look={[0.5, 0.3]} uid="h96" />
			{h.carry ? <Turtle x={h.x - 60} y={FL - 150} s={0.6} f={gf} dir={-1} /> : null}
			{f > at('097') - 10 ? <Actor who="nia" x={n2.x + 60} pose={mk(n2, 2)} facing={n2.dir} bob={Math.abs(Math.sin(f * 0.36 + 2)) * 4} mouth="smile" uid="nia96" /> : null}
			{f > at('097') - 10 && n2.carry ? <Turtle x={n2.x} y={FL - 150} s={0.6} f={gf} dir={-1} /> : null}
			<Pill t={f - at('097') - 10} x={n2.x + 60} y={headY() - 90} text="NIA" c="#9b5cf6" out={at('098') - at('097')} />
			{f > at('098') ? <PopText t={0} x={960} y={220} text={`${n} TURTLES`} size={90} c="#9ff0b0" rot={-3} /> : null}
			<PopText t={f - at('096') - 20} x={960} y={200} text="BY HAND" size={70} c="#fff" out={at('097') - at('096') - 10} />
		</Outdoor>
	);
};

/* 099-103: plants measure the night */
const S099: React.FC = () => {
	const {f, at} = useShot();
	let len = 0.5;
	if (f > at('101')) len = tw(f, at('101'), at('101') + 14, 0.5, 0.25);
	if (f > at('102')) len = tw(f, at('102'), at('102') + 14, 0.25, 0.85);
	if (f > at('103')) len = tw(f, at('103'), at('103') + 30, 0.85, 0);
	const flower = tw(f, at('099') + 10, at('100'), 0, 1);
	return (
		<Board tint="#13301e">
			<g transform={`translate(360,760) scale(${flower})`}>
				<path d="M0,0 q-10,-160 0,-260" stroke="#3a8a3a" strokeWidth={14} fill="none" />
				<ellipse cx={-50} cy={-120} rx={50} ry={20} fill="#4ab04a" transform="rotate(-30 -50 -120)" />
				{Array.from({length: 8}).map((_, i) => (
					<ellipse key={i} cx={Math.cos((i / 8) * Math.PI * 2) * 44} cy={-260 + Math.sin((i / 8) * Math.PI * 2) * 44} rx={30} ry={18} fill="#ff9ab8" transform={`rotate(${i * 45} ${Math.cos((i / 8) * Math.PI * 2) * 44} ${-260 + Math.sin((i / 8) * Math.PI * 2) * 44})`} />
				))}
				<circle cx={0} cy={-260} r={30} fill="#ffd34a" />
				<g transform={`translate(0,-260)`}>
					<circle cx={-10} cy={-4} r={4} fill="#5a3a1a" />
					<circle cx={10} cy={-4} r={4} fill="#5a3a1a" />
					<path d="M-8,8 q8,6 16,0" stroke="#5a3a1a" strokeWidth={3} fill="none" />
				</g>
			</g>
			<text x={1180} y={300} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#fff">
				NIGHT LENGTH
			</text>
			<rect x={760} y={380} width={840} height={110} rx={55} fill="#0a1020" stroke="#5a6aa0" strokeWidth={6} />
			<rect x={770} y={390} width={820 * len} height={90} rx={45} fill="#3a4aa0" />
			{Array.from({length: 12}).map((_, i) => (
				<circle key={i} cx={800 + i * 66} cy={435} r={4} fill="#fff" opacity={i / 12 < len ? 0.9 : 0} />
			))}
			<PopText t={f - at('101') - 6} x={960} y={720} text="SHORT = ☀ SUMMER" size={64} c="#ffd34a" out={at('102') - at('101') - 4} />
			<PopText t={f - at('102') - 6} x={1180} y={720} text="LONG = ❄ WINTER" size={64} c="#9fd8ff" out={at('103') - at('102') - 4} />
			<PopText t={f - at('103') - 26} x={1180} y={720} text="NO NIGHTS AT ALL" size={70} c="#ff5a6a" />
			<PopText t={f - at('100') - 40} x={1180} y={200} text="HOW LONG IS THE NIGHT?" size={44} c="#9ff0b0" out={at('101') - at('100') - 40} />
		</Board>
	);
};

/* 104-106: wheat flowers at the wrong time; apple trees bloom in autumn; farmers stare */
const S104: React.FC = () => {
	const {f, gf, at} = useShot();
	const bloom = tw(f, at('104') + 10, at('104') + 50, 0, 1);
	const cam = mixCam(camOn(700, 760, 1.4), camOn(1100, 600, 1.2), tw(f, at('105'), at('105') + 30, 0, 1));
	const fp = beats(idle(f, 4), f, at, [['106', 30, 999, 'scratch']]);
	return (
		<Outdoor id="s104" cam={cam} mode="hot" suns={SUNS_HOT} houses={false} yard={false} mid={<Farm f={gf} mode="hot" bloom={bloom} />}>
			<Tree x={1200} y={FL} s={0.9} c="#c8803a" f={gf} bloom={tw(f, at('105'), at('105') + 30, 0, 1)} />
			<Tree x={1500} y={FL - 20} s={0.75} c="#c8603a" f={gf} bloom={tw(f, at('105') + 10, at('105') + 40, 0, 1)} />
			{Array.from({length: 10}).map((_, i) => {
				const u = ((f / 80 + i / 10) % 1);
				return f > at('105') ? <ellipse key={i} cx={1100 + i * 50 + Math.sin(u * 8 + i) * 40} cy={600 + u * 300} rx={12} ry={6} fill="#d8602a" transform={`rotate(${u * 300})`} /> : null;
			})}
			<Actor who="farmer" x={820} s={1} pose={fp} facing={1} look={[0.8, -0.3]} expr="worried" uid="fa104" />
			<Pill t={f - at('104') - 30} x={500} y={500} text="WRONG TIME" c="#ffd34a" out={at('105') - at('104')} />
			<Pill t={f - at('105') - 20} x={1350} y={260} text="BLOOMING IN AUTUMN?" c="#ff9ab8" out={at('106') - at('105')} />
			<QMark t={f - at('106') - 40} x={960} y={420} s={0.7} />
		</Outdoor>
	);
};

/* 107-108: then comes the heat — Day 20 */
const S107: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const cam = usePush(camOn(960, 520, 1.0), camOn(960, 560, 1.4));
	const hp = beats(idle(f, 3), f, at, [['107', 10, 999, 'touchFace']]);
	return (
		<>
			<Outdoor id="s107" cam={shake(cam, f, at('107') + 4, 18, 6)} mode="hot" suns={SUNS_HOT} yard={{hoop: true}}>
				<Hero x={960} s={1.05} pose={hp} armOver expr="sleepy" mouth="open" uid="h107" />
				{Array.from({length: 6}).map((_, i) => (
					<path key={i} d={`M${700 + i * 100},${880 - ((f * 3 + i * 40) % 300)} q20,-20 0,-40 q-20,-20 0,-40`} stroke="#fff" strokeWidth={5} fill="none" opacity={0.35} />
				))}
				<circle cx={1010} cy={headY(1.05) + 10} r={7} fill="#7ad0ff" transform={`translate(0,${(f % 24) * 3})`} opacity={1 - (f % 24) / 24} />
			</Outdoor>
			<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 30%, rgba(255,120,40,0) 30%, rgba(255,90,20,0.35) 100%)', pointerEvents: 'none'}} />
			<Punch t={f - at('107') + 2} text="THE HEAT" top={100} c="#ff5a3a" out={at('108') - at('107') - 2} />
			<Punch t={f - at('108') + 2} text="DAY 20" top={100} c="#ff8a2a" size={140} out={dur} />
		</>
	);
};

/* 109-111: smaller sun, but more sunlight than ever; balanced on a knife's edge */
const S109: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = mixCam(camOn(960, 540, 1.0), camOn(960, 600, 1.35), tw(f, at('111'), at('111') + 20, 0, 1));
	const knife = f > at('111');
	const tip = knife ? Math.sin(f / 9) * 8 : 0;
	return (
		<SpaceStage cam={cam}>
			{!knife ? (
				<>
					<Star x={420} y={500} r={140} c={WHITE_SUN} f={gf} id="w109" />
					<Star x={1500} y={500} r={70} c={ORANGE_SUN} f={gf} id="o109" />
					<Pill t={f - at('109') - 10} x={1500} y={330} text="SMALLER" c="#ff8a2a" out={at('110') - at('109')} />
					{f > at('110')
						? Array.from({length: 16}).map((_, i) => {
								const u = ((f - at('110')) / 30 + i / 8) % 1;
								const fromL = i % 2 === 0;
								const sx = fromL ? 560 : 1430;
								return <line key={i} x1={sx + (960 - sx) * u} y1={500 + ((i % 8) - 4) * 30 * (1 - u)} x2={sx + (960 - sx) * Math.min(1, u + 0.12)} y2={500 + ((i % 8) - 4) * 30 * (1 - u)} stroke={fromL ? '#fff6c0' : ORANGE_SUN} strokeWidth={8} strokeLinecap="round" />;
							})
						: null}
					<Planet x={960} y={500} r={80} f={gf} />
					<PopText t={f - at('110') - 30} x={960} y={860} text="MORE SUNLIGHT THAN EVER" size={60} />
				</>
			) : (
				<g transform={`rotate(${tip} 960 700)`}>
					<path d="M640,1100 L960,700 L1280,1100 Z" fill="#c8ccd8" />
					<path d="M960,700 L1280,1100 L1120,1100 Z" fill="#9aa0b0" />
					<Planet x={960} y={590} r={110} f={gf} />
					<PopText t={f - at('111') - 20} x={960} y={430} text="KNIFE'S EDGE" size={80} c="#ff5a6a" rot={-tip} />
				</g>
			)}
		</SpaceStage>
	);
};

/* 112-117: a fact: our sun brightens; +10% in a billion years could boil the oceans */
const S112: React.FC = () => {
	const {f, at} = useShot();
	const prog = tw(f, at('114'), at('114') + 80, 0, 1);
	const boil = tw(f, at('115'), at('115') + 60, 0, 1);
	return (
		<Board tint="#2a1a10">
			<PopText t={f - at('112') - 2} x={960} y={150} text="FACT" size={100} c="#ffd34a" out={at('113') - at('112') + 20} />
			<text x={260} y={300} fontSize={40} fontFamily={FONT} fontWeight={800} fill="#fff" opacity={tw(f, at('113'), at('113') + 10, 0, 1)}>
				OUR SUN IS SLOWLY GETTING BRIGHTER
			</text>
			<line x1={260} y1={560} x2={1660} y2={560} stroke="#fff" strokeWidth={6} opacity={tw(f, at('113'), at('113') + 10, 0, 1)} />
			<text x={260} y={630} fontSize={36} fontFamily={FONT} fill="#aab3d6">
				TODAY
			</text>
			<text x={1660} y={630} textAnchor="end" fontSize={36} fontFamily={FONT} fill="#aab3d6">
				+1 BILLION YEARS
			</text>
			<g transform={`translate(${260 + 1400 * prog},470)`}>
				<circle r={60 + 12 * prog} fill={WHITE_SUN} opacity={0.3} />
				<circle r={44 + 8 * prog} fill={WHITE_SUN} />
			</g>
			<PopText t={f - at('114') - 70} x={1450} y={400} text="+10%" size={90} c="#ff8a2a" />
			{boil > 0 ? (
				<g>
					<path d={`M200,1000 ${Array.from({length: 18}).map((_, k) => `q50,${(k % 2 ? 1 : -1) * (10 + 10 * boil)} 100,0`).join(' ')} L2000,1080 L200,1080 Z`} fill="#2a8ad8" transform={`translate(0,${-40 * boil})`} />
					{Array.from({length: 16}).map((_, i) => {
						const u = ((f / 20 + i / 16) % 1);
						return <circle key={i} cx={260 + i * 100} cy={960 - u * 260} r={8 + 8 * u} fill="#fff" opacity={(1 - u) * 0.6 * boil} />;
					})}
					<PopText t={f - at('115') - 30} x={960} y={780} text="OCEANS BOIL AWAY" size={64} c="#7ad0ff" />
				</g>
			) : null}
			{f > at('116') ? (
				<AbsoluteFill style={{background: 'rgba(10,8,20,0.75)'}}>
					<Punch t={f - at('116')} text="10%" size={260} top={300} c="#ff8a2a" out={9999} sub={f > at('117') ? "THAT'S ALL IT TAKES" : undefined} />
				</AbsoluteFill>
			) : null}
		</Board>
	);
};

/* 118-121: way more than 10% — oceans heat slowly, land heats fast */
const S118: React.FC = () => {
	const {f, at} = useShot();
	const extra = tw(f, at('118') + 6, at('118') + 40, 0, 1);
	const sea = tw(f, at('120'), at('121') + 90, 0, 0.25);
	const land = tw(f, at('121'), at('121') + 30, 0, 0.9);
	const two = f > at('119') + 10;
	return (
		<Board tint="#2a1a10">
			{!two ? (
				<g>
					<rect x={300} y={480} width={1320} height={120} rx={60} fill="#0a1020" stroke="#5a6aa0" strokeWidth={6} />
					<rect x={310} y={490} width={1300 * (0.12 + 0.75 * extra)} height={100} rx={50} fill="#ff5a3a" />
					<line x1={310 + 1300 * 0.12} y1={440} x2={310 + 1300 * 0.12} y2={640} stroke="#fff" strokeWidth={6} />
					<text x={310 + 1300 * 0.12} y={420} textAnchor="middle" fontSize={40} fontFamily={FONT} fontWeight={800} fill="#fff">
						10%
					</text>
					<PopText t={f - at('118') - 30} x={1300} y={300} text="WAY MORE" size={84} c="#ff5a3a" />
					<PopText t={f - at('119') - 2} x={960} y={820} text="NOT ALL AT ONCE" size={64} c="#fff" />
				</g>
			) : (
				<g>
					{[[620, sea, '#2a8ad8', 'OCEANS: SLOW'], [1300, land, '#c8803a', 'LAND: FAST']].map(([x, v, c, t], i) => (
						<g key={i} transform={`translate(${x},880)`}>
							<rect x={-40} y={-560} width={80} height={580} rx={40} fill="#f4f4f4" stroke="#2a2a3a" strokeWidth={8} />
							<circle cx={0} cy={40} r={64} fill={c as string} stroke="#2a2a3a" strokeWidth={8} />
							<rect x={-22} y={30 - 560 * (v as number)} width={44} height={560 * (v as number)} rx={22} fill={c as string} />
							<text x={0} y={180} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#fff">
								{t as string}
							</text>
						</g>
					))}
				</g>
			)}
		</Board>
	);
};

/* 122-123: summer used to mean 30 degrees. Now it's 42. */
const S122: React.FC = () => {
	const {f, at} = useShot();
	const v = f < at('123') ? tw(f, at('122') + 10, at('122') + 40, 0, 30) : tw(f, at('123'), at('123') + 20, 30, 42);
	const cam = usePush(camOn(960, 560, 1.1), camOn(900, 560, 1.4));
	const fan = env(f, at('123') + 10, 9999, 8, 1);
	const hp = {...idle(f, 2), armF: [100 + Math.sin(f / 1.6) * 30 * fan, 60] as [number, number], lean: 6};
	return (
		<Outdoor id="s122" cam={shake(cam, f, at('123') + 18, 14, 10)} mode="hot" suns={SUNS_HOT}>
			<Thermo x={1360} y={760} v={v / 50} label={`${Math.round(v)}°`} s={1.1} />
			<Hero x={760} s={1.05} pose={hp} expr={v > 35 ? 'sleepy' : 'normal'} mouth={v > 35 ? 'open' : undefined} uid="h122" />
			{v > 35 ? Array.from({length: 3}).map((_, i) => <circle key={i} cx={720 + i * 40} cy={headY(1.05) + ((f * 2 + i * 20) % 80)} r={6} fill="#7ad0ff" opacity={0.8} />) : null}
		</Outdoor>
	);
};

/* 124: asphalt melts under bike tyres */
const S124: React.FC = () => {
	const {f, gf, at} = useShot();
	const x = tw(f, 0, 70, 700, 1200);
	const sink = tw(f, 60, 100, 0, 1);
	const cam = usePush(camOn(1150, 760, 1.6), camOn(1200, 800, 2.0));
	const sp: Pose = {...idle(f, 2), legB: [70, 60 + Math.sin(f / 3) * 30 * (1 - sink)], legF: [60, 70 - Math.sin(f / 3) * 30 * (1 - sink)], armF: [70, 10], armB: [64, 12], lean: 14};
	return (
		<Outdoor id="s124" cam={cam} mode="hot" suns={SUNS_HOT} yard={{melt: 1, hoop: false}}>
			<g transform={`translate(${x},${FL + 20 + 26 * sink})`}>
				<circle cx={-70} cy={-40} r={44} fill="none" stroke="#1a1a1e" strokeWidth={9} />
				<circle cx={80} cy={-40} r={44} fill="none" stroke="#1a1a1e" strokeWidth={9} />
				<path d="M-70,-40 L0,-110 L80,-40 M0,-110 L-10,-40 L-70,-40 M60,-130 L80,-40" stroke="#2f8fe8" strokeWidth={8} fill="none" />
			</g>
			<ellipse cx={x} cy={FL + 30} rx={200 * sink + 10} ry={24} fill="#1a1a1e" opacity={0.7} />
			<Actor who="sam" x={x - 10} seat={FL - 120 + 26 * sink} s={0.72} pose={sp} expr={sink > 0.5 ? 'wide' : 'normal'} mouth={sink > 0.5 ? 'open' : 'smile'} uid="sam124" />
			<PopText t={f - 70} x={x + 200} y={700} text="SQUELCH" size={56} c="#fff" />
			<Pill t={f - at('124') - 20} x={x} y={560} text="MELTING ASPHALT" c="#ff8a2a" />
			{gf < 0 ? null : null}
		</Outdoor>
	);
};

/* 125: glaciers pour water into rivers */
const S125: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 460, 1.0), camOn(1000, 560, 1.3));
	return (
		<Outdoor
			id="s125"
			cam={cam}
			mode="hot"
			suns={SUNS_HOT}
			houses={false}
			yard={false}
			mid={
				<Svg>
					<path d="M-200,900 L500,180 L900,620 L1300,120 L2100,900 Z" fill="#8a7a8a" />
					<path d={`M380,300 L500,180 L620,300 Q500,${330 - tw(f, 0, 200, 0, 60)} 380,300 Z`} fill="#fff" />
					<path d={`M1160,260 L1300,120 L1440,260 Q1300,${300 - tw(f, 0, 200, 0, 70)} 1160,260 Z`} fill="#fff" />
				</Svg>
			}
		>
			{[500, 1300].map((x, i) => (
				<g key={x}>
					<path d={`M${x},${300} q${-20 + i * 40},200 ${-40 + i * 80},600`} stroke="#7ad0ff" strokeWidth={30} fill="none" />
					{Array.from({length: 8}).map((_, k) => (
						<circle key={k} cx={x + (-40 + i * 80) * (((f / 20 + k / 8) % 1))} cy={300 + 600 * ((f / 20 + k / 8) % 1)} r={8} fill="#fff" opacity={0.7} />
					))}
				</g>
			))}
			<path d={`M-600,960 ${Array.from({length: 30}).map((_, k) => `q50,${(k % 2 ? 1 : -1) * 10} 110,0`).join(' ')} L2700,1100 L-600,1100 Z`} fill="#3a9ae8" transform={`translate(${-(f * 3) % 220},0)`} />
			<PopText t={f - at('125') - 30} x={960} y={160} text="GLACIERS MELT" size={70} c="#7ad0ff" />
		</Outdoor>
	);
};

/* 126: school moves to midnight-5 am */
const S126: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 520, 1.1), camOn(960, 520, 1.4));
	return (
		<Inside cam={cam} set={<School f={gf} night />} light={{x: 50, y: 10, o: 0.3, night: true}}>
			<text x={960} y={350} textAnchor="middle" fontSize={90} fontFamily={HAND} fontWeight={700} fill="#f4f1e6" opacity={tw(f, at('126') + 30, at('126') + 50, 0, 1)}>
				12:00 AM – 5:00 AM
			</text>
			<text x={960} y={480} textAnchor="middle" fontSize={56} fontFamily={HAND} fontWeight={700} fill="#ffd34a" opacity={tw(f, at('126') + 60, at('126') + 80, 0, 1)}>
				(the darkest hours)
			</text>
			{[400, 640, 880, 1120, 1360].map((x, i) => (
				<Extra key={x} i={i + 120} x={x} floor={FL + 30} s={0.78} seed="kid2" expr="sleepy" pose={{...idle(f, i), head: 20 + Math.sin(f / 15 + i) * 8}} facing={1} />
			))}
			<Zzz f={f} x={700} y={560} />
		</Inside>
	);
};

/* 127: mom works double shifts */
const S127: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const w = path(f, [[0, 1900], [dur * 0.5, 200], [dur, 1000]], 2, 0.3, 1);
	const cam = camOn(Math.max(500, Math.min(1400, w.x)), 560, 1.25);
	return (
		<Inside cam={cam} set={<Hospital f={gf} />} light={{x: 50, y: 10, o: 0.35}}>
			<Actor who="mom" x={w.x} pose={w.pose} facing={w.facing} vx={w.vx} bob={w.bob} expr="worried" uid="mom127" />
			<PopText t={f - at('127') - 10} x={w.x} y={300} text="DOUBLE SHIFT ×2" size={56} c="#3fbfb0" />
		</Inside>
	);
};

/* 128-131: back to day 41: 2 am, sunscreen, Sam shooting hoops */
const S128: React.FC = () => {
	const {f, at} = useShot();
	const cam = mixCam(camOn(760, 540, 1.6), camOn(1300, 600, 1.15), tw(f, at('131'), at('131') + 20, 0, 1));
	const hp = beats(idle(f, 2), f, at, [['130', 0, 999, 'sunscreen']]);
	const ph = f % 50;
	const u = ph / 50;
	const j = hops(f, 0, 9999, 50, 30);
	return (
		<>
			<Outdoor id="s128" cam={cam} mode="blue" suns={SUNS_HOT}>
				<Hero x={760} s={1.05} pose={hp} armOver expr="sleepy" uid="h128" />
				<Actor who="sam" x={1470} s={0.72} pose={{...idle(f, 4), armF: [150, 10], armB: [140, 10]}} bob={j.lift / 0.72} look={[0.6, -0.6]} uid="sam128" />
				<Ball x={1490 + 170 * u} y={720 - Math.sin(u * Math.PI) * 280 - u * 220} spin={f * 10} />
				<PopText t={f - at('129') - 4} x={980} y={300} text="2:00 AM" size={80} c="#fff" out={at('131') - at('129')} />
			</Outdoor>
			{f < at('128') + 30 ? <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,255,255,.08) 0 2px, transparent 2px 6px)', opacity: tw(f, 0, at('128') + 30, 1, 0)}} /> : null}
			<Punch t={f - at('128') - 30} text="BACK TO DAY 41" top={80} size={90} c="#ff8a2a" out={at('129') - at('128') + 10} />
		</>
	);
};

/* 132-133: grandpa on the porch with his useless telescope */
const S132: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(300, 560, 1.15), camOn(200, 600, 1.6));
	const gp: Pose = {...idle(f, 7), legB: [88, 85], legF: [92, 90], head: 10 + Math.sin(f / 40) * 3};
	return (
		<Outdoor id="s132" cam={cam} mode="hot" suns={SUNS_HOT}>
			<Chair x={220} y={800 - 30} seat="#8a5a3a" />
			<Actor who="grandpa" x={220} seat={760} s={1} pose={gp} look={[0.4, -0.5]} expr="sad" uid="gp132" />
			<Telescope x={-20} y={FL - 30} tilt={-20} />
			<path d="M-160,690 q60,-40 120,-60 M-150,700 q50,-10 100,-60" stroke="#fff" strokeWidth={2} opacity={0.6} />
			<Pill t={f - at('133') - 10} x={-20} y={500} text="UNUSED: 6 WEEKS" c="#aab3d6" />
		</Outdoor>
	);
};

/* 134-138: "You know what I miss? The stars." */
const S134: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = mixCam(camOn(260, 520, 2.0), camOn(300, 500, 1.6), tw(f, at('137'), at('137') + 30, 0, 1));
	const gp: Pose = beats({...idle(f, 7), legB: [88, 85], legF: [92, 90]}, f, at, [['134', 4, 40, 'presentF'], ['137', 10, 70, 'point'], ['138', 6, 60, 'shrug']]);
	return (
		<Outdoor id="s134" cam={cam} mode="hot" suns={SUNS_HOT}>
			<Chair x={220} y={770} seat="#8a5a3a" />
			<Actor who="grandpa" x={220} seat={760} s={1} pose={gp} look={[0.3, -0.6]} faceTurn={0.4} expr="sad" handF={on(f, at, '137', 10, 70) > 0.5 ? 'point' : undefined} uid="gp134" />
			<Bubble x={520} y={300} w={300} h={180} t={f - at('136') + 2} thought tail={[-180, 160]} fill="#14183a">
				{[[-90, -30], [-30, 30], [40, -40], [100, 20], [0, -10]].map(([x, y], i) => (
					<path key={i} d={`M${x},${y - 14} l4,10 l10,4 l-10,4 l-4,10 l-4,-10 l-10,-4 l10,-4 Z`} fill="#fff" />
				))}
			</Bubble>
			{f > at('138') + 20 ? (
				<g stroke="#ff2a3c" strokeWidth={14} strokeLinecap="round" opacity={tw(f, at('138') + 20, at('138') + 30, 0, 1)}>
					<line x1={400} y1={230} x2={640} y2={370} />
				</g>
			) : null}
			<PopText t={f - at('137') - 10} x={540} y={540} text="EVERY CLEAR NIGHT" size={40} c="#fff" out={at('138') - at('137')} />
			{gf < 0 ? null : null}
		</Outdoor>
	);
};

/* 139-140: you don't know what to say, so you sit with him */
const S139: React.FC = () => {
	const {f, at} = useShot();
	const w = path(f, [[0, 900], [at('140') - 10, 420]], 2);
	const sit = tw(f, at('140') - 6, at('140') + 14, 0, 1);
	const sitPose: Pose = {...idle(f, 1), legB: [88, 85], legF: [92, 90], head: 8};
	const hp = sit > 0 ? {...sitPose, legB: [88 * sit, 85 * sit] as [number, number], legF: [92 * sit, 90 * sit] as [number, number]} : beats(w.pose, f, at, [['139', 20, 60, 'scratch']]);
	const cam = usePush(camOn(560, 560, 1.3), camOn(340, 600, 1.4));
	return (
		<Outdoor id="s139" cam={cam} mode="orange" suns={[{x: 1450, y: 300, r: 60, c: WHITE_SUN}, {x: 900, y: 420, r: 40, c: ORANGE_SUN, glow: 1.6}]}>
			<Chair x={220} y={770} seat="#8a5a3a" />
			<Actor who="grandpa" x={220} seat={760} s={1} pose={{...idle(f, 7), legB: [88, 85], legF: [92, 90], head: 10}} look={[0.6, 0]} expr="sad" uid="gp139" />
			{sit > 0 ? <rect x={370} y={850} width={120} height={40} fill="#8a5a3a" /> : null}
			<Hero x={sit > 0 ? 430 : w.x} seat={sit > 0 ? FL - 157 + 60 * sit : undefined} pose={hp} facing={sit > 0 ? -1 : w.facing} vx={w.vx} bob={w.bob} expr="sad" look={[-0.6, 0]} badge={sit === 0} uid="h139" />
			<Bubble x={w.x + 40} y={360} w={140} h={90} t={f - at('139') - 10} thought tail={[0, 110]}>
				<text x={0} y={16} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#222">
					…
				</text>
			</Bubble>
		</Outdoor>
	);
};

/* 141-143: the real problem — not the heat. Day 60. */
const S141: React.FC = () => {
	const {f, gf, at, dur} = useShot();
	const cam = shake(usePush(camOn(960, 540, 1.0), camOn(960, 540, 1.5)), f, at('141') + 10, 40, 14);
	return (
		<>
			<SpaceStage cam={cam} tint="#5a0a1a">
				<Planet x={960} y={560} r={130} f={gf} />
				<circle cx={960} cy={560} r={200 + Math.sin(f / 3) * 10} fill="none" stroke="#ff2a3c" strokeWidth={6} opacity={0.5} />
			</SpaceStage>
			<AbsoluteFill style={{background: '#c8102e', mixBlendMode: 'multiply', opacity: 0.35 + 0.1 * Math.sin(f / 4)}} />
			<Punch t={f - at('141') - 4} text="THE REAL PROBLEM" top={140} c="#ff5a6a" out={at('142') - at('141') + 10} />
			<Punch t={f - at('142')} text="(NOT THE HEAT)" top={760} size={70} c="#fff" out={at('143') - at('142')} />
			<Punch t={f - at('143') + 2} text="DAY 60" top={330} size={170} c="#ff8a2a" out={dur} />
			<Flash f={f} at={at('143')} c="#ff2a3c" />
		</>
	);
};

export const SHOTS2: ShotDef[] = [
	{at: '063', C: S063, whip: true},
	{at: '068', C: S068, whip: true},
	{at: '069', C: S069},
	{at: '073', C: S073, whip: true},
	{at: '074', C: S074, whip: true},
	{at: '077', C: S077, whip: true},
	{at: '079', C: S079, whip: true},
	{at: '080', C: S080, whip: true},
	{at: '081', C: S081, whip: true},
	{at: '082', C: S082, whip: true},
	{at: '084', C: S084},
	{at: '086', C: S086, whip: true},
	{at: '088', C: S088, whip: true},
	{at: '090', C: S090},
	{at: '091', C: S091},
	{at: '092', C: S092, whip: true},
	{at: '096', C: S096},
	{at: '099', C: S099, whip: true},
	{at: '104', C: S104, whip: true},
	{at: '107', C: S107, whip: true},
	{at: '109', C: S109, whip: true},
	{at: '112', C: S112, whip: true},
	{at: '118', C: S118},
	{at: '122', C: S122, whip: true},
	{at: '124', C: S124},
	{at: '125', C: S125, whip: true},
	{at: '126', C: S126, whip: true},
	{at: '127', C: S127, whip: true},
	{at: '128', C: S128, whip: true},
	{at: '132', C: S132},
	{at: '134', C: S134},
	{at: '139', C: S139},
	{at: '141', C: S141, whip: true},
];
export {Thermo, Burst, Flash, QMark, Sleeper, KitchenTable, Telescope, Tree, Bird, CrowdRow, interpolate, random};
