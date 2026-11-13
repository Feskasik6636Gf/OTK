import type {Base} from '../kit/actions';

/* Characters of this video. The hero is the user's character: glossy black head,
   smug half-closed eyes, red hoodie with white drawstrings. */
export type CastMember = Base & {sp?: string};

export const CAST: Record<string, CastMember> = {
	hero: {color: '#ff2338', rim: '#ffd0d6', rimW: 2.4, gloss: true, lidRest: 0.38, mouth: 'smile', shoe: '#1b1b22', sp: 'HERO'},
	principal: {color: '#3a4256', outfit: 'suit', hair: 'grey', hairColor: '#cfd3dc', acc: ['glasses', 'mustache'], rim: '#e6ecff', rimW: 2.4, shoe: '#111', sp: 'PRINCIPAL'},
	secretary: {color: '#c46a8a', hair: 'bun', acc: ['glasses'], rim: '#ffe6ef', rimW: 2.4, shoe: '#3a2030', sp: 'SECRETARY'},
	mom: {color: '#7a5cc4', hair: 'bob', rim: '#ffe6c8', rimW: 2.4, shoe: '#2c2540', sp: 'MOM'},
	noah: {color: '#3fc1c9', hair: 'spiky', rim: '#e0fbff', rimW: 2.4, shoe: '#1d3a40', sp: 'NOAH'},
	teacher: {color: '#8e3a4f', outfit: 'suit', hair: 'bun', acc: ['glasses'], rim: '#ffe6d6', rimW: 2.4, shoe: '#2b1d24', sp: 'TEACHER'},
	ben: {color: '#2f6fd8', hair: 'cap', hairColor: '#f2b21c', rim: '#dce8ff', rimW: 2.4, shoe: '#f2f2f2', sp: 'BEN'},
	ayva: {color: '#8b5cf6', hair: 'ponytail', hairColor: '#ffd34a', rim: '#efe2ff', rimW: 2.4, shoe: '#efe2ff', sp: 'AYVA'},
	lunch: {color: '#3aa37a', outfit: 'apron', hair: 'bun', rim: '#e8fff2', rimW: 2.4, shoe: '#1d2b24', sp: 'LUNCH'},
	cop: {color: '#25336a', outfit: 'suit', hair: 'cap', hairColor: '#1a2450', acc: ['mustache'], rim: '#e6ecff', rimW: 2.4, shoe: '#111', sp: 'COP'},
	grandpa: {color: '#6b7f8e', outfit: 'tee', hair: 'grey', acc: ['glasses'], rim: '#eef4ff', rimW: 2.4, shoe: '#2b2f3a', sp: 'GRANDPA'},
	nurse: {color: '#eef3f2', outfit: 'coat', hair: 'bob', rim: '#d8fff2', rimW: 2.4, shoe: '#2c3a40', sp: 'NURSE'},
	kid1: {color: '#f08a3c', hair: 'short', rim: '#fff0dc', rimW: 2.2, sp: 'KID1'},
	kid2: {color: '#e86aa0', hair: 'ponytail', hairColor: '#7a3a2a', rim: '#ffe6f0', rimW: 2.2, sp: 'KID2'},
	kid3: {color: '#7cc46a', hair: 'spiky', rim: '#eaffdc', rimW: 2.2, sp: 'KID3'},
	host: {color: '#1b1e2a', outfit: 'suit', hair: 'short', rim: '#ffd0f0', rimW: 2.4, shoe: '#111', sp: 'HOST'},
	man: {color: '#9a6a3a', hair: 'none', acc: ['mustache'], rim: '#fff0dc', rimW: 2.4, sp: 'MAN'},
	chief: {color: '#c62a2a', outfit: 'coat', hair: 'cap', hairColor: '#f2b21c', acc: ['mustache'], rim: '#ffe0d0', rimW: 2.4, shoe: '#111', sp: 'CHIEF'},
	scientist: {color: '#eef3f2', outfit: 'coat', hair: 'grey', hairColor: '#d9d9d9', acc: ['glasses'], rim: '#d8fff2', rimW: 2.4, shoe: '#2c3a40', sp: 'SCI'},
};
