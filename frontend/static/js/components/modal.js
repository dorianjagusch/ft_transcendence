const Modal = (type, background, Form) => {
	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container');

	const innerModal = document.createElement('div');
	innerModal.classList.add(type, 'inner-modal', background);

	const header = document.createElement('h2');
	header.classList.add('modal-title');
	header.textContent = type;

	const form = new Form();
	const formElement = form.generateForm();

	innerModal.appendChild(header);
	innerModal.appendChild(formElement);
	modalContainer.appendChild(innerModal);
	return modalContainer;
};

export default Modal;
