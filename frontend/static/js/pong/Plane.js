import * as THREE from 'three';

export default class Plane {
	constructor({game}){
		this.plane = this.createPlane(game);
	}


	createPlane(game){
		const planeGeometry = new THREE.PlaneGeometry(game.width, game.height);
		const planeMaterial = new THREE.MeshLambertMaterial({color: 0x333333});
		const plane = new THREE.Mesh(planeGeometry, planeMaterial);
		plane.position.set(game.width / 2, game.height / 2, 0);
		plane.receiveShadow = true;
		return plane;
	}
}