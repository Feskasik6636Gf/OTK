import React from 'react';
import {AbsoluteFill, interpolate, random, spring, Easing} from 'remotion';
import {useShot} from '../kit/core';
import {Board, Cite, FONT, HAND, RuleCard} from '../kit/ui';
import {Split} from '../kit/graphics';
import {Stickman} from '../engine/Stickman';
import {idle} from '../kit/actions';
import {CAST} from './cast';
import {IconG, type Beat} from './engine';
import {Rat} from './places';

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const sp = (t: number, d = 12, s = 150) => spring({frame: t, fps: 30, config: {damping: d, stiffness: s}});
const T: React.FC<{x: number; y: number; t: number; size?: number; c?: string; children: React.ReactNode; anchor?: 'middle' | 'start' | 'end'; hand?: boolean}> = ({x, y, t, size = 60, c = '#fff', children, anchor = 'middle', hand}) => {
	const k = sp(t);
	if (t < 0) return null;
	return (
		<g transform={`translate(${x},${y + (1 - k) * 40}) scale(${0.7 + 0.3 * k})`} opacity={Math.min(1, k * 1.4)}>
			<text textAnchor={anchor} fontSize={size} fontFamily={hand ? HAND : FONT} fontWeight={900} fill={c} stroke="#0b0d1e" strokeWidth={size * 0.08} paintOrder="stroke">
				{children}
			</text>
		</g>
	);
};
const Fig: React.FC<{x: number; y: number; s?: number; who?: string; t?: number; laugh?: boolean; color?: string; id: string}> = ({x, y, s = 1, who = 'kid1', t = 0, laugh, color, id}) => {
	const {gf} = useShot();
	const b = laugh ? Math.sin(gf / 2.5 + x) : 0;
	const k = sp(t, 12, 170);
	if (t < 0) return null;
	return (
		<g transform={`translate(${x},${y}) scale(${k})`}>
			<Stickman id={id} x={0} y={-157 * s - (laugh ? Math.abs(b) * 6 : 0)} scale={s} pose={laugh ? {...idle(gf, x), lean: -10 + b * 4, head: -14 + b * 6, armF: [40, 80], armB: [-20, 70]} : idle(gf, x)} {...CAST[who]} {...(color ? {color} : {})} expr={laugh ? 'sleepy' : 'normal'} mouth={laugh ? 'open' : 'line'} look={[0, 0]} faceTurn={0.2} />
		</g>
	);
};

/* 10 vs 1000 */
const Ten: React.FC<{b: Beat}> = () => {
	const {f} = useShot();
	return <Split f={f} a={{label: 'ОБЫЧНЫЙ ЧЕЛОВЕК', num: '10', color: '#9fd2f0', who: 'kid3'}} b={{label: 'ТВОЙ ЮМОР', num: '1000', color: '#ff2338', who: 'hero', bg: '#3a1020'}} />;
};

/* rats laugh in ultrasound */
const Rats: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const hz = Math.round(interpolate(f, [20, dur * 0.7], [20, 50], {...clamp, easing: Easing.out(Easing.cubic)}));
	return (
		<Board tint="#1a2a50">
			<T x={960} y={140} t={f - 2} size={64}>КРЫСЫ ТОЖЕ СМЕЮТСЯ</T>
			{[0, 1, 2].map((i) => (
				<g key={i} opacity={sp(f - 10 - i * 6)}>
					<Rat x={520 + i * 420} y={700} f={f + i * 7} laugh={1} s={1.4} flip={i === 2} />
				</g>
			))}
			{/* finger tickling */}
			<g transform={`translate(${900 + Math.sin(f / 2) * 18},${520 + Math.cos(f / 2) * 10}) rotate(30)`}>
				<rect x={-16} y={-120} width={32} height={140} rx={16} fill="#f2c4a0" />
			</g>
			{[0, 1, 2, 3].map((i) => {
				const k = ((f / 20 + i / 4) % 1);
				return <path key={i} d={`M${940 - 40 - k * 200},${480 - k * 100} Q960,${380 - k * 220} ${980 + 40 + k * 200},${480 - k * 100}`} stroke="#7ff0ff" strokeWidth={6} fill="none" opacity={1 - k} />;
			})}
			<g transform="translate(960,900)" opacity={sp(f - 30)}>
				<rect x={-430} y={-60} width={860} height={110} rx={24} fill="#11142c" stroke="#7ff0ff" strokeWidth={4} />
				<text x={-390} y={14} fontSize={42} fontFamily={FONT} fill="#7ff0ff">ЧАСТОТА ПИСКА:</text>
				<text x={390} y={16} textAnchor="end" fontSize={60} fontFamily={FONT} fontWeight={900} fill="#fff">{hz} кГц</text>
			</g>
			<T x={1600} y={300} t={f - dur * 0.5} size={40} c="#ff9ab8">человек не слышит!</T>
			<Cite text="Panksepp, 2000-е — «смех» крыс при щекотке" t={f} />
		</Board>
	);
};

