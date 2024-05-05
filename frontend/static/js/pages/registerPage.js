import { Modal } from "../components/modal.js";
import { InputField } from "../components/inputField.js";
import userService from "../services/UserService.js";
import AView from "./AView.js";

export default class extends AView {

	constructor(params) {
		super(params);
		this.setTitle("Register");
		this.registerHandler = this.registerHandler.bind(this);
	}

	registerHandler = async (e) => {
		console.log("registerHandler");
		e.preventDefault();
		const username = document.getElementById("username").value;
		const password = document.getElementById("current-password").value;
		const repeatPassword = document.getElementById("password").value;

		if (username === "" || password === "" || repeatPassword === "") {
			alert("Please enter all fields");
			return;
		}

		if (password !== repeatPassword) {
			alert("Passwords do not match");
			return;
		}

		const data = {
			username: username,
			password: password,
		};

		userService
				.postUser(data)
				.then(() => {
				alert("User created successfully. Please login.");
				this.navigateTo("/login");
			})
			.catch((error) => {
				console.error(error);
			});
	};

	appendEventListeners(element) {
		const registerButton = element.querySelector(".primary-sign-btn");
		registerButton.addEventListener("click", this.registerHandler);

		const loginButton = element.querySelector(".secondary-sign-btn");
		console.log(loginButton);
		loginButton.addEventListener("click", () => {
			this.navigateTo("/login");
		});
	};

	createForm() {
		const form = document.createElement("form");

		const userNameField = InputField("text", "Username", "username");
		const passwordField = InputField("password", "Password", "current-password");
		const repeatPasswordField = InputField(
			"password",
			"Repeat Password",
			"password"
		);

		const registerButton = document.createElement("button");
		registerButton.classList.add("primary-sign-btn");
		registerButton.textContent = "Sign up";

		form.appendChild(userNameField);
		form.appendChild(passwordField);
		form.appendChild(repeatPasswordField);
		form.appendChild(registerButton);

		return form;
	};

	async getHTML(){

		const modalContainer = Modal("register", "bg-secondary");
		const registerModal = modalContainer.querySelector(".register");
		const form = this.createForm();
		registerModal.appendChild(form);

		const loginButton = document.createElement("button");
		loginButton.classList.add("secondary-sign-btn");
		loginButton.textContent = "Sign in";
		modalContainer.appendChild(loginButton);

		const main = document.querySelector("main");
		main.innerHTML = "";
		main.appendChild(modalContainer);
		this.appendEventListeners(main);
	};

}
