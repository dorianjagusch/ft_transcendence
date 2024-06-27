import Modal from '../components/modal.js';
import AView from './AView.js';
import RegisterForm from '../components/formComponents/registerForm.js';
import UserService from '../services/userService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Register');
		this.linkClicked = false;
		this.registerHandler = this.registerHandler.bind(this);
	}

	registerHandler = async (e) => {
		e.preventDefault();
		const username = document.getElementById('username').value;
		const password = document.getElementById('current-password').value;
		const repeatPassword = document.getElementById('password').value;

		if (username === '' || password === '' || repeatPassword === '') {
			this.notify('Please enter all fields', 'error');
			return;
		}

		if (password !== repeatPassword) {
			this.notify('Passwords do not match', 'error');
			return;
		}

		if (this.linkClicked == false) {
			this.notify(
				'Please click the link to agree to the Privacy Policy before registering.',
				'error'
			);
			return;
		}
		const data = {
			username: username,
			password: password,
		};

		const userService = new UserService();
		try {
			userService.postRequest(data);
			this.notify('User created successfully. Please login.');
			this.navigateTo('/login');
		} catch (error) {
			this.notify(error);
		}
	};

	appendEventListeners() {
		const registerButton = document.querySelector('.primary-btn');
		registerButton.addEventListener('click', this.registerHandler);
		const loginButton = document.querySelector('.secondary-btn');
		loginButton.addEventListener('click', () => {
			this.navigateTo('/login');
		});
		const linkElement = document.getElementById('privacyPolicy');
		linkElement.addEventListener('click', () => {
			this.linkClicked = true;
		});
	}

	async getHTML() {
		const modalContainer = Modal('register', 'bg-secondary', RegisterForm);

		const loginButton = document.createElement('button');
		loginButton.classList.add('secondary-btn');
		loginButton.textContent = 'Sign in';
		modalContainer.appendChild(loginButton);

		this.updateMain(modalContainer);
		this.appendEventListeners();
	}
}
