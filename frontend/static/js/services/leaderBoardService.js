import ARequestService from "./ARequestService.js";

export default class LeaderBoardService extends ARequestService {

	constructor() {
		super();
	}

	async getLeaderBoard() {
		return super.getRequest('leaderboard/');
	}

}