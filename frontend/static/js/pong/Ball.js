import * as THREE from 'three';

class Ball {
	constructor(constants) {
		this.ball = this.createBall(constants);
	}

	createBall({ball: {ballWidth, ballHeight}, game}) {
		const ballGeometry = new THREE.BoxGeometry(ballWidth, ballHeight, 0);
		const ballMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
		const ball = new THREE.Mesh(ballGeometry, ballMaterial);
		ball.position.set(game.width / 2, game.height / 2, 0);
		return ball;
	}
}
export default Ball;
