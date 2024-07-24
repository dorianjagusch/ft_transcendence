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

	async getMatchRequest(params) {
		const matchToken = localStorage.getItem('token');
		if (!params.tournament_id || !params.match_id || matchToken === "undefined") {
			throw new Error('Tournament and match id are required and a match token fetched');
		}
		const path =`${params.tournament_id}/matches/${params.match_id}`;
		const url = new URL(path, backendURL.tournamentURL);
		url.searchParams.append('token', matchToken);
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
