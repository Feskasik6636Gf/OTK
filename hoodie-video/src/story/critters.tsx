import React from 'react';
import {random} from 'remotion';
import {darken, lighten} from '../engine/color';

/* Animals and props of the jungle. Everything is drawn in local coordinates with the origin on the
   ground under the object, facing right; `face` mirrors it. Used inside <Svg>. */

type Mode = 'stand' | 'walk' | 'crouch' | 'lie' | 'sit';
export const Cat: React.FC<{
	kind: 'lion' | 'jaguar';
	x: number;
	y: number;
	s?: number;
	face?: 1 | -1;
	mode?: Mode;
	ph?: number;
	roar?: number;
	f: number;
	rot?: number;
	wet?: number;
	thin?: number;
	shadow?: boolean;
	eyesOnly?: boolean;
}> = ({kind, x, y, s = 1, face = 1, mode = 'stand', ph = 0, roar = 0, f, rot = 0, wet = 0, thin = 0, shadow = true}) => {
	const lion = kind === 'lion';
	const c = darken(lion ? '#dba44c' : '#e5a23a', wet * 0.25 + thin * 0.05);
	const dk = darken(c, 0.28);
	const by = mode === 'crouch' ? -66 : mode === 'lie' ? -40 : mode === 'sit' ? -100 : -118;
	const rx = (lion ? 108 : 98) * (1 - thin * 0.06);
	const ry = (lion ? 52 : 44) * (1 - thin * 0.22);
	const walking = mode === 'walk' || mode === 'stand';
	const sw = mode === 'walk' ? 38 : 0;
	const leg = (hx: number, hy: number, i: number, col: string) => {
		if (mode === 'lie') return <path key={i} d={`M${hx},${hy} L${hx + (i > 1 ? 70 : -30)},${-14}`} stroke={col} strokeWidth={28} strokeLinecap="round" />;
		const a = ph + i * 1.6;
		const dx = walking ? Math.sin(a) * sw : 0;
		const lift = mode === 'walk' ? Math.max(0, Math.cos(a)) * 22 : 0;
		const fx = hx + dx + (mode === 'crouch' && i > 1 ? 26 : 0);
		return (
			<g key={i}>
				<path d={`M${hx},${hy} L${fx},${-lift - 8}`} stroke={col} strokeWidth={28} strokeLinecap="round" />
				<ellipse cx={fx + 8} cy={-lift - 6} rx={20} ry={10} fill={col} />
			</g>
		);
	};
	const hxs = mode === 'lie' ? 112 : mode === 'crouch' ? 130 : 122;
	const hys = mode === 'lie' ? -64 : mode === 'crouch' ? by - 4 : by - 34 - (mode === 'sit' ? 20 : 0);
	const tilt = -roar * 16 + (mode === 'crouch' ? 10 : 0);
	const spots = lion
		? []
		: Array.from({length: 16}).map((_, i) => ({x: -80 + random('js' + i) * 170, y: by - 30 + random('jy' + i) * 56, r: 7 + random('jr' + i) * 5}));
	const tailY = by - 14 + Math.sin(f / 9) * 10;
	return (
		<g transform={`translate(${x},${y}) scale(${face * s},${s}) rotate(${rot})`}>
			{shadow ? <ellipse cx={0} cy={4} rx={150} ry={14} fill="#000" opacity={0.26} style={{filter: 'blur(5px)'}} /> : null}
			{/* tail */}
			<path d={`M${-rx + 12},${by - 8} C${-rx - 50},${tailY} ${-rx - 70},${tailY - 40} ${-rx - 40 - (lion ? 40 : 70)},${tailY - 80 + (mode === 'lie' ? 60 : 0)}`} stroke={dk} strokeWidth={14} fill="none" strokeLinecap="round" />
			{lion ? <ellipse cx={-rx - 82} cy={tailY - 80 + (mode === 'lie' ? 60 : 0)} rx={16} ry={22} fill="#6a3416" /> : null}
			{/* far legs */}
			{leg(-68, by + 12, 1, dk)}
			{leg(64, by + 12, 3, dk)}
			{/* body */}
			<ellipse cx={0} cy={by} rx={rx} ry={ry} fill={c} />
			<ellipse cx={4} cy={by + ry * 0.55} rx={rx * 0.8} ry={ry * 0.42} fill={lighten(c, 0.22)} opacity={0.8} />
			{spots.map((p, i) => (
				<g key={i}>
					<circle cx={p.x} cy={p.y} r={p.r} fill="none" stroke="#2a1708" strokeWidth={3.4} />
					<circle cx={p.x} cy={p.y} r={2.4} fill="#2a1708" />
				</g>
			))}
			{/* near legs */}
			{leg(-76, by + 14, 0, c)}
			{leg(56, by + 14, 2, c)}
			{/* head */}
			<g transform={`translate(${hxs},${hys}) rotate(${tilt})`}>
				{lion ? (
					<>
						<circle cx={-6} cy={4} r={82} fill="#7a3d18" />
						<circle cx={-2} cy={6} r={72} fill="#a2592a" />
						{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
							const a = (i / 8) * Math.PI * 2;
							return <circle key={i} cx={-6 + Math.cos(a) * 74} cy={4 + Math.sin(a) * 74} r={18} fill="#8a4a1e" />;
						})}
					</>
				) : (
					<>
						<circle cx={-18} cy={-38} r={14} fill={dk} />
						<circle cx={16} cy={-40} r={14} fill={dk} />
					</>
				)}
				<circle cx={0} cy={0} r={lion ? 48 : 42} fill={c} />
				{lion ? (
					<>
						<circle cx={-26} cy={-42} r={13} fill={c} />
						<circle cx={20} cy={-44} r={13} fill={c} />
					</>
				) : (
					<>
						{[[-10, -22], [8, -26], [-24, -8], [24, -14]].map((p, i) => (
							<circle key={i} cx={p[0]} cy={p[1]} r={4.5} fill="#2a1708" />
						))}
					</>
				)}
				{/* muzzle + open jaw */}
				{roar > 0.05 ? (
					<g>
						<path d={`M16,10 L${56},${6 + roar * 6} L${50},${30 + roar * 30} L${12},${34 + roar * 14} Z`} fill="#7a1022" />
						<path d={`M24,12 L30,${24 + roar * 8} L36,12 Z M42,10 L47,${22 + roar * 8} L52,8 Z`} fill="#fff" />
					</g>
				) : null}
				<ellipse cx={30} cy={16} rx={26} ry={19} fill="#f3dcaa" />
				<path d="M44,0 L58,6 L48,14 Z" fill="#3a1a12" />
				{roar > 0.05 ? null : <path d="M30,22 q8,8 18,-2" stroke="#3a1a12" strokeWidth={3} fill="none" strokeLinecap="round" />}
				<ellipse cx={20} cy={-10} rx={7} ry={6} fill="#fff" />
				<circle cx={22} cy={-9} r={3.6} fill="#1a1208" />
				<path d="M10,-20 L32,-14" stroke="#3a1a12" strokeWidth={4} strokeLinecap="round" />
			</g>
		</g>
	);
};

