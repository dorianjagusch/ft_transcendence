import * as THREE from 'three';

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
	const instructionText = `${player} press ${upkey} to move up and ${downkey} to move down.`
	const instruction = document.createElement('p');
	instruction.textContent = instructionText;
	return instruction;
}

const createIntructions = () => {
	const instructions = document.createElement('article');
	instructions.setAttribute('id', 'instructions');
	instructions.appendChild(playerInstructions('Player 1', 'w', 's'));
	instructions.appendChild(playerInstructions('Player 2', 'o', 'l'));
	return instructions;
}

const createPlayer = (constants, isLeft) => {
	const {PLAYER_WIDTH, PLAYER_HEIGHT, WALL_MARGIN, PLAYGROUND_HEIGHT} = constants;

	const playerGeometry = new THREE.BoxGeometry(PLAYER_WIDTH, PLAYER_HEIGHT, 0);
	const playerMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
	const player = new THREE.Mesh(playerGeometry, playerMaterial);
	if (isLeft) {
		player.position.set(WALL_MARGIN, PLAYGROUND_HEIGHT / 2, 0);
	} else {
		const {PLAYGROUND_WIDTH} = constants;
		player.position.set(
			PLAYGROUND_WIDTH - WALL_MARGIN - PLAYER_WIDTH,
			PLAYGROUND_HEIGHT / 2,
			0
		);
	}
	return player;
};

const createBall = (constants) => {
	const {BALL_WIDTH, BALL_HEIGHT, PLAYGROUND_HEIGHT, PLAYGROUND_WIDTH} = constants;
	const ballGeometry = new THREE.BoxGeometry(BALL_WIDTH, BALL_HEIGHT, 0);
	const ballMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
	const ball = new THREE.Mesh(ballGeometry, ballMaterial);
	ball.position.set(PLAYGROUND_WIDTH / 2, PLAYGROUND_HEIGHT / 2, 0);
	return ball;
};
export default {createBall, createPlayer, createScoreBoard, createIntructions};
