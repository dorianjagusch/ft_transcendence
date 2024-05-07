
import stateMachine from '../stateMachine.js';
import loginService from '../services/loginService.js';
import { InputField } from '../components/inputField.js';
import { Modal } from '../components/modal.js';

async function login(e) {
	e.preventDefault();
	const username = document.getElementById('username').value;
	const password = document.getElementById('current-password').value;
	if (username === '' || password === '') {
		alert('Please enter both username and password');
		return;
	}
	const toSend = {username, password};
	await loginService.postLogin(toSend)
		.then(() => {
			stateMachine.context.username =toSend.username;
			stateMachine.transition("goToFriends");
		})
		.catch((error) => {
			console.error(
				"There has been a problem with your fetch operation:",
				error
			);
		});;
}

function createForm(){

	const form = document.createElement('form');

	const userNameField = InputField('text', 'Username', 'username');
	const passwordField = InputField('password', 'Password', 'current-password');

	const loginButton = document.createElement('button');
	loginButton.classList.add('primary-sign-btn');
	loginButton.textContent = 'Sign in';
	loginButton.addEventListener('click', login);

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(loginButton);

	return form;
}

function showLoginPage() {
	const main = document.querySelector("main");
		main.innerHTML = "";

	const modalContainer = Modal('login', 'bg-secondary');
	const loginModal = modalContainer.querySelector('.login');
	const form = createForm();

	const signUpButton = document.createElement('button');
	signUpButton.classList.add('secondary-sign-btn');
	signUpButton.textContent = 'Sign up';
	signUpButton.addEventListener('click', () => {
		stateMachine.transition('goToRegister');
	});

	loginModal.appendChild(form);
	modalContainer.appendChild(signUpButton);


	main.appendChild(modalContainer);
}


export default showLoginPage;