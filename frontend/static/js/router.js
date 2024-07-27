import routes from './route.js';
import constants from './constants.js';
import UserService from './services/userService.js';

const pathToRegex = (path) =>  {
	return new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');
};

const getParams = (match) => {
	const values = match.result.slice(1);
	const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map((result) => result[1]);

	return Object.fromEntries(
		keys.map((key, i) => {
			return [key, values[i]];
		})
	);
};

const navigateTo = (url) => {
	history.pushState(null, null, url);
	router();
};

const router = async () => {
	const potentialMatches = routes.map((route) => {
		return {
			route: route,
			result: location.pathname.match(pathToRegex(route.path)),
		};
	});

	let match = potentialMatches.find((potentialMatch) => potentialMatch.result !== null);
	if (!match) {
		match = {
			route: routes[0],
			result: [location.pathname],
		};
	}

	const isLoggedOut = localStorage.getItem('isLoggedIn') !== 'true';

	if (isLoggedOut && !constants.allowedPaths.includes(match.route.path)) {
		navigateTo('/login');
		return;
	} else if (
		!isLoggedOut &&
		constants.allowedPaths.includes(match.route.path) &&
		match.route.path !== '/pong'
	) {
		const userService = new UserService();
		const user_id = localStorage.getItem('user_id');
		if (user_id === null || user_id === '')
		{
			navigateTo('/login');
			return;
		}

		await userService.getRequest(user_id);
		navigateTo('/dashboard');
		return;
	}
	const view = new match.route.view(getParams(match));
	document.querySelector('main').removeAttribute('class');
	view.getHTML();
};

export {navigateTo, router};
