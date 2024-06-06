import * as THREE from 'three';
import {createBall, createPlayer} from './setupSceneElements.js';


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

	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);
	document.querySelector('main').appendChild(renderer.domElement);

	const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 500);
	camera.position.set(90, 50, 200);
	camera.lookAt(90, 50, 0);

	const scene = new THREE.Scene();
	const playerLeft = createPlayer(constants, true);
	scene.add(playerLeft);

	const playerRight = createPlayer(constants, false);
	scene.add(playerRight);

	const ball = createBall(constants);
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

const displayGameOver = (data) => {
	document.getElementById('game-over').textContent = 'Game Over';
	document.getElementById('winner').textContent = data.game.winner;
	document.getElementById('loser').textContent = data.game.loser;
	return;
};

const animate = (data) => {
	requestAnimationFrame(animate);
	if (data.game.over == true) {
		removeSocket()
		displayGameOver(data);
	}
	playerLeft.position.set(data.players.left.position.x, data.players.left.position.y, 0);
	playerRight.position.set(data.players.right.position.x, data.players.right.position.y, 0);
	ball.position.set(data.ball.position.x, data.ball.position.y, 0);
	renderer.render(scene, camera);
};

export {
	setupGame,
	animate,
	displayGameOver,
	removeSocket}

