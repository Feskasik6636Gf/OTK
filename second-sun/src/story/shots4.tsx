import React from 'react';
import {AbsoluteFill, random} from 'remotion';
import {Pose} from '../engine/Stickman';
import {Chair} from '../engine/props';
import {env, gesture, handshake, idle, reach} from '../kit/actions';
import {Actor, useShot} from '../kit/core';
import {CrowdRow, Extra, Layer, Stage, Svg, camOn, mixCam, usePush} from '../kit/kit';
import {Board, Bubble, FONT} from '../kit/ui';
import {Split} from '../kit/graphics';
import type {ShotDef} from '../kit/coverage';
import {ORANGE_SUN, Planet, SpaceBG, Star, Studio, Telescope, Turtle, WHITE_SUN} from './places';
import {Burst, FL, Flash, Hero, Inside, Outdoor, Pill, PopText, Punch, SpaceStage, Zzz, beats, custom, headY, hops, on, path, shake, tw} from './h';

const SEAT = (f: number, seed: number): Pose => ({...idle(f, seed), legB: [88, 85], legF: [92, 90]});

/* 205-206: Day 180 — closest approach; the orange sun at its biggest */
const S205: React.FC = () => {
	const {f, at, dur} = useShot();
	const grow = tw(f, at('206'), at('206') + 50, 90, 220);
	const cam = shake(usePush(camOn(960, 420, 1.0), camOn(960, 360, 1.2)), f, at('206') + 40, 30, 6);
	return (
		<>
			<Outdoor id="s205" cam={cam} mode="orange" suns={[{x: 960, y: 320, r: grow, c: ORANGE_SUN, glow: 1.2}, {x: 1700, y: 160, r: 50, c: WHITE_SUN}]}>
				<Hero x={760} s={1.05} pose={beats(idle(f, 1), f, at, [['206', 10, 999, 'shade']])} look={[0.2, -1]} expr="wide" uid="h205" />
				<Actor who="sam" x={1000} s={0.72} pose={custom('lookUp', idle(f, 4), 1, f)} look={[0, -1]} expr="wide" uid="sam205" />
			</Outdoor>
			<Punch t={f - at('205') + 2} text="DAY 180" size={150} top={500} c="#fff" out={at('206') - at('205') + 6} sub="CLOSEST APPROACH" />
			<Punch t={f - at('206') - 40} text="BIGGEST EVER" top={820} size={80} c="#ffd34a" out={dur} />
		</>
	);
};

/* 207: every phone on Earth vibrates with the same alert */
const S207: React.FC = () => {
	const {f, at} = useShot();
	return (
		<Board tint="#2a0a14">
			{Array.from({length: 7}).map((_, i) => {
				const x = 260 + i * 233;
				const y = 540 + (i % 2) * 80;
				const k = tw(f, at('207') + i * 3, at('207') + 10 + i * 3, 0, 1);
				const buzz = Math.sin(f * 2.4 + i) * 6;
				return (
					<g key={i} transform={`translate(${x + buzz},${y}) scale(${k * (i === 3 ? 1.5 : 1)}) rotate(${buzz * 0.6})`}>
						<rect x={-80} y={-150} width={160} height={300} rx={24} fill="#14141c" />
						<rect x={-70} y={-136} width={140} height={272} rx={14} fill="#c8102e" />
						<text x={0} y={-30} textAnchor="middle" fontSize={70} fontFamily={FONT} fontWeight={900} fill="#fff">
							⚠
						</text>
						<text x={0} y={30} textAnchor="middle" fontSize={20} fontFamily={FONT} fontWeight={900} fill="#fff">
							CLOSEST
						</text>
						<text x={0} y={56} textAnchor="middle" fontSize={20} fontFamily={FONT} fontWeight={900} fill="#fff">
							APPROACH
						</text>
					</g>
				);
			})}
			<PopText t={f - at('207') - 20} x={960} y={200} text="BZZZ! BZZZ!" size={90} c="#ffd34a" />
		</Board>
	);
};

/* 208: every scientist on the planet watching the numbers */
const S208: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 420, 1.05), camOn(960, 400, 1.3));
	return (
		<Stage cam={cam} bg="#0e1430" light={{x: 50, y: 10, o: 0.3}}>
			<Layer depth={1.2}>
				<Studio f={gf} ticker="LIVE: ORBIT DATA">
					{Array.from({length: 9}).map((_, r) => (
						<text key={r} x={570} y={190 + r * 50} fontSize={34} fontFamily="monospace" fill="#5aff9a">
							{Array.from({length: 4}).map((_, c) => (random('n' + r + c + Math.floor(f / 3)) * 999.999).toFixed(3)).join('   ')}
						</text>
					))}
				</Studio>
			</Layer>
			<Layer depth={0.9}>
				<Svg>
					{[300, 640, 1280, 1620].map((x, i) => (
						<Extra key={x} i={i + 140} x={x} floor={1000} s={1.05} seed="sci" pose={gesture('rubChin', idle(f, i), 1, f)} facing={x < 960 ? 1 : -1} expr="worried" />
					))}
				</Svg>
			</Layer>
		</Stage>
	);
};

