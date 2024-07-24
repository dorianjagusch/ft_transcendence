import ADialog from "./ADialog.js";
import UpdateUserForm from "../formComponents/updateUserForm.js";

export default class UpdateUserModal extends ADialog {
    constructor(updateUser, userId) {
        super(new UpdateUserForm(), null);
        this.updateUser = updateUser;
        this.userId = userId;
        this.appendEventListeners();
    }

    appendEventListeners() {
        this.dialog.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.updateUser(this.userId);
            this.dialog.close();
        });
    }
}
