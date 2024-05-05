import constants from '../constants.js';

class ApiService {
	constructor() {
		if (this.constructor == ApiService) {
			throw new Error("Abstract classes can't be instantiated.");
		}
	}

	get = async (id) => {
		const request = fetch(`${backendURL.userURL}${ id}`)
		return request
		.then((response) => {
		  if (response.ok) {
			const data = response.json();
			return data;
		  } else throw new Error("Error: " + response.status);
		})
		.catch((error) => {
		  console.error(problemWithFetchMsg, error);
		});
	}
}

#https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
