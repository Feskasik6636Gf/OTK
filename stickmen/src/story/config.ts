/* Story-level settings: "You wake up every morning at a different age for 100 days". */
export type CounterKeyDef = {line: string; off?: number; v: number; roll?: number};

// ids are 1-based, 3 digits; the helper takes the 0-based index from the transcript listing
export const id3 = (i: number) => String(i + 1).padStart(3, '0');
const K = (i: number, v: number, roll = 14, off = 0): CounterKeyDef => ({line: id3(i), off, v, roll});

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
	title: 'You Wake Up at a Different Age Every Morning for 100 Days',
	hero: 'hero',
	counter: {
		label: 'AGE',
		keys: [
			{line: '001', v: 83},
			K(64, 6, 26), // day two: six years old
			K(104, 41, 26), // day three
			K(140, 19, 12),
			K(141, 23, 12, 0),
			K(143, 70, 12, 0),
			K(144, 8, 12, 0),
			K(149, 2, 12, 0),
			K(150, 60, 12, 0),
			K(159, 4, 16, 0),
			K(169, 16, 20),
			K(176, 45, 20),
			K(200, 83, 20),
			K(226, 6, 24),
			K(259, 30, 12),
			K(261, 15, 12),
			K(262, 57, 12),
			K(263, 94, 12),
			K(272, 16, 24),
			K(334, 41, 20),
			K(335, 8, 20),
			K(336, 16, 20),
		],
	},
	heroAge: (c) => (c >= 30 ? Math.min(1, (c - 28) / 50) : 0),
	bed: 'sfx/bed.wav',
	endCaption: ['WHAT AGE WOULD YOU BE FOR A DAY?', 'TELL US IN THE COMMENTS'],
};
