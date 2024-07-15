import AForm from './AForm.js';

export default class searchFriendsForm extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const searchField = InputField('text', 'Search', 'friend-name');
		searchField.setAttribute('placeholder', 'Search for friends');
		const resultSection = document.createElement('div');
		resultSection.classList.add('search-results');
		this.appendToForm(searchField, resultSection);
		return form;
	}
}
