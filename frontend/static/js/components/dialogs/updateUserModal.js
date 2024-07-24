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
            const username = document.getElementById('username').value;
            const password = document.getElementById('current-password').value;
            const repeatPassword = document.getElementById('password').value;

            if (password !== repeatPassword) {
                this.notify('Passwords do not match');
                return;
            }

            await this.updateUser(this.userId);
            this.dialog.close();
        }, false);
    }
}
