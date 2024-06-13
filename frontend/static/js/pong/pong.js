import {setupGame} from './pongGame.js';

const Pong = () => {
	const pongContainer = document.createElement('div');
	pongContainer.id = 'pong-container';

	setupGame();

	return pongContainer;
};

const PongContainer = () => {
	const pong = document.createElement('div');
	pong.id = 'pong';

	const pongContainer = Pong();
	pong.appendChild(pongContainer);

	return pong;
};

export default PongContainer;
