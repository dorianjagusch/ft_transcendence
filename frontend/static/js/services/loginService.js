import backendURL from '../constants.js';
import ARequestService from './ARequestService.js';

class LoginService extends ARequestService {
	constructor() {
		super();
	}

	async postRequest({username, password}) {
		return super.postRequest(
			`${backendURL.loginURL}`,
			JSON.stringify({
				username: username,
				password: password,
			})
		);
	}

	
}

export default LoginService;
