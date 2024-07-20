import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";

export default class AuthenticationService extends ARequestService {
	constructor() {
		super();
	}

	async postMatch({username, password}) {
		return super.postRequest(
			`${backendURL.authenticationURL}match/ `, //${urlParams ? `/${urlParams}` : ''}`,
			JSON.stringify({
				username: username,
				password: password,
			})
		);
	}
}