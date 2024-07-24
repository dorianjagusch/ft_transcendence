import AForm from './AForm.js';
import {PlayerCard} from './PlayerCard.js';

export default class summaryForm extends AForm {
	constructor(tournamentData) {
		super();
		this.tournamentData = tournamentData;
	}

	createFormButton(type, text) {
		const Button = document.createElement('button');
		Button.classList.add(type);
		Button.textContent = text;
		Button.setAttribute('type', 'submit');
		Button.setAttribute('formmethod', 'dialog');
		return Button;
	}

	generateForm() {
		this.form.classList.add('selected-players');

		const playerList = document.createElement('section');
		playerList.classList.add('player-list', `player-${this.tournamentData.players.length}`);

		this.tournamentData.players.forEach((player) => {
			const playerCard = PlayerCard(...Object.values(player), false);
			playerList.appendChild(playerCard);
		});

		const buttonBar = document.createElement('div');
		buttonBar.classList.add('button-bar', 'flex-row');

		const backButton = this.createFormButton('decline-btn', 'Start from Scratch');
		const continueButton = this.createFormButton('accept-btn', 'Start Tournament');
		buttonBar.appendChild(backButton);
		buttonBar.appendChild(continueButton);

		this.appendToForm(playerList, buttonBar);
		return this.form;
	}
}
