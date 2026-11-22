/* Pure helpers shared by the director (React) and the sound builder (node):
   how a line is cut into clauses and which effect / pop / sound each clause gets. */
export const clauses = (text: string): string[] => {
	const raw = text.split(/(?<=[.?!,;])\s+/).filter(Boolean);
	const out: string[] = [];
	for (const r of raw) {
		if (out.length && (out[out.length - 1].length < 16 || r.length < 10)) out[out.length - 1] += ' ' + r;
		else out.push(r);
	}
	return out.length ? out : [text];
};

export type Fx = 'impact' | 'sparkle' | 'flash' | 'exclaim' | 'question' | 'bulb' | 'pulse' | 'glitch' | 'smoke' | 'confetti' | 'lightning' | 'shock' | 'phone';
/* order matters: first matching rule wins */
export const FX_RULES: {re: RegExp; fx: Fx; text?: string; sfx: string; amp?: number}[] = [
	{re: /\bveto\b/i, fx: 'impact', text: 'VETO!', sfx: 'stamp', amp: 0.5},
	{re: /sign (your first law|an order)|you sign/i, fx: 'impact', text: 'SIGNED', sfx: 'stamp', amp: 0.45},
	{re: /\bno\.?$|still no|technically/i, fx: 'impact', text: 'NO.', sfx: 'thud', amp: 0.4},
	{re: /landfall|surge climbs|spills into/i, fx: 'lightning', sfx: 'thunder', amp: 0.4},
	{re: /power fails/i, fx: 'glitch', sfx: 'glitch', amp: 0.3},
	{re: /phone (buzzes|rings)|texts?\b|text(s|ed)\b|the phone rings|calls you/i, fx: 'phone', sfx: 'buzz', amp: 0.25},
	{re: /laughs|laughter|roars|stands\b|chants/i, fx: 'confetti', sfx: 'clap', amp: 0.25},
	{re: /storm|hurricane|swirl|cone|red/i, fx: 'pulse', sfx: 'heartbeat', amp: 0.3},
	{re: /\?/, fx: 'question', sfx: 'pop', amp: 0.25},
	{re: /idea|brilliant|page 902|found|name/i, fx: 'bulb', sfx: 'ding', amp: 0.25},
	{re: /salutes?|pizza|promised|stamp|photo|headlines?|born/i, fx: 'flash', sfx: 'shutter', amp: 0.25},
	{re: /nothing comes out|silence|nobody|quiet/i, fx: 'smoke', sfx: 'swoosh', amp: 0.2},
	{re: /suddenly|shifted|wrong|shak|crying|disaster|panic|coward/i, fx: 'exclaim', sfx: 'pop', amp: 0.28},
	{re: /fixed|91%|the best|appears|smile|dumb idea|keep it|nobody dies|first/i, fx: 'sparkle', sfx: 'sparkle', amp: 0.25},
];
export type Pop = {kind: 'day' | 'num'; text: string};
export const popFor = (t: string): Pop | null => {
	const d = t.match(/\b(?:day|Day|DAY|week|Week|hour|Hour|Our)\s+(\d+)/);
	if (d) {
		const w = /hour|our/i.test(d[0]) ? 'HOUR' : /week/i.test(d[0]) ? 'WEEK' : 'DAY';
		return {kind: 'day', text: `${w} ${d[1]}`};
	}
	const pct = t.match(/(\d+)\s?%/);
	if (pct) return {kind: 'num', text: pct[1] + '%'};
	const money = t.match(/\$\s?[\d.,]+\s?(?:million|billion)?/i);
	if (money) return {kind: 'num', text: money[0].replace(/\s+/g, ' ')};
	const n = t.match(/\b(\d{1,3}(?:,\d{3})+|\d{3,})\b/);
	if (n && !/a\.m\./.test(t)) return {kind: 'num', text: n[1]};
	if (/a\.m\.|\d+\.?\d* a\.?m/i.test(t)) {
		const m = t.match(/(\d+[.:]?\d*)\s?a\.?m/i);
		if (m) return {kind: 'num', text: m[1].replace(/(\d)(\d\d)$/, '$1:$2') + ' AM'};
	}
	return null;
};
export type Gest = 'point' | 'shrug' | 'facepalm' | 'handsOnHead' | 'think' | 'fist' | 'presentF' | 'stop' | 'wave' | 'rubChin' | 'touchFace' | 'scratch' | 'armsCrossed';
export const GEST_RULES: {re: RegExp; g: Gest}[] = [
	{re: /folder|hands you|brief|page|sheet|list|card|photo|name|decide|dinner|chicken/i, g: 'presentF'},
	{re: /point|swirl|map|cone|ask|asks|you ask/i, g: 'point'},
	{re: /no\b|still no|veto|stop|sorry|don't|never|nobody|not/i, g: 'stop'},
	{re: /storm|disaster|crying|shak|hands shaking|wrong|panic|coward|water|died|surge/i, g: 'handsOnHead'},
	{re: /\?|wonder|think|forget|quiet|silence|nothing|decision|choice|careful/i, g: 'think'},
	{re: /evacuate|keep going|now|go now|you say|fire|chant|roar|shout|promised|veto/i, g: 'fist'},
	{re: /wave|salute|hello|goodbye|helicopter|smile|grin|wave it away/i, g: 'wave'},
	{re: /sorry|mistake|ugly|embarrass|hold your breath|stand there/i, g: 'facepalm'},
	{re: /laugh|joke|funny|sunny|dumb|texts/i, g: 'scratch'},
	{re: /wait|maybe|unsure|might|can still|forecast/i, g: 'shrug'},
	{re: /tie|hat|cap|mug|coffee|tucks|stamp/i, g: 'rubChin'},
];
export const GEST_CYCLE: Gest[] = ['presentF', 'point', 'think', 'fist', 'shrug', 'wave', 'touchFace', 'stop', 'rubChin', 'handsOnHead'];