/* ----------------------------------- tree ---------------------------------- */
export const Tree: React.FC<{x: number; y: number; s?: number; fall?: number; shake?: number; f: number; h?: number; w?: number; dir?: 1 | -1; col?: string; leaves?: number}> = ({
	x,
	y,
	s = 1,
	fall = 0,
	shake = 0,
	f,
	h = 560,
	w = 84,
	dir = 1,
	col = '#6a4a2c',
	leaves = 1,
}) => {
	const sx = Math.sin(f * 2.1) * shake;
	return (
		<g transform={`translate(${x + sx},${y}) rotate(${fall * dir}) scale(${s})`}>
			<path d={`M${-w / 2},12 L${-w * 0.36},${-h} L${w * 0.36},${-h} L${w / 2},12 Z`} fill={col} />
			<path d={`M${-w * 0.3},0 L${-w * 0.22},${-h}`} stroke={lighten(col, 0.18)} strokeWidth={8} opacity={0.6} />
			{[0.25, 0.5, 0.75].map((k, i) => (
				<path key={i} d={`M${-w * 0.45},${-h * k} q${w * 0.45},12 ${w * 0.9},0`} stroke={darken(col, 0.3)} strokeWidth={5} fill="none" opacity={0.7} />
			))}
			{leaves > 0 ? (
				<g>
					<ellipse cx={0} cy={-h - 40} rx={170} ry={108} fill="#2f7a46" />
					<ellipse cx={-110} cy={-h} rx={120} ry={80} fill="#276c3e" />
					<ellipse cx={116} cy={-h - 10} rx={120} ry={84} fill="#3a9054" />
					<path d={`M${-60},${-h + 40} q8,90 -6,150 M${70},${-h + 36} q-10,70 6,130`} stroke="#2a6a3a" strokeWidth={7} fill="none" strokeLinecap="round" />
				</g>
			) : null}
		</g>
	);
};