/* 209-212: the whole family holding hands in the yard… and nothing visible changes */
const S209: React.FC = () => {
	const {f, at} = useShot();
	const xs = [560, 760, 960, 1160, 1360];
	const who = ['mom', 'hero', 'sam', 'dad', 'grandpa'];
	const ss = [1, 1.02, 0.72, 1.04, 1];
	const hold = env(f, at('210') - 10, 9999, 14, 1);
	const cam = f < at('211') ? usePush(camOn(960, 560, 1.15), camOn(960, 540, 1.3)) : f < at('212') ? camOn(960, 300, 1.0) : camOn(760, 520, 2.0);
	const poses = xs.map((_, i) => custom('lookUp', idle(f, i), 1, f));
	for (let i = 0; i < xs.length - 1; i++) {
		if (hold <= 0) break;
		const r = handshake(poses[i], {...poses[i + 1]}, hold, 0, {x: xs[i], y: FL - 157 * ss[i], s: ss[i], facing: 1}, {x: xs[i + 1], y: FL - 157 * ss[i + 1], s: ss[i + 1], facing: -1});
		poses[i] = r.a;
		poses[i + 1] = {...poses[i + 1], armB: reach(poses[i + 1], 'B', [-((xs[i + 1] - xs[i]) / 2) / ss[i + 1], -60], hold).armB};
	}
	return (
		<>
			<Outdoor id="s209" cam={cam} mode="orange" suns={[{x: 960, y: 260, r: 220, c: ORANGE_SUN, glow: 1.2}, {x: 1700, y: 160, r: 50, c: WHITE_SUN}]}>
				{xs.map((x, i) =>
					who[i] === 'hero' ? <Hero key={i} x={x} s={ss[i]} pose={poses[i]} facing={1} faceTurn={0.1} look={[0, -1]} expr="worried" uid="h209" /> : <Actor key={i} who={who[i]} x={x} s={ss[i]} pose={poses[i]} facing={1} faceTurn={0.1} look={[0, -1]} expr="worried" uid={'fam' + i} />,
				)}
			</Outdoor>
			<Punch t={f - at('211') - 4} text="THE MOST IMPORTANT MOMENT IN HISTORY" size={60} top={880} c="#fff" out={at('212') - at('211')} />
			<Punch t={f - at('212') - 30} text="…NOTHING CHANGES" size={80} top={860} c="#aab3d6" out={9999} />
		</>
	);
};

/* 213-215: a scientist on TV takes off her glasses, covers her face… Earth is staying */
const S213: React.FC = () => {
	const {f, gf, at} = useShot();
	const off = f > at('213') + 40;
	const p = beats(idle(f, 3), f, at, [['213', 10, 30, 'touchFace'], ['214', 0, at('215') - at('214') + 10, 'cover']]);
	const cam = f < at('215') ? usePush(camOn(960, 460, 1.6), camOn(960, 480, 2.1)) : camOn(960, 440, 1.0);
	const cry = f > at('214') + 20 && f < at('215') + 30;
	return (
		<>
			<Stage cam={cam} bg="#0e1430" light={{x: 50, y: 10, o: 0.3}}>
				<Layer depth={1.2}>
					<Studio f={gf} ticker={f > at('215') ? 'EARTH IS STAYING • EARTH IS STAYING' : 'LIVE'}>
						<SpaceBG f={gf} />
						<Planet x={960} y={400} r={110} f={gf} />
					</Studio>
				</Layer>
				<Layer depth={1}>
					<Svg>
						<Actor who="scientist" x={960} floor={920} s={1.25} pose={p} acc={off ? [] : ['glasses']} armOver={on(f, at, '214', 0, 200) > 0.3} expr={cry ? 'sad' : 'worried'} faceTurn={0.1} look={[0, 0]} uid="sc213" />
						{off && f < at('214') ? (
							<g stroke="#fff" strokeWidth={4} fill="none" transform="translate(1080,800)">
								<circle cx={-14} cy={0} r={13} />
								<circle cx={14} cy={0} r={13} />
							</g>
						) : null}
						{cry ? [0, 1].map((i) => <circle key={i} cx={940 + i * 44} cy={480 + ((f * 3 + i * 20) % 90)} r={7} fill="#7ad0ff" />) : null}
					</Svg>
				</Layer>
			</Stage>
			<Flash f={f} at={at('215')} />
			<Punch t={f - at('215') - 2} text="EARTH IS STAYING" size={120} top={700} c="#9ff0b0" out={9999} />
		</>
	);
};

