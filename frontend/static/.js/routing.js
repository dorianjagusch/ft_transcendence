
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
	404: `/pages/404.html`,
	"/": "./pages/landing.html",
	"/frontend/": "./pages/landing.html",
	"/login": "./pages/login.html",
	"/register": "./pages/registration.html",
	"/friends": "./pages/friends.html",
	"/menu": "./pages/menu.html",
}

const handleLocation = async () => {
	const path = window.location.pathname;
	console.log(path);
	const route = routes[path] || routes["/"];
	console.log(route);
	const html = await fetch(route).then(data => data.text());
	document.getElementById("content-container").innerHTML = html;
}