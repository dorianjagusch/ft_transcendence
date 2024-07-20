import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';
import NotImplementedError from '../exceptions/NotImplementedException.js';

class PongService extends ARequestService {
	constructor() {
		super();
	}

	async getRequest() {
		const matchToken = localStorage.getItem('token');
		const url = `${backendURL.pongURL}?` + (matchToken ? `token=${matchToken}`: '');
		return super.getRequest(url);
	}

	getAllRequest() {
		new NotImplementedError('GET (all) not implemented for PongService');

	}

	postRequest(data){
		new NotImplementedError('POST method not implemented for PongService');
	}

	putRequest(data){
		new NotImplementedError('PUT method not implemented for PongService');
	}

	deleteRequest(){
		new NotImplementedError('DELETE method not implemented for PongService');
	}

}

export default PongService;
