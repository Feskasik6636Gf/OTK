import type {ShotDef} from '../kit/coverage';
import {makeShot} from './engine2';
import {CH} from './chapters';
export const SHOTS: ShotDef[] = CH.map(makeShot);