/* a hut of whole logs; build 0..1 stacks the rows, roof comes last */
export const LogHut: React.FC<{x: number; y: number; s?: number; build?: number}> = ({x, y, s = 1, build = 1}) => {
	const rows = 7;
	const shown = build * (rows + 2);
	return (
		<g transform={`translate(${x},${y}) scale(${s})`}>
			<ellipse cx={0} cy={6} rx={320} ry={16} fill="#000" opacity={0.25} style={{filter: 'blur(6px)'}} />
			{Array.from({length: rows}).map((_, i) => {
				const k = Math.max(0, Math.min(1, shown - i));
				if (k <= 0) return null;
				const yy = -i * 40 - 36 - (1 - k) * 200;
				return (
					<g key={i} opacity={Math.min(1, k * 3)}>
						<rect x={-250} y={yy} width={500} height={40} rx={20} fill={i % 2 ? '#7a5632' : '#8a6238'} />
						<ellipse cx={-250} cy={yy + 20} rx={14} ry={20} fill="#c79a62" />
						<ellipse cx={250} cy={yy + 20} rx={14} ry={20} fill="#c79a62" />
						<path d={`M${-200},${yy + 12} h60 M${60},${yy + 26} h90`} stroke="#5a3e20" strokeWidth={3} opacity={0.6} />
					</g>
				);
			})}
			{shown > rows ? (
				<g opacity={Math.min(1, (shown - rows) * 2)} transform={`translate(0,${-(Math.max(0, 2 - (shown - rows)) * 90)})`}>
					<path d={`M-300,${-rows * 40 - 30} L0,${-rows * 40 - 190} L300,${-rows * 40 - 30} Z`} fill="#5a3a1c" />
					{[-210, -120, -30, 60, 150].map((p, i) => (
						<rect key={i} x={p} y={-rows * 40 - 150 + Math.abs(p) * 0.02} width={46} height={150} rx={20} fill="#6e4826" transform={`rotate(${p < 0 ? -22 : 22} ${p + 23} ${-rows * 40 - 75})`} />
					))}
					<ellipse cx={0} cy={-rows * 40 - 150} rx={240} ry={44} fill="#2f7a46" />
				</g>
			) : null}
			{shown >= rows ? <rect x={-62} y={-190} width={124} height={190} rx={14} fill="#1a0f08" /> : null}
		</g>
	);
};

