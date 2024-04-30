import backendURL from '../constants.js';

const getUser = async (id) => {
	const request = fetch(`${backendURL.userURL}${id}`)
	return request
    .then((response) => {
      if (response.ok) {
        const data = response.json();
        return data;
      } else throw new Error("Error: " + response.status);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation: ", error);
    });
}


const postUser = async ({ username, password }) => {
	console.log(username)
  const request = fetch(`${backendURL.userURL}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  return request
    .then((response) => {
      if (response.ok){
		const data = response.json();
	  	return data;
	  }
      else
	  	throw new Error("Error: " + response.status);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation: ", error);
    });
};


const putUser = async ({ id, username, password }) => {
  const request = fetch(`${backendURL.userURL}${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  return request
    .then((response) => {
      if (response.ok) {
        const data = response.json();
        return data;
      } else throw new Error("Error: " + response.status);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation: ", error);
    });
};


const deleteUser = async ({ id }) => {
  const request = fetch(`${backendURL.userURL}${id}`, {
    method: "Delete",
    headers: { "Content-Type": "application/json" },
	body: JSON.stringify({
				username: username,
				password: password
			})
  });
  return request
    .then((response) => {
      if (response.ok) {
        const data = response.json();
        return data;
      } else throw new Error("Error: " + response.status);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation: ", error);
    });
};


const getAllUsers = async () => {
	  const request = fetch(`${backendURL.userURL}`);
  return request.then((response) => {
	if (response.ok){
		const data = response.json();
	  	return data;
	  }
      else
	  	throw new Error("Error: " + response.status);
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation: ", error);
    });
}


export default {getUser, postUser, putUser, deleteUser, getAllUsers};