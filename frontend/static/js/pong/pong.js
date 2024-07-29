import elements from './setupSceneElements.js';

const PongContainer = () => {
	const pong = document.createElement('section');
	pong.id = 'pong';

	const points = elements.createScoreBoard();
	const instructions = elements.createIntructions();
	const gameOver = elements.createGameOver();
	const startInstructions = elements.startGameInstructions();
	pong.appendChild(points);
	pong.appendChild(instructions);
	pong.appendChild(gameOver);
	pong.appendChild(startInstructions);
	return pong
};

export default {PongContainer};
