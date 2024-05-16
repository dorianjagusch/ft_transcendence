import { router, navigateTo } from './router.js';
import logoutService from './services/logoutService.js';


sessionStorage.setItem('isLoggedIn', false);

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', (e) => {
		if (e.target.matches('[data-link]')) {
			e.preventDefault();
			navigateTo(e.target.href);
		}
	});

	router();
});
