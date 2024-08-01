const validateUsername = (username) => {
	if (username.length < 3) {
		throw new Error("Username needs to be at least 3 characters long.");
	}
};

export default validateUsername;
