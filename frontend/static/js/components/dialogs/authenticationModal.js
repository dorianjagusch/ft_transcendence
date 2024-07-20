import ADialog from './ADialog.js';
import loginForm from '../formComponents/loginForm.js';
import AuthenticationService from '../../services/AuthenticationService.js';

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
			const tokenData = await this.service.postMatch(userData);
			this.dialog.close();
			if (this.onDataReceived) {
				this.onDataReceived(tokenData);
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
					if (!username || !password) {
						this.notify('Provide a username and password.');
						return;
					}
					try {
						this.authenticateUser({username, password});
					} catch (error) {
						this.notify(error.message);
					}
				} else if (e.target.classList.contains('decline-btn')) {
					this.dialog.close();
				}
			},
			false
		);
	}
}
