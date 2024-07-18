import backendURL from '../constants.js';
import ARequestService from './ARequestService.js';

class UserService extends ARequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		return super.getRequest(`${backendURL.userURL}${id}`);
	}

	async getAllRequest(params) {
		const url = new URL(backendURL.userURL);
		Object.entries(params).forEach(([key, value]) => {
			url.searchParams.append(key, value);
		});
		return super.getAllRequest(`${url}`);
	}

	async postRequest({username, password}) {
		return super.postRequest(
			`${backendURL.userURL}`,
			JSON.stringify({
				username: username,
				password: password,
			})
		);
	}

	async putRequest(id, {username, password}) {
		return super.putRequest(
			`${backendURL.userURL}${id}`,
			id,
			JSON.stringify({
				username: username,
				password: password,
			})
		);
	}

	async deleteRequest(id) {
		return super.deleteRequest(`${backendURL.userURL}${id}`);
	}
}

export default UserService;
