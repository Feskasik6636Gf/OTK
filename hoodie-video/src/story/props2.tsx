import React from 'react';
import {random} from 'remotion';
import {FONT} from '../kit/ui';
import {darken, lighten} from '../engine/color';

/* small props and labels, local coordinates, used inside <Svg> */

export const Tag: React.FC<{x: number; y: number; text: string; sub?: string; k?: number; c?: string; size?: number}> = ({x, y, text, sub, k = 1, c = '#ffd23a', size = 36}) => {
	if (k <= 0.01) return null;
	const w = Math.max(text.length, (sub ?? '').length * 0.7) * size * 0.64 + 44;
	const h = size * (sub ? 2.5 : 1.7);
	return (
		<g transform={`translate(${x},${y}) scale(${k})`}>
			<rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h * 0.3} fill="#14060c" opacity={0.9} stroke={c} strokeWidth={4} />
			<text x={0} y={sub ? -size * 0.12 : size * 0.34} textAnchor="middle" fontSize={size} fontFamily={FONT} fontWeight={900} fill="#fff">
				{text}
			</text>
			{sub ? (
				<text x={0} y={size * 0.82} textAnchor="middle" fontSize={size * 0.6} fontFamily={FONT} fontWeight={700} fill={c}>
					{sub}
				</text>
			) : null}
		</g>
	);
};

export const Crown: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = 0}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<path d="M-60,0 L-70,-70 L-32,-36 L0,-86 L32,-36 L70,-70 L60,0 Z" fill="#ffc72a" stroke="#b8860b" strokeWidth={5} strokeLinejoin="round" />
		<rect x={-62} y={-6} width={124} height={16} rx={6} fill="#e8a010" />
		<circle cx={-70} cy={-72} r={9} fill="#ff2340" />
		<circle cx={0} cy={-88} r={10} fill="#3aa0ff" />
		<circle cx={70} cy={-72} r={9} fill="#ff2340" />
	</g>
);

export const Zebra: React.FC<{x: number; y: number; s?: number; face?: 1 | -1; ph?: number}> = ({x, y, s = 1, face = 1, ph = 0}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s})`}>
		{[-50, -30, 34, 54].map((p, i) => (
			<rect key={i} x={p - 7} y={-62 + Math.max(0, Math.sin(ph + i * 1.6)) * -12} width={14} height={64} rx={6} fill="#f2f2f2" stroke="#111" strokeWidth={3} />
		))}
		<ellipse cx={0} cy={-84} rx={78} ry={36} fill="#f6f6f6" />
		{[-50, -30, -10, 10, 30, 50].map((p, i) => (
			<path key={i} d={`M${p},-116 q8,30 -4,62`} stroke="#111" strokeWidth={8} fill="none" strokeLinecap="round" />
		))}
		<path d="M60,-100 L96,-138 L124,-120 L108,-82 Z" fill="#f2f2f2" stroke="#111" strokeWidth={3} />
		<path d="M64,-118 L78,-150 L88,-124" fill="#111" />
		<circle cx={104} cy={-110} r={4} fill="#111" />
		<path d="M-78,-92 q-30,10 -26,50" stroke="#111" strokeWidth={8} fill="none" strokeLinecap="round" />
	</g>
);

export const Bus: React.FC<{x: number; y: number; s?: number; face?: 1 | -1}> = ({x, y, s = 1, face = 1}) => (
	<g transform={`translate(${x},${y}) scale(${face * s},${s})`}>
		<rect x={-170} y={-150} width={340} height={120} rx={18} fill="#f2b21c" />
		{[-130, -60, 10, 80].map((p, i) => (
			<rect key={i} x={p} y={-134} width={56} height={44} rx={8} fill="#cfeaf7" />
		))}
		<rect x={-170} y={-70} width={340} height={10} fill="#d4892a" />
		<circle cx={-100} cy={-30} r={28} fill="#222" />
		<circle cx={100} cy={-30} r={28} fill="#222" />
		<circle cx={-100} cy={-30} r={12} fill="#aaa" />
		<circle cx={100} cy={-30} r={12} fill="#aaa" />
	</g>
);

export const Phone: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-56} y={-100} width={112} height={200} rx={20} fill="#1b1d28" stroke="#9aa0b8" strokeWidth={4} />
		<rect x={-46} y={-84} width={92} height={160} rx={8} fill="#4aa8ff" />
		<path d="M-30,-40 h60 M-30,-10 h40 M-30,20 h52" stroke="#fff" strokeWidth={6} strokeLinecap="round" />
		<circle cx={0} cy={86} r={6} fill="#9aa0b8" />
	</g>
);

export const Spear: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = -30}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<rect x={-6} y={-130} width={12} height={270} rx={6} fill="#8a5e34" />
		<path d="M0,-210 L22,-124 L-22,-124 Z" fill="#cfd5dc" stroke="#7a828c" strokeWidth={4} />
	</g>
);

export const XMark: React.FC<{x: number; y: number; k: number; s?: number}> = ({x, y, k, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`} opacity={Math.min(1, k * 3)}>
		<line x1={-110} y1={-110} x2={-110 + 220 * Math.min(1, k * 2)} y2={-110 + 220 * Math.min(1, k * 2)} stroke="#ff2340" strokeWidth={26} strokeLinecap="round" />
		<line x1={110} y1={-110} x2={110 - 220 * Math.max(0, Math.min(1, k * 2 - 0.6))} y2={-110 + 220 * Math.max(0, Math.min(1, k * 2 - 0.6))} stroke="#ff2340" strokeWidth={26} strokeLinecap="round" />
	</g>
);

