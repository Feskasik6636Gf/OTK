import React from 'react';
import type {ShotDef} from '../kit/coverage';
import {SceneCfg, makeScene} from './director';
import {Banquet, Field, Helicopter, Highway, Hospital, KBedroom, KCity, KCoast, KCorridor, KKitchen, Lawn, Oval, Press, Situation, Studio, UNHall} from './places';

/* THE CITIZEN PRESIDENT — scene table. Each row: first line of the scene, background,
   who is on stage and where (x on the 1920 stage, floor y = 900). The director does the rest
   (see director.tsx): new action / camera every clause, walks, effects, number pops. */
type Row = SceneCfg;

const hero = (x: number, o: Partial<Row['cast'][0]> = {}) => ({who: 'hero', x, ...o});
const P = (who: string, x: number, o: Partial<Row['cast'][0]> = {}) => ({who, x, ...o});

const ROWS: Row[] = [
	{at: '001', bg: (g) => <Oval f={g} />, cast: [hero(900, {enter: 'L'}), P('general', 1350, {face: -1}), P('aide', 500, {enter: 'L'})], crowd: [{n: 7, x0: 150, x1: 520, s: 0.8, mode: 'stand', seed: 'o1'}, {n: 6, x0: 1450, x1: 1800, s: 0.8, mode: 'stand', seed: 'o2'}]},
	{at: '005', whip: true, bg: (g) => <Lawn f={g} />, cast: [hero(700), P('okafor', 1150, {enter: 'R'}), P('aide', 1450)], crowd: [{n: 12, x0: 100, x1: 1800, s: 0.75, mode: 'stand', seed: 'lw1', floor: 960}], floor: 900},
	{at: '009', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(800), P('aide', 1250, {face: -1}), P('okafor', 450, {enter: 'L'})]},
	{at: '010', whip: true, bg: (g) => <KBedroom f={g} night ring />, cast: [hero(760, {enter: 'L'}), P('aide', 1050, {enter: 'R'})], night: true},
	{at: '011', whip: true, bg: (g) => <KCoast f={g} />, cast: [hero(700), P('matias', 1150, {enter: 'R'}), P('general', 1500)], rain: true, night: true},
	{at: '012', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(900), P('aide', 1400, {enter: 'R'}), P('okafor', 520)]},
	{at: '015', whip: true, bg: (g) => <KCorridor f={g} />, cast: [hero(650, {enter: 'L'}), P('aide', 1200, {enter: 'R'})]},
	{at: '018', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(800), P('suit', 1300, {face: -1}), P('okafor', 450)]},
	{at: '020', whip: true, bg: (g) => <Banquet f={g} />, cast: [hero(900), P('aide', 1400, {enter: 'R'}), P('suit', 520)], crowd: [{n: 9, x0: 150, x1: 1800, s: 0.7, mode: 'stand', seed: 'bq', floor: 640}]},
	{at: '024', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(850), P('suit', 1350, {enter: 'R'}), P('okafor', 520)]},
	{at: '027', whip: true, bg: (g) => <KCity f={g} />, cast: [hero(800, {enter: 'L'}), P('suit', 1250, {enter: 'R'})], crowd: [{n: 5, x0: 100, x1: 1800, s: 0.7, mode: 'walk', seed: 'cy1', floor: 880, dir: 1}]},
	{at: '031', whip: true, bg: (g) => <Oval f={g} night />, cast: [hero(900), P('aide', 1450, {enter: 'R'})], night: true},
	{at: '035', whip: true, bg: (g) => <Field f={g} />, cast: [hero(800, {enter: 'L'}), P('okafor', 1200), P('kid', 1500, {enter: 'R'})], front: (g) => <Helicopter f={g} x={500 + Math.sin(g / 60) * 80} y={250} s={0.9} />},
	{at: '040', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(850), P('okafor', 1300, {face: -1})]},
	{at: '044', whip: true, bg: (g) => <KKitchen f={g} />, cast: [hero(800), P('mom', 1150, {enter: 'R'})]},
	{at: '045', whip: true, bg: (g) => <Situation f={g} />, cast: [hero(800), P('matias', 1250, {face: -1}), P('okafor', 450, {enter: 'L'})], night: true},
	{at: '049', whip: true, bg: (g) => <KBedroom f={g} />, cast: [hero(760), P('sunny', 1100, {enter: 'R'})]},
	{at: '051', whip: true, bg: (g) => <KBedroom f={g} night ring />, cast: [hero(760), P('aide', 1050, {enter: 'R'})], night: true},
	{at: '057', whip: true, bg: (g) => <KCoast f={g} />, cast: [hero(800), P('captain', 1150, {enter: 'R'}), P('driver', 1450, {enter: 'R'})]},
	{at: '058', whip: true, bg: (g) => <UNHall f={g} />, cast: [hero(900, {enter: 'L'}), P('suit', 450), P('aide', 1450)]},
	{at: '062', whip: true, bg: (g) => <Studio f={g} />, cast: [P('host', 700), hero(1000, {enter: 'R', face: -1})], night: true},
	{at: '067', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(900), P('aide', 500), P('suit', 1300), P('econ', 1550, {enter: 'R'})]},
	{at: '074', whip: true, bg: (g) => <Press f={g} />, cast: [hero(600), P('econ', 1000), P('suit', 1350, {enter: 'R'})], bgc: '#1d3a7a'},
	{at: '078', whip: true, bg: (g) => <KKitchen f={g} night />, cast: [hero(800), P('mom', 1150, {enter: 'R'})], night: true},
	{at: '083', whip: true, bg: (g) => <Oval f={g} night />, cast: [hero(800), P('aide', 1300, {enter: 'R'})], night: true},
	{at: '085', whip: true, bg: (g) => <KBedroom f={g} night />, cast: [hero(900), P('aide', 1350, {enter: 'R'})], night: true},
	{at: '089', whip: true, bg: (g) => <Oval f={g} />, cast: [hero(850), P('okafor', 1250, {face: -1}), P('matias', 500, {enter: 'L'})]},
	{at: '091', whip: true, bg: (g) => <Situation f={g} alert />, cast: [hero(850), P('matias', 1250), P('general', 500, {enter: 'L'}), P('okafor', 1550)], night: true},
	{at: '095', whip: true, bg: (g) => <KCoast f={g} />, cast: [P('matias', 800), hero(1200, {enter: 'R'})], rain: true, night: true},
	{at: '098', whip: true, bg: (g) => <Highway f={g} jam />, cast: [hero(900), P('driver', 1300, {enter: 'R'})]},
	{at: '101', whip: true, bg: (g) => <Situation f={g} alert />, cast: [P('general', 700), hero(1000), P('okafor', 1350)], crowd: [{n: 8, x0: 200, x1: 1750, s: 0.7, mode: 'stand', seed: 'sr1', floor: 860}], night: true},
	{at: '104', whip: true, bg: (g) => <Hospital f={g} />, cast: [P('haddad', 650, {enter: 'L'}), hero(1150, {enter: 'R'})]},
	{at: '108', whip: true, bg: (g) => <Situation f={g} alert />, cast: [hero(900), P('general', 600), P('suit', 1300), P('okafor', 1600)], night: true},
	{at: '114', whip: true, bg: (g) => <Highway f={g} />, cast: [hero(800), P('aide', 1250, {enter: 'R'})]},
	{at: '122', whip: true, bg: (g) => <Situation f={g} alert />, cast: [P('matias', 700, {enter: 'L'}), hero(1100), P('general', 1450)], night: true},
	{at: '126', whip: true, bg: (g) => <Highway f={g} night bridge />, cast: [P('driver', 800), hero(1200, {enter: 'R'})], night: true},
	{at: '131', whip: true, bg: (g) => <KCoast f={g} />, cast: [hero(800), P('matias', 1200, {enter: 'R'})], rain: true, night: true},
	{at: '132', whip: true, bg: (g) => <Hospital f={g} flood />, cast: [P('haddad', 900), P('aide', 1400, {enter: 'R'})]},
	{at: '134', whip: true, bg: (g) => <Situation f={g} />, cast: [hero(900), P('general', 500), P('okafor', 1400)], night: true},
	{at: '136', whip: true, bg: (g) => <Oval f={g} night />, cast: [hero(900), P('aide', 1350, {enter: 'R'})], night: true},
	{at: '140', whip: true, bg: (g) => <Press f={g} />, cast: [hero(960, {enter: 'L'}), P('okafor', 1450)], night: true},
	{at: '142', whip: true, bg: (g) => <KCorridor f={g} />, cast: [hero(600), P('general', 1100, {enter: 'R'})], crowd: [{n: 6, x0: 1300, x1: 1800, s: 0.9, mode: 'stand', seed: 'cr1'}]},
	{at: '145', whip: true, bg: (g) => <Oval f={g} night />, cast: [hero(850), P('matias', 1200), P('econ', 1500, {enter: 'R'})], crowd: [{n: 6, x0: 150, x1: 600, s: 0.8, mode: 'stand', seed: 'o3'}], night: true},
	{at: '150', whip: true, bg: (g) => <Hospital f={g} />, cast: [hero(700), P('haddad', 1250, {enter: 'R'})]},
	{at: '154', whip: true, bg: (g) => <KKitchen f={g} />, cast: [hero(700), P('sunny', 1100, {enter: 'R'}), P('okafor', 1550, {enter: 'R'})]},
	{at: '162', whip: true, bg: (g) => <KCorridor f={g} />, cast: [hero(700, {enter: 'L'}), P('general', 1250)], crowd: [{n: 8, x0: 150, x1: 1800, s: 0.75, mode: 'stand', seed: 'cr2', floor: 860}]},
	{at: '165', whip: true, bg: (g) => <Lawn f={g} />, cast: [hero(700), P('okafor', 1200)], crowd: [{n: 12, x0: 100, x1: 1800, s: 0.75, mode: 'stand', seed: 'lw2', floor: 960}]},
];

export const SHOTS: ShotDef[] = ROWS.map((r, i) => ({at: r.at, whip: r.whip, C: makeScene(r, [], ROWS[i + 1]?.at)}));
