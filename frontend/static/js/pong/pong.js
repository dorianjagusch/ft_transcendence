import elements from './setupSceneElements.js';

const PongContainer = (isTournament) => {
	const pong = document.createElement('section');
	pong.id = 'pong';

	const points = elements.createScoreBoard();
	const instructions = elements.createIntructions();
	const gameOver = elements.createGameOver(isTournament);
	pong.appendChild(points);
	pong.appendChild(instructions);
	pong.appendChild(gameOver);
	return pong
};

export default {PongContainer};
