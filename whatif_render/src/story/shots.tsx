import React from 'react';
import type {ShotDef} from '../kit/coverage';
import {BEATS} from './beats';
import {BeatShot} from './engine';
import {CARDS} from './cards';

/* One shot per beat (= per voice line); `same` beats extend the previous shot. A change
   of location enters with a whip-pan. */
const pad = (n: number) => String(n).padStart(3, '0');

export const SHOTS: ShotDef[] = [];
let prevLoc = '';
let idx = 0;
BEATS.forEach((b, i) => {
	if ((b as any).same) return;
	const n = i + 1;
	const myIdx = idx++;
	const C: React.FC = () => <BeatShot b={b} idx={myIdx} lineNo={n} cards={CARDS} />;
	C.displayName = 'Beat' + pad(n);
	const loc = b.card ? 'card:' + b.card : b.loc;
	SHOTS.push({at: pad(n), C, whip: i > 0 && (b.whip || loc !== prevLoc)});
	prevLoc = loc;
});
