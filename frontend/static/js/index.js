import { route } from './route.js'; // Correct import path
import { routes } from './Routes.js'; // Correct import path
import { handleLocation } from './handleLocation.js';
import './displayFriend.js'; // Importing the file executes the code
import { confirmPassword } from './registration.js';

window.route = route;
window.confirmPassword = confirmPassword;

handleLocation();
