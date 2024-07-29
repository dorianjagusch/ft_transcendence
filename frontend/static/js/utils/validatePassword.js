const validatePassword = (password) => {
	if (password.length < 8) {
		throw new Error("Password needs to be at least 8 characters long.");
	}

	if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
		throw new Error("Password must contain at least one special character.");
	}

	if (!/\d/.test(password)) {
		throw new Error("Password must contain at least one digit.");
	}
};

export default validatePassword;
