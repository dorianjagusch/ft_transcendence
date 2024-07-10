import * as THREE from 'three';
import elements from './setupSceneElements.js';
import Player from './Player.js';
import Ball from './Ball.js';
import Light from './Light.js';
import Plane from './Plane.js';

class PongGame {
	constructor(constants) {
		this.PlayerLeft;
		this.PlayerRight;
		this.GameBall;
		this.renderer;
		this.scene;
		this.camera;
		this.light;
		this.light2;
		this.light3;
		this.plane;
		this.playgroundHeight = constants.game.playgroundHeight;
		this.sizeFactor = null;
		this.toggle3D = this.toggle3D.bind(this);
		this.setupGame(constants);
	}

	initializeRenderer(constants) {
		this.sizeFactor = window.innerWidth / constants.game.width;
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(
			Math.floor(window.innerWidth),
			Math.floor(constants.game.height * this.sizeFactor)
		);
		document.querySelector('#pong').appendChild(this.renderer.domElement);
	}

	setupCamera(constants) {
		const horizontalFOV = 75;
		const aspectRatio = constants.game.width / constants.game.height;
		const verticalFOV =
			2 *
			Math.atan(Math.tan((horizontalFOV * Math.PI) / 360) / aspectRatio) *
			(180 / Math.PI);

		this.camera = new THREE.PerspectiveCamera(verticalFOV, aspectRatio, 1, 500);

		this.camera.position.set(
			constants.game.width / 2,
			constants.game.height / 2,
			constants.game.height / (2 * Math.tan(verticalFOV * Math.PI / 360))
		);

		this.camera.lookAt(constants.game.width / 2, constants.game.height / 2, 0);
	}

	createScene() {
		this.scene = new THREE.Scene();
	}

	addPlayers(constants) {
		this.PlayerLeft = new Player(constants, true, 0xff0000);
		this.scene.add(this.PlayerLeft.player);

		this.PlayerRight = new Player(constants, false, 0x0000ff);
		this.scene.add(this.PlayerRight.player);
	}

	addBall(constants) {
		this.GameBall = new Ball(constants);
		this.scene.add(this.GameBall.ball);
	}

	addPlane(constants) {
		this.plane = new Plane(constants);
		this.scene.add(this.plane.plane);
		this.plane.plane.visible = false;
	}

	addLight(type, options) {
		const light = new Light(type, {
			color: options.color,
			intensity: options.intensity,
			position: options.position,
		});

		if (options.angle) {
			light.angle = options.angle;
		}

		if (options.penumbra) {
			light.penumbra = options.penumbra;
		}

		this.scene.add(light.light);
		return light;
	}

	setupLights(constants) {
		this.light = this.addLight(THREE.SpotLight, {
			color: 0xffffff,
			intensity: 750,
			position: {
				x: constants.game.width / 2,
				y: constants.game.height / 2,
				z: 30,
			},
			angle: Math.PI / 64,
		});

		this.light2 = this.addLight(THREE.SpotLight, {
			color: this.PlayerLeft.color,
			intensity: 1000,
			position: {
				x: this.PlayerRight.player.position.x,
				y: this.PlayerRight.player.position.y,
				z: 30,
			},
			penumbra: 0.7,
		});

		this.light3 = this.addLight(THREE.SpotLight, {
			color: this.PlayerRight.color,
			intensity: 1000,
			position: {
				x: this.PlayerLeft.player.position.x,
				y: this.PlayerLeft.player.position.y,
				z: 50,
			},
			penumbra: 0.7,
		});

		this.AmbientLight = this.addLight(THREE.AmbientLight, {
			color: 0x404040,
			intensity: 3,
			position: {},
		});
	}

	setupGame(constants) {
		this.initializeRenderer(constants);
		this.setupCamera(constants);
		this.createScene();
		this.addPlayers(constants);
		this.addBall(constants);
		this.addPlane(constants);
		this.setupLights(constants);
		this.renderer.render(this.scene, this.camera);
	}

	displayGameOver(game) {
		const gameOver = document.getElementById('game-over');
		gameOver.querySelector('p').textContent = 'Game Over';
		gameOver.style.display = 'grid';
		document.getElementById('winner').textContent = `${game.winner} won!`;
		return;
	}

	updateScore({left, right}) {
		const leftScore = document.querySelector('#left-score');
		leftScore.textContent = String(left.score);
		const rightScore = document.querySelector('#right-score');
		rightScore.textContent = String(right.score);
	}

	animate({players, ball, game}) {
		if (!game || game.over === undefined) {
			return;
		}
		requestAnimationFrame(this.animate);
		if (game.over === true) {
			this.displayGameOver(game);
		}

		this.PlayerLeft.player.position.setY(players.left.position.y);
		this.PlayerRight.player.position.setY(players.right.position.y);
		this.GameBall.ball.position.set(ball.position.x, ball.position.y, 0);

		if (ball.depth){
			this.GameBall.ball.rotation.x += 0.1;
			const rotationSpeed = 0.075;
			this.GameBall.ball.rotation.y += rotationSpeed;
		}
		this.light.followObject(this.GameBall.ball);
		this.light2.followObject(this.PlayerLeft.player);
		this.light3.followObject(this.PlayerRight.player);
		this.updateScore(players);
		this.renderer.render(this.scene, this.camera);
	}
}

export default PongGame;
