
const modal = (type, background) => {

	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container');

	const innermodal = document.createElement('div');
	innermodal.classList.add(type, `${background}`);

	const header = document.createElement('h2');
	header.classList.add('modal-title');
	header.textContent = type;

	innermodal.appendChild(header);
	modalContainer.appendChild(innermodal);
	return modalContainer;
}

export {modal}
