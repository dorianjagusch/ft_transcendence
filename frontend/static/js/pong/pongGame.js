import * as THREE from 'three';
import Player from './Player.js';
import Ball from './Ball.js';
import Light from './Light.js';
import Plane from './Plane.js';

class PongGame {
	constructor(constants) {
		this.playerLeft;
		this.playerRight;
		this.gameBall;
		this.renderer;
		this.scene;
		this.camera;
		this.sceneLights;
		this.plane;
		this.materials;
		this.is3D = false;
		this.playgroundHeight = constants.game.playgroundHeight;
		this.sizeFactor = null;
		this.display3D = this.display3D.bind(this);
		this.display2D = this.display2D.bind(this);
		this.setupGame(constants);
	}

	initializeRenderer(constants) {
		this.sizeFactor = (window.innerWidth / constants.game.width) * 0.8;
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(
			Math.floor(window.innerWidth * 0.8),
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
			constants.game.height / (2 * Math.tan((verticalFOV * Math.PI) / 360))
		);

		this.camera.lookAt(constants.game.width / 2, constants.game.height / 2, 0);
	}

	createScene() {
		this.scene = new THREE.Scene();
	}

	addObject(Entity, constants, options = null) {
		if (!Entity instanceof THREE.Object3D && !Entity instanceof THREE.Light) {
			throw new Error('Entity must be a Three Object3D constructor');
		}
		const object = new Entity(constants, options);
		this.scene.add(object.object || object.light);
		return object;
	}

	addLights(constants) {
		const gameLights = [
			{
				type: THREE.SpotLight,
				props: {
					color: 0xffffff,
					intensity: 1000,
					position: {
						x: constants.game.width / 2,
						y: constants.game.height / 2,
						z: 30,
					},
				},
			},
			{
				type: THREE.SpotLight,
				props: {
					color: this.playerLeft.color,
					intensity: 1250,
					position: {
						x: this.playerRight.object.position.x,
						y: this.playerRight.object.position.y,
						z: 30,
					},
					penumbra: 0.7,
				},
			},
			{
				type: THREE.SpotLight,
				props: {
					color: this.playerRight.color,
					intensity: 1250,
					position: {
						x: this.playerLeft.object.position.x,
						y: this.playerLeft.object.position.y,
						z: 50,
					},
					penumbra: 0.7,
				},
			},
			{
				type: THREE.AmbientLight,
				props: {
					color: 0x606060,
					intensity: 3,
					position: {},
				},
			},
		];

		const sceneLights = gameLights.map((light) => this.addObject(Light, null, light));
		return sceneLights;
	}

	createMaterials() {
		const materials = {
			default: new THREE.MeshBasicMaterial({color: 0xffffff}),
			plane: new THREE.MeshLambertMaterial({color: 0x444444}),
			playerLeft: new THREE.MeshLambertMaterial({color: 0xfd4444}),
			playerRight: new THREE.MeshLambertMaterial({color: 0x4444df}),
			ball: new THREE.MeshLambertMaterial({color: 0xffffff}),
		};
		this.materials = materials;
	}

	addLine(constants) {
		const points = [];
		points.push(new THREE.Vector3(constants.game.width / 2, 0, 0));
		points.push(new THREE.Vector3(constants.game.width / 2, constants.game.height, 0));
		const lineGeometry = new THREE.BufferGeometry().setFromPoints(points);

		const lineMaterial = new THREE.LineDashedMaterial({
			color: 0xffffff,
			dashSize: 5,
			gapSize: 5,
			linewidth: 3,
		});

		const line = new THREE.Line(lineGeometry, lineMaterial);
		line.computeLineDistances();

		this.scene.add(line);
	}

	setupGame(constants) {
		this.initializeRenderer(constants);
		this.setupCamera(constants);
		this.createScene();
		this.addLine(constants);
		this.createMaterials();

		this.playerLeft = this.addObject(Player, constants, {
			materials: {
				default: this.materials.default,
				alternative: this.materials.playerLeft,
			},
			isLeft: true,
			color: 0xfd4444,
		});

		this.playerRight = this.addObject(Player, constants, {
			materials: {
				default: this.materials.default,
				alternative: this.materials.playerRight,
			},
			isLeft: false,
			color: 0x4444df,
		});

		this.gameBall = this.addObject(Ball, constants, {
			materials: {
				default: this.materials.default,
				alternative: this.materials.ball,
			},
		});
		this.plane = this.addObject(Plane, constants, {
			materials: {
				default: this.materials.plane,
			},
			visible: false,
		});
		this.sceneLights = this.addLights(constants);
		this.renderer.render(this.scene, this.camera);
	}

	displayGameOver(playerLeft, playerRight, game) {
		const gameOver = document.getElementById('game-over');
		gameOver.querySelector('p').textContent = 'Game Over';
		gameOver.style.display = 'grid';
		document.getElementById('winner').textContent = `${
			game.winner == 'player_left' ? playerLeft.name : playerRight.name
		} won!`;
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
			this.displayGameOver(this.playerLeft, this.playerRight, game);
		}

		this.playerLeft.object.position.setY(players.left.position.y);
		this.playerRight.object.position.setY(players.right.position.y);
		this.gameBall.object.position.set(ball.position.x, ball.position.y, 0);
		if (this.is3D) {
			this.gameBall.object.rotation.x += 0.1;
			const rotationSpeed = 0.075;
			this.gameBall.object.rotation.y += rotationSpeed;
			this.gameBall.object.updateMatrix();
		}
		this.sceneLights[0].followObject(this.gameBall.object);
		this.sceneLights[1].followObject(this.playerLeft.object);
		this.sceneLights[2].followObject(this.playerRight.object);
		this.updateScore(players);
		this.renderer.render(this.scene, this.camera);
	}

	display3D() {
		this.is3D = true;
		this.playerLeft.switchMaterial(this.materials.playerLeft, true);
		this.playerLeft.setDepth(this.playerLeft.getDepth());
		this.playerRight.switchMaterial(this.materials.playerRight, true);
		this.playerRight.setDepth(this.playerLeft.getDepth());
		this.gameBall.switchMaterial(this.materials.ball, true);
		this.gameBall.setDepth(this.gameBall.getDepth());
		this.plane.setVisibility(true);
	}

	display2D() {
		this.is3D = false;
		this.playerLeft.switchMaterial(this.materials.default, false);
		this.playerLeft.setDepth(0);
		this.playerRight.switchMaterial(this.materials.default, false);
		this.playerRight.setDepth(0);
		this.gameBall.switchMaterial(this.materials.default, false);
		this.gameBall.setDepth(0);
		this.gameBall.object.rotation.x = 0;
		this.gameBall.object.rotation.y = 0;
		this.plane.setVisibility(false);
	}

	dispose() {
		for (let key in this.materials) {
			const material = this.materials[key];
			if (material.dispose) {
				material.dispose();
			}
		}

		if (this.scene) {
			this.scene.traverse((object) => {
				this.disposeObject(object);
			});
		}

		const gl = this.renderer.getContext();
		const loseContextExtension = gl.getExtension('WEBGL_lose_context');
		if (loseContextExtension) {
			loseContextExtension.loseContext();
		}
	}

	disposeObject(object) {
		if (object.geometry) {
			object.geometry.dispose();
		}
		if (object.material) {
			this.disposeMaterial(object.material);
		}
	}

	disposeMaterial(material) {
		if (Array.isArray(material)) {
			material.forEach((mat) => mat.dispose());
		} else {
			material.dispose();
		}
	}
}

export default PongGame;
