import * as THREE from 'three';

class Ball {
	constructor(constants) {
		this.ball = this.createBall(constants);
	}

	createBall({ball: {size}, game}) {
		const ballGeometry = new THREE.BoxGeometry(size, size, 0);
		const ballMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
		const ball = new THREE.Mesh(ballGeometry, ballMaterial);
		ball.position.set(Math.floor(game.width / 2), Math.floor(game.height / 2), 0);
		return ball;
	}
}
export default Ball;
