const userNotification = (message, type) => {
	const notificationSection = document.createElement('section');
	notificationSection.classList.add('notification-section');
	const notificationText = document.createElement('p');
	notificationText.classList.add('notification');

	notificationText.innerText = message.message || message;
	message instanceof Error || type === 'error'
		? notificationText.classList.add('error')
		: notificationText.classList.add('success');

	notificationSection.appendChild(notificationText);
	document.body.appendChild(notificationSection);
};

const inputNotification = (message, type) => {
	const notification = document.createElement('div');
	notification.classList.add('.input-notification');
	notification.innerText = message.message || message;
	message instanceof Error || type === 'error'
		? notification.classList.add('error')
		: notification.classList.add('success');
	return notification;
};

export {userNotification, inputNotification};
