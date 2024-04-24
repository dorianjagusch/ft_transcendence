
function generateInputField(type, label) {
	const labelElement = document.createElement('label');
	labelElement.textContent = label;
	labelElement.setAttribute('for', label);

	const inputElement = document.createElement('input');
	inputElement.setAttribute('type', type);
	inputElement.setAttribute('id', label);

	const container = document.createElement('div');
	container.classList.add('menu-item');
	container.appendChild(labelElement);
	container.appendChild(inputElement);

	document.body.appendChild(container);

	return container;
}

function sendLogin(username, password) {
	const response = fetch('http://127.0.0.1:8080/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			username: username,
			password: password
		})
	})
	return (
		response.then((response) =>
		{
			if (response.ok){
				return response.json()
			}
		})
		.catch((error)=>{
			return console.error(error);
		})
	)
}

async function login() {
	const username = document.getElementById('username').value;
	const password = document.getElementById('current-password').value;
	if (username === '' || password === '') {
		alert('Please enter both username and password');
		return;
	}
	await sendLogin(username, password)
	.then(data => {
		if (data.success) {
			window.location.href = '/dashboard';
		} else {
			alert('Invalid username or password');
		}
	})
	.catch(error => console.error('Error:', error));
}

function createForm(){

	const form = document.createElement('form');

	const userNameField = generateInputField('text', 'username');
	const passwordField = generateInputField('password', 'current-password');

	const loginButton = document.createElement('button');
	loginButton.classList.add('primary-sign-btn');
	loginButton.textContent = 'Sign in';
	loginButton.addEventListener('click', login);

	form.appendChild(userNameField);
	form.appendChild(passwordField);
	form.appendChild(loginButton);

	return form;
}

function showLoginPage() {
	const modalContainer = document.createElement('div');
	modalContainer.classList.add('modal-container');

	const loginModal = document.createElement('div');
	loginModal.classList.add('login', 'bg-secondary');

	const header = document.createElement('h2');
	header.classList.add('modal-title');
	header.textContent = 'Login';

	const form = createForm();

	const signUpButton = document.createElement('button');
	signUpButton.classList.add('secondary-sign-btn');
	signUpButton.textContent = 'Sign up';

	loginModal.appendChild(header);
	loginModal.appendChild(form);

	modalContainer.appendChild(loginModal);
	modalContainer.appendChild(signUpButton);

	const main = document.querySelector('main');
	main.innerHTML = '';
	main.appendChild(modalContainer);
}


export { showLoginPage };