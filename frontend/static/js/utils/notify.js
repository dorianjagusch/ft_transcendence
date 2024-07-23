import {userNotification} from '../components/userNotification.js';

const notify = (message, type = 'success') => {
	userNotification(message, type);
	setTimeout(() => {
		document.querySelector('.notification').remove();
	}, 3000);
}

export default notify;
