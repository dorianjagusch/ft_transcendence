class ChatSocket {
	constructor() {
		this.chatSocket = null;
	}

	receiveMessage(e) {
		const data = JSON.parse(e.data);
		document.querySelector('#received').innerText += data.message + '\n';
	}
	closeSocket(e) {
		console.error('Chat socket closed unexpectedly');
	}
	handleSocketError(e) {
		console.error('Chat socket error:', e);
	}
	sendMessage(e) {
		const keyPressed = document.querySelector('#key-pressed');
		const key = keyPressed.value;
		this.chatSocket.send(
			JSON.stringify({
				message: key,
			})
		);
		keyPressed.value = '';
	}

	connect() {
		this.chatSocket = new WebSocket(
			'ws://' + window.location.host + ':8080/pong/match/test' // + roomName + '/' //ADD ROOM NAME
		);

		this.chatSocket.addEventListener('message', this.receiveMessage);
		this.chatSocket.addEventListener('close', this.closeSocket);
		this.chatSocket.addEventListener('error', this.handleSocketError);
		document.querySelector('#key-pressed').addEventListener('keyup', this.sendMessage);
	}
}

export default ChatSocket;
