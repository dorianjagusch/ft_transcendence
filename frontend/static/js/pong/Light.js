import NotImplentedError from "../exceptions/NotImplementedException.js";
import * as THREE from 'three';

export default class Light {
	constructor(Light, {color, intensity, position, circleRadius, angleRad, speed, target}) {
		this.position = position;
		this.angleRad = angleRad || null;
		this.speed = speed || null;
		this.color = color;
		this.intensity = intensity;
		this.lightCircleRadius = circleRadius || null;
		this.light = this.createLight(Light);
		this.target = target || null;
	}

	createLight(Light) {
		const light = new Light(this.color, this.intensity);
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
		this.light.target = target;
		this.light.target.updateMatrixWorld();
	}

	moveLightCircular() {
		if (this.angleRad === null || this.speed === null) {
			throw new NotImplentedError('angleRad and speed must be set to move light circularly.');
		}
		this.light.position.x = this.position.x + this.lightCircleRadius * Math.cos(this.angleRad);
		this.light.position.z = this.position.z + this.lightCircleRadius * Math.sin(this.angleRad);
		this.angleRad += 0.1;
	}
}
