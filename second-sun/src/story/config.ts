/* Story-level settings for "What if Earth got a second sun". */
export type CounterKeyDef = {line: string; off?: number; v: number; roll?: number};

export const STORY: {
	title: string;
	hero: string;
	counter?: {label: string; color?: string; keys: CounterKeyDef[]};
	heroAge?: (counter: number) => number;
	heroGrow?: number;
	bed: string;
	musicVolume?: number;
	endCaption?: string[];
} = {
	title: 'What if Earth got a second sun',
	hero: 'hero',
	counter: {
		label: 'DAY',
		color: '#ff8a2a',
		keys: [
			{line: '001', v: 41},
			{line: '012', off: 40, v: 1, roll: 20},
			{line: '048', off: 2, v: 3, roll: 8},
			{line: '063', off: 30, v: 7, roll: 10},
			{line: '077', off: 2, v: 9, roll: 6},
			{line: '108', off: 2, v: 20, roll: 12},
			{line: '128', off: 30, v: 41, roll: 14},
			{line: '143', off: 2, v: 60, roll: 12},
			{line: '205', off: 2, v: 180, roll: 24},
			{line: '221', off: 2, v: 214, roll: 14},
			{line: '252', off: 2, v: 221, roll: 8},
		],
	},
	bed: 'sfx/bed.wav',
	endCaption: ['TWO SUNS… OR ONE?', 'TELL US IN THE COMMENTS'],
};
