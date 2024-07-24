import constants from '../constants.js';
import getCookie from '../utils/getCookie.js';
import {navigateTo} from '../router.js';

class ARequestService {
	constructor() {
		if (this.constructor == ARequestService) {
			throw new Error("Abstract classes can't be instantiated.");
		}
	}

	async checkResponseWithBody(request, logoutOn401 = true) {
		try {
			const response = await request;
			if (response.ok) {
				return response.json();
			}
			console.log();
			if (response.status === 401 && logoutOn401) {
				localStorage.clear();
				navigateTo('/login');
				return;
			}

			throw new Error(response.message);
		} catch (error) {
			if (error instanceof TypeError) {
				console.error(constants.problemWithFetchMsg, error);
			} else {
				throw error;
			}
		}
	}

	async checkResponseNoBody(request, logoutOn401 = true) {
		try {
			const response = await request;
			if (!response.ok) {
				if (response.status === 401) {
					localStorage.clear();
					navigateTo('/login');
					return;
				}
				throw new Error('Error: ' + response.message);
			}
			return '';
		} catch (error) {
			if (error instanceof TypeError) {
				console.error(constants.problemWithFetchMsg, error);
			} else {
				throw error;
			}
		}
	}

	async getRequest(url, logoutOn401 = true) {
		const request = fetch(`${url}`, {
			credentials: 'include',
		});
		return this.checkResponseWithBody(request, logoutOn401);
	}

	async getAllRequest(url, logoutOn401 = true) {
		const request = fetch(`${url}`, {
			credentials: 'include',
		});
		return this.checkResponseWithBody(request, logoutOn401);
	}

	async postRequest(url, jsonBody, logoutOn401 = true) {
		const request = fetch(`${url}`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json',
			},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponseWithBody(request, logoutOn401);
	}

	async putRequest(url, jsonBody, logoutOn401 = true) {
		const request = fetch(`${url}`, {
			method: 'PUT',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json',
			},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponseWithBody(request, logoutOn401);
	}

	async patchRequest(url, id) {
		const request = fetch(`${url}${id}`, {
			method: 'PATCH',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		});
		return this.checkResponseWithBody(request);
	}

	async deleteRequest(url, logoutOn401 = true) {
		const request = fetch(`${url}`, {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json',
			},
			credentials: 'include',
		});

		return this.checkResponseNoBody(request, logoutOn401);
	}
}

export default ARequestService;