export const Pot: React.FC<{x: number; y: number; s?: number; f: number; steam?: number}> = ({x, y, s = 1, f, steam = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<path d="M-70,-130 C-110,-100 -100,-20 -50,-6 L50,-6 C100,-20 110,-100 70,-130 Z" fill="#b8683a" />
		<path d="M-60,-120 C-80,-90 -76,-40 -50,-20" stroke="#d98a58" strokeWidth={8} fill="none" opacity={0.7} strokeLinecap="round" />
		<ellipse cx={0} cy={-130} rx={74} ry={16} fill="#8a4a24" />
		<ellipse cx={0} cy={-130} rx={62} ry={11} fill="#7ac4e0" />
		{[0, 1, 2, 3].map((i) => {
			const t = ((f * 0.8 + i * 22) % 90) / 90;
			return <circle key={i} cx={Math.sin(i * 2 + t * 5) * 28} cy={-140 - t * 110} r={10 + t * 20} fill="#fff" opacity={0.5 * (1 - t) * steam} />;
		})}
	</g>
);

/* a rock with a painted face (named Theo): eyes, glasses and a smile */
export const Rock: React.FC<{x: number; y: number; s?: number; face?: boolean; f?: number; glasses?: boolean}> = ({x, y, s = 1, face, f = 0, glasses}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<ellipse cx={0} cy={4} rx={86} ry={11} fill="#000" opacity={0.25} style={{filter: 'blur(4px)'}} />
		<path d="M-84,0 C-96,-60 -52,-116 0,-118 C60,-118 98,-64 86,0 Z" fill="#8a8f98" />
		<path d="M-60,-30 C-70,-70 -40,-100 -6,-104" stroke="#b6bbc4" strokeWidth={10} fill="none" strokeLinecap="round" opacity={0.7} />
		<path d="M30,-20 l30,-30 M48,-80 l26,12" stroke="#6d727a" strokeWidth={4} opacity={0.7} />
		{face ? (
			<g>
				<ellipse cx={-22} cy={-66} rx={13} ry={(f % 90 < 4 ? 2 : 12)} fill="#fff" />
				<ellipse cx={24} cy={-66} rx={13} ry={(f % 90 < 4 ? 2 : 12)} fill="#fff" />
				<circle cx={-18} cy={-64} r={5} fill="#111" />
				<circle cx={28} cy={-64} r={5} fill="#111" />
				<path d="M-22,-36 q22,22 46,0" stroke="#fff" strokeWidth={5} fill="none" strokeLinecap="round" />
				{glasses ? (
					<g stroke="#f2b21c" strokeWidth={4} fill="none">
						<circle cx={-22} cy={-66} r={19} />
						<circle cx={24} cy={-66} r={19} />
						<line x1={-3} y1={-66} x2={5} y2={-66} />
					</g>
				) : null}
			</g>
		) : null}
	</g>
);

export const Pod: React.FC<{x: number; y: number; s?: number; crack?: number}> = ({x, y, s = 1, crack = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		{crack < 0.05 ? (
			<g>
				<circle cx={0} cy={-46} r={46} fill="#6a4524" />
				<path d="M-30,-70 q14,-18 36,-14 M-36,-40 q10,24 34,28 M12,-26 q24,6 30,-22" stroke="#8a5e34" strokeWidth={5} fill="none" strokeLinecap="round" />
				<circle cx={-14} cy={-62} r={9} fill="#9a6e40" opacity={0.7} />
			</g>
		) : (
			<g>
				<path d={`M-46,-46 A46,46 0 0 1 0,-92 L0,-46 Z`} fill="#6a4524" transform={`translate(${-crack * 40},${-crack * 30}) rotate(${-crack * 30} -20 -46)`} />
				<path d={`M0,-92 A46,46 0 0 1 46,-46 L0,-46 Z`} fill="#5a3a1c" transform={`translate(${crack * 40},${-crack * 30}) rotate(${crack * 30} 20 -46)`} />
				<path d="M-46,-46 A46,46 0 0 0 0,0 L0,-46 Z" fill="#6a4524" />
				<path d="M0,-46 L0,0 A46,46 0 0 0 46,-46 Z" fill="#5a3a1c" />
				{[-24, -8, 8, 24].map((p, i) => (
					<path key={i} d={`M${p - 8},-30 q8,-30 16,0 Z`} fill="#e8d6b0" stroke="#b89c70" strokeWidth={2} transform={`translate(${p * crack * 1.4},${-crack * 26 - i * 4})`} />
				))}
			</g>
		)}
	</g>
);

export const Capy: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; f?: number; ph?: number}> = ({x, y, s = 1, face = 1, f = 0, ph = 0}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s})`}>
		<ellipse cx={0} cy={4} rx={80} ry={9} fill="#000" opacity={0.25} />
		{[-46, -26, 28, 48].map((p, i) => (
			<rect key={i} x={p - 9} y={-34 + Math.max(0, Math.sin(ph + i * 1.5)) * -8} width={18} height={36} rx={8} fill="#6a4a2a" />
		))}
		<ellipse cx={0} cy={-52} rx={76} ry={42} fill="#8a6038" />
		<ellipse cx={4} cy={-34} rx={58} ry={18} fill="#a07848" opacity={0.7} />
		<path d="M62,-84 C98,-92 118,-66 112,-42 C104,-30 70,-34 56,-46 Z" fill="#8a6038" />
		<ellipse cx={104} cy={-56} rx={12} ry={14} fill="#5a3a1c" />
		<circle cx={82} cy={-70} r={4.5} fill="#111" />
		<ellipse cx={66} cy={-92} rx={9} ry={7} fill="#6a4524" />
	</g>
);

export const Monkey: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; f?: number; throwT?: number}> = ({x, y, s = 1, face = 1, f = 0, throwT = -1}) => {
	const arm = throwT >= 0 && throwT < 14 ? -80 + throwT * 12 : 20 + Math.sin(f / 6) * 8;
	return (
		<g transform={`translate(${x},${y}) scale(${face * s},${s})`}>
			<path d={`M-34,-50 C-100,-40 -110,-110 -60,-130`} stroke="#5a3a24" strokeWidth={12} fill="none" strokeLinecap="round" />
			<rect x={-26} y={-96} width={52} height={86} rx={24} fill="#7a5436" />
			<ellipse cx={0} cy={-52} rx={20} ry={30} fill="#d9b48a" />
			<rect x={-30} y={-12} width={18} height={14} rx={7} fill="#5a3a24" />
			<rect x={12} y={-12} width={18} height={14} rx={7} fill="#5a3a24" />
			<circle cx={0} cy={-118} r={34} fill="#7a5436" />
			<ellipse cx={8} cy={-110} rx={24} ry={20} fill="#e0bf94" />
			<circle cx={-6} cy={-124} r={4.5} fill="#111" />
			<circle cx={16} cy={-124} r={4.5} fill="#111" />
			<path d="M0,-102 q8,6 16,0" stroke="#3a2010" strokeWidth={3} fill="none" />
			<circle cx={-32} cy={-120} r={12} fill="#7a5436" />
			<g transform={`translate(20,-80) rotate(${arm})`}>
				<rect x={-7} y={0} width={14} height={50} rx={7} fill="#7a5436" />
				<circle cx={0} cy={56} r={11} fill="#d9b48a" />
				{throwT < 0 ? <circle cx={0} cy={72} r={14} fill="#e8602a" /> : null}
			</g>
		</g>
	);
};

export const Fruit: React.FC<{x: number; y: number; r?: number; rot?: number}> = ({x, y, r = 16, rot = 0}) => (
	<g transform={`translate(${x},${y}) rotate(${rot})`}>
		<circle r={r} fill="#e8602a" />
		<circle cx={-r * 0.3} cy={-r * 0.3} r={r * 0.25} fill="#ffa060" />
		<path d={`M0,${-r} q6,-12 14,-10`} stroke="#3a7a2a" strokeWidth={4} fill="none" />
	</g>
);

export const Fish: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; rot?: number; f?: number}> = ({x, y, s = 1, face = 1, rot = 0, f = 0}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s}) rotate(${rot})`}>
		<path d={`M-70,0 L-104,${-26 + Math.sin(f / 2) * 6} L-104,${26 + Math.sin(f / 2) * 6} Z`} fill="#6c97b4" />
		<ellipse cx={0} cy={0} rx={76} ry={32} fill="#9cc4de" />
		<ellipse cx={4} cy={14} rx={58} ry={14} fill="#e6f1f8" opacity={0.8} />
		<path d="M-20,-30 q20,-26 50,-4" fill="#6c97b4" />
		<circle cx={50} cy={-6} r={7} fill="#fff" />
		<circle cx={52} cy={-6} r={3.5} fill="#111" />
		<path d="M-30,-10 q10,10 0,22 M-10,-14 q10,14 0,28" stroke="#6c97b4" strokeWidth={3} fill="none" />
	</g>
);

