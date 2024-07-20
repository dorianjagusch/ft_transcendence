import Aview from './AView.js';
import {PlayerInfo} from '../components/playerInfo.js';
import {OpponentSelection} from '../components/opponentSelection.js';
import UserService from '../services/userService.js'; // TODO: Switch out for stats service
import getProfilePicture from '../components/profilePicture.js';
import AcceptDeclineModal from '../components/dialogs/acceptDeclineModal.js';
import AuthenticationModal from '../components/dialogs/authenticationModal.js';

export default class extends Aview {
	constructor() {
		super();
		this.setTitle('Modal');
		this.userService = new UserService();
		this.attachEventListeners = this.attachEventListeners.bind(this);
		this.attachPlayerInfo = this.attachPlayerInfo.bind(this);
	}

	attachEventListeners() {
		const aiButton = document.querySelector('.opponent-selection > button');
		if (aiButton){
			aiButton.addEventListener('click', () => {
				const confirmModal = document.querySelector('.confirm-choice-modal');
				confirmModal.inert = true;
				confirmModal.showModal();
				confirmModal.inert = false;
			});
		}

		const localButton = document.querySelector('.opponent-selection > button:nth-child(3)');
		if (localButton){
			localButton.addEventListener('click', () => {
				const authenticationModal = document.querySelector('.authenticate-user-modal');
				authenticationModal.showModal();
			});
		}

		const startButton = document.querySelector('.start-btn');
		if (startButton){
			startButton.addEventListener('click', () => {
				this.navigateTo('/pong');
			});
		}
	}

	attachPlayerInfo(guestUserData) {
		const playerRight = PlayerInfo(guestUserData);

		const container = document.createElement('div');
		const vs = document.createElement('h2');
		vs.classList.add('vs');
		vs.textContent = 'vs';
		const startButton = document.createElement('button');
		startButton.classList.add('accept-btn', 'start-btn');
		startButton.textContent = 'Start Game';
		container.appendChild(vs);
		container.appendChild(startButton);

		const main = document.querySelector('main');
		main.appendChild(container);
		main.appendChild(playerRight);
		document.querySelector('.opponent-selection').remove();
		this.attachEventListeners();

	}

	adjustForm(authenticationForm) {
		const authenticationTitle = document.createElement('h3');
		authenticationTitle.textContent = 'Authenticate Opponent';
		const authenticationButton = authenticationForm.querySelector('button');
		authenticationButton.textContent = 'Authenticate';
		authenticationForm.prepend(authenticationTitle);
	}

	async getHTML() {

		let playerLeft = null;
		try {
			const userData = await this.userService.getRequest(localStorage.getItem('user_id'));
			userData.img = await getProfilePicture(userData.id);
			playerLeft = PlayerInfo(userData);
		}
		catch (error) {
			console.log(error);
		}

		const opponentSelection = OpponentSelection();

		const acceptDeclineModal = new AcceptDeclineModal();
		acceptDeclineModal.dialog.classList.add('confirm-choice-modal');

		const authenticationModal = new AuthenticationModal(this.attachPlayerInfo);
		authenticationModal.dialog.classList.add('authenticate-user-modal');
		this.adjustForm(authenticationModal.form.form);

		const main = document.querySelector('main');
		main.classList.add('flex-row');

		super.updateMain(
			playerLeft,
			opponentSelection,
			acceptDeclineModal.dialog,
			authenticationModal.dialog
		);

		this.attachEventListeners();
	}
}
