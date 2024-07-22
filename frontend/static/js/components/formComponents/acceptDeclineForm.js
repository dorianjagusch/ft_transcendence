import AForm from './AForm.js';

export default class AcceptForm extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const header = document.createElement('h3');
		header.textContent = 'So you think you can pong?';

		const buttonBar = document.createElement('div');
		buttonBar.classList.add('button-bar');

		const acceptButton = document.createElement('button');
		acceptButton.classList.add('accept-btn');
		acceptButton.textContent = 'Accept';

		const declineButton = document.createElement('button');
		declineButton.classList.add('decline-btn');
		declineButton.setAttribute('type', 'submit');
		declineButton.setAttribute('formmethod', 'dialog');
		declineButton.textContent = 'Decline';

		buttonBar.appendChild(acceptButton);
		buttonBar.appendChild(declineButton);

		this.appendToForm(header, buttonBar);
		return this.getForm();
	}
}
