import { Modal } from "../components/modal.js";
import userService from "../services/UserService.js";
import AView from "./AView.js";
import {RegisterForm} from "../components/forms.js";


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

  appendEventListeners() {
    const registerButton = document.querySelector(".primary-btn");
    registerButton.addEventListener("click", this.registerHandler);

    const loginButton = document.querySelector(".secondary-btn");
    console.log(loginButton);
    loginButton.addEventListener("click", () => {
      this.navigateTo("/login");
    });
  }


  async getHTML() {
    const modalContainer = Modal("register", "bg-secondary", RegisterForm);

    const loginButton = document.createElement("button");
    loginButton.classList.add("secondary-btn");
    loginButton.textContent = "Sign in";
    modalContainer.appendChild(loginButton);

	this.updateMain(modalContainer);
    this.appendEventListeners();
  }
}
