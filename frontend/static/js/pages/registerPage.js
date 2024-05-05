import { modal } from '../components/modal.js';
import { inputField } from '../components/inputField.js';
import UserService from '../services/userService.js';
import stateMachine from '../stateMachine.js';

const register = async (e) => {
	e.preventDefault();
	const username = document.getElementById('username').value;
	const password = document.getElementById('current-password').value;
	console.log(username, password);
	const repeatPassword = document.getElementById('password').value;

	if (username === '' || password === '' || repeatPassword === '') {
		alert('Please enter all fields');
		return;
	}

	if (password !== repeatPassword) {
		alert('Passwords do not match');
		return;
	}

	const data = {
		username: username,
		password: password
	};

	var userService = new UserService();
	userService.postRequest(data)
	.then((newData) => {
		alert('User created successfully. Please login.');
		stateMachine.transition('goToLogin');
	})
	.catch((error) => {
		console.error(error);
	});
}


const createForm = () => {
	const form = document.createElement('form');

	const userNameField = inputField('text', 'Username', 'username');
	const passwordField = inputField('password', 'Password', 'current-password');
	const repeatPasswordField = inputField('password', 'Repeat Password', 'password');

	const registerButton = document.createElement('button');
	registerButton.classList.add('primary-sign-btn');
	registerButton.textContent = 'Sign up';
	registerButton.addEventListener('click', register);

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(repeatPasswordField);
	form.appendChild(registerButton);

	return form;

}


const showRegisterPage = () => {
	const modalContainer = modal('register', 'bg-secondary');
	const registermodal = modalContainer.querySelector('.register');
	const form = createForm();

	const loginButton = document.createElement('button');
	loginButton.classList.add('secondary-sign-btn');
	loginButton.textContent = 'Sign in';

	registermodal.appendChild(form);
	modalContainer.appendChild(loginButton);

	const main = document.querySelector('main');
	main.innerHTML = '';
	main.appendChild(modalContainer);

	loginButton.addEventListener('click', () => {
		stateMachine.transition('goToLogin');
	});
}

export default showRegisterPage;
