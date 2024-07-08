const fileInputField = (handler) => {
	const fileInput = document.createElement('input');
	fileInput.setAttribute('type', 'file');
	fileInput.setAttribute('id', 'profilePicture');
	fileInput.style.display = 'none';

	fileInput.addEventListener('change', (event) => {
		const file = event.target.files[0];
		handler(file);
	});

	return fileInput;
};

export default fileInputField;
