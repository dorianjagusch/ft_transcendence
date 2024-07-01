class UnauthorizedException extends Error {
	constructor(message) {
		super(message);
		this.name = 'UnauthorizedException'
		this.status = 401;

		localStorage.removeItem('username');
		localStorage.removeItem('isLoggedIn');
	}
}

export default UnauthorizedException;