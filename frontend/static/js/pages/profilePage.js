import AView from './AView.js';
import buttonBar from '../components/profileComponents/buttonBar.js';
import profileImg from '../components/profileComponents/profileImg.js';
import profileTitle from '../components/profileComponents/profileTitle.js';
import profileDescription from '../components/profileComponents/profileDescription.js';
import smallPlacementCard from '../components/profileComponents/smallPlacementCard.js';

export default class extends AView {
	constructor(params) {
		super(params);
	}

	async getHTML() {
		

		this.updateMain();
	}
}
