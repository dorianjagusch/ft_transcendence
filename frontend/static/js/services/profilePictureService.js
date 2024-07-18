import backendURL from '../constants.js';
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
		return super.postRequest(`${backendURL.userURL}${id}/profile_pictures/`, data);
	}
}