/* contagious laugh: the brain lights up when hearing a laugh */
const Brain: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const glow = interpolate(f, [dur * 0.35, dur * 0.6], [0, 1], clamp);
	return (
		<Board tint="#2a1a50">
			<T x={960} y={130} t={f - 2} size={60}>СМЕХ ЗАРАЗЕН</T>
			<Fig id="br1" x={420} y={860} s={1.6} who="kid2" laugh t={f - 4} />
			{[0, 1, 2].map((i) => {
				const k = ((f / 18 + i / 3) % 1);
				return <path key={i} d={`M${560 + k * 400},${560 - 120} q30,120 0,240`} stroke="#ffd34a" strokeWidth={8} fill="none" opacity={(1 - k) * sp(f - 10)} />;
			})}
			<g transform="translate(1360,520)">
				<ellipse rx={300 * glow} ry={240 * glow} fill="#ff6ab0" opacity={0.25} style={{filter: 'blur(30px)'}} />
				<g opacity={sp(f - 8)}>
					<IconG i="brain" s={4.2} />
				</g>
				{glow > 0
					? Array.from({length: 9}).map((_, i) => (
							<circle key={i} cx={-120 + (i % 3) * 120} cy={-80 + Math.floor(i / 3) * 70} r={14 + 8 * Math.sin(f / 4 + i)} fill="#fff6a0" opacity={glow * (0.5 + 0.5 * Math.sin(f / 3 + i))} />
						))
					: null}
			</g>
			<T x={1360} y={900} t={f - dur * 0.45} size={44} c="#ffd34a">«готовься смеяться!»</T>
			<Cite text="Scott и др., UCL, 2006" t={f} />
		</Board>
	);
};

/* researcher: most laughs follow ordinary words */
const Study: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const pct = Math.round(interpolate(f, [20, dur * 0.6], [0, 80], {...clamp, easing: Easing.out(Easing.cubic)}));
	return (
		<Board tint="#1a3a40">
			<T x={960} y={130} t={f - 2} size={56}>1 200 СЛУЧАЕВ СМЕХА</T>
			<g transform="translate(560,600)">
				<circle r={260} fill="#2a4a50" />
				<path d={`M0,0 L0,-260 A260,260 0 ${pct > 50 ? 1 : 0},1 ${260 * Math.sin((pct / 100) * Math.PI * 2)},${-260 * Math.cos((pct / 100) * Math.PI * 2)} Z`} fill="#ffd34a" />
				<circle r={150} fill="#1a3a40" />
				<text y={30} textAnchor="middle" fontSize={96} fontFamily={FONT} fontWeight={900} fill="#fff">{pct}%</text>
			</g>
			<T x={1340} y={420} t={f - 20} size={50} c="#ffd34a" anchor="middle">смеются НЕ над шутками</T>
			<g opacity={sp(f - dur * 0.45)}>
				<rect x={1060} y={520} width={560} height={90} rx={45} fill="#fbf8ef" />
				<text x={1340} y={580} textAnchor="middle" fontSize={40} fontFamily={FONT} fill="#1b1e2a">«Увидимся позже»</text>
			</g>
			<g opacity={sp(f - dur * 0.6)}>
				<rect x={1100} y={650} width={480} height={90} rx={45} fill="#fbf8ef" />
				<text x={1340} y={710} textAnchor="middle" fontSize={40} fontFamily={FONT} fill="#1b1e2a">«Ты уверен?»</text>
			</g>
			<Cite text="Robert Provine, 1990-е" t={f} />
		</Board>
	);
};