export const Megaphone: React.FC = () => (
	<g transform="rotate(-40)">
		<path d="M0,-12 L60,-34 L60,34 L0,12 Z" fill="#e8402a" />
		<rect x={-18} y={-14} width={20} height={28} rx={6} fill="#3a3a44" />
		<ellipse cx={60} cy={0} rx={10} ry={36} fill="#ffb09a" />
	</g>
);
export const Wrench: React.FC = () => (
	<g transform="rotate(-50)">
		<rect x={-6} y={-70} width={12} height={90} rx={6} fill="#aab3c0" />
		<circle cx={0} cy={-78} r={20} fill="#aab3c0" />
		<rect x={-8} y={-102} width={16} height={22} fill="#e9a74a" />
	</g>
);
export const Tooth: React.FC = () => (
	<g transform="translate(6,-26)">
		<path d="M-22,-24 C-26,-44 -4,-48 0,-38 C4,-48 26,-44 22,-24 C24,0 14,26 8,26 C4,26 4,6 0,6 C-4,6 -4,26 -8,26 C-14,26 -24,0 -22,-24 Z" fill="#fff" stroke="#aab" strokeWidth={3} />
	</g>
);
export const PizzaBox: React.FC = () => (
	<g transform="translate(14,-24) rotate(-14)">
		<rect x={-46} y={-14} width={92} height={22} rx={3} fill="#d9a05c" />
		<rect x={-46} y={-14} width={92} height={7} fill="#c0813c" />
		<circle cx={0} cy={-3} r={7} fill="#e85a3a" />
	</g>
);
export const Calc: React.FC = () => (
	<g transform="translate(10,-22) rotate(-10)">
		<rect x={-20} y={-30} width={40} height={56} rx={6} fill="#2a2d3a" />
		<rect x={-14} y={-24} width={28} height={12} fill="#9be8a8" />
		{[0, 1, 2].map((r) => [0, 1, 2].map((c) => <rect key={r + '-' + c} x={-14 + c * 10} y={-6 + r * 10} width={8} height={7} rx={2} fill="#ccd" />))}
	</g>
);
export const Pillow: React.FC = () => (
	<g transform="translate(10,-20) rotate(-12)">
		<rect x={-40} y={-24} width={80} height={46} rx={20} fill="#f4f1ff" stroke="#b8b0e0" strokeWidth={3} />
		<path d="M-20,-4 h40" stroke="#b8b0e0" strokeWidth={3} />
	</g>
);
export const Pitchfork: React.FC = () => (
	<g transform="translate(8,-16) rotate(-6)">
		<rect x={-4} y={-150} width={8} height={190} rx={4} fill="#8a5e34" />
		<path d="M-22,-150 v-34 M0,-150 v-40 M22,-150 v-34 M-22,-150 h44" stroke="#bfc6cf" strokeWidth={7} strokeLinecap="round" fill="none" />
	</g>
);
export const Clipboard: React.FC = () => (
	<g transform="translate(10,-24) rotate(-8)">
		<rect x={-30} y={-40} width={60} height={80} rx={6} fill="#f6f1de" stroke="#9aa" strokeWidth={3} />
		<path d="M-18,-20 h36 M-18,-6 h30 M-18,8 h36 M-18,22 h20" stroke="#4a78c8" strokeWidth={4} strokeLinecap="round" />
	</g>
);

