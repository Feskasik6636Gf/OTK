import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {FONT} from '../kit/ui';

/* The user's AI image + clickbait text */
const stroke = (px: number, c = '#0a0206'): React.CSSProperties => ({WebkitTextStroke: `${px}px ${c}`, paintOrder: 'stroke', textShadow: '0 12px 28px rgba(0,0,0,.65)'});
export const Thumb3: React.FC = () => (
	<AbsoluteFill style={{background: '#000'}}>
		<Img src={staticFile('thumb_base.png')} style={{width: 1920, height: 1080, objectFit: 'cover'}} />
		{/* top-center headline */}
		<div style={{position: 'absolute', left: 560, top: 8, width: 800, textAlign: 'center', transform: 'rotate(-4deg)', fontFamily: FONT, fontWeight: 900, lineHeight: 0.92}}>
			<div style={{fontSize: 150, color: '#ffffff', ...stroke(18)}}>1 LION</div>
			<div style={{fontSize: 150, color: '#ffd23a', ...stroke(18)}}>VS 100 MEN</div>
		</div>
		{/* bottom hook */}
		<div style={{position: 'absolute', left: 0, bottom: 14, width: 1230, textAlign: 'center', transform: 'rotate(-2deg)', fontFamily: FONT, fontWeight: 900, fontSize: 118, lineHeight: 1, color: '#ff3a52', ...stroke(16)}}>WHO SURVIVES?!</div>
	</AbsoluteFill>
);
