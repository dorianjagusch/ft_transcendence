import backendURL from '../constants.js';
import RequestService from './requestService.js'

class UserService extends RequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		return super.getRequest(`${backendURL.userURL}${id}`);
	}

	async getAllRequest() {
		return super.getAllRequest(`${backendURL.userURL}`);
	}

	async postRequest({username, password}) {
		return super.postRequest(
			`${backendURL.userURL}`,
			JSON.stringify({
				username: username,
				password: password,
		}));
	}

	async putRequest(id, {username, password}) {
		return super.putRequest(
			`${backendURL.userURL}${id}`,
			id,
			JSON.stringify({
				username: username,
				password: password,
		}));
	}

	async deleteRequest(id) {
		return super.deleteRequest(`${backendURL.userURL}${id}`);
	}
}

export default UserService;
