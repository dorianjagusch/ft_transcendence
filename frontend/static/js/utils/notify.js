import {userNotification} from '../components/userNotification.js';

const notify = (message, type = 'success') => {
	userNotification(message, type);
	setTimeout(() => {
		document.querySelector('.notification').innerText = '';
	}, 3000);
}

export default notify;
