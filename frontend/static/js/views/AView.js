import { navigateTo } from '../router.js';
import { userNotification } from '../components/userNotification.js';;

export default class Aview{
	constructor(params) {
		this.params = params;
		if (this.constructor == Aview) {
			throw new Error("Abstract classes can't be instantiated.");
		}
	}

	setTitle(title) {
		document.title = title;
	}

	navigateTo(path) {
		navigateTo(path);
	}

	getHTML() {
		return;
	}

	notify(message, type='success') {
		userNotification(message, type);
		setTimeout(() => {
			document.querySelector('.notification').remove();
		}, 3000);
	}

	updateMain(...elements) {
		const main = document.querySelector('main');
		main.innerHTML = '';
		elements.forEach((element) => {
			if (element){
				main.appendChild(element);
			}
		});
	}
}

