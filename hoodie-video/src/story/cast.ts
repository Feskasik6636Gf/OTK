import type {Base} from '../kit/actions';

/* Cast of "Lion vs 100 Men vs Max". Max (the hero) is the black-headed kid in the red hoodie. */
export type CastMember = Base & {sp?: string};

export const CAST: Record<string, CastMember> = {
	max: {color: '#ff2340', hair: 'none', rim: '#ffc4cc', rimW: 2.4, shoe: '#f4f4f4', gloss: true, mouth: 'smirk', lidL: 0.35, lidR: 0.35},
	sam: {color: '#3aa37a', hair: 'cap', hairColor: '#d9b13a', rim: '#e6fff0', rimW: 2.4, shoe: '#2a2a2a'},
	danny: {color: '#2f6fd8', hair: 'spiky', acc: ['mustache'], rim: '#dce8ff', rimW: 2.4, shoe: '#f2f2f2'},
	theo: {color: '#f2b21c', hair: 'short', acc: ['glasses'], rim: '#fff0cc', rimW: 2.4, shoe: '#3a2a1a'},
};
