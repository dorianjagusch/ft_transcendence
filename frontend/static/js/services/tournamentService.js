import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";
import NotImplementedError from "../exceptions/NotImplementedException.js";

export default class TournamentService extends ARequestService{
	constructor() {
		super();
	}

	async getAll() {
		throw new NotImplementedError("GET (resource) not implemented for TournamentService");
	}

	async getRequest(id) {
		let url = `${backendURL.tournamentURL}/` + (id ? id : "");
		const response = await super.getRequest(url);
		return response;
	}

	async postRequest(data) {
		const response = await super.postRequest(backendURL.tournamentURL, data);
		return response;
	}

	async putRequest(data) {
		const response = await super.putRequest(backendURL.tournamentURL, data);
		return response;
	}

	async deleteRequest(){
		throw new NotImplementedError("DELETE not implemented for TournamentService");
	}
}