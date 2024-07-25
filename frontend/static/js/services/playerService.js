import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";

export default class PlayerService extends ARequestService {
	constructor() {
		super();
	}

	async getAll() {
		return super.getRequest(backendURL.playerUrl);
	}

	async getRequest(id) {
		let url = `${backendURL.playerUrl}/` + (id ? id : '');
		return super.getRequest(url);
	}

	async postRequest(data) {
		throw new NotImplementedError('POST not implemented for PlayerService');
	}

	async patchRequest(context) {
		throw new NotImplementedError('PUT not implemented for PlayerService');
	}

	async putRequest() {
		throw new NotImplementedError('PUT not implemented for PlayerService');
	}

	async deleteRequest(context) {
		throw new NotImplementedError('PUT not implemented for PlayerService');
	}
}