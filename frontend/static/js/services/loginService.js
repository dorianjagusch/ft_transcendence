import backendURL from "../constants.js";

async function postLogin({ username, password }) {
  console.log(backendURL.loginURL);
  return fetch(backendURL.loginURL, {
		method: "POST",
		headers: {
		"Content-Type": "application/json",
		},
		body: JSON.stringify({
		username: username,
		password: password,
		}),
  	})
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error(`${response.status}`);
      }
    })
    .catch((error) => {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
    });
}


export default {postLogin};
