import * as THREE from 'three';

const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 500);
camera.position.set(0, 0, 100);
camera.lookAt(0, 0, 0);

const scene = new THREE.Scene();
const material = new THREE.LineBasicMaterial({
	color: 0x0000ff,
	linewidth: 10,});

const createPlayer = (position = 'left')

const LineLeft = [];
LineLeft.push(new THREE.Vector3(0, -10, 0));
LineLeft.push(new THREE.Vector3(0, 10, 0));

const geometry = new THREE.BufferGeometry().setFromPoints(LineLeft);
const playerLeft = new THREE.Line(geometry, material);

scene.add(playerLeft);
renderer.render(scene, camera);