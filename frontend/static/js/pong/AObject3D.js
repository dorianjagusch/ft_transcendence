import * as THREE from 'three';

export default class AObject3D {
	constructor({materials, dimensions, ...rest}) {
		if (!materials)
			throw new TypeError('materials must be provided');
		for (const material of Object.values(materials)){
			if (!(material instanceof THREE.Material)){
				throw new TypeError('all materials must be an instance of THREE.Material');
			}
		}

		Object.assign(this, rest);
		this.object;
		this.materials = materials;
		this.dimensions = dimensions;
	}

	create() {
		throw new Error('create method must be implemented');
	}

	switchMaterial(material, hasShadow) {
		if (!(material instanceof THREE.Material))
			throw new TypeError('Material must be an instance of THREE.Material');

		if (!(typeof hasShadow === 'boolean'))
			throw new TypeError('hasShadow must be a boolean');

		this.object.material = material;
		this.object.receiveShadow = hasShadow;
		this.object.castShadow = hasShadow;
	}

	getDepth() {
		return this.dimensions.depth;
	}

	setDepth(newDepth) {
		if (!this.dimensions)
			throw new Error('dimensions must be set to update depth');

		const geometry = new THREE.BoxGeometry(
			this.dimensions.width,
			this.dimensions.height,
			newDepth
		);
		this.object.geometry.dispose();
		this.object.geometry = geometry;
	}
}