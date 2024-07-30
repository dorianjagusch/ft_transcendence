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

	async getImage(userId, type) {
		try {
			const response = await fetch(`${backendURL.userURL}${userId}/${type}/`, {
				method: 'GET',
				headers: {
					'X-CSRFToken': getCookie('csrftoken'),
					'Content-Type': 'application/json',
				},
				credentials: 'include',
			});
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			const svgText = await response.text();
			return svgText;
		} catch (error) {
			console.error("Couldn't fetch data", error);
		}
	}
}
