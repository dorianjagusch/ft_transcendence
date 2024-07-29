import getProfilePicture from './profilePicture.js';

const toggleSideBar = (e) => {
	e.preventDefault();
	e.stopPropagation();
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

const createUserSection = async () => {
	const userSection = document.createElement('div');
	userSection.classList.add('nav-partition', 'logged-in', 'user-section');

	try {
		const userImage = await getProfilePicture(localStorage.getItem('user_id'));
		const userImageItem = navbarItem('/dashboard', 'image', userImage);
		userSection.appendChild(userImageItem);

		const userLinkItem = navbarItem('/dashboard', 'text', localStorage.getItem('username'));
		userLinkItem.id = 'user';
		userSection.appendChild(userLinkItem);

		const gearItem = navbarItem('', 'image', './static/assets/img/gear.png');
		gearItem.addEventListener('click', toggleSideBar);
		gearItem.querySelector('img').setAttribute('id', 'menu');
		userSection.appendChild(gearItem);

		return userSection;
	} catch (error) {
		return null;
	}
};

const createLoggedOutSection = () => {
	const loggedOutSection = document.createElement('div');
	loggedOutSection.classList.add('nav-partition', 'logged-out');

	const loginItem = navbarItem('/login', 'text', 'Login');
	loggedOutSection.appendChild(loginItem);

	const registerItem = navbarItem('/register', 'text', 'Register');
	loggedOutSection.appendChild(registerItem);
	localStorage.setItem('isLoggedIn', 'false');
	return loggedOutSection;
};

const updateNavbar = async () => {
	const ul = document.querySelector('nav ul');
	ul.innerHTML = '';
	if (localStorage.getItem('isLoggedIn') === 'true') {
		const loggedInSection = createdLoggedInSection();
		ul.appendChild(loggedInSection);

		const userSection = await createUserSection();
		if (userSection && !ul.querySelector('.user-section'))
			ul.appendChild(userSection);
	} else {
		const loggedOutSection = createLoggedOutSection();
		ul.appendChild(loggedOutSection);
	}
};

const Navbar = async () => {
	const nav = document.createElement('nav');
	const ul = document.createElement('ul');

	nav.appendChild(ul);

	document.querySelector('header').appendChild(nav);
};

export {Navbar, updateNavbar};
