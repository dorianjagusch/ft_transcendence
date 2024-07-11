import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

class PongService extends ARequestService {
	constructor() {
		super();
	}

	async getRequest() {
		return super.getRequest(backendURL.pongURL);
	}
}

export default PongService;
