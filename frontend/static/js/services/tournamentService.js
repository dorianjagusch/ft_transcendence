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

	async getTournamentMatches(context) {
		return super.getRequest(`${backendURL.tournamentURL}${context.tournament_id}/matches/`);
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

	async postPlayer(tournamentData, context, logoutOn401) {
		const response = super.postRequest(
			`${backendURL.tournamentURL}${context.tournamentId}/players/`,
			JSON.stringify({
				username: tournamentData.username,
				password: tournamentData.password,
			}),
			logoutOn401
		);
		return response;
	}

	async patchRequest(context) {
		return super.patchRequest(backendURL.tournamentURL, context.tournamentId);
	}

	async putRequest() {
		throw new NotImplementedError('PUT not implemented for TournamentService');
	}

	async deleteTournamentPlayer(context) {
		super.deleteRequest(`${backendURL.tournamentURL}${context.tournamentId}/players/${context.playerId}`);
	}
}
