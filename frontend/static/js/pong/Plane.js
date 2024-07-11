import * as THREE from 'three';
import AObject3D from './AObject3D.js';

export default class Plane extends AObject3D{
	constructor({game}, options){
		super(options)
		this.object = this.create(game);
	}

	create(game){
		const planeGeometry = new THREE.PlaneGeometry(game.width, game.height);
		const planeMaterial = new THREE.MeshLambertMaterial({color: 0x333333});
		const plane = new THREE.Mesh(planeGeometry, planeMaterial);
		plane.position.set(game.width / 2, game.height / 2, 0);
		plane.visible = false;
		plane.receiveShadow = true;
		return plane;
	}

	setVisibility(isVisible){
		if (!(typeof isVisible === 'boolean'))
			throw new TypeError('isVisible must be a boolean');

		this.object.visible = isVisible;
	}
}