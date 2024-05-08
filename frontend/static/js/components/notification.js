const Notification = (message) => {
	const notification = document.createElement('div');
	notification.classList.add('notification');
	notification.innerText = message.message || message;

	message instanceof Error
		? notification.classList.add('error')
		: notification.classList.add('success');

	return notification;
};
