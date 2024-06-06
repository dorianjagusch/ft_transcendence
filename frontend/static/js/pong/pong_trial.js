import * as THREE from 'three';

const width = window.innerWidth;
const height = window.innerHeight;
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(width, height);

document.body.appendChild(renderer.domElement);

const fov = 75;
const aspect = width / height;
const nearField = 0.1;
const farField = 1000;
const camera = new THREE.PerspectiveCamera(fov, width / height, nearField, farField);
camera.position.z = 2;

const scene = new THREE.Scene();

const geo = new THREE.IcosahedronGeometry(1, 2);
const mat = new THREE.MeshStandardMaterial({color: 0xffffff,
	flatShading: true,
});
const mesh = new THREE.Mesh(geo, mat);
scene.add(mesh);


const wireMat = new THREE.MeshBasicMaterial({color: 0xffffff, wireframe: true});
const wiremesh = new THREE.Mesh(geo, wireMat);
wiremesh.scale.setScalar(1.001);
scene.add(wiremesh);
mesh.add(wiremesh);

const hemiLight = new THREE.HemisphereLight(0x0099ff, 0xaa5500, 1);
scene.add(hemiLight);

function animate(t = 0) {
	requestAnimationFrame(animate);
	mesh.rotation.x += 0.001;
	mesh.rotation.y += 0.001;
	renderer.render(scene, camera);
}

animate();