import AView from './AView.js';
import LogoutService from '../services/logoutService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Logout');
	}

	getHTML() {
		const logoutService = new LogoutService();
		logoutService.postRequest()
			.then((logoutResponse) => {
				localStorage.setItem('isLoggedIn', false);
				localStorage.setItem('username', '');
				document.querySelector('aside').remove();
				document.cookie.split(';').forEach((c) => {
					document.cookie = c
						.replace(/^ +/, '')
						.replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/');
				});
				return this.navigateTo('/login');
			})
			.catch((error) => {
				this.navigateTo('/dashboard');
			});
	}
}
