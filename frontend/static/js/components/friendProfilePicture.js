import ProfilePictureService from '../services/profilePictureService.js';

const getFriendProfilePicture = (id) => {
	const img = document.createElement('img');
	var profilePictureService = new ProfilePictureService();

	try {
		const response = profilePictureService.getFriendProfilePictureRequest(id)
		if (response.image) {
			img.setAttribute('src', `data:image/jpeg;base64,${response.image}`);
		}
		else {
			img.setAttribute('src', './static/assets/img/default-user.png');
		}

		return img;
	} catch (error) {
		console.log('Error: ', error);
		img.setAttribute('src', './static/assets/img/default-user.png');
	}

	return img;
};

export default getFriendProfilePicture;
