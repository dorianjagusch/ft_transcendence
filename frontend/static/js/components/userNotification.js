const userNotification = (message, type) => {

	const notification = document.querySelector('.notification')
	notification.classList.remove('error', 'success');
	notification.innerText = message.message || message;

	message instanceof Error || type === 'error'
		? notification.classList.add('error')
		: notification.classList.add('success');
};

const inputNotification = (message, type) => {
	const notification = document.createElement('div')
	notification.classList.add('.input-notification');
	notification.innerText = message.message || message;

	notification.classList.add('error')
	return notification;
};

export { userNotification, inputNotification };