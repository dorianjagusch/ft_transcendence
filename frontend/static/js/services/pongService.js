import RequuestService from './requestService.js';
import backendUrl from '../constants.js';

export default class extends RequuestService {
	constructor() {
		super();
	}

	async getRequest() {
		this.getRequest(backendUrl.pongURL);
	}
}