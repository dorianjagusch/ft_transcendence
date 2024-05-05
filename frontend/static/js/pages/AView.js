import { navigateTo } from "../index.js";

export default class {
	constructor(params) {
		this.params = params;
	};

	setTitle(title) {
		document.title = title;
	};

	navigateTo(path){
		navigateTo(path);
	}

	async getHTML(){
		return ;
	}
}