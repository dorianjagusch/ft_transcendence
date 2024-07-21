import {router, navigateTo} from './router.js';

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', (e) => {
		if (e.target.matches('[data-link]')) {
			e.preventDefault();
			navigateTo(e.target.href);
		}
		if (!e.target.matches('[active]') && !e.target.matches("img#menu")) {
			document.querySelector('aside')?.removeAttribute('active');
		}
	});
	router();
});
