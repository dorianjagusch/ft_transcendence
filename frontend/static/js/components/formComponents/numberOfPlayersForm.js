import AForm from './AForm.js';
import inputField from './inputField.js';
import RadioSection from './RadioSection.js';

export default class extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const header = document.createElement('h2');
		header.textContent = 'Pong Tournament';
		const tournamentName = inputField('text', 'Battle Name', 'tournament-name');
		tournamentName.setAttribute('placeholder', 'optional')
		const question = document.createElement('p');
		question.innerText='How many players?';

		const radioSection = RadioSection('number-of-players', ["4", "8"])

		const continueButton = document.createElement('button');
		continueButton.classList.add('tournament-btn', "primary-btn");
		continueButton.setAttribute('type', 'submit');
		continueButton.setAttribute('formmethod', 'dialog');
		continueButton.textContent = 'Continue';

		this.appendToForm(header, tournamentName, question, radioSection, continueButton);
		return this.getForm();
	}
}
