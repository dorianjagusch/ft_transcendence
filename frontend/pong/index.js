import ChatSocket from "./websocket.js";
import showPong from "./pong.js";


showPong();
const chatSocket = ChatSocket();

document.addEventListener('keydown', (event) => {
	const key = event.key;
	document.getElementById('key-pressed').textContent = key;
	chatSocket.send(
		JSON.stringify({
			message: key,
		})
	);
});