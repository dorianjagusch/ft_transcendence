import AView from './AView.js';
import uploadImageButton from '../components/profileComponents/uploadImageButton.js'
import ProfilePictureService from '../services/profilePictureService.js';

export default class extends AView {
	constructor(params) {
		super(params);
		this.setTitle('Profile picture');
	}

	profilePictureHandler = async (user_id) => {
		const file = document.getElementById('profilePicture').value;
		if (!file){
			this.notify('Profile picture is null', 'error');
			return;
		}

		const formData = new FormData();
		formData.append('file', file);

		const profilePictureService = new ProfilePictureService();
		profilePictureService
			.postRequest(user_id, file)
			.then(() => {
				this.notify('User profile picture added successfully. Please login.');
				this.navigateTo('/dashboard');
			})
			.catch((error) => {
				this.notify(error);
			});
	}

	appendEventListeners() {
		const profilePictureButton = document.querySelector('.primary-btn');
		profilePictureButton.addEventListener('click', this.profilePictureHandler);
	}

	async getHTML() {
		const buttonContainer = uploadImageButton(this.profilePictureHandler);

		this.updateMain(buttonContainer);
		this.addEventListener();
	}
}
