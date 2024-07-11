import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";

export default class AuthenticationService extends ARequestService {
	constructor() {
		super();
	}

	async postRequest({username, password}) {
		return super.postRequest(
			`${backendURL.authenticationURL}`,
			JSON.stringify({
				username: username,
				password: password,
			})
		);
	}
}