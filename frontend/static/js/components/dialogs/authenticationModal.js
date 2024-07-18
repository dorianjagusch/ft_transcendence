import ADialog from './ADialog.js';
import loginForm from '../formComponents/loginForm.js';
import AuthenticationService from '../../services/AuthenticationService.js';
import {navigateTo} from '../../router.js';
import {inputNotification} from '../userNotification.js';

export default class AuthenticationModal extends ADialog {
	constructor(parentCallback) {
		super(new loginForm(), new AuthenticationService());
		this.notify = this.notify.bind(this);
		this.getFormData = this.getFormData.bind(this);
		this.authenticateUser = this.authenticateUser.bind(this);
		this.getFormData = this.getFormData.bind(this);
		this.onDataReceived = parentCallback;
		this.appendEventlistenters();
	}

	getFormData() {
		const form = this.form.getForm();
		const username = form.querySelector('#username').value;
		const password = form.querySelector('#current-password').value;
		return {username, password};
	}

	notify(message) {
		const notification = inputNotification(message);
		this.form.form.querySelector('h3').after(notification);
		setTimeout(() => {
			notification.remove();
		}, 3000);
	}

	async authenticateUser(guestUser) {
		try {
			const guestData = {
				username: 'Player 2',
				img: './static/assets/img/default-user.png',
				wins: 20,
				losses: 0,
			};
			// const guestData = await this.service.postRequest(guestUser);
			this.dialog.close();
			if (this.onDataReceived) {
				this.onDataReceived(guestData);
			}
		} catch (error) {
			this.notify(error.message);
		}
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			(e) => {
				if (e.target.classList.contains('primary-btn')) {
					e.preventDefault();
					const {username, password} = this.getFormData();
					console.log(username, password);
					if (!username || !password) {
						this.notify('Provide a username and password.');
						return;
					}
					try {
						this.authenticateUser({username, password});
					} catch (error) {
						console.error(error);
					}
				} else if (e.target.classList.contains('decline-btn')) {
					this.dialog.close();
				}
			},
			false
		);
	}
}
