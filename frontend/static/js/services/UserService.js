import { baseURL } from '../constants.js';

userUrl = baseURL + 'user/'

const getUser = async (id) => {
	const respone = await fetch(`${userUrl}${id}`)
	return respone.then((response) => {
		if (response.ok)
			return response.json()
	});
}

const postUser = async ({username, password}) => {
	const response = fetch(`${userUrl}`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			username: username,
			password: password
		})
	})
	return response.then((response) => {
			if (response.ok)
				return response.json();
});
}


const putUser = async ({id, username, password}) => {
	const response = fetch(`${userUrl}/${id}`,	{
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				username: username,
				password: password
			})}
	)
	return response.then((response) => {
			if (response.ok)
				return response.json();
		});
}



export default {getUser, postUser, putUser, deleteUser, getAllUsers};