import ArequestService from './ArequestService.js';
import backendURL from '../constants.js';

class PongService extends ArequestService {
	constructor() {
		super();
	}

	async getRequest() {
		return super.getRequest(backendURL.pongURL);
	}
}

export default PongService;
