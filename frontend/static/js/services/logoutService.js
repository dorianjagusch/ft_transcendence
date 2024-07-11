import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

class LogoutService extends ARequestService {
	constructor() {
		super();
	}

	async postRequest() {
		return super.postRequest(backendURL.logoutURL);
	}
}

export default LogoutService;
