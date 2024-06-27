// import menuEventlisters from './settingsMenu.js';
import {navigateTo} from '../router.js';

const sideBarButton = (classes, text, callback) => {
	const sideBarButton = document.createElement('button');
	sideBarButton.classList.add(...classes);
	sideBarButton.textContent = text;
	sideBarButton.addEventListener('click', callback);
	return sideBarButton;
};

const SideBar = () => {
	const aside = document.createElement('aside');

	const img = document.createElement('img');
	img.setAttribute('src', 'static/assets/img/default-user.png');
	img.setAttribute('alt', '');
	aside.appendChild(img);

	const editProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Edit profile');
	const viewProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'View profile', () => navigateTo('/dashboard'));
	const createTournamentBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Create Tournament', () => navigateTo('/tournament'));
	const logoutBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Logout', () => navigateTo('/logout'));
	const deleteAccountBtn = sideBarButton(['sidebar-element', 'error'], 'Delete account');

	aside.appendChild(editProfileBtn);
	aside.appendChild(viewProfileBtn);
	aside.appendChild(createTournamentBtn);
	aside.appendChild(logoutBtn);
	aside.appendChild(deleteAccountBtn);

	return aside;
};

export default SideBar;
