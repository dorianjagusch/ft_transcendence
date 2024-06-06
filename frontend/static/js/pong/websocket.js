import {animate} from './lines.js';

const acceptMessage = (e) => {
	const data = JSON.parse(e.data);
};

const handleClose = (e) => {
	console.error('Chat socket closed unexpectedly');
};

const handleError = (e) => {
	console.error('Chat socket error:', e);
};

const sendKey = (chatSocket, key) => {
	//TODO: Handle esc or whatever other quit key
	chatSocket.send(
		JSON.stringify({
			message: key,
		})
	);
};

const ChatSocket = () => {
	// const roomName = document.getElementById('room-name').textContent // ADD ROOM NAME
	// JSON.parse(
	// 	document.getElementById('room-name').textContent;
	// );

	const chatSocket = new WebSocket(
		'ws://' + window.location.host + ':8080/pong/' // + roomName + '/' //ADD ROOM NAME
	);

	chatSocket.addEventListener('message', acceptMessage);

	chatSocket.addEventListener('close', handleClose);

	chatSocket.addEventListener('error', handleError);

	document.body.addEventListener("keyUp", sendKey);

	return chatSocket;
};

export default ChatSocket;
