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

		const linkElement = document.createElement('a');
		linkElement.setAttribute('href', '../../../privacypolicy.html');
		linkElement.setAttribute('target', '_blank');
		linkElement.setAttribute('rel', 'noopener noreferrer');
		linkElement.innerHTML = '<span>By clicking here, you agree to our Privacy Policy.</span>';
		
		this.appendToForm(
			userNameField,
			passwordField,
			repeatPasswordField,
			linkElement,
			registerButton
		);

		return this.getForm();
	}
}
