import type {Base} from '../kit/actions';

/* Cast of "The Citizen President". Hero (you) = glossy black head, red hoodie — in
   pyjama trousers on day one and again on day 30. Nobody else is red. */
export type CastMember = Base & {sp?: string};

export const CAST: Record<string, CastMember> = {
	hero: {color: '#ff2540', hero: true, outfit: 'hoodie', legColor: '#7fb2e8', shoe: '#f4f1ea', rim: '#ffd0d6', rimW: 2.4},
	general: {color: '#33422f', outfit: 'suit', build: 'm', hair: 'cap', hairColor: '#22301f', acc: ['mustache'], skin: '#c98d63', eye: '#4a3a2a', legColor: '#22301f', rim: '#e6ecff', rimW: 2.4, shoe: '#111', age: 0.4},
	okafor: {color: '#6a2f5a', outfit: 'suit', build: 'f', hair: 'bun', hairColor: '#d9d9d9', acc: ['glasses'], skin: '#8d5a3b', eye: '#3a2a1a', age: 0.75, legColor: '#2b1d24', rim: '#ffe6d6', rimW: 2.4, shoe: '#2b1d24'},
	matias: {color: '#e8eef2', outfit: 'coat', build: 'm', hair: 'short', hairColor: '#2a1c14', acc: ['glasses'], skin: '#d9a07a', eye: '#4a3a2a', legColor: '#2c3a40', rim: '#d8fff2', rimW: 2.4, shoe: '#2c3a40'},
	haddad: {color: '#e9f6f3', outfit: 'coat', build: 'f', hair: 'long', hairColor: '#2b1f3a', skin: '#8d5a3b', eye: '#3a2a1a', legColor: '#2c8a8a', rim: '#d8fff2', rimW: 2.4, shoe: '#2c3a40', age: 0.2},
	sunny: {color: '#8b5cf6', outfit: 'hoodie', build: 'f', hair: 'ponytail', hairColor: '#2b1f1a', skin: '#e6b088', eye: '#3a2a1a', legColor: '#2d3a63', rim: '#efe2ff', rimW: 2.4, shoe: '#efe2ff'},
	aide: {color: '#2f3a56', outfit: 'suit', build: 'f', hair: 'bob', hairColor: '#4a2c22', skin: '#f1c4a0', eye: '#6a4a3a', legColor: '#1d2236', rim: '#e6ecff', rimW: 2.4, shoe: '#111'},
	suit: {color: '#3a4256', outfit: 'suit', hair: 'short', hairColor: '#2a2a2a', skin: '#e6b088', eye: '#4a3a2a', legColor: '#22262e', rim: '#e6ecff', rimW: 2.4, shoe: '#111'},
	econ: {color: '#7a6a3a', outfit: 'suit', hair: 'grey', hairColor: '#cfcfcf', acc: ['glasses'], skin: '#e8b48c', eye: '#6a7a8a', age: 0.5, legColor: '#3a3f4b', rim: '#fff0d0', rimW: 2.4, shoe: '#2b2f3a'},
	host: {color: '#d9433d', outfit: 'suit', hair: 'spiky', hairColor: '#8a3f1e', skin: '#f3cba8', eye: '#3a5a8a', legColor: '#2b2f3a', rim: '#ffe0c8', rimW: 2.4, shoe: '#f2f2f2'},
	kid: {color: '#3aa37a', outfit: 'tee', build: 'k', hair: 'cap', hairColor: '#3a2a1a', skin: '#c98d63', eye: '#4a3a2a', legColor: '#2b2f3a', rim: '#e8fff2', rimW: 2.4, shoe: '#f2f2f2'},
	mom: {color: '#7a5cc4', outfit: 'tee', build: 'f', hair: 'bob', hairColor: '#4a2c22', skin: '#e9b58c', eye: '#8a5a2a', legColor: '#3a3f5c', rim: '#ffe6c8', rimW: 2.4, shoe: '#2c2540'},
	captain: {color: '#2f6a8a', outfit: 'coat', hair: 'cap', hairColor: '#1a2a3a', skin: '#c98d63', beard: true, eye: '#3a2a1a', legColor: '#1d2b3a', rim: '#d8f0ff', rimW: 2.4, shoe: '#111'},
	driver: {color: '#e0a02a', outfit: 'tee', hair: 'cap', hairColor: '#4a3a2a', skin: '#e2b48a', acc: ['mustache'], eye: '#3a2a1a', legColor: '#3a3a4a', rim: '#fff0d0', rimW: 2.4, shoe: '#2b2f3a'},
};