export const Ant: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; f?: number}> = ({x, y, s = 1, face = 1, f = 0}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s})`}>
		{[-1, 0, 1].map((i) => (
			<g key={i} stroke="#3a0e08" strokeWidth={7} fill="none" strokeLinecap="round">
				<path d={`M${i * 26},-30 L${i * 40 - 22},${-4 + Math.sin(f / 3 + i) * 5}`} />
				<path d={`M${i * 26},-30 L${i * 40 + 12},${-2 + Math.cos(f / 3 + i) * 5}`} />
			</g>
		))}
		<ellipse cx={-62} cy={-44} rx={52} ry={36} fill="#5a160c" />
		<ellipse cx={0} cy={-42} rx={28} ry={22} fill="#6e1c10" />
		<circle cx={54} cy={-52} r={30} fill="#7a2214" />
		<path d="M76,-62 q36,-8 40,12 M76,-44 q34,10 38,-6" stroke="#2a0a06" strokeWidth={8} fill="none" strokeLinecap="round" />
		<path d="M66,-80 q20,-40 50,-46" stroke="#2a0a06" strokeWidth={4} fill="none" strokeLinecap="round" />
		<circle cx={60} cy={-58} r={5} fill="#ffcf40" />
		<ellipse cx={-70} cy={-56} rx={26} ry={12} fill="#a04030" opacity={0.5} />
	</g>
);

export const Mosq: React.FC<{x: number; y: number; s?: number; f?: number}> = ({x, y, s = 1, f = 0}) => (
	<g transform={`translate(${x},${y + Math.sin(f / 5) * 8}) scale(${s})`}>
		<ellipse cx={-6} cy={-8} rx={30} ry={14} fill="#fff" opacity={0.35} transform={`rotate(${-24 + Math.sin(f * 1.6) * 20} -6 -8)`} />
		<ellipse cx={4} cy={-10} rx={30} ry={14} fill="#fff" opacity={0.35} transform={`rotate(${24 - Math.sin(f * 1.6) * 20} 4 -10)`} />
		<ellipse cx={0} cy={0} rx={30} ry={10} fill="#2a2a30" />
		<circle cx={34} cy={0} r={9} fill="#2a2a30" />
		<path d="M42,2 L72,12" stroke="#2a2a30" strokeWidth={3} />
		{[-14, 0, 14].map((p, i) => (
			<path key={i} d={`M${p},6 l${-6 + i * 6},20`} stroke="#2a2a30" strokeWidth={2} />
		))}
	</g>
);

export const Larva: React.FC<{x: number; y: number; s?: number; f?: number; i?: number}> = ({x, y, s = 1, f = 0, i = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		{[0, 1, 2, 3, 4].map((k) => (
			<ellipse key={k} cx={k * 22 - 40} cy={-14 + Math.sin(f / 4 + k * 0.8 + i) * 6} rx={15 - Math.abs(k - 2) * 1.6} ry={14} fill={k === 4 ? '#f6e6a8' : '#fff4d0'} stroke="#e2cf94" strokeWidth={2} />
		))}
		<circle cx={52} cy={-13 + Math.sin(f / 4 + 3.2 + i) * 6} r={2.6} fill="#222" />
	</g>
);

export const Eyes: React.FC<{x: number; y: number; s?: number; o?: number; c?: string; gap?: number}> = ({x, y, s = 1, o = 1, c = '#ffd23a', gap = 34}) => (
	<g transform={`translate(${x},${y}) scale(${s})`} opacity={o}>
		{[-gap / 2, gap / 2].map((p, i) => (
			<g key={i}>
				<circle cx={p} cy={0} r={22} fill={c} opacity={0.22} />
				<ellipse cx={p} cy={0} rx={10} ry={7} fill={c} />
				<ellipse cx={p} cy={0} rx={2.6} ry={6} fill="#1a0f00" />
			</g>
		))}
	</g>
);

export const Caiman: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; f?: number}> = ({x, y, s = 1, face = 1, f = 0}) => (
	<g transform={`translate(${x},${y + Math.sin(f / 14) * 4}) scale(${face * s},${s})`}>
		<path d="M-120,0 C-60,-26 20,-22 60,-14 L140,-10 L146,6 L60,12 C0,16 -60,12 -120,0 Z" fill="#4b6a3a" />
		<path d="M-110,-4 l16,-18 l16,16 l16,-16 l16,16 l16,-14 l16,14" fill="#3a5a2c" />
		<circle cx={30} cy={-22} r={8} fill="#e8d44a" />
		<circle cx={32} cy={-22} r={3} fill="#111" />
		<path d="M70,4 l8,-8 l8,8 l8,-8 l8,8 l8,-8" stroke="#fff" strokeWidth={3} fill="none" />
	</g>
);

export const Heli: React.FC<{x: number; y: number; s?: number; f: number; face?: 1 | -1; tilt?: number}> = ({x, y, s = 1, f, face = 1, tilt = 0}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s}) rotate(${tilt})`}>
		<ellipse cx={0} cy={60} rx={170} ry={14} fill="#000" opacity={0.0} />
		<path d="M-210,-6 L-90,-18 L-90,14 L-210,8 Z" fill="#b8c0cc" />
		<path d="M-210,-6 l-24,-40 l30,0 l22,38 Z" fill="#ff2340" />
		<ellipse cx={0} cy={0} rx={112} ry={62} fill="#f2f4f8" />
		<path d="M-112,0 A112,62 0 0 0 112,0 Z" fill="#c9ced8" />
		<path d="M20,-52 C80,-52 112,-22 112,2 L22,2 Z" fill="#7ec8ee" />
		<path d="M-60,-30 h50 v30 h-50 Z" fill="#7ec8ee" opacity={0.7} />
		<rect x={-112} y={4} width={224} height={8} fill="#ff2340" />
		<rect x={-6} y={-76} width={12} height={22} fill="#3a404c" />
		<ellipse cx={0} cy={-78} rx={Math.abs(Math.cos(f * 1.3)) * 240 + 16} ry={5} fill="#3a404c" opacity={0.85} />
		<ellipse cx={0} cy={-78} rx={300} ry={9} fill="#fff" opacity={0.18} />
		<ellipse cx={-226} cy={-26} rx={Math.abs(Math.sin(f * 1.7)) * 26 + 3} ry={26} fill="#3a404c" opacity={0.5} />
		<path d="M-80,70 L100,70 M-50,58 L-50,70 M60,58 L60,70" stroke="#3a404c" strokeWidth={8} strokeLinecap="round" />
	</g>
);

