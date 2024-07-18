import Aview from './AView.js';
import {PlayerInfo} from '../components/playerInfo.js';
import {OpponentSelection} from '../components/opponentSelection.js';
import AcceptDeclineModal from '../components/dialogs/acceptDeclineModal.js';
import AuthenticationModal from '../components/dialogs/authenticationModal.js';

export default class extends Aview {
	constructor() {
		super();
		this.setTitle('Modal');
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
		console.log(guestUserData);
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
		const playerInfo = {
			username: 'Player 1',
			img: './static/assets/img/default-user.png',
			wins: 20,
			losses: 0,
		};

		const playerLeft = PlayerInfo(playerInfo);
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
