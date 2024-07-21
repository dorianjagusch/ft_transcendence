import getProfilePicture from '../profilePicture.js';
import AForm from './AForm.js';
import PlayerCard from './PlayerCard.js';

export default class selectPlayersForm extends AForm {
	constructor({tournament, tournament_player}) {
		super();
		this.numberOfPlayers = tournament.player_amount;
		this.tournamentName = tournament.name;
		this.tournamenHostId = tournament_player.id;
		this.playerIds = [];
		this.generateForm = this.generateForm.bind(this);
	}

	generateForm() {
		const form = document.createElement('form');
		form.classList.add('player-selection');

		const playerList = document.createElement('section');
		playerList.classList.add('player-list', `player-${this.numberOfPlayers}`);
		form.appendChild(playerList);
		debugger;
		for (let i = 0; i < this.numberOfPlayers; i++) {
			if (i == 0) {
				const playerCard = PlayerCard(
					localStorage.getItem('username'),
					getProfilePicture(localStorage.getItem('user_id')),
					this.tournamentHostId,
					true
				);
				playerCard.setAttribute('data-user-selected', 'true')
				playerList.appendChild(playerCard);
				continue;
			}
			const playerCard = PlayerCard(
				'Add Participant',
				'../static/assets/img/default-user.png',
				i,
				true
			);
			playerCard.classList.add('bg-inactive');
			playerList.appendChild(playerCard);
		}

		const buttonBar = document.createElement('div');
		buttonBar.classList.add('button-bar', 'flex-row');
		form.appendChild(buttonBar);

		const backButton = document.createElement('button');
		backButton.classList.add('decline-btn');
		backButton.textContent = 'Back';
		backButton.setAttribute('type', 'submit');
		backButton.setAttribute('formmethod', 'dialog');
		buttonBar.appendChild(backButton);

		const continueButton = document.createElement('button');
		continueButton.classList.add('accept-btn');
		continueButton.textContent = 'Continue';
		continueButton.setAttribute('type', 'submit');
		continueButton.setAttribute('formmethod', 'dialog');
		buttonBar.appendChild(continueButton);

		return form;
	}
}
