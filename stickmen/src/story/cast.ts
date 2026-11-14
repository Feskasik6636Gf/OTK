import type {Base} from '../kit/actions';

/* Cast of "100 Days, Every Age". Hero = the channel character: black glossy head, red hoodie. */
export type CastMember = Base & {sp?: string};

export const CAST: Record<string, CastMember> = {
	hero: {color: '#ff2340', hair: 'none', gloss: true, lidL: 0.32, lidR: 0.32, mouth: 'smile', rim: '#ffd0d6', rimW: 2.4, shoe: '#f2f2f2', sp: 'HERO'},
	heroOld: {color: '#ff2340', hair: 'none', gloss: true, lidL: 0.32, lidR: 0.32, mouth: 'smile', rim: '#ffd0d6', rimW: 2.4, shoe: '#f2f2f2', age: 0.95, sp: 'HERO'},
	heroKid: {color: '#ff2340', hair: 'none', gloss: true, lidL: 0.32, lidR: 0.32, mouth: 'smile', rim: '#ffd0d6', rimW: 2.4, shoe: '#f2f2f2', sp: 'HERO'},
	mom: {color: '#7a5cc4', hair: 'bob', hairColor: '#2c1f3a', rim: '#ffe6c8', rimW: 2.4, shoe: '#2c2540', sp: 'MOM'},
	eli: {color: '#2f7be0', hair: 'cap', hairColor: '#f2b21c', rim: '#d8ecff', rimW: 2.4, shoe: '#f2f2f2', sp: 'ELI'},
	danny: {color: '#f08a3c', hair: 'spiky', hairColor: '#4a2a12', rim: '#ffe6c8', rimW: 2.4, shoe: '#2b2f3a', sp: 'DANNY'},
	ruth: {color: '#e86aa0', hair: 'ponytail', hairColor: '#ffd34a', rim: '#ffe6f0', rimW: 2.4, shoe: '#efe2ff', sp: 'RUTH'},
	okafor: {color: '#6b7f8e', outfit: 'tee', hair: 'grey', acc: ['glasses'], rim: '#eef4ff', rimW: 2.4, shoe: '#2b2f3a', age: 0.9, sp: 'OKAFOR'},
	teacher: {color: '#8e3a4f', outfit: 'suit', hair: 'bun', acc: ['glasses'], rim: '#ffe6d6', rimW: 2.4, shoe: '#2b1d24', sp: 'TEACHER'},
	lunch: {color: '#3aa37a', outfit: 'apron', hair: 'bun', rim: '#e8fff2', rimW: 2.4, shoe: '#1d2b24', sp: 'LUNCH'},
	coach: {color: '#3a4256', outfit: 'tee', hair: 'cap', hairColor: '#c0392b', acc: ['mustache'], rim: '#e6ecff', rimW: 2.4, shoe: '#111', sp: 'COACH'},
	bully: {color: '#3c3f4a', hair: 'spiky', hairColor: '#111', rim: '#e6ecff', rimW: 2.2, shoe: '#111', sp: 'BULLY'},
	stranger: {color: '#3aa37a', hair: 'bob', hairColor: '#7a3b1d', rim: '#e8fff2', rimW: 2.2, shoe: '#222', sp: 'STRANGER'},
};
