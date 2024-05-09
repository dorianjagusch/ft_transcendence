import { InputField } from '../components/inputField.js';
import { CountrySelector } from './countrySelector.js';
import { InputMediaField } from './inputMediaField.js';

const RegisterForm = () => {
	const form = document.createElement('form');

	const userNameField = InputField('text', 'Username', 'username');
	const passwordField = InputField(
		'password',
		'Password',
		'current-password'
	);
	const repeatPasswordField = InputField(
		'password',
		'Repeat Password',
		'password'
	);

	const textElement = document.createElement('p');
	textElement.innerHTML = 'Read our privacy policy <a href="https://example.com/privacy-policy" target="_blank" rel="noopener noreferrer">HERE</a>.'


	const registerButton = document.createElement('button');
	registerButton.classList.add('primary-btn');
	registerButton.textContent = 'Sign up';

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(repeatPasswordField);
	form.appendChild(textElement);
	form.appendChild(registerButton);

	return form;
};

const LoginForm = () => {
	const form = document.createElement('form');

	const userNameField = InputField('text', 'Username', 'username');
	const passwordField = InputField(
		'password',
		'Password',
		'current-password'
	);

	const loginButton = document.createElement('button');
	loginButton.classList.add('primary-btn');
	loginButton.textContent = 'Sign in';

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(loginButton);

	return form;
};

const ProfileForm = () => {
	const form = document.createElement('form');
	const avatarField = InputMediaField('image', 'Avatar', 'avatar');
	const countryField = CountrySelector();
	const aboutField = InputField('textfield', 'About you', 'about');

	form.appendChild(avatarField);
	form.appendChild(countryField);
	form.appendChild(aboutField);

	return form;
};

export { RegisterForm, LoginForm, ProfileForm };
