import ARequestService from './ARequestService.js';
import backendURL from '../constants.js';
import NotImplementedError from '../exceptions/NotImplementedException.js';

export default class TournamentService extends ARequestService {
	constructor() {
		super();
	}

	async getAll() {
		throw new NotImplementedError('GET (resource) not implemented for TournamentService');
	}

	async getRequest(id) {
		let url = `${backendURL.tournamentURL}/` + (id ? id : '');
		const response = super.getRequest(url);
		return response;
	}

	async postRequest(data) {
		const response = super.postRequest(
			backendURL.tournamentURL,
			JSON.stringify({
				name: data.tournamentName,
				player_amount: data.numberOfPlayers,
				host_user_display_name: '',
			})
		);
		return response;
	}

	async postPlayer(token, tournamentId) {
		const response = super.postRequest(
			`${backendURL.tournamentURL}/${tournamentId}/players/`
		);
		return response;
	}

	async putRequest() {
		throw new NotImplementedError('PUT not implemented for TournamentService');
	}

	async deleteRequest() {
		throw new NotImplementedError('DELETE not implemented for TournamentService');
	}
}
