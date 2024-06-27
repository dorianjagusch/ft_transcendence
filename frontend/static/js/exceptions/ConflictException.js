import {navigateTo} from '../router.js';

class ConflictException extends Error {
	constructor() {
		super("User already exists. Please login.");
		this.name = 'Conflict';
		navigateTo('/login');
	}
}

export default ConflictException;