export const Confetti: React.FC<{x: number; y: number; t: number; n?: number}> = ({x, y, t, n = 40}) => {
	if (t < 0 || t > 60) return null;
	const cols = ['#ff2340', '#ffd23a', '#3aa0ff', '#3ad07a', '#ff7ad9'];
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const a = -Math.PI / 2 + (random('cf' + i) - 0.5) * 2.4;
				const v = 10 + random('cv' + i) * 16;
				const px = x + Math.cos(a) * v * t * 0.9;
				const py = y + Math.sin(a) * v * t * 0.9 + 0.5 * 0.9 * t * t * 0.6;
				return <rect key={i} x={px} y={py} width={12} height={20} fill={cols[i % 5]} transform={`rotate(${t * (6 + i % 9)} ${px} ${py})`} opacity={Math.min(1, (60 - t) / 20)} />;
			})}
		</g>
	);
};

export const Ring: React.FC<{x: number; y: number; t: number; c?: string; r?: number; n?: number}> = ({x, y, t, c = '#fff', r = 500, n = 3}) => {
	if (t < 0) return null;
	return (
		<g>
			{Array.from({length: n}).map((_, i) => {
				const k = (t - i * 8) / 40;
				if (k < 0 || k > 1) return null;
				return <circle key={i} cx={x} cy={y} r={20 + r * k} fill="none" stroke={c} strokeWidth={10 * (1 - k)} opacity={1 - k} />;
			})}
		</g>
	);
};

export const SpeedLines: React.FC<{f: number; y0?: number; y1?: number; dir?: 1 | -1; c?: string}> = ({f, y0 = 420, y1 = 900, dir = 1, c = '#fff'}) => (
	<g>
		{Array.from({length: 16}).map((_, i) => {
			const y = y0 + random('sl' + i) * (y1 - y0);
			const len = 160 + random('sll' + i) * 260;
			const x = ((f * (38 + i * 4) * dir + random('slx' + i) * 3000) % 3000) - 500;
			return <line key={i} x1={dir > 0 ? x : 2400 - x} y1={y} x2={(dir > 0 ? x : 2400 - x) - len * dir} y2={y} stroke={c} strokeWidth={4 + (i % 3) * 2} opacity={0.35} strokeLinecap="round" />;
		})}
	</g>
);

export const Thermo: React.FC<{x: number; y: number; k: number; s?: number}> = ({x, y, k, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-16} y={-150} width={32} height={150} rx={16} fill="#f4f4f8" stroke="#334" strokeWidth={5} />
		<circle cx={0} cy={10} r={30} fill="#f4f4f8" stroke="#334" strokeWidth={5} />
		<circle cx={0} cy={10} r={20} fill="#ff2340" />
		<rect x={-8} y={-130 + (1 - k) * 130} width={16} height={130 * k + 10} rx={8} fill="#ff2340" />
	</g>
);

