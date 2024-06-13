import {animate} from './pongGame.js';

class ChatSocket {
	// const roomName = document.getElementById('room-name').textContent // ADD ROOM NAME
	// JSON.parse(
	// 	document.getElementById('room-name').textContent;
	// );

	constructor() {
		this.chatSocket = null; // + roomName + '/' //ADD ROOM NAME
	}

	acceptMessage(e) {
		const data = JSON.parse(e.data);
	}

	handleClose(e) {
		console.error('Chat socket closed unexpectedly');
	}

	handleError(e) {
		console.error('Chat socket error:', e);
	}

	sendKey(chatSocket, key) {
		//TODO: Handle esc or whatever other quit key
		chatSocket.send(
			JSON.stringify({
				message: key,
			})
		);
	}

	connect() {
		const chatSocket = new WebSocket(
			'ws://' + window.location.host + ':8080/pong/' // + roomName + '/' //ADD ROOM NAME
		);

		chatSocket.addEventListener('message', acceptMessage);

		chatSocket.addEventListener('close', handleClose);

		chatSocket.addEventListener('error', handleError);

		document.body.addEventListener('keyUp', sendKey);

		return chatSocket;
	}
}

export default ChatSocket;
