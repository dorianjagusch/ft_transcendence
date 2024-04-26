
import loginService from '../services/loginService.js';
import { InputField } from '../components/inputField.js';
import { Modal } from '../components/modal.js';


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
		};
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
	// loginButton.addEventListener('click', login); TODO: Uncomment this line when backend is ready

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(loginButton);

	return form;
}

function showLoginPage() {
	const main = document.querySelector("main");
    main.innerHTML = "";

	const modalContainer = Modal('login', 'bg-secondary');
	console.log(modalContainer.innerHTML);
	const loginModal = modalContainer.querySelector('.login');
	const form = createForm();
	console.log(loginModal);

	const signUpButton = document.createElement('button');
	signUpButton.classList.add('secondary-sign-btn');
	signUpButton.textContent = 'Sign up';
	signUpButton.addEventListener('click', () => {
		showRegisterPage();
	});

	loginModal.appendChild(form);
	modalContainer.appendChild(signUpButton);


	main.appendChild(modalContainer);
}


export default showLoginPage;