import * as THREE from 'three';

const PLAYER_MOVEMENT_UNIT = 1;
const PLAYGROUND_WIDTH = 180;
const PLAYGROUND_HEIGHT = 100;
const MESSAGE_INTERVAL_SECONDS = 0.05;
const PLAYER_WIDTH = 20;
const PLAYER_HEIGHT = 20;
const BALL_SIZE = 1;
const WALL_MARGIN = 20;
const BALL_SPEED = 5;
const MAX_BOUNCE_ANGLE = 90;
const MIN_BOUNCE_ANGLE = -90;

const fake_data = {
	'players': {
		width: PLAYER_WIDTH,
		height: PLAYER_HEIGHT,
		movementUnit: PLAYER_MOVEMENT_UNIT,
	},
	'ball': {
		ballSize: BALL_SIZE,
		ballSpeed: BALL_SPEED,
	},
	'game': {
		wallMargin: WALL_MARGIN,
		playgroundWidth: PLAYGROUND_WIDTH,
		playgroundHeight: PLAYGROUND_HEIGHT,
	},
};

const createPlayer = (players, position, settings) => {
	const geometry = new THREE.BoxGeometry(players.width, players.height, 0);
	const material = new THREE.MeshBasicMaterial({color: '#ffffff'});
	const mesh = new THREE.Mesh(geometry, material);
	mesh.position.set(
		position === 'left' ? settings.wallMargin : settings.width - settings.wallMargin,
		settings.height >> 1,
		0
	);
	return mesh;
};

const createBall = (ball) => {
	const geometry = new THREE.BoxGeometry(ball.size);
	const material = new THREE.MeshBasicMaterial({color: '#ffffff'});
	const mesh = new THREE.Mesh(geometry, material);
	mesh.position.set(
		fake_data.game.width >> 1,
		fake_data.game.height >> 1,
		0
	);
	return mesh;
};

const populateScene = ({players, ball, game}) => {
	console.log(game);
};

const initialiseGame = () => {
	const width = window.innerWidth;
	const height = window.innerHeight;
	const renderer = new THREE.WebGLRenderer({antialias: true});
	renderer.setSize(width, height);
	document.querySelector('#pong').appendChild(renderer.domElement);

	const fov = 75;
	const aspect = width / height;
	const near = 0.1;
	const far = 1000;

	const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
	camera.position.set(fake_data.game.width >> 1, fake_data.game.height >> 1, 100);
	camera.lookAt(fake_data.game.width >> 1, fake_data.game.height >> 1, 0);

	const scene = new THREE.Scene();
	scene.add(camera);

	fake_data.game.width = width;
	fake_data.game.height = height;

	// const meshes = populateScene(fake_data);
	const playerLeft = createPlayer(fake_data.players, 'left', fake_data.game);
	const playerRight = createPlayer(fake_data.players, 'right', fake_data.game);
	const gameBall = createBall(fake_data.ball);
	console.log(playerLeft, playerRight, gameBall)
	scene.add(playerLeft)
	scene.add(playerRight)
	scene.add(gameBall);

	renderer.render(scene, camera);
};

export default {initialiseGame};
