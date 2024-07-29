import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';
import getCookie from '../utils/getCookie.js';

export default class StatsService extends ARequestService {
	constructor(params) {
		super(params);
	}

	async getRequest(userId) {
		return super.getRequest(`${backendURL.userURL}${userId}/stats/`);
	}

	async getImage(id, graphType) {
		const request = fetch(`${backendURL.userURL}${id}/${graphType}/`, {
			method: 'GET',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'image/svg+xml',
			},
			credentials: 'include',
		});
		return this.checkResponseWithNonJsonBody(request);
	}
}
