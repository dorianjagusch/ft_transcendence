import { router, navigateTo } from './router.js';

sessionStorage.setItem('isLoggedIn', true);

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', (e) => {
		if (e.target.matches('[data-link]')) {
			e.preventDefault();
			console.log(e.target.href);
			navigateTo(e.target.href);
		}
	});

	router();
});
