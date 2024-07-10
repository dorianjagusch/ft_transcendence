import * as THREE from 'three';

class Ball {
	constructor(constants) {
		this.materials = {
			default: new THREE.MeshBasicMaterial({color: 0xffffff}),
			alternative: new THREE.MeshLambertMaterial({color: 0xffffff}),
		};
		this.size = constants.ball.size;
		this.depth = 0;
		this.ball = this.createBall(constants);
	}

	createBall({game}) {
		const ballGeometry = new THREE.BoxGeometry(this.size, this.size, this.depth);
		const ballMaterial = this.materials.default;
		const ball = new THREE.Mesh(ballGeometry, ballMaterial);
		ball.position.set(Math.floor(game.width / 2), Math.floor(game.height / 2), 0);
		return ball;
	}

	switchMaterial() {
		if (this.ball.material === this.materials.default) {
			this.ball.material = this.materials.alternative;
			this.ball.castShadow = true;
			this.ball.receiveShadow = true;
		} else {
			this.ball.material = this.materials.default;
			this.ball.castShadow = false;
			this.ball.receiveShadow = false;
		}
	}

	updateBallDepth() {
		const ballGeometry = new THREE.BoxGeometry(
			this.size,
			this.size,
			this.depth ? 0 : this.size
		);
		this.ball.geometry.dispose();
		this.ball.geometry = ballGeometry;
	}
}
export default Ball;
