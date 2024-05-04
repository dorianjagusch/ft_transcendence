
const Modal = (type, background) => {

	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container');

	const innerModal = document.createElement('div');
	innerModal.classList.add(type, `${background}`);

	const header = document.createElement('h2');
	header.classList.add('modal-title');
	header.textContent = type;

	innerModal.appendChild(header);
	modalContainer.appendChild(innerModal);
	return modalContainer;
}

export {Modal}