export const Germ: React.FC<{x: number; y: number; s?: number; f?: number; c?: string; angry?: boolean}> = ({x, y, s = 1, f = 0, c = '#7ad84a', angry = true}) => (
	<g transform={`translate(${x},${y + Math.sin(f / 8 + x) * 6}) scale(${s})`}>
		{Array.from({length: 10}).map((_, i) => {
			const a = (i / 10) * Math.PI * 2 + f / 60;
			return (
				<g key={i}>
					<line x1={Math.cos(a) * 40} y1={Math.sin(a) * 40} x2={Math.cos(a) * 60} y2={Math.sin(a) * 60} stroke={darken(c, 0.2)} strokeWidth={7} strokeLinecap="round" />
					<circle cx={Math.cos(a) * 64} cy={Math.sin(a) * 64} r={8} fill={c} />
				</g>
			);
		})}
		<circle cx={0} cy={0} r={46} fill={c} />
		<circle cx={-10} cy={-12} r={16} fill={lighten(c, 0.3)} opacity={0.6} />
		<ellipse cx={-14} cy={-4} rx={9} ry={12} fill="#fff" />
		<ellipse cx={14} cy={-4} rx={9} ry={12} fill="#fff" />
		<circle cx={-12} cy={-2} r={4.5} fill="#111" />
		<circle cx={16} cy={-2} r={4.5} fill="#111" />
		{angry ? <path d="M-26,-22 L-6,-14 M26,-22 L6,-14" stroke="#1a3a10" strokeWidth={5} strokeLinecap="round" /> : null}
		<path d="M-14,18 q14,10 28,0" stroke="#1a3a10" strokeWidth={5} fill="none" strokeLinecap="round" />
	</g>
);

export const SteelDoor: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x},${y}) scale(${s})`}>
		<rect x={-190} y={-380} width={380} height={380} rx={10} fill="#7d8794" stroke="#4a525e" strokeWidth={10} />
		<rect x={-160} y={-350} width={320} height={320} rx={6} fill="#97a1ae" />
		{[-150, 150].map((px, i) => [-340, -40].map((py, j) => <circle key={i + '-' + j} cx={px} cy={py} r={9} fill="#5a626e" />))}
		<rect x={-14} y={-210} width={28} height={80} rx={8} fill="#4a525e" />
		<path d="M-160,-350 L-60,-350 L-160,-250 Z" fill="#fff" opacity={0.12} />
	</g>
);

export const Blueprint: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = 0}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<rect x={-80} y={-100} width={160} height={200} rx={6} fill="#2a63c8" stroke="#bfe0ff" strokeWidth={4} />
		<path d="M-56,-60 h112 M-56,-30 h70 M-56,0 h112 M-56,30 h50" stroke="#bfe0ff" strokeWidth={4} opacity={0.8} />
		<circle cx={34} cy={52} r={22} fill="none" stroke="#bfe0ff" strokeWidth={4} />
	</g>
);

export const Sign: React.FC<{x: number; y: number; text: string; s?: number; rot?: number}> = ({x, y, text, s = 1, rot = 0}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<rect x={-8} y={-220} width={16} height={230} fill="#6a4a2c" />
		<rect x={-130} y={-290} width={260} height={90} rx={10} fill="#9a6e3a" stroke="#4a3018" strokeWidth={6} />
		<text x={0} y={-228} textAnchor="middle" fontSize={44} fontFamily={FONT} fontWeight={900} fill="#2a1808">
			{text}
		</text>
	</g>
);

export const Sweat: React.FC<{x: number; y: number; f: number; n?: number; s?: number}> = ({x, y, f, n = 6, s = 1}) => (
	<g>
		{Array.from({length: n}).map((_, i) => {
			const t = ((f * 1.2 + i * 13) % 40) / 40;
			const side = i % 2 ? 1 : -1;
			return <path key={i} d="M0,-12 C8,0 10,8 0,14 C-10,8 -8,0 0,-12 Z" fill="#9fe0ff" opacity={1 - t} transform={`translate(${x + side * (52 + (i % 3) * 14) * s},${y - 30 + t * 120 * s}) scale(${s})`} />;
		})}
	</g>
);

export const Leaf: React.FC<{x: number; y: number; s?: number; rot?: number; c?: string}> = ({x, y, s = 1, rot = 0, c = '#2f8a50'}) => (
	<g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
		<path d="M0,0 C60,-110 250,-110 360,0 C250,70 60,70 0,0 Z" fill={c} />
		<path d="M0,0 L340,-4" stroke={darken(c, 0.3)} strokeWidth={5} />
	</g>
);
