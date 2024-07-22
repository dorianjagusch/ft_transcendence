import getProfilePicture from '../profilePicture.js';
import AForm from './AForm.js';
import {PlayerCard} from './PlayerCard.js';

export default class selectPlayersForm extends AForm {
	constructor({tournament, tournament_player}) {
		super();
		this.numberOfPlayers = tournament.player_amount;
		this.tournamentName = tournament.name;
		this.tournamentHostId = tournament_player.id;
		this.playerIds = [];
		this.generateForm = this.generateForm.bind(this);
	}

	createFormButton(type, text) {
		const Button = document.createElement('button');
		Button.classList.add(type);
		Button.textContent = text;
		Button.setAttribute('type', 'submit');
		Button.setAttribute('formmethod', 'dialog');
		return Button;
	}

	createPlayerCards(playerContainer) {
		for (let i = 0; i < this.numberOfPlayers; i++) {
			if (i == 0) {
				const playerCard = PlayerCard(
					localStorage.getItem('username'),
					this.tournamentHostId,
					true
				);
				playerCard.setAttribute('data-user-selected', 'true');
				playerCard.setAttribute('data-player-id', this.tournamentHostId);
				playerContainer.appendChild(playerCard);
				getProfilePicture(localStorage.getItem('user_id'))
				.then((img) => {
					playerCard.querySelector(
						`[data-player-id="${this.tournamentHostId}"] > .player-img`
					).src = img;
				});
				continue;
			}
			const playerCard = PlayerCard(
				'Add Participant',
				'../static/assets/img/default-user.png',
				i,
				true
			);
			playerCard.classList.add('bg-inactive');
			playerContainer.appendChild(playerCard);
		}
	}

	generateForm() {
		this.form.classList.add('player-selection');

		const playerList = document.createElement('section');
		playerList.classList.add('player-list', `player-${this.numberOfPlayers}`);

		this.createPlayerCards(playerList);

		const buttonBar = document.createElement('div');
		buttonBar.classList.add('button-bar', 'flex-row');

		const backButton = this.createFormButton('decline-btn', 'Back');
		const continueButton = this.createFormButton('accept-btn', 'Continue');
		buttonBar.appendChild(backButton);
		buttonBar.appendChild(continueButton);

		this.appendToForm(playerList, buttonBar);
		return this.getForm();
	}
}
