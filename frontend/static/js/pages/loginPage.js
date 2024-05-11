import loginService from '../services/loginService.js';
import LoginForm from '../components/formComponents/loginForm.js';
import ProfileForm from '../components/formComponents/completeProfileForm.js';
import Modal from '../components/modal.js';
import AView from './AView.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Login');
	}

	setNavbar() {
		const navPartitions = document.querySelectorAll('.nav-partition');
		navPartitions.forEach((partition) => {
			const visibility = partition.getAttribute('data-visible');
			partition.setAttribute('data-visible', visibility === 'true' ? 'false' : 'true');

			document.querySelector('#user').innerHTML = document.getElementById('username').value;
		});
	}

	loginHandler = async (e) => {
		e.preventDefault();
		const username = document.getElementById('username').value;
		const password = document.getElementById('current-password').value;
		if (username === '' || password === '') {
			this.notify('Please enter both username and password', 'error');
			return;
		}
		const toSend = {username, password};
		await loginService
			.postLogin(toSend)
			.then(() => {
				this.setNavbar();
				this.navigateTo('/friends');
			})
			.catch((error) => {
				console.error('There has been a problem with your fetch operation:', error);
			});
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
