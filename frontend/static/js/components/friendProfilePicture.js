import ProfilePictureService from '../services/profilePictureService.js';

const getFriendProfilePicture = (id) => {
	const img = document.createElement('img');
	var profilePictureService = new ProfilePictureService();

	profilePictureService.getFriendProfilePictureRequest(id)
	.then(response => {
		if (!response.ok) {
			throw new Error(`Error: ${response.status}`);
		}

		return response.json();
	})
	.then(responseBody => {
		if (responseBody.image === '') {
			img.setAttribute('src', './static/assets/img/default-user.png');
		}
		else {
			img.setAttribute('src', `data:image/jpeg;base64,${responseBody.image}`);
		}
	})
	.catch(error => {
		console.error('Error fetching profile picture:', error);
		img.setAttribute('src', './static/assets/img/default-user.png');
	});

	return img;
};

export default getFriendProfilePicture;
