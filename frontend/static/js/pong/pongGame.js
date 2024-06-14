import * as THREE from 'three';
import elements from './setupSceneElements.js';

const createGameBoard  = () => {
	const points = elements.createScoreBoard();
	const instructions = elements.createIntructions();
	const pong = document.querySelector('#pong');
	pong.appendChild(points);
	pong.appendChild(instructions);
}

const setupGame = () => {

	const constants = {
		PLAYER_MOVEMENT_UNIT: 1,
		PLAYGROUND_WIDTH: 180,
		PLAYGROUND_HEIGHT: 100,
		MESSAGE_INTERVAL_SECONDS: 0.05,
		PLAYER_WIDTH: 1,
		PLAYER_HEIGHT: 20,
		BALL_WIDTH: 1,
		BALL_HEIGHT: 1,
		WALL_MARGIN: 2,
		BALL_SPEED: 5,
		MAX_BOUNCE_ANGLE: 90,
		MIN_BOUNCE_ANGLE: -90,
	};

	const canvasSizing = 0.8;
	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(Math.floor(window.innerWidth * 0.8), Math.floor(window.innerHeight * 0.8));
	document.querySelector('#pong').appendChild(renderer.domElement);

	const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 500);
	camera.position.set(90, 50, 200);
	camera.lookAt(90, 50, 0);

	const scene = new THREE.Scene();
	const playerLeft = elements.createPlayer(constants, true);
	scene.add(playerLeft);

	const playerRight = elements.createPlayer(constants, false);
	scene.add(playerRight);

	const ball = elements.createBall(constants);
	scene.add(ball);

	renderer.render(scene, camera);
};

const removeSocket = (data) => {
	const chatSocket = document.getElementById('chat-socket');
	if (chatSocket.readyState == WebSocket.OPEN) {
		chatSocket.close();
	}
	chatSocket.removeEventListener('close');
	chatSocket.removeEventListener('error');
	chatSocket.removeEventListener('message');
}

const displayGameOver = ({game}) => {
	document.getElementById('game-over').textContent = 'Game Over';
	document.getElementById('winner').textContent = game.winner;
	document.getElementById('loser').textContent = game.loser;
	return;
};

const updateScore = ({left, right}) => {
	const leftScore = document.querySelector('#left-score')
	leftScore.textContent = String(players.left.score);
	const rightScore = document.querySelector('#right-score')
	rightScore.textContent = String(players.left.score);
}

const animate = ({players, ball, game}) => {
	requestAnimationFrame(animate);
	if (game.over == true) {
		removeSocket()
		displayGameOver(data);
	}
	playerLeft.position.set(players.left.position.x, players.left.position.y, 0);
	playerRight.position.set(players.right.position.x, players.right.position.y, 0);
	ball.position.set(ball.position.x, ball.position.y, 0);
	updateScore(players);
	renderer.render(scene, camera);
};

export {
	createGameBoard,
	setupGame,
	animate,
	displayGameOver,
	removeSocket}

