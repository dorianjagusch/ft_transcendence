import {InputField} from './inputField.js';
import {CountrySelector} from './countrySelector.js';
import {InputMediaField} from './inputMediaField.js';
import NotImplementedError from '../../exceptions/notImplemented.js';

class AForm {
	constructor() {
		this.form = document.createElement('form');
	}

	appendToForm(...formElements) {
		formElements.forEach((element) => {
			this.form.appendChild(element);
		});
	}

	getForm() {
		return this.form;
	}

	generateForm() {
		throw new NotImplementedError('generateForm method must be implemented by child classes');
	}
}

class RegisterForm extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const userNameField = new InputField('text', 'Username', 'username');
		const passwordField = new InputField('password', 'Password', 'current-password');
		const repeatPasswordField = new InputField('password', 'Repeat Password', 'password');
		const registerButton = document.createElement('button');
		registerButton.classList.add('primary-btn');
		registerButton.textContent = 'Sign up';
		this.appendToForm(
			userNameField.getInputElement(),
			passwordField.getInputElement(),
			repeatPasswordField.getInputElement(),
			registerButton
		);
		return this.getForm();
	}
}

class LoginForm extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const userNameField = new InputField('text', 'Username', 'username');
		const passwordField = new InputField('password', 'Password', 'current-password');
		const loginButton = document.createElement('button');
		loginButton.classList.add('primary-btn');
		loginButton.textContent = 'Sign in';
		this.appendToForm(
			userNameField.getInputElement(),
			passwordField.getInputElement(),
			loginButton
		);
		return this.getForm();
	}
}

class ProfileForm extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const avatarField = new InputMediaField('image', 'Avatar', 'avatar');
		const countryField = new CountrySelector();
		const aboutField = new InputField('textfield', 'About you', 'about');
		this.appendToForm(
			avatarField.getInputElement(),
			countryField,
			aboutField.getInputElement()
		);
		return this.getForm();
	}
}