/* 216-218: the orbit changed a tiny bit: a year is 3 days longer; every calendar needs fixing */
const S216: React.FC = () => {
	const {f, at} = useShot();
	const days = Math.round(tw(f, at('217') + 10, at('217') + 50, 365, 368));
	return (
		<Board tint="#13301e">
			<g transform={`translate(960,520) rotate(${Math.sin(f / 20) * 3})`}>
				<rect x={-300} y={-260} width={600} height={520} rx={30} fill="#fff" />
				<rect x={-300} y={-260} width={600} height={130} rx={30} fill="#c8102e" />
				<text x={0} y={-170} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill="#fff">
					1 YEAR =
				</text>
				<text x={0} y={90} textAnchor="middle" fontSize={230} fontFamily={FONT} fontWeight={900} fill={days > 365 ? '#c8102e' : '#222'}>
					{days}
				</text>
				<text x={0} y={200} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={800} fill="#444">
					DAYS
				</text>
			</g>
			<PopText t={f - at('216') - 20} x={960} y={130} text="A TINY BIT" size={70} c="#ffd34a" out={at('217') - at('216')} />
			<PopText t={f - at('217') - 52} x={1500} y={260} text="+3 DAYS" size={90} c="#ff5a6a" />
			{f > at('218')
				? Array.from({length: 6}).map((_, i) => (
						<g key={i} transform={`translate(${200 + i * 300},${900 + Math.sin(f / 6 + i) * 10}) rotate(${(i % 2 ? 1 : -1) * 8}) scale(${tw(f, at('218') + i * 4, at('218') + 10 + i * 4, 0, 1)})`}>
							<rect x={-70} y={-60} width={140} height={120} rx={10} fill="#fff" />
							<rect x={-70} y={-60} width={140} height={34} rx={10} fill="#c8102e" />
							<text x={0} y={40} textAnchor="middle" fontSize={30} fontFamily={FONT} fontWeight={900} fill="#c8102e">
								FIX ME
							</text>
						</g>
					))
				: null}
		</Board>
	);
};

/* 219-220: nobody cares — the whole planet cheers */
const S219: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 520, 1.3), camOn(960, 540, 1.0));
	const j = hops(f, at('219'), 9999, 16, 60);
	return (
		<>
			<Outdoor id="s219" cam={cam} mode="gold" suns={[{x: 1450, y: 170, r: 62, c: WHITE_SUN}, {x: 500, y: 220, r: 110, c: ORANGE_SUN, glow: 1.3}]} yard={{hoop: true}}>
				<CrowdRow n={10} x0={0} x1={1920} floor={FL + 30} s={0.85} mode="dance" seed="cheer" />
				<Hero x={960} s={1.05} pose={custom('cheer', idle(f, 1), 1, f)} bob={j.lift} squash={j.squash} mouth="open" look={[0, -0.6]} uid="h219" />
				{Array.from({length: 5}).map((_, i) => (
					<Burst key={i} t={((f - at('219') - i * 14) % 50 + 50) % 50} x={300 + i * 330} y={220 + (i % 2) * 80} seed={'fw' + i} r={180} />
				))}
			</Outdoor>
			<Punch t={f - at('219')} text="NOBODY CARES!" top={90} out={at('220') - at('219')} c="#ff9ab8" />
			<Punch t={f - at('220')} text="WE'RE STAYING!" top={90} out={9999} c="#9ff0b0" />
		</>
	);
};

/* 221-225: Day 214 — each evening the orange sun is smaller, until it's just a star */
const S221: React.FC = () => {
	const {f, at, dur} = useShot();
	const r = tw(f, at('221'), at('225'), 80, 5);
	const cam = usePush(camOn(1200, 380, 1.15), camOn(1250, 320, 1.6));
	const mode = f < at('223') ? 'dusk' : 'night';
	return (
		<>
			<Outdoor id="s221" cam={cam} mode={mode} stars={tw(f, at('223'), at('225'), 0, 0.4)} suns={[{x: 1250, y: 300, r, c: ORANGE_SUN, glow: r < 12 ? 2.5 : 1.3}]} lit={f > at('223') ? 0.8 : 0}>
				<Hero x={760} pose={custom('lookUp', idle(f, 1), 1, f)} look={[0.8, -0.8]} uid="h221" />
			</Outdoor>
			<Punch t={f - at('221') + 2} text="DAY 214" size={130} top={100} c="#ff8a2a" out={at('222') - at('221') + 4} />
			<Punch t={f - at('222') - 4} text="SMALLER… WEAKER…" size={70} top={880} c="#fff" out={at('223') - at('222')} />
			<Punch t={f - at('225') - 4} text="JUST A BRIGHT STAR" size={80} top={880} c="#ffd34a" out={dur} />
		</>
	);
};

