import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

export default class MatchService extends ARequestService {
	constructor() {
		super();
	}

	async postPlayer({username, password}, context, logoutOn401) {
		return super.postRequest(
			`${backendURL.authenticationURL}match/ `,
			JSON.stringify({
				username: username,
				password: password,
			}),
			logoutOn401
		);
	}

	async postAiMatch() {
		return super.postRequest(`${backendURL.authenticationURL}match/?ai_opponent=true`);
	}
}
