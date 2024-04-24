function postLogin({username, password}) {
	const response = fetch('http://127.0.0.1:8080/login', {
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
