import {userNotification} from '../components/userNotification.js';

const notify = (message, type = 'success') => {
	userNotification(message, type);
	setTimeout(() => {
		document.querySelector('.notification-section').remove();
	}, 3000);
}

export default notify;
