import ChatSocket from '../websocket.js';
import PongService from '../services/pongService.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';
import {createGameBoard, setupGame} from '../pong/pongGame.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
		this.pongService = new PongService();
	}

	async getHTML() {
		let matchUrl = null;
		try {
			matchUrl = await this.pongService.getRequest();
			console.log(matchUrl);
		} catch (error) {
			console.log(error);
		}

		const pong = Pong();
		this.updateMain(pong);
		createGameBoard();
		setupGame();
		// document.getElementById('room-name').textContent = 'room'; //ADD ROOM NAME	}
	}
}
