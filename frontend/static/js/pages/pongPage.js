import ChatSocket from '../websocket.js';
import { Pong } from '../components/pong.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
	}

	appendEventListeners() {
		const chatSocket = ChatSocket();
		document.addEventListener('keydown', (event) => {
			const key = event.key;
			document.getElementById('key-pressed').textContent = key;
			chatSocket.send(
				JSON.stringify({
					message: key,
				})
			);
		});
	}

	async getHTML() {

		const pong = Pong();
		this.updateMain(pong);
		this.appendEventListeners();
	}
}
