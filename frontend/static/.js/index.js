const base_url="127.0.0.1:8080"

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


const confirmPassword = function() {
	const userPassword = document.getElementById("pwd");
	const confirmPassword = document.getElementById("repeat-pwd");
	if (userPassword.value !== confirmPassword.value){
		confirmPassword.setCustomValidity("Passwords Don't Match");
	} else {
		confirmPassword.setCustomValidity("Passwords Don't Match");
	}
}


const registerUser = async () => {
	const formData = new FormData(document.getElementById("registration-form"));
	console.log(formData);
	const request = await fetch(url = `${base_url}/users/`,
								{
									method: "post",
									data: data,
								});
	return request.then(response => response.data);
}


window.onpopstate = handleLocation
window.route = route;

handleLocation()