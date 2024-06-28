const userNotification = (message, type) => {

	const notification = document.querySelector('#notification')
	notification.classList.remove('error', 'success');
	notification.innerText = message.message || message;

	message instanceof Error || type === 'error'
		? notification.classList.add('error')
		: notification.classList.add('success');
};

export { userNotification };