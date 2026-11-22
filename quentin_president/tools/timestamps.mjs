// Prints the start time of every line of the finished video: use it to write chapters
// (timestamps) in the YouTube description.   node tools/timestamps.mjs [timeline=src/story/timeline.json]
import {readJson, say} from './lib.mjs';

const tl = readJson(process.argv[2] ?? 'src/story/timeline.json');
const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;
for (const l of tl.lines) say(`${fmt(l.from / tl.fps)}  ${l.id.slice(0, 3)}  ${(l.text || '').slice(0, 70)}`);
say(`total ${fmt(tl.total / tl.fps)}`);
