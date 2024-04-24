import { route } from './route.js';
import { routes } from './Routes.js';
import { handleLocation } from './handleLocation.js';
import './displayFriend.js';
import { confirmPassword } from './registration.js';

window.route = route;
window.confirmPassword = confirmPassword;

handleLocation();
