const PlayerScore = (side) => {
	const PlayerScore = document.createElement('span');
	PlayerScore.setAttribute('id', `${side}-score`);
	PlayerScore.textContent = '0';
	return PlayerScore;
};

const createScoreBoard = () => {
	const scores = document.createElement('article');
	scores.classList.add('flex-row');
	scores.setAttribute('id', 'score-board');
	const leftPlayerScore = PlayerScore('left');
	const colon = document.createElement('span');
	colon.textContent = ':';
	const rightPlayerScore = PlayerScore('right');

	scores.appendChild(leftPlayerScore);
	scores.appendChild(colon);
	scores.appendChild(rightPlayerScore);

	return scores;
};

const playerInstructions = (player, upkey, downkey) => {
	const instructionText = `${player} press ${upkey} to move up and ${downkey} to move down.`;
	const instruction = document.createElement('p');
	instruction.textContent = instructionText;
	return instruction;
};

const createIntructions = () => {
	const instructions = document.createElement('article');
	instructions.setAttribute('id', 'instructions');
	instructions.appendChild(playerInstructions('Player 1', 'w', 's'));
	instructions.appendChild(playerInstructions('Player 2', 'o', 'l'));
	return instructions;
};

const createGameOver = () => {
	const gameOver = document.createElement('article');
	gameOver.setAttribute('id', 'game-over');
	const gameOverText = document.createElement('p');

	const winner = document.createElement('p');
	winner.setAttribute('id', 'winner');

	const newGameButton = document.createElement('button');
	newGameButton.textContent = 'New Game';
	newGameButton.classList.add('new-game-button');
	
	newGameButton.addEventListener('click', () => {
		window.location.reload();
	});

	gameOver.appendChild(gameOverText);
	gameOver.appendChild(winner);
	gameOver.appendChild(newGameButton);
	gameOver.style.display = 'none';
	return gameOver;
};

export default {createScoreBoard, createIntructions, createGameOver};
