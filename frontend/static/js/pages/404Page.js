import AView from "./AView.js";

export default class extends AView {
  constructor() {
    super();
    this.setTitle("404 Not Found");
  }

  async getHTML() {
    const title404 = "<h2>Page not found</h2>";
	
    this.updateMain(title404);
  }
}
