import {L} from '../kit/core';

/* Day / men / score counters on the screen HUD, tied to lines. */
export const DAYS: [string, number][] = [['032', 1], ['052', 2], ['077', 3], ['087', 5], ['121', 8], ['147', 10], ['155', 12], ['171', 14], ['201', 18], ['224', 20], ['255', 29], ['300', 30]];
export const MEN: [string, number][] = [['032', 100], ['138', 88], ['154', 71], ['242', 41]];
export const SCORE: [string, [number, number, number]][] = [['032', [0, 0, 0]], ['051', [0, 0, 1]], ['086', [0, 1, 1]], ['120', [0, 1, 2]], ['200', [0, 2, 2]]];
export const HUD_FROM = '032';
export const HUD_TO = '319';

const resolve = <T,>(k: [string, T][], off = 0) => k.map(([l, v]) => ({at: L(l).from + off, v}));
export const valueAt = <T,>(keys: {at: number; v: T}[], gf: number): {v: T; ago: number} => {
	let cur = keys[0];
	for (const k of keys) if (gf >= k.at) cur = k;
	return {v: cur.v, ago: gf - cur.at};
};
let cache: any = null;
export const hudKeys = () =>
	(cache ??= {
		days: resolve(DAYS, -4),
		men: resolve(MEN),
		score: resolve(SCORE, 40),
		from: L(HUD_FROM).from - 6,
		to: L(HUD_TO).from + L(HUD_TO).dur,
	}) as {days: {at: number; v: number}[]; men: {at: number; v: number}[]; score: {at: number; v: [number, number, number]}[]; from: number; to: number};