/* 226-229: for the first time in 214 days it gets dark; street lights go off */
const S226: React.FC = () => {
	const {f, at, dur} = useShot();
	const dark = tw(f, at('226'), at('227') + 20, 0, 1);
	const cam = usePush(camOn(960, 500, 1.0), camOn(960, 480, 1.2));
	return (
		<>
			<Outdoor id="s226" cam={cam} mode={dark > 0.5 ? 'dark' : 'night'} stars={0.3} lit={1 - dark * 0.6}>
				{[200, 700, 1200, 1700].map((x, i) => {
					const offAt = at('228') + 10 + i * 12;
					const lit = f < offAt;
					return (
						<g key={x}>
							<rect x={x - 8} y={500} width={16} height={400} fill="#2a2f3a" />
							<rect x={x - 40} y={490} width={80} height={20} rx={8} fill="#2a2f3a" />
							{lit ? <path d={`M${x - 30},510 L${x - 180},${FL} L${x + 180},${FL} L${x + 30},510 Z`} fill="#ffe3a0" opacity={0.25} /> : null}
							<circle cx={x} cy={514} r={14} fill={lit ? '#fff6c0' : '#3a3f4a'} />
							{f >= offAt && f < offAt + 10 ? <PopText t={f - offAt} x={x} y={440} text="CLICK" size={30} c="#fff" out={6} /> : null}
						</g>
					);
				})}
				<Hero x={960} pose={custom('lookUp', idle(f, 1), dark, f)} look={[0, -1]} expr="wide" uid="h226" />
			</Outdoor>
			<Punch t={f - at('227') - 2} text="REAL DARK" size={120} top={140} c="#c8d0ff" out={at('228') - at('227') + 10} />
			{dur < 0 ? null : null}
		</>
	);
};

/* 230-232: eight billion people walk outside; nobody talks; everyone looks up */
const S230: React.FC = () => {
	const {f, at} = useShot();
	const cam = usePush(camOn(960, 600, 1.0), camOn(960, 520, 1.3));
	const look = env(f, at('232'), 9999, 14, 1);
	return (
		<Outdoor id="s230" cam={cam} mode="dark" stars={0.5}>
			{Array.from({length: 11}).map((_, i) => {
				const w = path(f, [[i * 4, i % 2 ? -200 - i * 40 : 2100 + i * 40], [60 + i * 6, 120 + i * 170]], i);
				const p = custom('lookUp', w.pose, look, f);
				return i === 5 ? <Hero key={i} x={w.x} pose={p} facing={w.facing} vx={w.vx} bob={w.bob} look={[0, -1 * look]} uid="h230" /> : <Extra key={i} i={i + 200} x={w.x} floor={FL + (i % 3) * 10} s={0.9} seed="out" pose={p} facing={w.facing} />;
			})}
			<Pill t={f - at('230') - 30} x={960} y={200} text="8,000,000,000 PEOPLE" c="#c8d0ff" size={44} out={at('231') - at('230') + 20} />
			<Bubble x={960} y={240} w={150} h={90} t={f - at('231') - 4} tail={[0, 110]}>
				<text x={0} y={16} textAnchor="middle" fontSize={56} fontFamily={FONT} fontWeight={900} fill="#222">
					…
				</text>
			</Bubble>
		</Outdoor>
	);
};

/* 233-235: thousands, then millions of stars; the Milky Way like spilled sugar */
const S233: React.FC = () => {
	const {f, at} = useShot();
	const stars = tw(f, at('233'), at('234'), 0.2, 1);
	const milky = tw(f, at('234'), at('235') + 30, 0, 1);
	const cam = usePush(camOn(960, 700, 1.05), camOn(960, 140, 1.0));
	return (
		<>
			<Outdoor id="s233" cam={cam} mode="dark" stars={stars} milky={milky} lit={0}>
				<CrowdRow n={9} x0={100} x1={1820} floor={FL + 20} s={0.9} mode="stand" seed="sky" />
			</Outdoor>
			<Punch t={f - at('233') - 20} text="THOUSANDS" size={80} top={880} c="#fff" out={at('234') - at('233') - 10} />
			<Punch t={f - at('234') - 6} text="MILLIONS" size={90} top={880} c="#c8d0ff" out={at('235') - at('234')} />
			<Punch t={f - at('235') - 30} text="THE MILKY WAY" size={90} top={880} c="#ffd6a8" out={9999} />
		</>
	);
};

