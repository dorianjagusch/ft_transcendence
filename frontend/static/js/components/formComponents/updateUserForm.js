import AForm from './AForm.js';
import InputField from './inputField.js';

export default class UpdateUserForm extends AForm {
    constructor() {
        super();
    }

    generateForm() {
        const header = document.createElement('h3');
        header.textContent = 'Update Information';

        const infoHeader = document.createElement('h5');
        infoHeader.textContent = 'Changing the password will log you out.';

        const userNameField = InputField('text', 'New username', 'username');
        const passwordField = InputField('password', 'New password', 'current-password');
        const repeatPasswordField = InputField('password', 'Repeat password', 'password');
        const updateUserButton = document.createElement('button');
        updateUserButton.classList.add('primary-btn');
        updateUserButton.setAttribute('type', 'submit');
        updateUserButton.setAttribute('formmethod', 'dialog');
        updateUserButton.textContent = 'Save information';

        const buttonBar = document.createElement('div');
        buttonBar.classList.add('button-bar');
        buttonBar.appendChild(updateUserButton);

        this.appendToForm(header, infoHeader, userNameField, passwordField, repeatPasswordField, buttonBar);
        return this.getForm();
    }
}
