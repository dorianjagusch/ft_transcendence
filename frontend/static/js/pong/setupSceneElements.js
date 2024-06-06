import * as THREE from 'three';

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
export {createBall, createPlayer};