/* x30: with others vs alone */
const X30: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const h = interpolate(f, [10, dur * 0.6], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
	return (
		<Board tint="#3a1a30">
			<T x={960} y={130} t={f - 2} size={50}>В КОМПАНИИ СМЕЁМСЯ В 30 РАЗ ЧАЩЕ</T>
			<rect x={520} y={860 - 20} width={240} height={20} fill="#9aa3b5" />
			<rect x={1160} y={860 - 600 * h} width={240} height={600 * h} rx={10} fill="#ff2338" />
			<rect x={520} y={860 - 20 * h} width={240} height={20 * h} fill="#9aa3b5" />
			<Fig id="x1" x={640} y={1010} s={0.8} who="kid3" t={f - 10} />
			{[0, 1, 2].map((i) => (
				<Fig key={i} id={'x2' + i} x={1180 + i * 100} y={1010} s={0.7} who={['kid1', 'kid2', 'hero'][i]} laugh t={f - 14 - i * 4} />
			))}
			<T x={640} y={800} t={f - 16} size={50}>×1</T>
			<T x={1280} y={860 - 600 * h - 30} t={f - 20} size={80} c="#ffd34a">×30</T>
			<Cite text="Provine & Fischer, 1989" t={f} />
		</Board>
	);
};

/* 40 million views */
const Views: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const v = Math.round(interpolate(f, [6, dur * 0.85], [0, 40000000], {...clamp, easing: Easing.in(Easing.cubic)}));
	return (
		<Board tint="#20103a">
			<g transform={`translate(960,560) rotate(${Math.sin(f / 20) * 3}) scale(${sp(f) * 1.05})`}>
				<rect x={-280} y={-460} width={560} height={920} rx={60} fill="#15171f" />
				<rect x={-256} y={-430} width={512} height={860} rx={40} fill="#2a2d55" />
				<rect x={-230} y={-380} width={460} height={300} rx={12} fill="#3a1f4a" />
				<g transform="translate(0,-210)">
					<Stickman id="vw" x={0} y={40} scale={0.7} pose={{lean: -8, head: -6, armF: [150, 20], armB: [-20, 10], legB: [-4, 0], legF: [4, 0]}} {...CAST.hero} look={[0, 0]} faceTurn={0.1} />
				</g>
				<text x={0} y={30} textAnchor="middle" fontSize={34} fontFamily={FONT} fill="#fff">ШКОЛЬНОЕ ШОУ</text>
				<text x={0} y={140} textAnchor="middle" fontSize={84} fontFamily={FONT} fontWeight={900} fill="#ffd34a">{v.toLocaleString('ru-RU')}</text>
				<text x={0} y={200} textAnchor="middle" fontSize={34} fontFamily={FONT} fill="#aab3d6">просмотров</text>
				{Array.from({length: 8}).map((_, i) => {
					const k = ((f / 16 + i / 8) % 1);
					return (
						<g key={i} transform={`translate(${200 + Math.sin(i * 3 + f / 10) * 40},${380 - k * 700}) scale(${0.5})`} opacity={1 - k}>
							<IconG i={i % 2 ? 'heart' : 'like'} />
						</g>
					);
				})}
			</g>
		</Board>
	);
};

