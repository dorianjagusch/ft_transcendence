import constants from '../constants.js';
import getCookie from '../utils/getCookie.js';

class RequestService {
	constructor() {
		if (this.constructor == RequestService) {
			throw new Error("Abstract classes can't be instantiated.");
		}
	}

	async checkResponse(request) {
		try {
			const response = await request;
			if (!response.ok) {
				throw new Error('Error: ' + response.status);
			}
			return response.json();
		} catch (error) {
			if (error instanceof TypeError) {
				console.error(constants.problemWithFetchMsg, error);
			} else {
				throw error;
			}
		}
	}

	async getRequest(url, id) {
		const request = fetch(`${url}${id}`, {
			credentials: 'include',
		});
		return this.checkResponse(request);
	}

	async getAllRequest(url) {
		const request = fetch(`${url}`, {
			credentials: 'include',
		});
		return this.checkResponse(request);
	}

	async postRequest(url, jsonBody) {
		const cookies = getCookie('csrftoken')
		const request = fetch(`${url}`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json'},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponse(request);
	}

	async putRequest(url, id, jsonBody) {
		const request = fetch(`${url}${id}`, {
			method: 'PUT',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json'},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponse(request);
	}

	async deleteRequest(url, id) {
		const request = fetch(`${url}${id}`, {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json'},
			credentials: 'include',
			});

		return this.checkResponse(request);
	}
}

export default RequestService;
