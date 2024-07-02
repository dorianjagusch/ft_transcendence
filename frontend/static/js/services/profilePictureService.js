import userURL from "../constants.js";
import RequestService from "./requestService.js";

class ProfilePictureService extends RequestService {
	constructor() {
		super();
	}

	async postRequest({user_id, data}) {
		return super.postRequest(
			`${userURL}${user_id}/profile_picture/`,
			data);
	}
}

export default ProfilePictureService;
