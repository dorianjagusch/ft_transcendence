import backendURL from "../constants.js";
import getCookie from '../utils/getCookie.js';

class ProfilePictureService {
	constructor() {
	}

	async checkResponseWithBody(request) {
		const response = await request;
		return response;
	}

	async getRequest(user_id) {
		const request = fetch(`${backendURL.userURL}${user_id}/profile_pictures/`, {
			credentials: 'include',
		});

		return this.checkResponseWithBody(request);
	}

	async getFriendProfilePictureRequest(user_id) {
		const request = fetch(`${backendURL.friendURL}${user_id}/profile_pictures/`, {
			credentials: 'include',
		});

		return this.checkResponseWithBody(request);
	}

	async postProfilePictureRequest(user_id, data) {
		const postRequest = fetch(`${backendURL.userURL}${user_id}/profile_pictures/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: data,
			credentials: 'include',
		});

		const response = await postRequest;
		if (!response.ok) {
			const responseData = await response.json();
			throw new Error(responseData.message || 'Error occurred.');
		}
	}
}

export default ProfilePictureService;
