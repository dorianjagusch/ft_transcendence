import { Modal } from '../components/modal.js';
import { InputField } from '../components/inputField.js';
// import userService from '../services/UserService.js';
import stateMachine from '../stateMachine.js';

const register = async (e) => {
	e.preventDefault();
	const username = document.getElementById('username').value;
	const password = document.getElementById('current-password').value;
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

	// const USER = userService.postUser(data).
	// catch((error) => {
	// 	console.error(error);
	// });
	// console.log(USER); TODO: Test this on Thursday with the containers running
}

const createForm = () => {
	const form = document.createElement('form');

	const userNameField = InputField('text', 'Username', 'username');
	const passwordField = InputField('password', 'Password', 'current-password');
	const repeatPasswordField = InputField('password', 'Repeat Password', 'password');

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
	const modalContainer = Modal('register', 'bg-secondary');
	const registerModal = modalContainer.querySelector('.register');
	const form = createForm();

	const loginButton = document.createElement('button');
	loginButton.classList.add('secondary-sign-btn');
	loginButton.textContent = 'Sign in';

	registerModal.appendChild(form);
	modalContainer.appendChild(loginButton);

	const main = document.querySelector('main');
	main.innerHTML = '';
	main.appendChild(modalContainer);

	loginButton.addEventListener('click', () => {
		stateMachine.transition('goToLogin');
	});
}

export default showRegisterPage;