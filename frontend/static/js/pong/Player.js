import * as THREE from 'three';

class Player {
	constructor(constants, isLeft, color) {
		this.isLeft = isLeft;
		this.color = color;
		this.materials = {
			default: new THREE.MeshBasicMaterial({color: 0xffffff}),
			alternative: new THREE.MeshLambertMaterial({color: color}),
		};
		this.depth = 3 * constants.ball.size;
		this.width = constants.players.width;
		this.height = constants.players.height;
		this.player = this.createPlayer(constants);
	}

	createPlayer({players, game}) {
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

	switchMaterial() {
		if (this.player.material === this.materials.default) {
			this.player.material = this.materials.alternative;
			this.player.receiveShadow = true;
			this.player.castShadow = true;
		} else {
			this.player.material = this.materials.default;
			this.player.receiveShadow = false;
			this.player.castShadow = false;
		}
	}

	updatePlayerDepth() {
		const playerGeometry = new THREE.BoxGeometry(
			this.width,
			this.height,
			this.player.geometry.parameters.depth ? 0 : this.depth
		);
		this.player.geometry.dispose();
		this.player.geometry = playerGeometry;
	}
}
export default Player;
