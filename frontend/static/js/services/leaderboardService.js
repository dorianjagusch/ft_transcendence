import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

export default class leaderboardService extends ARequestService {
	constructor() {
		super();
	}

	async getRequest() {
		return super.getRequest(`${backendURL.leaderboardURL}`);
	}
}
