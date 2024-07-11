import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

class LogoutService extends ARequestService {
	constructor() {
		super();
	}

	async postRequest() {
		return super.postRequest(backendURL.logoutURL);
	}

	getAllRequest() {
		throw new NotImplementedError('GET (all) not implemented for LogoutService');
	}

	getRequest() {
		throw new NotImplementedError('GET method not implemented for LogoutService');
	}

	putRequest() {
		throw new NotImplementedError('PUT method not implemented for LogoutService');
	}

	deleteRequest() {
		throw new NotImplementedError('DELETE method not implemented for LogoutService');
	}
}

export default LogoutService;
