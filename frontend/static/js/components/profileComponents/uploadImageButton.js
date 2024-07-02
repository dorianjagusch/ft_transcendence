const uploadImageButton = (uploadFunction) => {
	const container = document.createElement('div');
	container.classList.add('menu-item');

	const fileInput = document.createElement('input');
	fileInput.setAttribute('type', 'file');
	fileInput.setAttribute('accept', 'image/*');
	fileInput.classList.add('file-input');
	fileInput.setAttribute('id', 'profilePicture');
	fileInput.style.display = 'none';

	const button = document.createElement('button');
	button.classList.add('primary-btn');
	button.textContent = 'Upload Image';

	button.addEventListener('click', () => {
		fileInput.click();
	});

	fileInput.addEventListener('change', () => uploadFunction);

	container.appendChild(fileInput);
	container.appendChild(button);
};

export default uploadImageButton;
