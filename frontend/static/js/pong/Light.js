import NotImplentedError from '../exceptions/NotImplementedException.js';
import * as THREE from 'three';

export default class Light {
	constructor(constants, {type, props}) {
		Object.assign(this, props);
		this.light = this.createLight(type);
	}

	createLight(Light) {
		const light = new Light(this.color, this.intensity);

		if (!(light instanceof THREE.Light)) {
			throw new Error('Light must be a Three Light constructor');
		}

		light.position.set(this.position.x, this.position.y, this.position.z);
		light.castShadow = true;
		if (this.target) {
			light.target = this.target;
		}
		return light;
	}

	followObject(target) {
		if (!(this.light instanceof THREE.SpotLight)) {
			throw new TypeError('Light must be a SpotLight to follow an object.');
		}
		if (!target instanceof THREE.Object3D) {
			throw new TypeError('target must be a THREE.Object3D');
		}
		this.light.target = target;
		this.light.target.updateMatrixWorld();
	}

	moveLightCircular() {
		if (!this.angleRad || !this.speed) {
			throw new Error('angleRad and speed must be set to move light circularly.');
		}
		this.light.position.x = this.position.x + this.lightCircleRadius * Math.cos(this.angleRad);
		this.light.position.z = this.position.z + this.lightCircleRadius * Math.sin(this.angleRad);
		this.angleRad += 0.1;
	}
}
