import PongGame from './pongGame.js';

class ChatSocket {
	constructor(url) {
		this.chatSocket = new WebSocket(url);
		this.acceptMessage = this.acceptMessage.bind(this);
		this.handleClose = this.handleClose.bind(this);
		this.handleError = this.handleError.bind(this);
		this.sendKey = this.sendKey.bind(this);
		this.removeEventListeners = this.removeEventListeners.bind(this);
		this.connect = this.connect.bind(this);
		this.game = null;
	}

	acceptMessage(e) {
		const data = JSON.parse(e.data);
		if (this.game === null) {
			this.game = new PongGame(data);
		}
		this.game.animate(data);
	}

	handleClose(e) {
		console.error('Chat socket closed unexpectedly');
		this.removeEventListeners();
	}

	handleError(e) {
		console.error('Chat socket error:', e);
		if (chatSocket.readyState == WebSocket.OPEN) {
			chatSocket.close();
		}
		this.removeEventListeners();
	}

	sendKey(e) {
		this.chatSocket.send(e.key);
	}

	removeEventListeners() {
		this.chatSocket.removeEventListener('close', this.handleClose);
		this.chatSocket.removeEventListener('error', this.handleError);
		this.chatSocket.removeEventListener('message', this.acceptMessage);
		window.removeEventListener('keyup', this.sendKey);
	}

	connect() {
		this.chatSocket.addEventListener('message', this.acceptMessage);
		this.chatSocket.addEventListener('close', this.handleClose);
		this.chatSocket.addEventListener('error', this.handleError);
		window.addEventListener('keyup', this.sendKey);
	}
}

export default ChatSocket;
