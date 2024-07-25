import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import TournamentService from '../services/tournamentService.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
		this.pongService = new PongService();
		this.tournamentService = new TournamentService();
		this.attachObserver = this.attachObserver.bind(this);
		this.attachEventListeners = this.attachEventListeners.bind(this);
		this.checkForPongClosing = this.checkForPongClosing.bind(this);
	}

	scrollToCanvas(mutation) {
		if (!mutation.addedNodes) {
			return;
		}
		mutation.addedNodes.forEach((node) => {
			if (node.tagName === 'CANVAS') {
				document
					.querySelector('canvas')
					.scrollIntoView({behavior: 'smooth', block: 'center'});
			}
		});
	}

	checkForPongClosing(mutation, observer) {
		if (!mutation.removedNodes) {
			return;
		}
		mutation.removedNodes.forEach((node) => {
			if (node.id != 'pong') {
				return;
			}
			this.chatSocket?.handleClose();
			observer?.disconnect();
		});
	}

	attachObserver() {
		const observer = new MutationObserver((mutationsList, observer) => {
			for (let mutation of mutationsList) {
				this.checkForPongClosing(mutation, observer);
				this.scrollToCanvas(mutation);
			}
		});
		observer.observe(document.body.querySelector('main'), {childList: true, subtree: true});
	}

	attachEventListeners() {
		document.querySelector('.new-game-button').addEventListener('click', async () => {
			if (this.params?.tournament_id) {
				const match_id = parseInt(this.params.match_id) + 1;
				this.navigateTo(`/preview/${this.params.tournament_id}/matches/${match_id}`);
			} else {
				this.navigateTo(`/match`);
			}
		});

		document.querySelectorAll('.nav-link').forEach((link) => {
			link.addEventListener('click', this.chatSocket.handleClose);
		});

		window.addEventListener('beforeunload', this.chatSocket.handleClose);
	}

	async getHTML() {
		let matchUrl = null;
		try {
			if (this.params.tournament_id && this.params.match_id) {
				matchUrl = await this.pongService.getTournamentMatchRequest(this.params);
			} else {
				matchUrl = await this.pongService.getRequest();
				localStorage.removeItem('token');
			}
			this.chatSocket = new ChatSocket(matchUrl);
			this.chatSocket.connect();
		} catch (error) {
			this.notify(error);
			this.navigateTo('/play');
		}

		this.attachObserver();
		const pong = Pong.PongContainer(this.params.tournament_id);
		this.updateMain(pong);
		this.attachEventListeners();
	}
}
