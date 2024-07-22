import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";


// TODO: Extend for tournaments
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

	async postAiMatch(URLParams) {
		const url = new URL(`${backendURL.authenticationURL}match/`);
		Object.keys(URLParams).forEach(key => url.searchParams.append(key, URLParams[key]));
		return super.postRequest(url);
	}
}
