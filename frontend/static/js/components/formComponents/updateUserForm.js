import AForm from './AForm.js';
import InputField from './inputField.js';

export default class extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const userNameField = InputField('text', 'Input new username', 'username');
		const passwordField = InputField('password', 'Input new password', 'current-password');
		const repeatPasswordField = InputField('password', 'Repeat new password', 'password');
		const updateUserButton = document.createElement('button');
		updateUserButton.classList.add('primary-btn');
		updateUserButton.textContent = 'Save information';

		this.appendToForm(
			userNameField,
			passwordField,
			repeatPasswordField,
			updateUserButton
		);

		return this.getForm();
	}
}
