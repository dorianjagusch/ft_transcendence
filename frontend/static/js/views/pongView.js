import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';
import PongGame from '../pong/pongGame.js';

/*TODO: Let it take parameters to distingish between match and tournament
		expect /tournament/id/match/id or /match/id*/

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
		this.pongService = new PongService();
		this.attachEventListeners = this.attachEventListeners.bind(this);
	}

	attachEventListeners() {
		document.querySelectorAll('.nav-link').forEach((link) => {
			link.addEventListener('click', this.chatSocket.handleClose);
		});

		window.addEventListener('beforeunload', this.chatSocket.handleClose);


		// TODO unnest the conditionals in the loop
		const observer = new MutationObserver((mutationsList, observer) => {
			for (let mutation of mutationsList) {
				if (mutation.removedNodes) {
					mutation.removedNodes.forEach((node) => {
						if (node.id = "pong") {
							this.chatSocket.handleClose();
							observer.disconnect();
						}
					});
				}
			}
		});
		observer.observe(document.body, {childList: true, subtree: true});
	}

	async getHTML() {
		let matchUrl = null;
		try {
			matchUrl = await this.pongService.getRequest();
			this.chatSocket = new ChatSocket(matchUrl);
			this.chatSocket.connect();
		} catch (error) {
			this.notify(error);
			this.navigateTo('/play');
		}

		const pong = Pong.PongContainer();
		this.updateMain(pong);
		this.attachEventListeners();
	}
}
