/* Story-level settings. */
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
	title: 'Что если твой юмор — 1000?',
	hero: 'hero',
	counter: {
		label: 'ЮМОР',
		color: '#ff2338',
		keys: [
			{line: '001', v: 1000},
			{line: '019', v: 10, roll: 12},
			{line: '020', off: 4, v: 1000, roll: 26},
		],
	},
	bed: 'sfx/bed.wav',
};
