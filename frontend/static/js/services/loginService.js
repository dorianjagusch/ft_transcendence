import { baseURL } from "../constants.js";


function postLogin({username, password}) {
	const response = fetch(`${baseURL}login/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			username: username,
			password: password
		})
	})
	return (
		response.then((response) =>
		{
			if (response.ok){
				return response.json()
			}
		})
		.catch((error)=>{
			return console.error(error);
		})
	)
}

export default {postLogin};
