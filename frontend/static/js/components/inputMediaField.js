
const InputMediaField = (type, label, id) => {

	const mediaItem = document.createElement('div');
	mediaItem.classList.add('menu-item');

	const mediaLabel = document.createElement('label');
	mediaLabel.setAttribute('for', id);
	mediaLabel.textContent = label;
	mediaItem.appendChild(mediaLabel);

	const mediaInput = document.createElement('input');
	mediaInput.setAttribute('id', id);
	mediaInput.setAttribute('name', id);
	mediaInput.setAttribute('type', type);
	mediaInput.setAttribute('accept', 'image/*');
	mediaInput.setAttribute('width', '200px');
	mediaInput.setAttribute('height', '200px');
	mediaItem.appendChild(mediaInput);

	return mediaItem;
}

export { InputMediaField }