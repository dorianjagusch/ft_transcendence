
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

const friendButtons = document.querySelectorAll(".user-card")

friendButtons.forEach(userCard => {
    userCard.addEventListener("click", () => {
        // Accessing all subelements of the user-card
        const userCardText = userCard.querySelector(".user-card-text");
        const userName = userCardText.querySelector(".user-name").textContent;
        const status = userCardText.querySelector(".status").getAttribute("data-status");

        console.log("User Name:", userName);
        console.log("Status:", status);
    });
});


window.onpopstate = handleLocation
window.route = route;

handleLocation()