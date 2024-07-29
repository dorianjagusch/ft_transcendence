import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

export default class MatchService extends ARequestService {
	constructor() {
		super();
	}

	async getHistoryMatches(userId) {
		return await super.getRequest(`${backendURL.matchURL}?user_id=${userId}`);
	}

	async getMatchPlayers(matchId) {
		return await super.getRequest(`${backendURL.matchURL}${matchId}/players/`);
	}
}
