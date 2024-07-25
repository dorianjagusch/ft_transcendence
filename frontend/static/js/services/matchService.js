import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';

export default class extends ARequestService {
	contructor() {
		super();
	}

	async getUserMatches(matchId, user_id) {
		return await this.get(`${backendURL}matches/${matchId}/${user_id}`);
	}
}
