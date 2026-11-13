import type {ShotDef} from '../kit/coverage';
import {SHOTS_A} from './shotsA';
import {SHOTS_B} from './shotsB';
import {SHOTS_B2} from './shotsB2';
import {SHOTS_C} from './shotsC';
import {SHOTS_D} from './shotsD';

export const SHOTS: ShotDef[] = [...SHOTS_A, ...SHOTS_B, ...SHOTS_B2, ...SHOTS_C, ...SHOTS_D];
