import notify from '../../utils/notify.js';

function validateFile(file) {
	//const validImageTypes = ['image/jpeg', 'image/png', 'image/jpg'];
	//if (!validImageTypes.includes(file.type)) {
	//	notify('Please select a valid image file (JPEG, PNG, JPG).', 'error');
	//	return false;
	//}

	//const maxSizeInBytes = 2097152;
	//if (file.size > maxSizeInBytes) {
	//	notify('Please select an image smaller than 2MB.', 'error');
	//	return false;
	//}

	return true;
}

const fileInputField = (handler) => {
	const fileInput = document.createElement('input');
	fileInput.setAttribute('type', 'file');
	fileInput.setAttribute('id', 'profilePicture');
	fileInput.style.display = 'none';

	fileInput.addEventListener('change', (event) => {
		const file = event.target.files[0];
		if (validateFile(file)) {
			handler(file);
		}
	});

	return fileInput;
};

export default fileInputField;
