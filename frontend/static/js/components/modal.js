
const Modal = (type, background, formCallBack) => {

  const modalContainer = document.createElement('div');
  modalContainer.classList.add('modal-container');

  const innerModal = document.createElement('div');
  innerModal.classList.add(type, 'inner-modal', background);

  const header = document.createElement('h2');
  header.classList.add('modal-title');
  header.textContent = type;

  const form = formCallBack();

  innerModal.appendChild(header);
  innerModal.appendChild(form);
  modalContainer.appendChild(innerModal);
  return modalContainer;
}

export {Modal}