import backendURL from "../constants.js";
import getCookie from '../utils/getCookie.js';
import ArequestService from "./ArequestService.js";

class ProfilePictureService extends ArequestService {
	constructor() {
		super();
	}

	async getRequest() {
		return super.getRequest(`${backendURL.userURL}${user_id}/profile_pictures/`);
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
			this.throwCustomError(response.status, response.statusText);
		}

		return response;
	}
}

export default ProfilePictureService;
