import AView from './AView.js';
import {GameCard} from '../components/gameCard.js';
import TournamentModal from '../components/dialogs/tournamentModals/tournamentModal.js';
import SelectPlayersModal from '../components/dialogs/tournamentModals/selectPlayersModal.js';
import SummaryModal from '../components/dialogs/tournamentModals/summaryModal.js';


export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Play');
		this.openSelectPlayersModal = this.openSelectPlayersModal.bind(this);
		this.openSummaryModal = this.openSummaryModal.bind(this);
	}

	attachEventListeners() {
		const gameCard = document.querySelector('.game-card');
		gameCard.addEventListener('click', () => {
			this.navigateTo('/match');
		});

		const tournamentButton = document.querySelector('.tournament-button');
		if (tournamentButton) {
			tournamentButton.addEventListener('click', () => {
				const playerModal = document.querySelector('.player-number-modal');
				playerModal.showModal();
			});
		}
		if (!document.querySelector('.select-players-modal')) {
			return;
		}
	}

	adjustSummaryModal() {
		document.querySelector('main').appendChild(this.summaryModal.dialog);
		this.summaryModal.dialog.classList.add('summary-modal');
		this.summaryModal.dialog.classList.remove('bg-secondary');
		this.summaryModal.dialog.classList.add('bg-primary');
		const summaryTitle = document.createElement('h3');
		summaryTitle.textContent = 'Start this tournament?';
		document.querySelector('.selected-players').prepend(summaryTitle);
	}

	openSummaryModal(tournamentData) {
		this.selectPlayersModal.dialog.close();
		this.summaryModal = new SummaryModal(this.startTournament, tournamentData);
		this.adjustSummaryModal();
		this.summaryModal.dialog.addEventListener('click', async (e) => {
			if (e.target.classList.contains('accept-btn')) {
				e.preventDefault();
				this.summaryModal.dialog.close();
				console.log(tournamentData);
				debugger;
				await this.summaryModal.service.patchRequest(tournamentData);
				// const matchData = await this.summaryModal.service.startTournament(tournamentData);
				console.log(matchData);
				debugger;
			} else if (e.target.classList.contains('decline-btn')) {
				e.preventDefault();
				this.summaryModal.dialog.close();
				this.selectPlayersModal.dialog.showModal();
			}
		});
		this.summaryModal.dialog.showModal();
	}

	startTournament(tournamentData) {
		console.log(tournamentData);
		debugger;

		// this.navigateTo(`/tournament/${tournamentData.id}/match/${tournamentData.match_id}`);
	}

	adjustSelectPlayerModal() {
		document.querySelector('main').appendChild(this.selectPlayersModal.dialog);
		this.selectPlayersModal.dialog.classList.add('player-modal');
		this.selectPlayersModal.dialog.classList.remove('bg-secondary');
		this.selectPlayersModal.dialog.classList.add('bg-primary');
		const selectPlayerTitle = document.createElement('h3');
		selectPlayerTitle.textContent = 'Select Players';
		document.querySelector('.player-selection').prepend(selectPlayerTitle);
	}

	openSelectPlayersModal(tournamentData) {
		this.playerNumberModal.dialog.close();
		if (this.selectPlayersModal && this.selectPlayersModal.tournamentId === tournamentData.tournament_id) {
			this.selectPlayersModal.dialog.showModal();
			return;
		}
		console.log(tournamentData);
		this.selectPlayersModal = new SelectPlayersModal(this.openSummaryModal, tournamentData);
		this.adjustSelectPlayerModal();
		this.selectPlayersModal.dialog.addEventListener('click', (e) => {
			if (e.target.classList.contains('decline-btn')) {
				e.preventDefault();
				this.selectPlayersModal.dialog.close();
				this.playerNumberModal.dialog.showModal();
			}
		});
		this.selectPlayersModal.dialog.showModal();

	}

	async getHTML() {
		const gameOne = GameCard('Pong', 'pong-front', 'pong-card');

		this.playerNumberModal = new TournamentModal(this.openSelectPlayersModal);
		this.playerNumberModal.dialog.classList.add('player-number-modal');
		this.playerNumberModal.dialog.classList.remove('bg-secondary');
		this.playerNumberModal.dialog.classList.add('bg-primary');

		this.updateMain(gameOne, this.playerNumberModal.dialog);
		const main = document.querySelector('main');
		main.classList.add('flex-row');
		this.attachEventListeners();
	}
}


//TODO: check that the data from tournament modal arrives correctly in selectPlayersModal (removed await in tournament service and haven't tested it further)