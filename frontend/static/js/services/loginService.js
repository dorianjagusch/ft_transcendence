import backendURL from "../constants.js";

async function postLogin({ username, password }) {
	const request = fetch(backendURL.loginURL, {
			method: "POST",
			headers: {
			"Content-Type": "application/json",
			},
			body: JSON.stringify({
				username: username,
				password: password,
			}),
		})
	return request.then((response) => {
		if (response.ok) {
			const newData = response.json();
			return newData;
		} else {
			throw new Error(`${response.status}`);
		}
	})
}


export default {postLogin};
