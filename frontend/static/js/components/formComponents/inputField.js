function InputField(type, label, id) {
	const labelElement = document.createElement('label');
	labelElement.textContent = label;
	labelElement.setAttribute('for', id);

	const inputElement = document.createElement('input');
	inputElement.setAttribute('type', type);
	inputElement.setAttribute('id', id);

	const container = document.createElement('div');
	container.classList.add('menu-item');

	const inputNotification = document.createElement('div');
	inputNotification.classList.add('input-notification');
	
	container.appendChild(inputNotification);

	container.appendChild(labelElement);
	container.appendChild(inputElement);

	document.body.appendChild(container);

	return container;
}

export default InputField;
