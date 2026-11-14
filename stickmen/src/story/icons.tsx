import React from 'react';
import {FONT} from '../kit/ui';

/* Flat little props used as hand items (scale 1) and world icons (scale 2). Origin = centre. */
type Ic = (s: number) => React.ReactNode;
const G = (s: number, c: React.ReactNode) => <g transform={`scale(${s})`}>{c}</g>;

export const ICONS: Record<string, Ic> = {
	can: (s) => G(s, <><rect x={-9} y={-24} width={18} height={40} rx={5} fill="#3fd0ff" stroke="#0b0b0d" strokeWidth={2} /><rect x={-9} y={-8} width={18} height={10} fill="#fff" opacity={0.9} /><rect x={-6} y={-28} width={12} height={5} rx={2} fill="#bbb" /></>),
	cards: (s) => G(s, <><rect x={-20} y={-24} width={30} height={42} rx={4} fill="#ffd34a" stroke="#0b0b0d" strokeWidth={2} transform="rotate(-14)" /><rect x={-8} y={-26} width={30} height={42} rx={4} fill="#ff6a5a" stroke="#0b0b0d" strokeWidth={2} transform="rotate(10)" /><circle cx={8} cy={-5} r={7} fill="#fff" transform="rotate(10)" /></>),
	pancakes: (s) => G(s, <><ellipse cx={0} cy={8} rx={34} ry={9} fill="#d99a4e" /><ellipse cx={0} cy={0} rx={32} ry={9} fill="#f0b968" /><ellipse cx={0} cy={-8} rx={30} ry={9} fill="#f7c97e" /><path d="M-18,-12 q18,14 36,0 q-4,16 -18,14 q-10,0 -18,-14z" fill="#7a3a12" /></>),
	syrup: (s) => G(s, <><rect x={-12} y={-26} width={24} height={44} rx={8} fill="#a8561b" stroke="#0b0b0d" strokeWidth={2} /><rect x={-7} y={-34} width={14} height={9} rx={3} fill="#5c2e0c" /><rect x={-9} y={-8} width={18} height={14} fill="#f3e3b8" /></>),
	bill: (s) => G(s, <><rect x={-24} y={-30} width={48} height={60} rx={4} fill="#fbf8ef" stroke="#0b0b0d" strokeWidth={2} /><path d="M-14,-16 H14 M-14,-6 H14 M-14,4 H6" stroke="#8a8f9e" strokeWidth={3} /><text x={0} y={24} textAnchor="middle" fontSize={16} fontFamily={FONT} fontWeight={900} fill="#d6342f">$$$</text></>),
	notebook: (s) => G(s, <><rect x={-24} y={-32} width={48} height={64} rx={4} fill="#2f7be0" stroke="#0b0b0d" strokeWidth={2} /><rect x={-24} y={-32} width={9} height={64} fill="#1f56a3" /><path d="M-6,-16 H18 M-6,-6 H18 M-6,4 H18 M-6,14 H10" stroke="#fff" strokeWidth={3} strokeLinecap="round" /></>),
	cocoa: (s) => G(s, <><path d="M-18,-14 h36 v26 q0,14 -18,14 q-18,0 -18,-14z" fill="#f2f2f2" stroke="#0b0b0d" strokeWidth={2} /><path d="M18,-6 q16,0 16,10 q0,10 -16,10" fill="none" stroke="#f2f2f2" strokeWidth={5} /><ellipse cx={0} cy={-14} rx={18} ry={5} fill="#6b3a1e" /><path d="M-6,-24 q-6,-10 0,-18 M6,-24 q-6,-10 0,-18" stroke="#fff" strokeWidth={3} fill="none" opacity={0.7} /></>),
	phone: (s) => G(s, <><rect x={-14} y={-26} width={28} height={52} rx={6} fill="#14162a" stroke="#9aa3b5" strokeWidth={2} /><rect x={-10} y={-20} width={20} height={36} rx={2} fill="#3fc1c9" /></>),
	heart: (s) => G(s, <path d="M0,22 C-34,-4 -26,-30 -8,-26 C-2,-25 0,-18 0,-18 C0,-18 2,-25 8,-26 C26,-30 34,-4 0,22z" fill="#ff3d5a" stroke="#0b0b0d" strokeWidth={2} />),
	clock: (s) => G(s, <><circle r={26} fill="#fbf8ef" stroke="#0b0b0d" strokeWidth={3} /><path d="M0,-16 V0 L12,8" stroke="#14162a" strokeWidth={4} strokeLinecap="round" fill="none" /></>),
	calendar: (s) => G(s, <><rect x={-28} y={-30} width={56} height={60} rx={5} fill="#fbf8ef" stroke="#0b0b0d" strokeWidth={2} /><rect x={-28} y={-30} width={56} height={16} rx={5} fill="#ff2340" /><text x={0} y={20} textAnchor="middle" fontSize={34} fontFamily={FONT} fontWeight={900} fill="#14162a">100</text></>),
	cane: (s) => G(s, <path d="M-16,-30 q-14,-4 -14,10 M-16,-30 q10,0 14,8 L12,36" stroke="#8a5a2b" strokeWidth={7} fill="none" strokeLinecap="round" transform="translate(8,-6) rotate(14)" />),
	skate: (s) => G(s, <><rect x={-34} y={-4} width={68} height={9} rx={4} fill="#2f2f3a" /><circle cx={-22} cy={12} r={6} fill="#ffd34a" /><circle cx={22} cy={12} r={6} fill="#ffd34a" /></>),
	zzz: (s) => G(s, <text fontSize={34} fontFamily={FONT} fontWeight={900} fill="#bcd0ff" transform="rotate(-8)">Z z z</text>),
	question: (s) => G(s, <text textAnchor="middle" y={26} fontSize={90} fontFamily={FONT} fontWeight={900} fill="#ff2340" stroke="#12060a" strokeWidth={8} paintOrder="stroke">?</text>),
	glasses: (s) => G(s, <g stroke="#fff" strokeWidth={4} fill="none"><circle cx={-14} r={11} /><circle cx={14} r={11} /><path d="M-3,0 h6" /></g>),
	crayon: (s) => G(s, <><rect x={-26} y={-5} width={46} height={10} fill="#ff6a5a" /><path d="M20,-5 L32,0 L20,5z" fill="#c0392b" /></>),
	pen: (s) => G(s, <><rect x={-26} y={-3} width={46} height={7} rx={3} fill="#2f7be0" /><path d="M20,-3 L30,1 L20,5z" fill="#14162a" /></>),
	suitcase: (s) => G(s, <><rect x={-28} y={-18} width={56} height={40} rx={6} fill="#b5651d" stroke="#0b0b0d" strokeWidth={2} /><path d="M-10,-18 v-8 h20 v8" stroke="#0b0b0d" strokeWidth={3} fill="none" /><rect x={-4} y={-2} width={8} height={8} fill="#ffd34a" /></>),
	tray: (s) => G(s, <><rect x={-34} y={-4} width={68} height={8} rx={3} fill="#9aa3b5" /><circle cx={-12} cy={-10} r={10} fill="#ffd34a" /><rect x={8} y={-18} width={18} height={14} rx={3} fill="#d6342f" /></>),
	toast: (s) => G(s, <><rect x={-24} y={-22} width={48} height={44} rx={12} fill="#e8b86a" stroke="#8a5a2b" strokeWidth={3} /><rect x={-14} y={-12} width={28} height={24} rx={7} fill="#f6d9a0" /></>),
	bag: (s) => G(s, <><rect x={-18} y={-22} width={36} height={44} rx={8} fill="#2f7be0" stroke="#0b0b0d" strokeWidth={2} /><rect x={-14} y={-4} width={28} height={16} rx={4} fill="#1f56a3" /></>),
	popcorn: (s) => G(s, <><path d="M-18,-4 h36 l-6,32 h-24z" fill="#d6342f" /><path d="M-8,-4 l-3,28 M8,-4 l3,28" stroke="#fff" strokeWidth={5} /><circle cx={-12} cy={-12} r={9} fill="#fff6d0" /><circle cx={2} cy={-16} r={10} fill="#fff6d0" /><circle cx={14} cy={-10} r={8} fill="#fff6d0" /></>),
	star: (s) => G(s, <path d="M0,-28 L8,-9 L28,-8 L12,5 L18,25 L0,13 L-18,25 L-12,5 L-28,-8 L-8,-9z" fill="#ffd34a" stroke="#0b0b0d" strokeWidth={2} />),
	zero: (s) => G(s, <><rect x={-46} y={-52} width={92} height={104} rx={8} fill="#fbf8ef" stroke="#0b0b0d" strokeWidth={3} /><text x={0} y={30} textAnchor="middle" fontSize={96} fontFamily={FONT} fontWeight={900} fill="#d6342f">0</text></>),
	ball: (s) => G(s, <><circle r={26} fill="#e8772e" stroke="#0b0b0d" strokeWidth={2} /><path d="M-26,0 H26 M0,-26 V26 M-18,-18 Q0,0 -18,18 M18,-18 Q0,0 18,18" stroke="#0b0b0d" strokeWidth={2} fill="none" /></>),
	snail: (s) => G(s, <><ellipse cx={0} cy={14} rx={34} ry={8} fill="#c9a06a" /><circle cx={-4} cy={-4} r={20} fill="#ff9a5c" stroke="#8a4a1c" strokeWidth={3} /><path d="M-4,-4 m-8,0 a8,8 0 1,1 8,8" stroke="#8a4a1c" strokeWidth={3} fill="none" /><path d="M30,8 q8,-18 4,-26 M36,8 q10,-14 10,-24" stroke="#c9a06a" strokeWidth={4} fill="none" /></>),
	lamp: (s) => G(s, <><path d="M-22,-6 L22,-6 L12,-34 L-12,-34z" fill="#ffd34a" stroke="#0b0b0d" strokeWidth={2} /><rect x={-3} y={-6} width={6} height={36} fill="#444" /><ellipse cx={0} cy={32} rx={18} ry={5} fill="#444" /></>),
	thumb: (s) => G(s, <path d="M-26,-4 h14 v34 h-14z M-8,-6 l14,-28 q10,0 8,12 l-2,12 h20 q10,2 6,14 l-6,22 q-2,6 -10,6 h-30z" fill="#ffd34a" stroke="#0b0b0d" strokeWidth={2.5} />),
	food: (s) => G(s, <><rect x={-26} y={-6} width={52} height={22} rx={6} fill="#fbf8ef" stroke="#0b0b0d" strokeWidth={2} /><circle cx={-8} cy={-12} r={8} fill="#ffd34a" /><circle cx={8} cy={-10} r={7} fill="#6ad08a" /></>),
	hotdog: (s) => G(s, <circle r={0} />),
};