/* 236-238: grandpa with his telescope again; his hands are shaking */
const S236: React.FC = () => {
	const {f, at} = useShot();
	const shakeK = f > at('238') ? 1 : 0.3;
	const gp = {...beats(idle(f, 7), f, at, [['236', 0, 999, 'carry']]), armF: [62 + Math.sin(f * 1.8) * 6 * shakeK, 40] as [number, number]};
	const cam = f < at('238') ? usePush(camOn(760, 560, 1.3), camOn(700, 560, 1.5)) : camOn(820, 640, 2.4);
	return (
		<Outdoor id="s236" cam={cam} mode="dark" stars={1} milky={1}>
			<Telescope x={860} y={FL} tilt={-35 + Math.sin(f * 1.8) * 2 * shakeK} s={0.9} />
			<Actor who="grandpa" x={700} s={1} pose={gp} look={[0.6, -0.6]} expr="sad" mouth="smile" uid="gp236" />
			<Hero x={1080} pose={idle(f, 1)} facing={-1} look={[-0.6, 0]} uid="h236" />
			<Pill t={f - at('237') - 10} x={860} y={430} text="7 MONTHS UNUSED" c="#aab3d6" out={at('238') - at('237')} />
			{f > at('238') ? <PopText t={f - at('238') - 10} x={1000} y={500} text="shaking…" size={40} c="#fff" /> : null}
		</Outdoor>
	);
};

/* 239-241: "Vega," you say, pointing. "Sirius. And that red one is Betelgeuse." */
const S239: React.FC = () => {
	const {f, gf, at} = useShot();
	const targets: [string, number, number, string, string][] = [
		['239', 600, 240, 'VEGA', '#bfe0ff'],
		['240', 1000, 180, 'SIRIUS', '#ffffff'],
		['241', 1400, 260, 'BETELGEUSE', '#ff6a4a'],
	];
	const cur = f < at('240') ? 0 : f < at('241') ? 1 : 2;
	const [, tx, ty] = targets[cur];
	const hp = reach(custom('lookUp', idle(f, 1), 1, f), 'F', [((tx - 860) / 1) * 1, (ty - 743) / 4 - 60], 1);
	const cam = mixCam(camOn(860, 560, 1.5), camOn(tx, 380, 1.1), 0.4);
	return (
		<Outdoor id="s239" cam={cam} mode="dark" stars={1} milky={1}>
			<Hero x={860} pose={{...custom('lookUp', idle(f, 1), 1, f), armF: [150 - cur * 20, 10]}} facing={1} handF="point" look={[0.6, -1]} mouth="smile" uid="h239" />
			<Actor who="grandpa" x={660} pose={custom('lookUp', idle(f, 7), 1, f)} facing={1} look={[0.6, -1]} mouth="smile" uid="gp239" />
			{targets.map(([l, x, y, n, c], i) =>
				f > at(l) ? (
					<g key={n}>
						<circle cx={x} cy={y} r={12 + 2 * Math.sin(gf / 4 + i)} fill={c} />
						<circle cx={x} cy={y} r={50 * tw(f, at(l), at(l) + 10, 2, 1)} fill="none" stroke={c} strokeWidth={4} opacity={0.7} />
						<PopText t={f - at(l) - 4} x={x} y={y + 90} text={n} size={46} c={c} rot={0} />
					</g>
				) : null,
			)}
			{hp ? null : null}
		</Outdoor>
	);
};

/* 242-243: he looks at you for a long time… then hugs you so hard you can't breathe */
const S242: React.FC = () => {
	const {f, at} = useShot();
	const close = tw(f, at('243') - 6, at('243') + 14, 0, 1);
	const gx = 700 + 120 * close;
	const hx = 1000 - 60 * close;
	const hug = env(f, at('243') + 4, 9999, 10, 1);
	const cam = f < at('243') ? usePush(camOn(760, 520, 2.0), camOn(760, 520, 2.3)) : camOn(860, 560, 1.7);
	return (
		<Outdoor id="s242" cam={cam} mode="dark" stars={1} milky={1}>
			<Actor who="grandpa" x={gx} pose={custom('hug', idle(f, 7), hug, f)} facing={1} look={[0.6, 0]} faceTurn={0.5} expr={hug > 0.5 ? 'sleepy' : 'sad'} mouth="smile" uid="gp242" />
			<Hero x={hx} pose={custom('hug', idle(f, 1), hug, f)} facing={-1} squash={hug * 0.08} look={[-0.6, 0]} faceTurn={0.5} expr={hug > 0.5 ? 'wide' : 'normal'} badge={false} uid="h242" />
			{hug > 0.5 ? <PopText t={f - at('243') - 14} x={860} y={320} text="SQUEEZE!" size={60} c="#ff9ab8" /> : null}
			{hug > 0.5 ? <Burst t={f - at('243') - 10} x={860} y={440} c={['#ff5a8a', '#ffd34a']} seed="hug" /> : null}
		</Outdoor>
	);
};

