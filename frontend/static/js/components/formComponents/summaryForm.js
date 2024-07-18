import AForm from "./AForm.js";7
import PlayerCard from "./PlayerCard.js";

export default class summaryForm extends AForm {
	constructor(tournamentData) {
		super();
		this.tournamentData = tournamentData;
	}

	generateForm() {
		const form = document.createElement('form');
		form.classList.add('selected-players');

		const playerList = document.createElement('section');
		playerList.classList.add('player-list', `player-${this.tournamentData.players.length}`);
		form.appendChild(playerList);

		this.tournamentData.players.forEach(player => {
			const playerCard = PlayerCard(
				...Object.values(player),
				false
			);
			playerList.appendChild(playerCard);
		});

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
		continueButton.textContent = 'Start Tournament';
		continueButton.setAttribute('type', 'submit');
		continueButton.setAttribute('formmethod', 'dialog');
		buttonBar.appendChild(continueButton);
		return form;
	}
}