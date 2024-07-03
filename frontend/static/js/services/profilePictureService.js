import backendURL from "../constants.js";
import getCookie from '../utils/getCookie.js';
import ArequestService from "./ArequestService.js";

class ProfilePictureService extends ArequestService {
	constructor() {
		super();
	}

	async postProfilePictureRequest(user_id, data) {
		const request = fetch(`${backendURL.userURL}${user_id}/profile_pictures/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'multipart/form-data',
			},
			body: data,
			credentials: 'include',
		});

		return this.checkResponseWithBody(request);
	}
}

export default ProfilePictureService;