/* 244: that night the whole world sleeps for 14 hours */
const S244: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 540, 1.0), camOn(960, 540, 1.3));
	return (
		<SpaceStage cam={cam}>
			<Planet x={960} y={560} r={220} f={gf * 0.3} />
			<path d="M800,500 q80,-40 160,0 q80,-40 160,0 l0,40 q-80,30 -160,0 q-80,30 -160,0 Z" fill="#3a2a6a" />
			<path d="M840,640 q120,40 240,0" stroke="#fff" strokeWidth={8} fill="none" strokeLinecap="round" />
			<Zzz f={f} x={1180} y={360} s={2} />
			<PopText t={f - at('244') - 30} x={960} y={900} text="14 HOURS OF SLEEP" size={70} c="#a99aff" />
		</SpaceStage>
	);
};

/* 245-251: everything depends on one ordinary star — the most extraordinary thing */
const S245: React.FC = () => {
	const {f, gf, at} = useShot();
	const a = gf / 40;
	const cam = usePush(camOn(960, 540, 1.2), camOn(960, 540, 0.95));
	const labels: [string, string, number, number][] = [
		['248', 'NOT TOO CLOSE', 0, 0],
		['248', 'NOT TOO FAR', 30, 1],
		['248', 'NOT TOO BRIGHT', 60, 2],
	];
	return (
		<>
			<SpaceStage cam={cam}>
				<ellipse cx={960} cy={560} rx={360} ry={150} fill="none" stroke="#9ff0b0" strokeWidth={3} strokeDasharray="8 10" />
				<Star x={960} y={560} r={80} c={WHITE_SUN} f={gf} id="w245" />
				<Planet x={960 + Math.cos(a) * 360} y={560 + Math.sin(a) * 150} r={30} f={gf} />
				{labels.map(([l, t, off, i]) => (
					<Pill key={t} t={f - at(l) - off} x={[500, 1420, 960][i]} y={[300, 300, 900][i]} text={t} c={['#ff5a3a', '#5ad0ff', '#ffd34a'][i]} size={38} out={at('250') - at(l) - off - 10} />
				))}
				<PopText t={f - at('249') - 4} x={960} y={420} text="ALONE IN THE SKY" size={50} c="#fff" out={at('250') - at('249')} />
				<PopText t={f - at('246') - 20} x={960} y={150} text="EVERYTHING YOU LOVE" size={60} c="#ff9ab8" out={at('248') - at('246') - 10} />
			</SpaceStage>
			{f > at('250') ? (
				<AbsoluteFill style={{pointerEvents: 'none'}}>
					<div style={{position: 'absolute', top: 820, left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontWeight: 900, fontSize: 96, color: '#fff', WebkitTextStroke: '5px #0b0d1e', paintOrder: 'stroke'}}>
						<span style={{color: '#ffd34a', display: 'inline-block', transform: `scale(${tw(f, at('251') + 30, at('251') + 40, 0, 1)})`, width: f > at('251') + 30 ? undefined : 0, overflow: 'hidden'}}>EXTRA</span>
						ORDINARY
					</div>
				</AbsoluteFill>
			) : null}
			<Flash f={f} at={at('251') + 30} />
		</>
	);
};

