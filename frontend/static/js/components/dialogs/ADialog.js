import NotImplementedError from '../../exceptions/NotImplementedException.js';
import { inputNotification } from '../userNotification.js';

export default class ADialog {
	constructor(Form, Service) {
		if (this.constructor == ADialog) {
			throw new Error("Abstract classes can't be instantiated.");
		}
		this.service = Service || null;
		this.form = Form || null;
		this.constructBaseDialog = this.constructBaseDialog.bind(this);
		this.dialog = this.constructBaseDialog();
		this.notify = this.notify.bind(this);
		this.appendBaseEventlistenters = this.appendBaseEventlistenters.bind(this);
		this.appendBaseEventlistenters();
	}

	appendEventlistenters(Service) {
		throw new NotImplementedError('Method not implemented in ADialog abstract class');
	}

	appendBaseEventlistenters(dialog) {
		this.dialog.addEventListener('click', (e) => {
			const dialogDimensions = this.dialog.getBoundingClientRect();
			if (
				e.clientX < dialogDimensions.left ||
				e.clientX > dialogDimensions.right ||
				e.clientY < dialogDimensions.top ||
				e.clientY > dialogDimensions.bottom
			) {
				this.dialog.close();
			} else if (e.target === this.dialog.querySelector('.x-btn')) {
				this.dialog.close();
			}
		});
	}

	notify(message, type) {
		const notification = inputNotification(message, type);
		this.dialog.querySelector('h3').after(notification);
		setTimeout(() => {
			notification.remove();
		}, 3000);
	}

	cancelButton() {
		const cancelButton = document.createElement('button');
		cancelButton.classList.add('x-btn');
		cancelButton.setAttribute('type', 'submit');
		cancelButton.setAttribute('formmethod', 'dialog');
		return cancelButton;
	}

	constructBaseDialog() {
		const form = this.form?.generateForm() || document.createElement('form');

		const dialog = document.createElement('dialog');
		dialog.classList.add('bg-secondary');
		form.appendChild(this.cancelButton());
		dialog.appendChild(form);
		return dialog;
	}
}