/* Tanzania 1962 */
const Tanz: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const spread = interpolate(f, [10, dur * 0.85], [0, 1], clamp);
	return (
		<Board tint="#3a2a10">
			<T x={960} y={120} t={f - 2} size={60}>ТАНГАНЬИКА, 1962</T>
			<path d="M700,300 C820,240 1060,260 1180,320 C1300,380 1320,520 1260,640 C1220,760 1120,880 980,900 C860,910 760,820 720,700 C680,580 620,380 700,300 Z" fill="#c98a4a" stroke="#ffd34a" strokeWidth={4} />
			<text x={980} y={560} textAnchor="middle" fontSize={34} fontFamily={HAND} fill="#5a3a1a">Танзания</text>
			{Array.from({length: 60}).map((_, i) => {
				const a = random('tz' + i) * Math.PI * 2;
				const r = Math.sqrt(random('tr' + i)) * 260;
				const on = r / 260 < spread;
				return <circle key={i} cx={900 + Math.cos(a) * r * 1.2} cy={520 + Math.sin(a) * r} r={on ? 9 + 3 * Math.sin(f / 3 + i) : 5} fill={on ? '#ff2338' : '#7a5a3a'} />;
			})}
			<circle cx={900} cy={520} r={30 + 10 * Math.sin(f / 4)} fill="none" stroke="#ff2338" strokeWidth={6} />
			<T x={1560} y={430} t={f - dur * 0.3} size={56} c="#ffd34a">~1000 человек</T>
			<T x={1560} y={540} t={f - dur * 0.55} size={44}>школы закрыты</T>
			<T x={1560} y={620} t={f - dur * 0.55} size={44}>на месяцы</T>
			<Cite text="«Эпидемия смеха», Кашаша, 1962" t={f} />
		</Board>
	);
};

/* hands in ice water */
const Pain: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const a = interpolate(f, [8, dur * 0.45], [0, 0.55], clamp);
	const b = interpolate(f, [8, dur * 0.9], [0, 1], clamp);
	return (
		<Board tint="#102a4a">
			<T x={960} y={120} t={f - 2} size={56}>РУКА В ЛЕДЯНОЙ ВОДЕ</T>
			{[0, 1].map((i) => (
				<g key={i} transform={`translate(${560 + i * 800},640)`}>
					<rect x={-180} y={-60} width={360} height={260} rx={20} fill="#7ad0ff" opacity={0.5} />
					{[0, 1, 2].map((k) => (
						<rect key={k} x={-130 + k * 90} y={-20 + (k % 2) * 30} width={60} height={50} rx={8} fill="#e8f8ff" transform={`rotate(${k * 20 - 10})`} />
					))}
					<rect x={-28} y={-260} width={56} height={260} rx={28} fill="#f2c4a0" />
					<rect x={-200} y={-420} width={400} height={30} rx={15} fill="#2a3a5a" />
					<rect x={-200} y={-420} width={400 * (i ? b : a)} height={30} rx={15} fill={i ? '#ffd34a' : '#9aa3b5'} />
					<text x={0} y={-450} textAnchor="middle" fontSize={40} fontFamily={FONT} fill="#fff">{i ? 'посмеялись вместе' : 'без смеха'}</text>
					<text x={0} y={280} textAnchor="middle" fontSize={54} fontFamily={FONT} fontWeight={900} fill={i ? '#ffd34a' : '#cfd6df'}>{Math.round((i ? b : a) * 100)} с</text>
				</g>
			))}
			<Cite text="Dunbar и др., Оксфорд, 2011" t={f} />
		</Board>
	);
};

/* raised hand = serious (rule card) */
const Rule: React.FC<{b: Beat}> = () => {
	const {f} = useShot();
	return <RuleCard n="1" title="ПРАВИЛО" text="Поднял руку — значит, говоришь всерьёз" t={f} icon={<g transform="scale(1.6)"><rect x={-18} y={-80} width={36} height={110} rx={18} fill="#f4f1e6" /><rect x={-40} y={-70} width={16} height={60} rx={8} fill="#f4f1e6" transform="rotate(-20)" /></g>} />;
};

