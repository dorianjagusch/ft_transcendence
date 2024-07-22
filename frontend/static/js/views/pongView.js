import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';

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

	scrollToCanvas(mutation) {
		if (!mutation.addedNodes) {
			return;
		}
		mutation.addedNodes.forEach((node) => {
			if (node.tagName === 'CANVAS') {
				document.querySelector('canvas').scrollIntoView({behavior: 'smooth', block: 'center'});
			}
		});
	}

	checkForPongClosing(mutation) {
		if (!mutation.removedNodes) {
			return;
		}
		mutation.removedNodes.forEach((node) => {
			if (node.id != 'pong') {
				return;
			}
			this.chatSocket.handleClose();
			observer.disconnect();
		});
	}

	attachEventListeners() {
		document.querySelectorAll('.nav-link').forEach((link) => {
			link.addEventListener('click', this.chatSocket.handleClose);
		});

		window.addEventListener('beforeunload', this.chatSocket.handleClose);

		const observer = new MutationObserver((mutationsList, observer) => {
			for (let mutation of mutationsList) {
				this.checkForPongClosing(mutation, observer);
				this.scrollToCanvas(mutation);
			}
		});
		observer.observe(document.body.querySelector('main'), {childList: true, subtree: true});
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

		this.attachEventListeners();
		const pong = Pong.PongContainer();
		this.updateMain(pong);
	}
}
