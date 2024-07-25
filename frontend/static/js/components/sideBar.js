import {navigateTo} from '../router.js';
import notify from '../utils/notify.js';
import fileInputField from '../components/formComponents/fileInputField.js';
import getProfilePicture from './profilePicture.js';
import AcceptDeclineModal from './dialogs/acceptDeclineModal.js';
import UpdateUserModal from './dialogs/updateUserModal.js';
import UserService from '../services/userService.js';
import ProfilePictureService from '../services/profilePictureService.js';

const sideBarButton = (classes, text, callback) => {
	const sideBarButton = document.createElement('button');
	sideBarButton.classList.add(...classes);
	sideBarButton.textContent = text;
	sideBarButton.addEventListener('click', callback);
	return sideBarButton;
};

const profilePictureHandler = async (file) => {
	if (!file) {
		notify('Profile picture was not given.', 'error');
		return;
	}

	const formData = new FormData();
	formData.append('file', file);
	const userIdStr = localStorage.getItem('user_id');
	if (!userIdStr) {
		throw new Error('User ID is not found in local storage');
	}

	const userId = parseInt(userIdStr, 10);
	if (isNaN(userId)) {
		throw new Error('User ID is not a valid number');
	}

	try {
		const profilePictureService = new ProfilePictureService();
		await profilePictureService.postRequest(userId, formData);
	} catch (error) {
		notify(error, 'error');
	}
	navigateTo('/dashboard');
};

let updateUser = async (userId) => {
	let savebleUsername = localStorage.getItem('username');
	let saveblePassword = '';

	let usernameField = document.getElementById('username');
	let currentPasswordField = document.getElementById('current-password');
	let newPasswordField = document.getElementById('password');

	const username = usernameField.value;
	const password = currentPasswordField.value;
	const repeatPassword = newPasswordField.value;

	if (username !== '' && username !== savebleUsername) {
		savebleUsername = username;
	}

	if (password === '' && username === '') {
		notify('No new password or new username provided', 'error');
		return;
	}

	if (password !== '' && password !== repeatPassword) {
		notify('Passwords do not match', 'error');
		return;
	}

	if (password !== '' && repeatPassword !== '') {
		saveblePassword = password;
	}

	const data = {
		username: savebleUsername,
		password: saveblePassword,
	};

	const userService = new UserService();
	try {
		await userService.putRequest(userId, data);
		if (username === savebleUsername)
			localStorage.setItem('username', savebleUsername);

		if (saveblePassword !== '') {
			notify('User updated successfully. Please log in again.');
			localStorage.clear();
			navigateTo('/logout');
			return;
		}

	} catch (error) {
		notify(error);
	}

	notify('User updated successfully.');
	navigateTo('/dashboard');
};

const deleteAccount = async (userId) => {
	try {
		new UserService().deleteRequest(userId);
		localStorage.clear();
		navigateTo('/');
	} catch (error) {
		notify(error, 'error');
		navigateTo('/dashboard');
	}
};

const SideBar = async () => {
	const aside = document.createElement('aside');
	const img = document.createElement('img');
	try {
		img.src = await getProfilePicture(localStorage.getItem('user_id'));
	} catch (error) {
		console.log('Error getting the profile picture element: ', error);
	}
	const fileInput = fileInputField(profilePictureHandler);
	aside.appendChild(fileInput);

	const UpdateModal = new UpdateUserModal(updateUser, localStorage.getItem('user_id'));
	const editProfileBtn = sideBarButton(['sidebar-element', 'bg-primary'], 'Edit profile', () => {
		aside.appendChild(UpdateModal.dialog);
		UpdateModal.dialog.showModal();
	});

	const profilePictureBtn = sideBarButton(
		['sidebar-element', 'bg-primary'],
		'Update profile picture',
		() => fileInput.click()
	);
	const createTournamentBtn = sideBarButton(
		['sidebar-element', 'bg-primary'],
		'Create Tournament',
		() => navigateTo('/tournament')
	);
	const logoutBtn = sideBarButton
	(['sidebar-element', 'bg-primary'],
		'Logout',
		() => navigateTo('/logout')
	);

	const AreYouSureModal = new AcceptDeclineModal(deleteAccount, localStorage.getItem('user_id'));
	AreYouSureModal.form.form.querySelector('h3').textContent =
		'Are you sure you want to delete your account?';
	const deleteAccountBtn = sideBarButton(['sidebar-element', 'error'], 'Delete account', () => {
		document.querySelector;
		AreYouSureModal.dialog.showModal();
	});

	aside.appendChild(img);
	aside.appendChild(fileInput);
	aside.appendChild(logoutBtn);
	aside.appendChild(editProfileBtn);
	aside.appendChild(profilePictureBtn);
	aside.appendChild(createTournamentBtn);
	aside.appendChild(deleteAccountBtn);
	aside.appendChild(AreYouSureModal.dialog);

	document.querySelector('body').appendChild(aside);
};

export default SideBar;
