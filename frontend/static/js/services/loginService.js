import backendURL from '../constants.js';
import ArequestService from './ArequestService.js';

class LoginService extends ArequestService {
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
