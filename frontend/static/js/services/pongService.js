import RequestService from './requestService.js';
import backendURL from '../constants.js';

class PongService extends RequestService {
	constructor() {
		super();
	}

	async getRequest() {
		return super.getRequest(backendURL.pongURL);
	}
}

export default PongService;