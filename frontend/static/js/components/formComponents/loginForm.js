import AForm from './AForm.js';
import InputField from './inputField.js';

export default class extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const userNameField = InputField('text', 'Username', 'username');
		const passwordField = InputField('password', 'Password', 'current-password');
		const loginButton = document.createElement('button');
		loginButton.classList.add('primary-btn');
		loginButton.textContent = 'Sign in';
		this.appendToForm(
			userNameField,
			passwordField,
			loginButton
		);
		return this.getForm();
	}
}
