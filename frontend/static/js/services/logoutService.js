import ArequestService from './ArequestService.js';
import backendURL from '../constants.js';

class LogoutService extends ArequestService {
	constructor() {
		super();
	}

	async postRequest() {
		return super.postRequest(backendURL.logoutURL);
	}
}

export default LogoutService;
