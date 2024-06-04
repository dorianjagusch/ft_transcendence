const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.serSize (window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 500);
CanvasCaptureMediaStreamTrack.position.set( 0, 0, 100 );
camera.lookAt(0, 0, 0);

const scene = new THREE.Scene();

