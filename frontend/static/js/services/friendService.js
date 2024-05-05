import backendURL from '../constants.js'
import RequestService from './requestService.js'

class FriendService extends RequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		return super.getRequest(`${backendURL.friendURL}${id}`, id);
	}

	async getAllRequest() {
		return super.getAllRequest(`${backendURL.friendURL}`);
	}

	async postRequest({ user_id, friend_id }) {
		console.log(username);
		return super.postRequest(
			`${backendURL.friendURL}`,
			JSON.stringify({
				user_id: user_id,
				friend_id: friend_id,
		}));
	}

	async putRequest(id, {username, password}) {
		return super.putRequest(
			`${backendURL.friendURL}${id}`,
			id,
			JSON.stringify({
				username: username,
				password: password,
		}));
	}

	async deleteRequest(id) {
		return super.deleteRequest(`${backendURL.friendURL}${id}`, id);
	}
}

export default FriendService;