/* final question + like/subscribe */
const Outro: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	return (
		<AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 40%, #8a1424 0%, #4a0a14 55%, #1a0408 100%)'}}>
			<svg viewBox="0 0 1920 1080" width={1920} height={1080}>
				<g transform={`translate(560,${940})`}>
					<Stickman id="out" x={0} y={-157 * 1.9} scale={1.9} pose={{...idle(f, 1), armF: [155 + Math.sin(f / 2.2) * 18, 25]}} facing={1} {...CAST.hero} look={[0.3, 0]} faceTurn={0.3} mouth="smile" />
				</g>
				<g transform={`translate(1500,330) rotate(${Math.sin(f / 10) * 8}) scale(${sp(f - 4)})`}>
					<IconG i="q" s={2.6} />
				</g>
				<T x={1300} y={560} t={f - 8} size={60}>ЕСЛИ БЫ ТВОЙ ЮМОР</T>
				<T x={1300} y={650} t={f - 14} size={92} c="#ffd34a">БЫЛ 1000…</T>
				<T x={1300} y={780} t={f - dur * 0.35} size={48}>напиши худшую шутку в комментах</T>
				<g transform={`translate(1150,920) scale(${sp(f - dur * 0.55)})`}>
					<rect x={-150} y={-50} width={300} height={100} rx={50} fill="#ff2338" />
					<text y={16} textAnchor="middle" fontSize={44} fontFamily={FONT} fontWeight={900} fill="#fff">ЛАЙК</text>
				</g>
				<g transform={`translate(1500,920) scale(${sp(f - dur * 0.65)})`}>
					<rect x={-190} y={-50} width={380} height={100} rx={50} fill="#fff" />
					<text y={16} textAnchor="middle" fontSize={40} fontFamily={FONT} fontWeight={900} fill="#c62a2a">ПОДПИСКА</text>
				</g>
			</svg>
		</AbsoluteFill>
	);
};

/* laughter spreads through the city/county as a wave of dots */
const Spread: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	const r = interpolate(f, [0, dur], [40, 1100], clamp);
	return (
		<Board tint="#1a1040">
			<T x={960} y={120} t={f - 2} size={56}>СМЕХ ПЕРЕДАЁТСЯ, КАК ПРОСТУДА</T>
			{Array.from({length: 120}).map((_, i) => {
				const x = random('sx' + i) * 1800 + 60;
				const y = random('sy' + i) * 780 + 220;
				const d = Math.hypot(x - 960, y - 620);
				const on = d < r;
				return <circle key={i} cx={x} cy={y} r={on ? 12 + 4 * Math.sin(f / 3 + i) : 7} fill={on ? '#ffd34a' : '#4a4a7a'} />;
			})}
			<circle cx={960} cy={620} r={r} fill="none" stroke="#ffd34a" strokeWidth={4} opacity={0.4} />
		</Board>
	);
};

/* laugh = "I'm safe with you" */
const Safe: React.FC<{b: Beat}> = () => {
	const {f, dur} = useShot();
	return (
		<Board tint="#3a1030">
			<Fig id="sf1" x={760} y={900} s={1.5} who="hero" laugh t={f - 2} />
			<Fig id="sf2" x={1160} y={900} s={1.5} who="ben" laugh t={f - 6} />
			<g transform={`translate(960,${300 + Math.sin(f / 12) * 10}) scale(${sp(f - 10) * (1 + 0.06 * Math.sin(f / 5))})`}>
				<IconG i="heart" s={3} />
			</g>
			<T x={960} y={140} t={f - dur * 0.25} size={56}>«Мне с тобой безопасно»</T>
		</Board>
	);
};

export const CARDS: Record<string, React.FC<{b: Beat}>> = {ten: Ten, rats: Rats, brain: Brain, study: Study, x30: X30, views: Views, tanz: Tanz, pain: Pain, rule: Rule, outro: Outro, spread: Spread, safe: Safe};
