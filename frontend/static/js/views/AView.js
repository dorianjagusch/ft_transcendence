import {navigateTo} from '../router.js';
import {Navbar, updateNavbar} from '../components/navbar.js';
import SideBar from '../components/sideBar.js';
import notify from '../utils/notify.js';

export default class Aview {
	constructor(params) {
		this.params = params;
		if (this.constructor == Aview) {
			throw new Error("Abstract classes can't be instantiated.");
		}
		if (!document.querySelector('nav')) {
			Navbar();
		}
		updateNavbar();
		if (document.querySelector('aside')) {
			document.querySelector('aside').remove();
		}
		if (localStorage.getItem('isLoggedIn') === 'true') {
			SideBar();
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

	notify(message, type = 'success') {
		notify(message, type);
	}

	updateMain(...elements) {
		const main = document.querySelector('main');
		main.innerHTML = '';
		elements.forEach((element) => {
			if (element) {
				main.appendChild(element);
			}
		});
	}
}
