import { baseURL } from "../constants.js";

const loginURL = `${baseURL}users/login/`
function postLogin({username, password}) {
	console.log(loginURL)
	const response = await fetch(loginURL, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			username: username,
			password: password
		})
	})
	console.log(response);
	response.then((response) =>
	{
		if (response.ok){
			return response.json()
		}
	})
	.catch((error)=>{
		return console.error(error);
	})
}

export default {postLogin};