export const Burger: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s}) rotate(${rot})`}>
		<path d="M-40,-24 C-40,-62 40,-62 40,-24 Z" fill="#e0a050" />
		<circle cx={-14} cy={-42} r={2.4} fill="#fff0c8" />
		<circle cx={8} cy={-48} r={2.4} fill="#fff0c8" />
		<circle cx={20} cy={-38} r={2.4} fill="#fff0c8" />
		<path d="M-44,-24 q8,10 16,0 q8,10 16,0 q8,10 16,0 q8,10 16,0 q8,10 16,0 L44,-18 L-44,-18 Z" fill="#5aba40" />
		<rect x={-42} y={-20} width={84} height={12} rx={6} fill="#6a3a1c" />
		<path d="M-40,-8 h80 l-6,10 h-68 Z" fill="#f2c438" />
		<path d="M-40,2 C-40,12 40,12 40,2 Z" fill="#e0a050" />
	</g>
);

/* wristband with the big red button */
export const Band: React.FC<{x: number; y: number; s?: number; f: number; press?: number}> = ({x, y, s = 1, f, press = 0}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<defs>
			<radialGradient id="btnglow">
				<stop offset="0" stopColor="#ff4a5a" stopOpacity="0.8" />
				<stop offset="1" stopColor="#ff4a5a" stopOpacity="0" />
			</radialGradient>
		</defs>
		<circle cx={0} cy={0} r={150 + Math.sin(f / 7) * 12} fill="url(#btnglow)" />
		<rect x={-210} y={-44} width={420} height={88} rx={40} fill="#14151c" />
		<rect x={-200} y={-34} width={400} height={16} rx={8} fill="#2a2c38" />
		<circle cx={0} cy={0} r={62} fill="#2a2c38" />
		<circle cx={0} cy={press * 8} r={50 - press * 4} fill="#d4122a" />
		<circle cx={-14} cy={-14 + press * 8} r={14} fill="#ff6a78" opacity={0.7} />
	</g>
);

export const Spark: React.FC<{x: number; y: number; t: number; c?: string; n?: number; r?: number}> = ({x, y, t, c = '#ffe08a', n = 12, r = 120}) => {
	if (t < 0 || t > 22) return null;
	const k = t / 22;
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const a = (i / n) * Math.PI * 2 + random('sp' + i);
				const d = r * (0.4 + random('sd' + i) * 0.7) * k;
				return <circle key={i} cx={x + Math.cos(a) * d} cy={y + Math.sin(a) * d + k * k * 30} r={6 * (1 - k)} fill={c} opacity={1 - k} />;
			})}
		</g>
	);
};
