import PongGame from './pongGame.js';
import {navigateTo} from '../router.js';
import notify from '../utils/notify.js';

class ChatSocket {
	constructor(url) {

		this.chatSocket = null;

		try {
			this.chatSocket = new WebSocket(url);
		} catch (error) {
			notify('Could not connect to server', 'error');
			setTimeout(() => navigateTo('/play'), 100);
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

		notify('Connection closed');
		setTimeout(() => navigateTo('/play'), 100);
	}

	handleError(e) {
		if (this.chatSocket && this.chatSocket.readyState == WebSocket.OPEN) {
			chatSocket.close();
		}
		this.removeEventListeners();

		setTimeout(() => navigateTo('/play'), 100);
	}

	sendKey(e) {
		if (e.key == " " && this.game){
			if (!this.game.is3D){
				this.game.display3D();
			} else {
				this.game.display2D();
			}
		}
		if (this.chatSocket && this.chatSocket.readyState == WebSocket.OPEN)
			this.chatSocket.send(e.key);
		if (e.key == "Enter" && this.game){
			Array.from(document.querySelectorAll('.instructions')).forEach(instruction => {
				instruction.style.display = 'none';
			})
		}
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
        try {
            this.chatSocket.addEventListener('message', this.acceptMessage);
            this.chatSocket.addEventListener('close', this.handleClose);
            this.chatSocket.addEventListener('error', this.handleError);
            window.addEventListener('keyup', this.sendKey);
        } catch (error) {
            notify('Could not connect to server', 'error');
            this.scheduleReconnect();
        }
    }

    scheduleReconnect() {
        setTimeout(() => this.connect(), 1000);
    }
}

export default ChatSocket;
