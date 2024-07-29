import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";

export default class PlayerService extends ARequestService {
	constructor() {
		super();
	}

	async getAll() {
		return super.getRequest(backendURL.playerURL);
	}

	async getRequest(id) {
		let url = `${backendURL.playerURL}/` + (id ? id : '');
		return super.getRequest(url);
	}

	async postRequest(data) {
		throw new NotImplementedError('POST not implemented for PlayerService');
	}

	async patchRequest(context) {
		throw new NotImplementedError('PATCH not implemented for PlayerService');
	}

	async putRequest() {
		throw new NotImplementedError('PUT not implemented for PlayerService');
	}

	async deleteRequest(context) {
		throw new NotImplementedError('DELETE not implemented for PlayerService');
	}
}