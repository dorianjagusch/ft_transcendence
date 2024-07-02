import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';
import PongGame from '../pong/pongGame.js';


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
			this.chatSocket = new ChatSocket(matchUrl);
			this.chatSocket.connect();
		} catch (error) {
			console.log(error);
		}

		const pong = Pong.PongContainer();
		this.updateMain(pong);
	}
}
