import ChatSocket from '../pong/ChatSocket.js';
import PongService from '../services/pongService.js';
import TournamentService from '../services/tournamentService.js';
import constants from '../constants.js';
import Pong from '../pong/pong.js';
import AView from './AView.js';
import parseWStoMatchId from '../utils/parseWStoMatchId.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Pong');
		this.chatSocket = null;
		this.pongService = new PongService();
		this.tournamentService = new TournamentService();
		this.matchUrl = null;
		this.attachObserver = this.attachObserver.bind(this);
		this.attachEventListeners = this.attachEventListeners.bind(this);
		this.checkForPongClosing = this.checkForPongClosing.bind(this);
		this.isTournamentFinished = this.isTournamentFinished.bind(this);
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

	async isTournamentFinished() {
		const tournamentData = await this.tournamentService.getTournamentMatches(this.params);
		const matchesPlayed = tournamentData.reduce((acc, match) => {
			return match.state === constants.MATCHSTATUS.FINISHED ? acc + 1 : acc;
		}, 0);
		return matchesPlayed === (tournamentData.length - 1);
	}

	attachEventListeners() {
		document.querySelector('.new-game-button').addEventListener('click', async () => {
			if (!this.params?.tournament_id) {
				this.navigateTo(`/winner/match/${parseWStoMatchId(this.matchUrl)}`);
				return;
			}
			const match_id = parseInt(this.params.match_id) + 1;
			if (await this.isTournamentFinished(this.params)) {
				this.navigateTo(`/winner/tournament/${this.params.tournament_id}`);
			} else {
				this.navigateTo(`/preview/${this.params.tournament_id}/matches/${match_id}`);
			}
		});

		document.querySelectorAll('.nav-link').forEach((link) => {
			link.addEventListener('click', this.chatSocket.handleClose);
		});

		window.addEventListener('beforeunload', this.chatSocket.handleClose);
	}

	async getHTML() {
		try {
			if (this.params.tournament_id && this.params.match_id) {
				this.matchUrl = await this.pongService.getTournamentMatchRequest(this.params);
			} else {
				this.matchUrl = await this.pongService.getRequest(this.params);
				localStorage.removeItem('token');
			}
			this.chatSocket = new ChatSocket(this.matchUrl);
			this.chatSocket.connect();
		} catch (error) {
			this.notify(error.message, 'error');
			this.navigateTo('/play');
			return;
		}

		this.attachObserver();
		const pong = Pong.PongContainer(this.params.tournament_id);
		this.updateMain(pong);
		this.attachEventListeners();
	}
}
