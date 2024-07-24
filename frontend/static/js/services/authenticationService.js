import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";


// TODO: Extend for tournaments
export default class AuthenticationService extends ARequestService {
	constructor() {
		super();
	}

	async postMatch({username, password}, logoutOn401 = true) {
		return super.postRequest(
			`${backendURL.authenticationURL}match/ `,
			JSON.stringify({
				username: username,
				password: password,
			}),
			logoutOn401
		);
	}

	async postAiMatch(URLParams) {
		const url = new URL(`${backendURL.authenticationURL}match/`);
		Object.keys(URLParams).forEach(key => url.searchParams.append(key, URLParams[key]));
		return super.postRequest(url);
	}
}
