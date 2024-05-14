import AForm from './AForm.js';
import InputField from './inputField.js';
import CountrySelector from './countrySelector.js';
import InputMediaField from './inputMediaField.js';

export default class extends AForm {
	constructor() {
		super();
	}

	generateForm() {
		const avatarField = InputMediaField('image', 'Avatar', 'avatar');
		const countryField = CountrySelector();
		const aboutField = InputField('textfield', 'About you', 'about');
		this.appendToForm(
			avatarField,
			countryField,
			aboutField
		);
		return this.getForm();
	}
}
