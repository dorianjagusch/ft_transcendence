import AView from './AView.js';
import LogoutService from '../services/logoutService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Logout');
	}

	async getHTML() {
		const logoutService = new LogoutService();
		try {
			 await logoutService.postRequest();
			localStorage.clear();
			localStorage.setItem('isLoggedIn', false);
			sessionStorage.setItem('isLoggedInSession', false);
			document.cookie.split(';').forEach((c) => {
				document.cookie = c
					.replace(/^ +/, '')
					.replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
			});
			this.notify("You are now logged out.", 'success')
		} catch (error) {
			if (!error.status) {
				this.notify(error);
			} else if ((error.status = 401)) {
				this.notify('Session expired, please login.', 'error');
			} else {
				this.notify(error);
			}
		}
		this.navigateTo('/login');
	}
}
