
const route = (event) => {
	event = event || window.event;
	if (event.preventDefault){
		event.preventDefault();
	};
	const destination = event.target && event.target.href ?  event.target.href : event;
	window.history.pushState({}, "", destination);
	handleLocation();
}

const routes = {
	404: `/frontend/pages/404.html`,
	"/": "./pages/landing.html",
	"/frontend/": "./pages/landing.html",
	"/login": "./frontend/pages/login.html",
	"/register": "./frontend/pages/registration.html",
	"/friends": "./frontend/pages/friends.html",
	"/menu": "./frontend/pages/menu.html",
}

const handleLocation = async () => {
	const path = window.location.pathname;
	console.log(path);
	const route = routes[path] || routes[404];
	console.log(route);
	const html = await fetch(route).then(data => data.text());
	document.getElementById("content-container").innerHTML = html;
}