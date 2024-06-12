import ChatSocket from '../components/pong/ChatSocket.js';
import {Pong} from '../components/pong/pong.js';
import pongGame from '../components/pong/pongGame.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
	}

	async getHTML() {
		const pong = Pong();
		this.updateMain(pong);
		pongGame.initialiseGame();
		// document.getElementById('room-name').textContent = 'room'; //ADD ROOM NAME
		const chatSocket = new ChatSocket();
		chatSocket.connect();
	}
}
