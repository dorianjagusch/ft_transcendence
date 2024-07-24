import ADialog from '../ADialog.js';
import AuthenticationModal from '../authenticationModal.js';
import selectPlayersForm from '../../formComponents/selectPlayersForm.js';
import TournamentService from '../../../services/tournamentService.js';

export default class SelectPlayersModal extends ADialog {
	constructor(parentDataHandler, tournamentData) {
		super(new selectPlayersForm(tournamentData), new TournamentService());
		this.authenticateUser = this.authenticateUser.bind(this);
		this.getFormData = this.getFormData.bind(this);
		this.onDataReceived = parentDataHandler;
		this.receiveUserData = this.receiveUserData.bind(this);
		this.numberOfPlayers = tournamentData.player_amount;
		this.tournamentName = tournamentData.name;
		this.player_ids = tournamentData.player_ids;
		this.tournamentId = tournamentData.id;
		this.adjustAuthenticationModal = this.adjustAuthenticationModal.bind(this);
		this.appendEventlistenters();
	}

	adjustAuthenticationModal(authenticationModal) {
		const authenticationTitle = document.createElement('h3');
		authenticationTitle.textContent = 'Authenticate Player';
		const authenticationButton = authenticationModal.form.form.querySelector('button');
		authenticationButton.textContent = 'Authenticate';
		authenticationModal.form.form.prepend(authenticationTitle);
	}

	authenticateUser(playerId) {
		let authenticationModal = document.querySelector(`[data-modal-${playerId}]`);
		if (!authenticationModal) {
			authenticationModal = new AuthenticationModal(this.receiveUserData);
			authenticationModal.dialog.classList.add('authenticate-user-modal', 'bg-primary');
			authenticationModal.dialog.setAttribute(`data-modal-id`, playerId);
			authenticationModal.dialog.classList.remove('bg-secondary');
			const main = document.querySelector('main');
			document.querySelector('main').appendChild(authenticationModal.dialog);
			this.adjustAuthenticationModal(authenticationModal);
		}
		authenticationModal.dialog.showModal();
	}

	updateCard(userData) {
		const clickedCard = document.querySelector(`[data-player-id="${userData.player_id}"]`);
		clickedCard.querySelector('.player-name').textContent = userData.username;
		clickedCard.querySelector('.player-img').src = userData.img;
		// TODO: make cog visible
		clickedCard.querySelector('.toggle-user > img').src = '../static/assets/img/minus.png';
		clickedCard.setAttribute('data-user-selected', 'true');
		clickedCard.classList.remove('bg-inactive');
	}

	receiveUserData(userData) {
		const authenticationModal = document.querySelector(
			`[data-modal-id="${userData.player_id}"]`
		);
		authenticationModal.close();
		this.updateCard(userData);
	}

	getFormData() {
		const form = this.form.getForm();
		const playerCards = document.querySelectorAll('[data-user-selected="true"]');
		if (playerCards.length !== parseInt(this.numberOfPlayers)) {
			return null;
		}
		const selectedPlayers = [];
		playerCards.forEach((playerCard) => {
			if (playerCard.getAttribute('data-user-selected') === 'true') {
				selectedPlayers.push({
					username: playerCard.querySelector('.player-name').textContent,
					img: playerCard.querySelector('.player-img').src,
					playerId: playerCard.getAttribute('data-player-id'),
				});
			}
		});
		return selectedPlayers;
	}

	completeTournamentData() {
		const players = this.getFormData();
		if (!players) {
			this.notify('All players must be provided');
			return;
		}
		const tournamentData = {
			players,
			tournamentId: this.tournamentId,
			tournamentName: this.tournamentName,
		};
		return tournamentData;
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			(e) => {
				if (e.target.classList.contains('accept-btn')) {
					e.preventDefault();
					const completeData = this.completeTournamentData();
					if (!completeData) {
						return;
					}
					try {
						this.onDataReceived(completeData);
					} catch (error) {
						this.notify(error.message);
					}
				}
			},
			false
		);
		this.dialog.querySelectorAll('.player-card').forEach((card) => {
			card.addEventListener('click', (e) => {
				e.preventDefault();
				if (e.target.parentElement.classList.contains('add')) {
					this.authenticateUser(
						e.target.parentElement.parentElement.parentElement.getAttribute(
							'data-player-id'
						)
					);
				} else if (e.target.classList.contains('add')) {
					this.authenticateUser(
						e.target.parentElement.parentElement.getAttribute('data-player-id')
					);
				}
			});
		});
	}
}
