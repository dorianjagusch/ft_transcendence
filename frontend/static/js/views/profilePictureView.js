import AView from './AView.js';
import uploadImageButton from '../components/profileComponents/uploadImageButton.js'
import ProfilePictureService from '../services/profilePictureService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Profile picture');
	}

	appendEventListeners() {
		const registerButton = document.querySelector('.primary-btn');
		registerButton.addEventListener('click', this.profilePictureHandler);
	}

	async getHTML() {
		const profilePictureButton = document.querySelector('.primary-btn');
		profilePictureButton.addEventListener('click', this.profilePictureHandler);

		this.updateMain(profilePictureButton);
		this.appendEventListeners();
	}
}
