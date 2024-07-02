import userURL from "../constants.js";
import ArequestService from "./ArequestService.js";

class ProfilePictureService extends ArequestService {
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
