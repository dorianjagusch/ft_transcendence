import {navigateTo} from '../router.js';
import {userNotification} from '../components/userNotification.js';
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
		alert('Profile picture is null');
		return;
	}

	const formData = new FormData();
	formData.append('file', file);

	try
	{
		const userIdStr = localStorage.getItem('user_id');
		if (!userIdStr) {
			throw new Error("User ID is not found in local storage");
		}

		const userId = parseInt(userIdStr, 10);
		if (isNaN(userId)) {
			throw new Error("User ID is not a valid number");
		}

		const profilePictureService = new ProfilePictureService();
		profilePictureService.postProfilePictureRequest(userId, file);

		notify('User profile picture added successfully. Please login.');
	}
	catch (error) {
		notify('Updating the profile picture failed', 'error');
	};
}

const SideBar = () => {
	const aside = document.createElement('aside');

	const img = document.createElement('img');
	let profile_pic = localStorage.getItem('user_profile_picture');
	if (!profile_pic) {
		img.setAttribute('src', 'static/assets/img/default-user.png');
	}
	else {
		img.setAttribute('src', profile_pic);
	}
	img.setAttribute('alt', '');
	aside.appendChild(img);

	const fileInput = document.createElement('input');
	fileInput.setAttribute('type', 'file');
	fileInput.setAttribute('id', 'profilePicture');
	aside.appendChild(fileInput);

	fileInput.addEventListener('change', (event) => {
		const file = event.target.files[0];
		profilePictureHandler(file);
	});

	const editProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Edit profile');
	const viewProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'View profile', () => navigateTo('/dashboard'));
	const profilePictureBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Update profilepicture', () => fileInput.click());
	const createTournamentBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Create Tournament', () => navigateTo('/tournament'));
	const logoutBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Logout', () => navigateTo('/logout'));
	const deleteAccountBtn = sideBarButton(['sidebar-element', 'error'], 'Delete account');

	aside.appendChild(editProfileBtn);
	aside.appendChild(viewProfileBtn);
	aside.appendChild(profilePictureBtn);
	aside.appendChild(createTournamentBtn);
	aside.appendChild(logoutBtn);
	aside.appendChild(deleteAccountBtn);

	return aside;
};

export default SideBar;
