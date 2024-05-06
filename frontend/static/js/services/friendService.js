import backendURL from '../constants.js'
import RequestService from './requestService.js'

class FriendService extends RequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		throw new NotImplentedError("GET method not implemented for FriendService");
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

	async putRequest(id, {user_id, friend_id}) {
		throw new NotImplentedError("PUT method not implemented for FriendService");
	}

	async deleteRequest(id) {
		return super.deleteRequest(`${backendURL.friendURL}${id}`, id);
	}
}

export default FriendService;
