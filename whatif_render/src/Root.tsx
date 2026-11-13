import React from 'react';
import {Composition} from 'remotion';
import {Long, LONG_FRAMES} from './Long';
import {Short, SHORT_FRAMES} from './Short';
import {Sheet, SheetProps, sheetSize} from './Sheet';
import {PauseTime} from './reference/PauseTime';
import {RUBIK, CAVEAT} from './fonts-inline';

/* open-licence fonts from public/fonts, loaded before the first frame renders */
// generous timeout: with several render tabs at once a cold font load can take a while;
// if it still fails the frame renders with the fallback font instead of crashing
/* fonts are inlined (base64) and injected as CSS @font-face: nothing to fetch, nothing to wait
   for, so a busy render tab can never stall on a font handle */
const fontCss = document.createElement('style');
fontCss.textContent = `@font-face{font-family:'Rubik';src:url(data:font/ttf;base64,${RUBIK}) format('truetype');font-weight:300 900;font-display:block}
@font-face{font-family:'Caveat';src:url(data:font/ttf;base64,${CAVEAT}) format('truetype');font-weight:400 700;font-display:block}`;
document.head.appendChild(fontCss);

// headings are heavy unless a text asks for another weight (the style's chunky lettering)
const css = document.createElement('style');
css.textContent = `text[font-family*="Rubik"]:not([font-weight]){font-weight:800}`;
document.head.appendChild(css);

const defaultSheet: SheetProps = {comp: 'Long', frames: [0, 30, 60, 90], cols: 4};

export const Root: React.FC = () => (
	<>
		<Composition id="Long" component={Long} durationInFrames={Math.max(1, LONG_FRAMES)} fps={30} width={1920} height={1080} />
		<Composition id="Short" component={Short} durationInFrames={Math.max(1, SHORT_FRAMES)} fps={30} width={1080} height={1920} />
		<Composition
			id="Sheet"
			component={Sheet}
			// as long as the videos: frozen scenes keep their Sequences alive
			durationInFrames={Math.max(LONG_FRAMES, SHORT_FRAMES, 1)}
			fps={30}
			width={1920}
			height={1080}
			defaultProps={defaultSheet}
			calculateMetadata={({props}) => {
				const s = sheetSize(props);
				return {width: s.width, height: Math.ceil(s.height / 2) * 2};
			}}
		/>
		{/* the approved style reference: 10 s, built by hand, shows what "our level" means */}
		<Composition id="Reference" component={PauseTime} durationInFrames={300} fps={30} width={1920} height={1080} />
	</>
);
