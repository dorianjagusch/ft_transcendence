import routes from './route.js';

const pathToRegex = (path) =>
	new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

const getParams = (match) => {
	const values = match.result.slice(1);
	const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(
		(result) => result[1]
	);

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

	let match = potentialMatches.find(
		(potentialMatch) => potentialMatch.result !== null
	);
	console.log(match);
	if (!match) {
		match = {
			route: routes[0],
			result: [location.pathname],
		};
	}
	const view = new match.route.view(getParams(match));
	document.querySelector('main').removeAttribute('class');
	await view.getHTML();
};

export { navigateTo, router };
