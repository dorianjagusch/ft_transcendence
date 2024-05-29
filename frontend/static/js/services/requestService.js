import constants from '../constants.js';
import getCookie from '../utils/getCookie.js';

class RequestService {
	constructor() {
		if (this.constructor == RequestService) {
			throw new Error("Abstract classes can't be instantiated.");
		}
	}

	async checkResponseWithBody(request) {
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

	async checkResponseNoBody(request) {
		try {
			const response = await request;
			if (!response.ok) {
				throw new Error('Error: ' + response.status);
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

	async getRequest(url) {
		const request = fetch(`${url}`, {
			credentials: 'include',
		});
		return this.checkResponseWithBody(request);
	}

	async getAllRequest(url) {
		const request = fetch(`${url}`, {
			credentials: 'include',
		});
		return this.checkResponseWithBody(request);
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

		return this.checkResponseWithBody(request);
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

		return this.checkResponseWithBody(request);
	}

	async deleteRequest(url) {
		const request = fetch(`${url}`, {
			method: 'DELETE',
			headers: {
				'X-CSRFToken': getCookie('csrftoken'),
				'Content-Type': 'application/json'},
			credentials: 'include',
			});

		return this.checkResponseNoBody(request);
	}
}

export default RequestService;
