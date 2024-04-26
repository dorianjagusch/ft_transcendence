import { baseURL } from '../constants.js';

const userURL = baseURL + 'users/'

const getUser = async (id) => {
	const request = await fetch(`${userURL}${id}`)
	return request.then((response) => {
		if (response.ok)
			return response.json()
	});
}

const postUser = async ({username, password}) => {
	const request = await fetch(`${userURL}`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			username: username,
			password: password
		})
	})
	return request.then((response) => {
		if (response.ok)
			return response.json();
});
}


const putUser = async ({id, username, password}) => {
	const request = fetch(`${userURL}/${id}`,	{
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				username: username,
				password: password
			})}
	)
	return request.then((response) => {
			if (response.ok)
				return response.json();
		});
}



export default {getUser, postUser, putUser};