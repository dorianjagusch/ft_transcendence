import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

export default class MatchService extends ARequestService {
	constructor() {
		super();
	}

	async getHistoryMatches(matchId, userId) {
		return await this.get(`${backendURL}matches/${matchId}/${userId}`);
	}

	async getMatchPlayers(matchId) {
		return await this.get(`${backendURL}matches/${matchId}/players`);
	}
}
