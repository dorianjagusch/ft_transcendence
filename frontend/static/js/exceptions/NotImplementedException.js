
class NotImplentedError extends Error {
	constructor(message) {
		super(message);
		this.name = "NotImplementedError";
	}
}

export default NotImplentedError;
