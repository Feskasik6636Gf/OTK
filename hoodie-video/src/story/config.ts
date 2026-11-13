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
	title: 'Lion vs 100 Men vs Max',
	hero: 'max',
	bed: 'sfx/bed.wav',
	endCaption: ['WHO WOULD YOU BET ON?', 'TELL US IN THE COMMENTS'],
};
