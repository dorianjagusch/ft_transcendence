import constants from '../constants.js';

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
				console.log(constants.problemWithFetchMsg, error);
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
		const request = fetch(`${url}`, {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponse(request);
	}

	async putRequest(url, id, jsonBody) {
		const request = fetch(`${url}${id}`, {
			method: 'PUT',
			headers: {'Content-Type': 'application/json'},
			body: jsonBody,
			credentials: 'include',
		});

		return this.checkResponse(request);
	}

	async deleteRequest(url, id) {
		const request = fetch(`${url}${id}`, {
			method: 'DELETE',
			headers: {'Content-Type': 'application/json'},
			credentials: 'include',
		});

		return this.checkResponse(request);
	}
}

export default RequestService;
