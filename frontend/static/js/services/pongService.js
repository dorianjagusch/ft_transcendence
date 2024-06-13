import RequestService from './requestService.js';
import backendURL from '../constants.js';

export default class extends RequestService {
	constructor() {
		super();
	}

	async getRequest(jsonBody) {
		return super.getRequest(backendURL.pongURL, jsonBody);
	}
}