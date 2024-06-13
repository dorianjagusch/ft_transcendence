import ChatSocket from '../pong/ChatSocket.js';
import PongContainer from '../pong/pong.js';
import AView from './AView.js';
import {setupGame} from '../pong/pongGame.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
	}

	async getHTML() {
		const pong = PongContainer();
		this.chatSocket = new ChatSocket();
		this.chatSocket.connect();
		this.updateMain(pong);
		setupGame();
		// document.getElementById('room-name').textContent = 'room'; //ADD ROOM NAME	}
	}
}