/* 252-257: a week later, grandpa at the telescope at midnight; he stops, frowns, adjusts a dial */
const S252: React.FC = () => {
	const {f, at} = useShot();
	const gp: Pose = {...idle(f, 7), lean: 16, head: 10, armF: [70, 50], armB: [60, 60]};
	const dial = env(f, at('257'), 9999, 8, 1);
	const pose = dial > 0 ? reach(gp, 'F', [90, -110 + Math.sin(f / 3) * 4], dial) : gp;
	const cam = f < at('255') ? usePush(camOn(700, 520, 1.2), camOn(760, 480, 1.6)) : f < at('257') ? camOn(800, 440, 2.4) : camOn(880, 560, 2.0);
	return (
		<Outdoor id="s252" cam={cam} mode="night" stars={1} milky={0.6} suns={[{x: 1500, y: 260, r: 6, c: ORANGE_SUN, glow: 3}]}>
			<Telescope x={900} y={FL - 30} tilt={-32} />
			<Actor who="grandpa" x={760} floor={FL - 30} pose={pose} facing={1} lidL={1} expr={f > at('256') ? 'angry' : 'normal'} mouth={f > at('256') ? 'frown' : 'line'} look={[1, -0.3]} uid="gp252" />
			<Pill t={f - at('252') - 20} x={760} y={300} text="MIDNIGHT • 1 WEEK LATER" c="#c8d0ff" size={36} out={at('254') - at('252')} />
			<Callout_ f={f} t0={at('254')} t1={at('255')} />
			{f > at('255') && f < at('256') ? <PopText t={f - at('255')} x={860} y={380} text="!" size={100} c="#ffd34a" /> : null}
			{dial > 0 ? <PopText t={f - at('257') - 10} x={1000} y={680} text="click… click…" size={34} c="#fff" /> : null}
		</Outdoor>
	);
};
const Callout_: React.FC<{f: number; t0: number; t1: number}> = ({f, t0, t1}) => {
	const k = env(f, t0, t1, 8, 8);
	return k > 0 ? <PopText t={f - t0} x={1500} y={340} text="DRIFTING AWAY" size={40} c="#ff8a2a" /> : null;
};

/* 258-262: "Huh. That's strange." "What?" … "It's not leaving alone." */
const S258: React.FC = () => {
	const {f, gf, at} = useShot();
	const reveal = f > at('262') - 10;
	const gp: Pose = {...idle(f, 7), lean: 16, head: 10, armF: [70, 50], armB: [60, 60]};
	const cam = f < at('260') ? camOn(760, 500, 2.3) : f < at('261') ? camOn(1120, 520, 2.2) : camOn(860, 520, 1.6);
	const u = tw(f, at('262') - 10, at('262') + 80, 0, 1);
	return (
		<>
			<Outdoor id="s258" cam={cam} mode="night" stars={1} milky={0.6}>
				<Telescope x={900} y={FL - 30} tilt={-32} />
				<Actor who="grandpa" x={760} floor={FL - 30} pose={gp} facing={1} lidL={1} expr="worried" look={[1, -0.3]} uid="gp258" />
				<Hero x={1120} pose={beats(idle(f, 1), f, at, [['260', 0, 60, 'shrug']])} facing={-1} look={[-0.8, 0]} expr={f > at('260') ? 'wide' : 'normal'} uid="h258" />
				<Bubble x={600} y={300} w={200} h={90} t={f - at('258') + 2} tail={[80, 110]}>
					<text x={0} y={14} textAnchor="middle" fontSize={44} fontFamily={FONT} fontWeight={900} fill="#222">
						Huh.
					</text>
				</Bubble>
			</Outdoor>
			{reveal ? (
				<AbsoluteFill style={{background: '#000', opacity: tw(f, at('262') - 10, at('262'), 0, 1)}}>
					<svg viewBox="0 0 1920 1080" width={1920} height={1080}>
						<defs>
							<clipPath id="eye262">
								<circle cx={960} cy={540} r={430} />
							</clipPath>
						</defs>
						<g clipPath="url(#eye262)">
							<g transform={`translate(960,540) scale(${1 + 0.2 * u}) translate(-960,-540)`}>
								<rect x={0} y={0} width={1920} height={1080} fill="#04040f" />
								{Array.from({length: 120}).map((_, i) => (
									<circle key={i} cx={random('ts' + i) * 1920} cy={random('tt' + i) * 1080} r={1 + random('tr' + i) * 2} fill="#fff" opacity={0.7} />
								))}
								<Star x={900 + u * 40} y={520} r={60} c={ORANGE_SUN} f={gf} id="o262" />
								<g opacity={tw(f, at('262') + 20, at('262') + 50, 0, 1)}>
									<circle cx={1120 + u * 40} cy={600} r={18} fill="#8a9ab0" />
									<circle cx={1120 + u * 40} cy={600} r={40} fill="none" stroke="#ff2a3c" strokeWidth={4} opacity={0.5 + 0.5 * Math.sin(f / 3)} />
								</g>
							</g>
						</g>
						<circle cx={960} cy={540} r={430} fill="none" stroke="#14141c" strokeWidth={30} />
						<line x1={960} y1={110} x2={960} y2={970} stroke="#fff" strokeWidth={2} opacity={0.3} />
						<line x1={530} y1={540} x2={1390} y2={540} stroke="#fff" strokeWidth={2} opacity={0.3} />
					</svg>
				</AbsoluteFill>
			) : null}
			<Punch t={f - at('259')} text="THAT'S STRANGE." size={70} top={860} c="#fff" out={at('260') - at('259')} />
			<Punch t={f - at('260')} text="WHAT?" size={90} top={860} c="#ff5a6a" out={at('261') - at('260')} />
			<Punch t={f - at('262') - 30} text="IT'S NOT LEAVING ALONE." size={80} top={960} c="#ff2a3c" out={9999} />
		</>
	);
};

