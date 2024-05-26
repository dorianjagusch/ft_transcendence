import backendURL from "../constants.js";
import RequestService from "./requestService.js";

class LoginService extends RequestService {
	constructor() {
		super();
	}

	async postRequest({username, password}) {
		return super.postRequest(
			`${backendURL.loginURL}`,
			JSON.stringify({
				username: username,
				password: password,
		}));
	}
}

export default LoginService;
