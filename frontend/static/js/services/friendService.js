import backendURL from '../constants.js'
import RequestService from './requestService.js'
import NotImplementedError from '../exceptions/notImplemented.js'

class FriendService extends RequestService {
	constructor() {
		super();
	}

	async getRequest(id) {
		throw new NotImplementedError("GET method not implemented for FriendService");
	}

	async getAllRequest(friendship_status) {
		return super.getAllRequest(`${backendURL.friendURL}?friendship_status=${friendship_status}`);
	}

	async postRequest({ friend_id }) {
		return super.postRequest(
			`${backendURL.friendURL}`,
			JSON.stringify({
				friend_id: friend_id
		}));
	}

	async putRequest(id, {user_id, friend_id}) {
		throw new NotImplementedError("PUT method not implemented for FriendService");
	}

	async deleteRequest(friend_id) {
		return super.deleteRequest(`${backendURL.friendURL}${friend_id}`);
	}
}

export default FriendService;
