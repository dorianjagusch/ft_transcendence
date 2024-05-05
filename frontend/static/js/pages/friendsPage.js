import { modal } from '../components/modal.js';
import { inputField } from '../components/inputField.js';

const createForm = () => {
}

const showFriends = () => {
	const modalContainer = modal('friends', 'bg-secondary');
	const friendsmodal = modalContainer.querySelector('.friends');
	const form = createForm('');
}

export default showFriends;
