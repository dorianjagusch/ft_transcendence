import ADialog from '../ADialog.js';
import AuthenticationModal from '../authenticationModal.js';
import selectPlayersForm from '../../formComponents/selectPlayersForm.js';
import TournamentService from '../../../services/tournamentService.js';
import getProfilePicture from '../../profilePicture.js';
import {updateCard, resetCard} from '../../formComponents/PlayerCard.js';

export default class SelectPlayersModal extends ADialog {
	constructor(parentDataHandler, {tournament, tournament_player}) {
		super(new selectPlayersForm({tournament, tournament_player}), new TournamentService());
		this.onDataReceived = parentDataHandler;
		this.numberOfPlayers = tournament.player_amount;
		this.tournamentName = tournament.name;
		this.tournamentId = tournament.id;
		this.tournamentHostId = tournament_player.id;

		this.authenticateUser = this.authenticateUser.bind(this);
		this.getFormData = this.getFormData.bind(this);
		this.receiveUserData = this.receiveUserData.bind(this);
		this.adjustAuthenticationModal = this.adjustAuthenticationModal.bind(this);
		this.updateCard = updateCard.bind(this);
		this.resetCard = resetCard.bind(this);
		this.deletePlayer = this.deletePlayer.bind(this);
		this.addPlayer = this.addPlayer.bind(this);

		this.appendEventlistenters();
	}

	adjustAuthenticationModal(authenticationModal) {
		const authenticationTitle = document.createElement('h3');
		authenticationTitle.textContent = 'Authenticate Player';
		const authenticationButton = authenticationModal.form.form.querySelector('button');
		authenticationButton.textContent = 'Authenticate';
		authenticationModal.form.form.prepend(authenticationTitle);
	}

	authenticateUser(modalId) {
		const authenticationModal = new AuthenticationModal(
			TournamentService,
			this.receiveUserData,
			{
				tournamentId: this.tournamentId,
			}
		);
		authenticationModal.dialog.classList.add('authenticate-user-modal', 'bg-primary');
		authenticationModal.dialog.classList.remove('bg-secondary');
		authenticationModal.dialog.setAttribute('data-modal-id', modalId);
		document.querySelector('main').appendChild(authenticationModal.dialog);
		this.adjustAuthenticationModal(authenticationModal);
		authenticationModal.dialog.showModal();
	}

	async receiveUserData(userData) {
		try {
			await userData;
		} catch (error) {
			this.notify(error.message);
			return;
		}
		userData.img = await getProfilePicture(userData.user);
		document.querySelector('.authenticate-user-modal').remove();
		const clickedCard = document.querySelector(`[data-fetching]`);
		this.updateCard(clickedCard, userData);
	}

	getFormData() {
		const form = this.form.getForm();
		const playerCards = form.querySelectorAll('[data-player-id]');
		if (playerCards.length !== parseInt(this.numberOfPlayers)) {
			return null;
		}
		const selectedPlayers = Array.from(playerCards).map((playerCard) => {
			if (playerCard.getAttribute('data-user-selected') === 'true') {
				return {
					username: playerCard.querySelector('.player-name').textContent,
					img: playerCard.querySelector('.player-img').src,
					playerId: playerCard.getAttribute('data-player-id'),
				};
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

	addPlayer(playerButton) {
		const targetModal = playerButton.closest('[data-modal-id]');
		targetModal.setAttribute('data-fetching', '');
		const modalId = targetModal.getAttribute('data-modal-id');
		if (targetModal) {
			this.authenticateUser(modalId);
		}
	}

	async deletePlayer(playerButton) {
		const targetModal = playerButton.closest('[data-modal-id]');
		const playerId = targetModal.getAttribute('data-player-id');
		try {
			const context = {tournamentId: this.tournamentId, playerId};
			await this.service.deleteTournamentPlayer(context);
		} catch (error) {
			this.notify(error.message);
		}
		targetModal.removeAttribute('data-player-id');
		this.resetCard(targetModal);
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
		this.dialog.addEventListener('click', (e) => {
			e.preventDefault();
			if (e.target.closest('decline-btn') || e.target.closest('x-btn')) {
				this.dialog.remove();
			}
			const playerButton = e.target.closest('.toggle-user');
			if (playerButton?.classList.contains('add')) {
				this.addPlayer(playerButton);
			}
			if (playerButton?.classList.contains('remove')) {
				this.deletePlayer(playerButton);
			}
		});
	}
}

//TODO: this is not going to be fun, but modals and players need their individual ids. as the array does not come with
// the POST tournament/ response. When an add-event is fired the modal id needs to be known to update the right card (the do have ids atm).
// and when the player data comes in that card needs to be found and the data-user-id updated.
