const userNotification = (message, type) => {

	const existingNotification = document.querySelector('.notification')
	if (existingNotification){
		document.querySelector('.notification').remove();
	}

	const notification = document.createElement('div');
	notification.classList.add('notification');
	notification.innerText = message.message || message;

	message instanceof Error || type === 'error'
		? notification.classList.add('error')
		: notification.classList.add('success');

	document.querySelector("nav").appendChild(notification);
};

export { userNotification };