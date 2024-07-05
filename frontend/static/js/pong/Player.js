import * as THREE from 'three';

class Player {
	constructor(constants, isLeft) {
		this.isLeft = isLeft;
		this.player = this.createPlayer(constants);
	}

	createPlayer({players, game}) {
		const playerGeometry = new THREE.BoxGeometry(players.width, players.height, 0);
		const playerMaterial = new THREE.MeshBasicMaterial({color: 0xffffff});
		const player = new THREE.Mesh(playerGeometry, playerMaterial);
		if (this.isLeft) {
			player.position.set(game.margin + players.width / 2, Math.floor(game.height / 2), 0);

		} else {
			player.position.set(game.width - game.margin - players.width / 2, Math.floor(game.height / 2), 0);
		}
		return player;
	}
}
export default Player;
