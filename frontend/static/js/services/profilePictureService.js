import backendURL from '../constants.js';
import getCookie from '../utils/getCookie.js';
import ARequestService from './ARequestService.js';

export default class ProfilePictureService extends ARequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		return await super.getRequest(`${backendURL.userURL}${id}/profile_pictures/`);
	}

	async getFriendProfilePictureRequest(id) {
		return super.getRequest(`${backendURL.friendURL}${id}/profile_pictures/`);
	}

	async postRequest(id, data) {
		const postRequest = fetch(`${backendURL.userURL}${id}/profile_pictures/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
			},
			body: data,
			credentials: 'include',
		});
		const responseData = this.checkResponseWithBody(postRequest);
		return responseData;
	}
}
