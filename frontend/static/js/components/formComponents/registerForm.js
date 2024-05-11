import AForm from './AForm.js';
import InputField from './inputField.js';

export default class extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const userNameField = InputField('text', 'Username', 'username');
		const passwordField = InputField('password', 'Password', 'current-password');
		const repeatPasswordField = InputField('password', 'Repeat Password', 'password');
		const registerButton = document.createElement('button');
		registerButton.classList.add('primary-btn');
		registerButton.textContent = 'Sign up';
		this.appendToForm(
			userNameField,
			passwordField,
			repeatPasswordField,
			registerButton
		);
		return this.getForm();
	}
}
