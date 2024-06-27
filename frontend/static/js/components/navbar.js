const setNavbar = (isLoggedOut) => {
	const navPartitions = document.querySelectorAll('.nav-partition');
	navPartitions.forEach((partition) => {
		const isVisible = partition.classList.contains('logged-out') ? isLoggedOut : !isLoggedOut;
		partition.setAttribute('data-visible', isVisible);
	});
	document.querySelector('#user').innerHTML = localStorage.getItem('username');
};

const toggleSideBar = (e) => {
	e.preventDefault();
	document.querySelector('aside').toggleAttribute('active');
};

const navbarItem = (link, type, content) => {
	const navbarItem = document.createElement('li');
	navbarItem.classList.add('nav-item');
	const navbarLink = document.createElement('a');
	navbarLink.href = link;
	navbarLink.setAttribute('data-link', '');

	if (type === 'image') {
		const img = document.createElement('img');
		img.src = content;
		navbarLink.appendChild(img);
	} else {
		navbarLink.textContent = content;
	}

	navbarItem.appendChild(navbarLink);
	return navbarItem;
};

const Navbar = (username) => {
	const nav = document.createElement('nav');
	const ul = document.createElement('ul');

	const loggedInSection = document.createElement('div');
	loggedInSection.classList.add('nav-partition', 'logged-in');
	loggedInSection.setAttribute('data-visible', 'true');

	const leaderboardItem = navbarItem('/leaderboard', 'text', 'Leaderboard');
	loggedInSection.appendChild(leaderboardItem);

	const playItem = navbarItem('/play', 'text', 'Play');
	loggedInSection.appendChild(playItem);

	const friendsItem = navbarItem('/friends', 'text', 'Friends');
	loggedInSection.appendChild(friendsItem);

	ul.appendChild(loggedInSection);

	const userSection = document.createElement('div');
	userSection.classList.add('nav-partition', 'logged-in');
	userSection.setAttribute('data-visible', 'true');

	const userImageItem = navbarItem('/dashboard', 'image', './static/assets/img/default-user.png');
	userSection.appendChild(userImageItem);

	const userLinkItem = navbarItem('/user', 'text', username);
	userLinkItem.id = 'user';
	userSection.appendChild(userLinkItem);

	const gearItem = navbarItem('', 'image', './static/assets/img/gear.png');
	gearItem.addEventListener('click', toggleSideBar);
	gearItem.querySelector('img').setAttribute('id', 'menu');
	userSection.appendChild(gearItem);

	ul.appendChild(userSection);

	const loggedOutSection = document.createElement('div');
	loggedOutSection.classList.add('nav-partition', 'logged-out');
	loggedOutSection.setAttribute('data-visible', 'false');

	const loginItem = navbarItem('/login', 'text', 'Login');
	loggedOutSection.appendChild(loginItem);

	const registerItem = navbarItem('/register', 'text', 'Register');
	loggedOutSection.appendChild(registerItem);

	ul.appendChild(loggedOutSection);

	nav.appendChild(ul);

	return nav;
};

export {Navbar, setNavbar};
