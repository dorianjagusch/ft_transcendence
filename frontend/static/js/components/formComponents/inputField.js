function InputField(type, label, id) {
	const labelElement = document.createElement('label');
	labelElement.textContent = label;
	labelElement.setAttribute('for', id);

	const inputElement = document.createElement('input');
	inputElement.setAttribute('type', type);
	inputElement.setAttribute('id', id);

	const container = document.createElement('div');
	container.classList.add('menu-item');
	container.appendChild(labelElement);
	container.appendChild(inputElement);

	document.body.appendChild(container);

	return container;
}

export default InputField;
