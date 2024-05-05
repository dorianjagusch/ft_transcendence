import { modal } from '../components.modal.js';
import { inputField } from '../components/inputField.js';

const createForm = () => {
	const form = document.createElement('form');

	const userIdField = inputField('number', 'User ID', 'user_id');
	const friendsUserIdField = inputField('number', 'Friends User ID', 'friend_id');
}

const showFriends = () => {
	const modalContainer = modal('friends', 'bg-secondary');
	const friendsmodal = modalContainer.querySelector('.friends');
	const form = createForm('');
}

export default showFriends;
