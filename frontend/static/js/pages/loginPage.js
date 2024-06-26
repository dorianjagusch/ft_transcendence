import LoginService from '../services/loginService.js';
import LoginForm from '../components/formComponents/loginForm.js';
import ProfileForm from '../components/formComponents/completeProfileForm.js';
import Modal from '../components/modal.js';
import AView from './AView.js';
import SideBar from '../components/sideBar.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Login');
	}

	loginHandler = async (e) => {
		e.preventDefault();
		const username = document.getElementById('username').value;
		const password = document.getElementById('current-password').value;
		if (username === '' || password === '') {
			this.notify('Please enter both username and password', 'error');
			return;
		}
		const loginService = new LoginService();
		try {
			await loginService.postRequest({username, password});
			localStorage.setItem('username', username);
			localStorage.setItem('isLoggedIn', true);
			this.navigateTo('/dashboard');
		} catch (error) {
			if (!error.status){
				console.error('Could not connect to server:', error);
			} else if (error.status === 401) {
				this.notify("Username or password is incorrect. Try again.", 'error');
			} else {
				this.notify(error);
			}
		}
	};

	appendEventListeners() {
		const loginButton = document.querySelector('.primary-btn');
		loginButton.addEventListener('click', this.loginHandler);

		const signUpButton = document.querySelector('.secondary-btn');
		signUpButton.addEventListener('click', () => {
			this.navigateTo('/register');
		});
	}

	async getHTML() {
		const modalContainer = Modal('login', 'bg-secondary', LoginForm);
		const loginModal = modalContainer.querySelector('.login');

		const signUpButton = document.createElement('button');
		signUpButton.classList.add('secondary-btn');
		signUpButton.textContent = 'Sign up';

		modalContainer.appendChild(signUpButton);

		const ProfileModal = Modal('profile', 'bg-secondary', ProfileForm);
		ProfileModal.classList.add('overlay');
		ProfileModal.setAttribute('data-visible', 'false');

		this.updateMain(modalContainer, ProfileModal);
		this.appendEventListeners();
	}
}
