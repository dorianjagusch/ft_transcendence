import {setupGame} from './lines.js';


const PongContainer = () => {
	const pongContainer = document.createElement('div');
	pongContainer.id = 'pong-container';

	setupGame();


	return pongContainer;
};

const Pong = () => {
	const pong = document.createElement('div');
	pong.id = 'pong';

	const pongContainer = PongContainer();
	pong.appendChild(pongContainer);

	return pong;
};

export {Pong};
