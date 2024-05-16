import RequestService from "./requestService.js";
import backendURL from "../constants.js";

class LogoutService extends RequestService {
	constructor() {
		super();
	}

	async postRequest() {
		return super.postRequest(backendURL.logoutURL);
	}
}

export default LogoutService;