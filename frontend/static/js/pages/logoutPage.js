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
			const logoutResponse = await logoutService.postRequest();
			localStorage.setItem('isLoggedIn', false);
			localStorage.setItem('username', '');
			document.cookie.split(';').forEach((c) => {
				document.cookie = c
					.replace(/^ +/, '')
					.replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
			});
			this.notify("You are not logged out.", 'success')
		} catch (error) {
			if (!error.status) {
				this.nofity(error);
			} else if ((error.status = 401)) {
				this.notify('Session expired, please login.', 'error');
			} else {
				this.notify(error);
			}
		}
		this.navigateTo('/login');
	}
}
