import * as THREE from 'three'
import AObject3D from './AObject3D.js'


class Ball extends AObject3D{
	constructor(constants, options) {
		super(options)
		this.dimensions = {
			width: constants.ball.size,
			height: constants.ball.size,
			depth: constants.ball.size,
		};
		this.object = this.create(constants);
	}

	create({game}) {
		const ballGeometry = new THREE.BoxGeometry(this.dimensions.width, this.dimensions.height, this.dimensions.depth);
		const ballMaterial = this.materials.default;
		const ball = new THREE.Mesh(ballGeometry, ballMaterial);
		ball.position.set(Math.floor(game.width / 2), Math.floor(game.height / 2), 0);
		return ball;
	}
}
export default Ball;
