import PongGame from './pongGame.js';

class ChatSocket {
	constructor(url) {

		this.chatSocket = null;

		try {
			this.chatSocket = new WebSocket(url);
		} catch (error) {
			throw new Error('Could not connect to chat socket');
		}

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
		if (this.chatSocket && this.chatSocket.readyState == WebSocket.OPEN) {
			this.chatSocket.close();
			this.removeEventListeners();
			this.chatSocket = null;
		}
	}

	handleError(e) {
		console.error('Chat socket error:', e);
		if (this.chatSocket && chatSocket.readyState == WebSocket.OPEN) {
			chatSocket.close();
		}
		this.removeEventListeners();
	}

	sendKey(e) {
		if (e.key == " " && this.game){
			if (!this.game.is3D){
				this.game.display3D();
			} else {
				this.game.display2D();
			}
		}
		this.chatSocket.send(e.key);
	}

	removeEventListeners() {
		if (this.chatSocket){
			this.chatSocket.removeEventListener('close', this.handleClose);
			this.chatSocket.removeEventListener('error', this.handleError);
			this.chatSocket.removeEventListener('message', this.acceptMessage);
			window.removeEventListener('keyup', this.sendKey);
		}
	}

	connect() {
		this.chatSocket.addEventListener('message', this.acceptMessage);
		this.chatSocket.addEventListener('close', this.handleClose);
		this.chatSocket.addEventListener('error', this.handleError);
		window.addEventListener('keyup', this.sendKey);
	}
}

export default ChatSocket;
