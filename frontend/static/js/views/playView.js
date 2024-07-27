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
		this.startTournament = this.startTournament.bind(this);
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

	adjustSummaryModal(tournamentName) {
		document.querySelector('main').appendChild(this.summaryModal.dialog);
		this.summaryModal.dialog.classList.add('summary-modal');
		this.summaryModal.dialog.classList.remove('bg-secondary');
		this.summaryModal.dialog.classList.add('bg-primary');
		const summaryTitle = document.createElement('h3');
		summaryTitle.textContent = `Start tournament ${tournamentName}?`;
		document.querySelector('.selected-players').prepend(summaryTitle);
	}

	openSummaryModal(tournamentData) {
		this.selectPlayersModal.dialog.close();
		this.summaryModal = new SummaryModal(this.startTournament, tournamentData);
		this.adjustSummaryModal(tournamentData.tournamentName);
		this.summaryModal.dialog.showModal();
	}

	startTournament(matchData) {
		document.querySelector('.summary-modal').close();
		if (matchData.token)
			localStorage.setItem('token', matchData.token);
		this.navigateTo(`/preview/${matchData.id}/matches/${matchData.next_match}`);
	}

	adjustSelectPlayerModal(tournamentName) {
		document.querySelector('main').appendChild(this.selectPlayersModal.dialog);
		this.selectPlayersModal.dialog.classList.add('player-modal');
		this.selectPlayersModal.dialog.classList.remove('bg-secondary');
		this.selectPlayersModal.dialog.classList.add('bg-primary');
		const selectPlayerTitle = document.createElement('h3');
		selectPlayerTitle.textContent = `Select Players for ${tournamentName}`;
		document.querySelector('.player-selection').prepend(selectPlayerTitle);
	}

	openSelectPlayersModal(tournamentData) {
		this.playerNumberModal.dialog.close();
		if (this.selectPlayersModal && this.selectPlayersModal.tournamentId === tournamentData.tournament_id) {
			this.selectPlayersModal.dialog.showModal();
			return;
		}
		this.selectPlayersModal = new SelectPlayersModal(this.openSummaryModal, tournamentData);
		this.adjustSelectPlayerModal(tournamentData.tournament.name);
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