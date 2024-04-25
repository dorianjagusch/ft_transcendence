
import loginService from '../services/loginService.js';
import {InputField} from '../components/inputField.js';


async function login() {
	const username = document.getElementById('username').value;
	const password = document.getElementById('current-password').value;
	if (username === '' || password === '') {
		alert('Please enter both username and password');
		return;
	}
	await loginService.postLogin(username, password)
	.then(data => {
		if (data.success) {
			window.location.href = '/dashboard';
		} else {
			alert('Invalid username or password');
		}
	})
	.catch(error => console.error('Error:', error));
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
	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container');

	const loginModal = document.createElement('div');
	loginModal.classList.add('login', 'bg-secondary');

	const header = document.createElement('h2');
	header.classList.add('modal-title');
	header.textContent = 'Login';

	const form = createForm();

	const signUpButton = document.createElement('button');
	signUpButton.classList.add('secondary-sign-btn');
	signUpButton.textContent = 'Sign up';

	loginModal.appendChild(header);
	loginModal.appendChild(form);

	modalContainer.appendChild(loginModal);
	modalContainer.appendChild(signUpButton);

	const main = document.querySelector('main');
	main.innerHTML = '';
	main.appendChild(modalContainer);
}


export default showLoginPage;