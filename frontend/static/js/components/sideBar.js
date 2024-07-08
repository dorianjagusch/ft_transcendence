import {navigateTo} from '../router.js';
import {userNotification} from '../components/userNotification.js';
import fileInputField from '../components/formComponents/fileInputField.js'
import getProfilePicture from './profilePicture.js';
import ProfilePictureService from '../services/profilePictureService.js';

const notify = (message, type = 'success') => {
	userNotification(message, type);
	setTimeout(() => {
		document.querySelector('.notification').innerText = '';
	}, 3000);
}

const sideBarButton = (classes, text, callback) => {
	const sideBarButton = document.createElement('button');
	sideBarButton.classList.add(...classes);
	sideBarButton.textContent = text;
	sideBarButton.addEventListener('click', callback);
	return sideBarButton;
};

const profilePictureHandler = async (file) => {
	if (!file) {
		alert('Profile picture was not given.');
		return;
	}

	const formData = new FormData();
	formData.append('file', file);
	const userIdStr = localStorage.getItem('user_id');
	if (!userIdStr) {
		throw new Error("User ID is not found in local storage");
	}

	const userId = parseInt(userIdStr, 10);
	if (isNaN(userId)) {
		throw new Error("User ID is not a valid number");
	}

	try
	{
		const profilePictureService = new ProfilePictureService();
		profilePictureService.postProfilePictureRequest(userId, formData);
	} catch (error) {
		notify(error, 'error');
	}

	navigateTo('/dashboard');
};

const SideBar = () => {
	const aside = document.createElement('aside');

	try {
		const img = getProfilePicture();
		aside.appendChild(img);
	} catch (error) {
		console.error('Error creating profile picture element:', error);
	}

	const fileInput = fileInputField(profilePictureHandler);
	aside.appendChild(fileInput);

	const logoutBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Logout', () => navigateTo('/logout'));
	const editProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Edit profile');
	const viewProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'View profile', () => navigateTo('/dashboard'));
	const profilePictureBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Update profile picture', () => fileInput.click());
	const createTournamentBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Create Tournament', () => navigateTo('/tournament'));
	const deleteAccountBtn = sideBarButton(['sidebar-element', 'error'], 'Delete account');

	aside.appendChild(logoutBtn);
	aside.appendChild(editProfileBtn);
	aside.appendChild(viewProfileBtn);
	aside.appendChild(profilePictureBtn);
	aside.appendChild(createTournamentBtn);
	aside.appendChild(deleteAccountBtn);

	return aside;
};

export default SideBar;
