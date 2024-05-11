import NotImplementedError from '../../exceptions/notImplemented.js';

export default class AForm {
	constructor() {
		this.form = document.createElement('form');
	}

	appendToForm(...formElements) {
		formElements.forEach((element) => {
			this.form.appendChild(element);
		});
	}

	getForm() {
		return this.form;
	}

	generateForm() {
		throw new NotImplementedError('generateForm method must be implemented by child classes');
	}
}
