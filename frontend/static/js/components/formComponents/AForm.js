import NotImplementedError from '../../exceptions/NotImplementedException.js';

export default class AForm {
	constructor() {
		if (this.constructor == AForm) {
			throw new Error("Abstract classes can't be instantiated.");
		}
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

	generateForm() {}
}
