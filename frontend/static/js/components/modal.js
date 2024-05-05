
const modal = (type, background) => {

  const modalContainer = document.createElement('div');
  modalContainer.classList.add('modal-container');

	const inerModal = document.createElement('div');
	inerModal.classList.add(type, `${background}`);

  const header = document.createElement('h2');
  header.classList.add('modal-title');
  header.textContent = type;

  inerModal.appendChild(header);
  modalContainer.appendChild(inerModal);
  return modalContainer;
}

export { modal }
