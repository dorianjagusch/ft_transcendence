import ChatSocket from '../pong/websocket.js';
import { Pong } from '../pong/pong.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
	}

	appendEventListeners() {
		const chatSocket = ChatSocket();
	}

	async getHTML() {

		const pong = Pong();
		this.updateMain(pong);
		document.querySelector('main').classList.add('pong', 'flex-col');
		this.appendEventListeners();
	}
}
