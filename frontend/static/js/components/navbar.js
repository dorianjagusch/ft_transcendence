import getProfilePicture from './profilePicture.js';

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

const getPictureNavbarItem = (href, userSection) => {
	try {
		const navbarItem = document.createElement('li');
		navbarItem.classList.add('nav-item');

		const img = getProfilePicture();
		navbarItem.appendChild(img);

		const navbarLink = document.createElement('a');
		navbarLink.href = href;
		navbarLink.setAttribute('data-link', '');
		navbarLink.appendChild(navbarItem);

		userSection.appendChild(navbarLink);
	} catch (error) {
		console.log('Error getting the profile picture element: ', error);
	}
};

const createdLoggedInSection = () => {
	const loggedInSection = document.createElement('div');
	loggedInSection.classList.add('nav-partition', 'logged-in');

	const leaderboardItem = navbarItem('/leaderboard', 'text', 'Leaderboard');
	loggedInSection.appendChild(leaderboardItem);

	const playItem = navbarItem('/play', 'text', 'Play');
	loggedInSection.appendChild(playItem);

	const friendsItem = navbarItem('/friends', 'text', 'Friends');
	loggedInSection.appendChild(friendsItem);
	return loggedInSection;
};

const createUserSection = () => {
	const userSection = document.createElement('div');
	userSection.classList.add('nav-partition', 'logged-in');

	getPictureNavbarItem('/dashboard', userSection);

	const userLinkItem = navbarItem('/user', 'text', localStorage.getItem('username'));
	userLinkItem.id = 'user';
	userSection.appendChild(userLinkItem);

	const gearItem = navbarItem('', 'image', './static/assets/img/gear.png');
	gearItem.addEventListener('click', toggleSideBar);
	gearItem.querySelector('img').setAttribute('id', 'menu');
	userSection.appendChild(gearItem);

	return userSection;
};

const createLoggedOutSection = () => {
	const loggedOutSection = document.createElement('div');
	loggedOutSection.classList.add('nav-partition', 'logged-out');

	const loginItem = navbarItem('/login', 'text', 'Login');
	loggedOutSection.appendChild(loginItem);

	const registerItem = navbarItem('/register', 'text', 'Register');
	loggedOutSection.appendChild(registerItem);
	return loggedOutSection;
};

const Navbar = () => {
	const nav = document.createElement('nav');
	const ul = document.createElement('ul');

	if (localStorage.getItem('isLoggedIn') === 'true') {
		const loggedInSection = createdLoggedInSection();
		ul.appendChild(loggedInSection);

		const notificationSection = document.createElement('p');
		notificationSection.classList.add('notification');
		ul.appendChild(notificationSection);

		const userSection = createUserSection();
		ul.appendChild(userSection);
	} else {
		const notificationSection = document.createElement('p');
		notificationSection.classList.add('notification');
		ul.appendChild(notificationSection);

		const loggedOutSection = createLoggedOutSection();
		ul.appendChild(loggedOutSection);
	}

	nav.appendChild(ul);

	return nav;
};

export {Navbar};
