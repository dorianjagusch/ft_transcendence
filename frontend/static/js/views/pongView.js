import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import TournamentService from '../services/tournamentService.js';
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
		this.tournamentService = new TournamentService();
		this.attachObserver = this.attachObserver.bind(this);
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

	attachEventListeners() {
		debugger;
		document.querySelector('.new-game-button').addEventListener('click', async () => {
			debugger
			const nextMatch = await this.tournamentService.getNextMatch(this.params);
			console.log(nextMatch);
			debugger;
			this.navigateTo(`/pong/tournaments/${this.params.tournament_id}/matches/${nextMatch}`);
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
				matchUrl = await this.pongService.getMatchRequest(this.params);
			} else {
				matchUrl = await this.pongService.getRequest();
			}
			localStorage.removeItem('token');
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
