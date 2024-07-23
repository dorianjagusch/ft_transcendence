import ADialog from './ADialog.js';
import loginForm from '../formComponents/loginForm.js';
import AuthenticationService from '../../services/authenticationService.js';

export default class AuthenticationModal extends ADialog {
	constructor(parentCallback) {
		super(new loginForm(), new AuthenticationService());
		this.getFormData = this.getFormData.bind(this);
		this.authenticateUser = this.authenticateUser.bind(this);
		this.onDataReceived = parentCallback;
		this.tournamentId;
		this.appendEventlistenters();
	}

	getFormData() {
		const form = this.form.getForm();
		const username = form.querySelector('#username').value;
		const password = form.querySelector('#current-password').value;
		return {username, password};
	}

	async authenticateUser(userData) {
		try {
			const tokenData = await this.service.postMatch(userData, false);
			this.dialog.close();
			if (this.onDataReceived) {
				this.onDataReceived(tokenData);
			}
		} catch (error) {
			this.notify(error.message, 'error');
		}
	}

	appendEventlistenters() {
		this.dialog.addEventListener(
			'click',
			(e) => {
				if (e.target.classList.contains('primary-btn')) {
					e.preventDefault();
					const {username, password} = this.getFormData();
					if (!username || !password) {
						this.notify('Provide a username and password.'), 'error';
						return;
					}
					try {
						this.authenticateUser({username, password});
					} catch (error) {
						this.notify(error.message, 'error');
					}
				} else if (e.target.classList.contains('decline-btn')) {
					this.dialog.close();
				}
			},
			false
		);
	}
}
