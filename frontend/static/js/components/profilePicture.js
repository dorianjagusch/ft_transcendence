import ProfilePictureService from '../services/profilePictureService.js';

const getProfilePicture = async (userIdStr) => {
	if (!userIdStr) {
		throw new Error('User ID is not found in local storage');
	}
	const userId = parseInt(userIdStr, 10);
	if (isNaN(userId)) {
		throw new Error('User ID is not a valid number');
	}

	const profilePictureService = new ProfilePictureService();

	try {
		const responseBody = await profilePictureService.getRequest(userId);
		if (responseBody.image === '') {
			return './static/assets/img/default-user.png';
		} else {
			return `data:image/jpeg;base64,${responseBody.image}`;
		}
	} catch (error) {
		'./static/assets/img/default-user.png';
	}
	return ''
};

export default getProfilePicture;
