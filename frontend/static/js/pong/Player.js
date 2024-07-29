import * as THREE from 'three';
import AObject3D from './AObject3D.js';

class Player extends AObject3D{
	constructor(constants, options) {
		super(options)
		if (this.isLeft === undefined || !(typeof this.isLeft === 'boolean'))
			throw new TypeError('isLeft needs to be provided as a boolean');
		if (!this.color)
			throw new TypeError('color must be a number');

		this.dimensions = {
			width: constants.players.width,
			height: constants.players.height,
			depth: 3 * constants.ball.size,
		};
		this.name = this.isLeft ? constants.players.left_name : constants.players.right_name;
		this.object = this.create(constants);
	}

	create({players, game}) {
		const playerGeometry = new THREE.BoxGeometry(players.width, players.height, 0);
		const playerMaterial = this.materials.default;
		const player = new THREE.Mesh(playerGeometry, playerMaterial);
		if (this.isLeft) {
			player.position.set(game.margin + players.width / 2, Math.floor(game.height / 2), 0);
		} else {
			player.position.set(
				game.width - game.margin - players.width / 2,
				Math.floor(game.height / 2),
				0
			);
		}
		return player;
	}

}
export default Player;
