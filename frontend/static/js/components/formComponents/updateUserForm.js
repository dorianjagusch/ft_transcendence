import AForm from './AForm.js';
import InputField from './inputField.js';

export default class UpdateUserForm extends AForm {
    constructor() {
        super();
    }

    generateForm() {
        const header = document.createElement('h3');
        header.textContent = 'Update Information';

        const userNameField = InputField('text', 'Input new username', 'username');
        const passwordField = InputField('password', 'Input new password', 'current-password');
        const repeatPasswordField = InputField('password', 'Repeat new password', 'password');
        const updateUserButton = document.createElement('button');
        updateUserButton.classList.add('primary-btn');
        updateUserButton.setAttribute('type', 'submit');
        updateUserButton.textContent = 'Save information';

        const buttonBar = document.createElement('div');
        buttonBar.classList.add('button-bar');
        buttonBar.appendChild(updateUserButton);

        this.appendToForm(header, userNameField, passwordField, repeatPasswordField, buttonBar);
        return this.getForm();
    }
}
