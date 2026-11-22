/* Story-level settings. Claude rewrites this file for every new video. */
export type CounterKeyDef = {line: string; off?: number; v: number; roll?: number};

export const STORY: {
	title: string;
	hero: string; // cast id of the main character
	counter?: {label: string; color?: string; keys: CounterKeyDef[]}; // badge over the hero (age, lives, money…)
	heroAge?: (counter: number) => number; // 0..1 body ageing driven by the counter (optional)
	heroGrow?: number; // how much bigger the hero gets at full ageing (0.07 = +7 %)
	bed: string; // sound bed in public/ (ambience + sfx, music only if the user wants it)
	musicVolume?: number; // only if the bed has music in it
	endCaption?: string[]; // last words on screen (call to action), optional
} = {
	title: 'The Citizen President',
	hero: 'hero',
	counter: {
		label: 'APPROVAL %',
		color: '#ffd34a',
		keys: [
			{line: '001', v: 50},
			{line: '023', off: 20, v: 91, roll: 40},
			{line: '030', off: 10, v: 84, roll: 30},
			{line: '039', off: 40, v: 88, roll: 30},
			{line: '061', off: 160, v: 91, roll: 40},
			{line: '085', off: 120, v: 78, roll: 30},
			{line: '086', off: 0, v: 64, roll: 20},
			{line: '086', off: 50, v: 48, roll: 20},
			{line: '139', off: 6, v: 31, roll: 40},
		],
	},
	bed: 'sfx/bed.wav',
	endCaption: ['WOULD YOU EVACUATE?', 'TELL ME IN THE COMMENTS'],
};
