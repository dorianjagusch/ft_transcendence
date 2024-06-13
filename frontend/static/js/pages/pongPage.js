<<<<<<< Updated upstream
import ChatSocket from '../pong/ChatSocket.js';
import PongContainer from '../pong/pong.js';
=======
import ChatSocket from '../websocket.js';
import pongService from '../services/pongService.js';
import { Pong } from '../components/pong.js';
>>>>>>> Stashed changes
import AView from './AView.js';
import {createGameBoard, setupGame} from '../pong/pongGame.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
	}

	async getHTML() {
<<<<<<< Updated upstream
		const pong = PongContainer();
		this.chatSocket = new ChatSocket();
		// this.chatSocket.connect();
=======
		let matchUrl = null;
		try {
			matchUrl = await pongService.getRequest();
			console.log(data);
		} catch {
			console.log('error in pong');
		}

		const pong = Pong();
>>>>>>> Stashed changes
		this.updateMain(pong);
		createGameBoard();
		setupGame();
		// document.getElementById('room-name').textContent = 'room'; //ADD ROOM NAME	}
	}
}
