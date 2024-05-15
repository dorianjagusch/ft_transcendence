import { router, navigateTo } from './router.js';
import logoutService from './services/logoutService.js';


sessionStorage.setItem('isLoggedIn', false);

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', (e) => {
		if (e.target.matches('[data-link]')) {
			e.preventDefault();
			if (e.target.href.includes('logout')) {
				logoutService.postLogout()
					.then(() => {
						sessionStorage.setItem('isLoggedIn', false);
						sessionStorage.removeItem('username');
						navigateTo('/login');
					})
					.catch((error) => {
						console.error('There has been a problem with your fetch operation:', error);
					})
			} else {
				navigateTo(e.target.href);
			}
		}
	});

	router();
});
