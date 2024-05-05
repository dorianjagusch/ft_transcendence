import loginService from "../services/loginService.js";
import { InputField } from "../components/inputField.js";
import { Modal } from "../components/modal.js";
import AView from "./AView.js";

export default class extends AView {

	constructor(params) {
		super(params);
		this.setTitle("Login");
	}

	loginHandler = async (e) => {
		e.preventDefault();
		const username = document.getElementById("username").value;
		const password = document.getElementById("current-password").value;
		if (username === "" || password === "") {
			alert("Please enter both username and password");
			return;
		}
		const toSend = { username, password };
		await loginService
			.postLogin(toSend)
			.then(() => {
			this.navigateTo("/friends");
			})
			.catch((error) => {
			console.error(
				"There has been a problem with your fetch operation:",
				error
			);
			});
	}

	appendEventListeners(element) {
		const loginButton = element.querySelector(".primary-sign-btn");
			loginButton.addEventListener("click", this.loginHandler);

		const signUpButton = element.querySelector(".secondary-sign-btn");
			signUpButton.addEventListener("click", () => {
			this.navigateTo("/register");
		});
	}

	createForm() {
		const form = document.createElement("form");

		const userNameField = InputField("text", "Username", "username");
		const passwordField = InputField("password", "Password", "current-password");

		const loginButton = document.createElement("button");
		loginButton.classList.add("primary-sign-btn");
		loginButton.textContent = "Sign in";


		form.appendChild(userNameField);
		form.appendChild(passwordField);
		form.appendChild(loginButton);

		return form;
	};

	async getHTML() {

		const modalContainer = Modal("login", "bg-secondary");
		const loginModal = modalContainer.querySelector(".login");
		const form = this.createForm();

		const signUpButton = document.createElement("button");
		signUpButton.classList.add("secondary-sign-btn");
		signUpButton.textContent = "Sign up";

		loginModal.appendChild(form);
		modalContainer.appendChild(signUpButton);


		const main = document.querySelector("main");
		main.innerHTML = "";
		main.appendChild(modalContainer);
		this.appendEventListeners(main);
	}
}