/* 263-267: call to action */
const S263: React.FC = () => {
	const {f, gf, at} = useShot();
	return (
			<Split
				f={f - at('263') + 6}
				a={{label: 'TWO SUNS', num: '☀☀', color: '#ff8a2a', bg: '#3a1a10', icon: <g><Star x={-80} y={0} r={90} c={WHITE_SUN} f={gf} id="cta1" /><Star x={110} y={-30} r={60} c={ORANGE_SUN} f={gf} id="cta2" /></g>}}
				b={{label: 'ONE SUN + NIGHT', num: '☾', color: '#c8d0ff', bg: '#0a1030', icon: <g>{Array.from({length: 30}).map((_, i) => <circle key={i} cx={(random('cs' + i) - 0.5) * 380} cy={(random('ct' + i) - 0.5) * 300} r={2 + random('cu' + i) * 3} fill="#fff" />)}<circle cx={0} cy={0} r={70} fill="#eef1ff" /></g>}}
			/>
	);
};
const S265: React.FC = () => {
	const {f, gf, at} = useShot();
	const cam = usePush(camOn(960, 520, 1.2), camOn(960, 540, 1.4));
	const press = (l: string, off: number) => tw(f, at(l) + off, at(l) + off + 6, 1, 0.85) + tw(f, at(l) + off + 6, at(l) + off + 12, 0, 0.15);
	const liked = f > at('267') + 16;
	const subbed = f > at('267') + 40;
	return (
		<Outdoor id="s263" cam={cam} mode="night" stars={1} milky={0.8}>
			<Hero x={760} s={1.05} pose={beats(idle(f, 1), f, at, [['265', 0, 60, 'point'], ['266', 0, at('267') - at('266'), 'carry'], ['267', 0, 999, 'cheer']])} look={[0.6, -0.2]} mouth="smile" uid="h263" />
			{f > at('266') && f < at('267') ? <Turtle x={840} y={FL - 150} s={0.7} f={gf} /> : null}
			<Bubble x={1300} y={300} w={400} h={130} t={f - at('265') + 2} tail={[-160, 140]}>
				<text x={0} y={18} textAnchor="middle" fontSize={48} fontFamily={FONT} fontWeight={900} fill="#222">
					COMMENTS ✎
				</text>
			</Bubble>
			<g transform={`translate(1150,560) scale(${press('267', 10)})`} opacity={tw(f, at('267'), at('267') + 8, 0, 1)}>
				<rect x={-140} y={-50} width={280} height={100} rx={50} fill={liked ? '#2f7fe6' : '#2a2f3a'} />
				<text x={0} y={18} textAnchor="middle" fontSize={50} fontFamily={FONT} fontWeight={900} fill="#fff">
					♥ LIKE
				</text>
			</g>
			<g transform={`translate(1500,560) scale(${press('267', 34)})`} opacity={tw(f, at('267') + 6, at('267') + 14, 0, 1)}>
				<rect x={-190} y={-50} width={380} height={100} rx={50} fill={subbed ? '#c8102e' : '#2a2f3a'} />
				<text x={0} y={18} textAnchor="middle" fontSize={46} fontFamily={FONT} fontWeight={900} fill="#fff">
					{subbed ? 'SUBSCRIBED' : 'SUBSCRIBE'}
				</text>
			</g>
			{liked ? <Burst t={f - at('267') - 16} x={1150} y={560} seed="like" /> : null}
		</Outdoor>
	);
};

export const SHOTS4: ShotDef[] = [
	{at: '205', C: S205, whip: true},
	{at: '207', C: S207, whip: true},
	{at: '208', C: S208, whip: true},
	{at: '209', C: S209, whip: true},
	{at: '213', C: S213, whip: true},
	{at: '216', C: S216, whip: true},
	{at: '219', C: S219, whip: true},
	{at: '221', C: S221, whip: true},
	{at: '226', C: S226},
	{at: '230', C: S230},
	{at: '233', C: S233},
	{at: '236', C: S236},
	{at: '239', C: S239},
	{at: '242', C: S242},
	{at: '244', C: S244, whip: true},
	{at: '245', C: S245, whip: true},
	{at: '252', C: S252, whip: true},
	{at: '258', C: S258},
	{at: '263', C: S263, whip: true},
	{at: '265', C: S265, whip: true},
];
export {Chair, headY, SEAT};
