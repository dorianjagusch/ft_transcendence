import { baseURL } from '../constants.js';

userUrl = baseURL + 'user/'

const getUser = async (id) => {
	const request = await fetch(`${userUrl}${id}`)
	return request.then((response) => {
		if (response.ok)
			return response.json()
	});
}


const postUser = async ({username, password}) => {
	const request = await fetch(`${userUrl}`, {
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
	const request = await fetch(`${userUrl}/${id}`,	{
			method: 'PUT',
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


const deleteUser = async ({ id }) => {
  const request = await fetch(`${userUrl}/${id}`, {
    method: "Delete",
    headers: { "Content-Type": "application/json" },
	body: JSON.stringify({
				username: username,
				password: password
			})
  });
  return request.then((response) => {
    if (response.ok) return response.json();
  });
};


const getAllUsers = async () => {
	  const request = await fetch(`${userUrl}`);
  return request.then((response) => {
	if (response.ok) return response.json();
  });
}


export default {getUser, postUser, putUser, deleteUser, getAllUsers};