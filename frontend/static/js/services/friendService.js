import backendURL from '../constants.js'

const getFriends = async () => {
	const request = fetch(`${backendURL.friendURL}`)
	return request
		.then((response) => {
			if (response.ok) {
				const data = response.json();
				return data;
			}
			else
				throw new Error("Error: " + response.status);
		})
		.catch((error) => {
			console.error(problemWithFetchMsg, error);
		})
}

const getFriend = async ({ id }) => {
	const request = fetch(`${backendURL.friendURL}`)
	return request
		.then((response) => {
			if (response.ok) {
				const data = response.json();
				return data;
			}
			else
				throw new Error("Error: " + response.status);
		})
		.catch((error) => {
			console.error(problemWithFetchMsg, error);
		})
}

const postFriend = async ({ user_id, friend_id }) => {
	const request = fetch(`${backendURL.friendURL}`, {
		method: "POST",
		headers: jsonContentType,
		body: JSON.stringify({
			user_id: user_id,
			friend_id: friend_id
		})
	});

	return request
		.then((response) => {
			if (response.ok) {
				const data = response.json();
				return data;
			}
			else
				throw new Error("Error: " + response.status);
		})
		.catch((error) => {
			console.error(problemWithFetchMsg, error)
		})
}
