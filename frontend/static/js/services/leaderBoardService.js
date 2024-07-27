import ARequestService from "./ARequestService.js";
import backendURL from "../constants.js";

export default class LeaderBoardService extends ARequestService {

	constructor() {
		super();
	}

	async getLeaderBoard() {
		return super.getRequest(`${backendURL.leaderboardURL}`);
	}

}