import type {Base} from '../kit/actions';

/* Characters of "What if Earth got a second sun". The hero is the user's character:
   black glossy head, half-lidded white eyes, calm smile, red hoodie with drawstrings. */
export type CastMember = Base & {sp?: string};

export const CAST: Record<string, CastMember> = {
	hero: {color: '#ff2a3c', rim: '#ffd0d4', rimW: 2.4, gloss: true, eyeStyle: 'lazy', mouth: 'smile', shoe: '#f4f4f4'},
	sam: {color: '#2f8fe8', hair: 'cap', hairColor: '#f2b21c', rim: '#d8ecff', rimW: 2.2, gloss: true, shoe: '#f2f2f2'},
	grandpa: {color: '#7d8a99', outfit: 'tee', hair: 'grey', hairColor: '#e8e8ee', acc: ['glasses', 'mustache'], rim: '#eef4ff', rimW: 2.2, shoe: '#3a2f2a'},
	mom: {color: '#3fbfb0', outfit: 'coat', hair: 'bun', rim: '#e0fff8', rimW: 2.2, shoe: '#f2f2f2'},
	dad: {color: '#4a9a4a', outfit: 'tee', hair: 'short', rim: '#e6ffe0', rimW: 2.2, shoe: '#2b2b30'},
	nia: {color: '#9b5cf6', hair: 'ponytail', hairColor: '#ffd34a', rim: '#efe2ff', rimW: 2.2, shoe: '#efe2ff', gloss: true},
	neighbor: {color: '#f08a3c', outfit: 'tee', hair: 'cap', hairColor: '#3a4256', rim: '#ffe6cc', rimW: 2.2, shoe: '#2b2b30'},
	scientist: {color: '#eef3f2', outfit: 'coat', hair: 'bob', hairColor: '#000', acc: ['glasses'], rim: '#d8fff2', rimW: 2.2, shoe: '#2c3a40'},
	farmer: {color: '#c9a03a', outfit: 'apron', hair: 'cap', hairColor: '#7a4a2a', rim: '#fff0cc', rimW: 2.2, shoe: '#3a2a1a'},
	seller: {color: '#3aa37a', outfit: 'apron', hair: 'bun', rim: '#e8fff2', rimW: 2.2, shoe: '#1d2b24'},
	teacher: {color: '#8e3a4f', outfit: 'suit', hair: 'bun', acc: ['glasses'], rim: '#ffe6d6', rimW: 2.2, shoe: '#2b1d24'},
};
