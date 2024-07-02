import * as THREE from 'three';
import elements from './setupSceneElements.js';
import Player from './Player.js';
import Ball from './Ball.js';

class PongGame {
	constructor(constants) {
		this.PlayerLeft;
		this.PlayerRight;
		this.GameBall;
		this.renderer;
		this.scene;
		this.camera;
		this.playgroundHeight = constants.game.playgroundHeight;
		this.sizeFactor = null;
		this.setupGame(constants);
	}

	setupGame(constants) {
		this.sizeFactor = window.innerWidth / constants.game.width;
		this.renderer = new THREE.WebGLRenderer();
		this.renderer.setSize(
			Math.floor(window.innerWidth),
			Math.floor(constants.game.height * this.sizeFactor)
		);
		document.querySelector('#pong').appendChild(this.renderer.domElement);

		this.camera = new THREE.PerspectiveCamera(
			90,
			constants.game.width / constants.game.height,
			1,
			500
		);
		this.camera.position.set(
			constants.game.width / 2,
			constants.game.height / 2,
			constants.game.height / 2
		);
		this.camera.lookAt(constants.game.width / 2, constants.game.height / 2, 0);

		this.scene = new THREE.Scene();

		this.PlayerLeft = new Player(constants, true);
		this.scene.add(this.PlayerLeft.player);

		this.PlayerRight = new Player(constants, false);
		this.scene.add(this.PlayerRight.player);

		this.GameBall = new Ball(constants);
		this.scene.add(this.GameBall.ball);

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
		this.updateScore(players);
		this.renderer.render(this.scene, this.camera);
	}
}

export default PongGame;
