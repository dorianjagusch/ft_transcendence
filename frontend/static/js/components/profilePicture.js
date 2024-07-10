import ProfilePictureService from '../services/profilePictureService.js';

const getProfilePicture = () => {
	const userIdStr = localStorage.getItem('user_id');
	if (!userIdStr) {
		throw new Error("User ID is not found in local storage");
	}

	const userId = parseInt(userIdStr, 10);
	if (isNaN(userId)) {
		throw new Error("User ID is not a valid number");
	}

	const img = document.createElement('img');
	var profilePictureService = new ProfilePictureService();

	profilePictureService.getRequest(userId)
	.then(response => {
		if (!response.ok) {
			if (response.status === 404) {
				return '';
			}
			else {
				throw new Error(`Error: ${response.status}`);
			}
		}

		return response.json();
	})
	.then(responseBody => {
		if (responseBody === '') {
			img.setAttribute('src', 'static/assets/img/default-user.png');
		}
		else {
			img.setAttribute('src', `data:image/jpeg;base64,${responseBody.image}`);
		}
	})
	.catch(error => {
		console.error('Error fetching profile picture:', error);
		img.setAttribute('src', 'static/assets/img/default-user.png');
	});

	return img;
}

export default getProfilePicture;
