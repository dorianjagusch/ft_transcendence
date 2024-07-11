import AView from './AView.js';
import {GameCard} from '../components/gameCard.js';
import TournamentModal from '../components/dialogs/tournamentModals/tournamentModal.js';
import playersModal from '../components/dialogs/tournamentModals/playerModal.js';
import changeNickNameModal from '../components/dialogs/tournamentModals/changeNickNameModal.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Play');
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
	}

	async getHTML() {
		const gameOne = GameCard('Pong', 'pong-front', 'pong-card');

		const playerNumberModal = new TournamentModal();
		playerNumberModal.dialog.classList.add('player-number-modal');
		playerNumberModal.dialog.classList.remove('bg-secondary');
		playerNumberModal.dialog.classList.add('bg-primary');

		const selectPlayersModal = new playersModal();
		const playerNameModal = new changeNickNameModal();

		this.updateMain(
			gameOne,
			playerNumberModal.dialog,
			selectPlayersModal.dialog,
			playerNameModal.dialog
		);
		const main = document.querySelector('main');
		main.classList.add('flex-row');
		this.attachEventListeners();
	}
}
