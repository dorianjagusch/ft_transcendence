import landingPage from './views/landingView.js';
import loginPage from './views/loginView.js';
import logoutPage from './views/logoutView.js';
import registerPage from './views/registerView.js';
import dashboardPage from './views/dashboardView.js';
import friendsPage from './views/friendsView.js';
import profilePage from './views/profileView.js';
import playPage from './views/playView.js';
import pongPage from './views/pongView.js';
import leaderBoard from './views/leaderboardView.js';
import show404Page from './views/404View.js';
import profilePicturePage from './views/profilePictureView.js';

export default [
	{ path: '/404', view: show404Page },
	{ path: '/', view: landingPage },
	{ path: '/login', view: loginPage },
	{ path: '/logout', view: logoutPage },
	{ path: '/register', view: registerPage },
	{ path: '/dashboard', view: dashboardPage },
	{ path: '/profilePicture', view: profilePicturePage },
	{ path: '/friends', view: friendsPage },
	{ path: '/play', view: playPage },
	{ path: '/pong', view: pongPage },
	{ path: '/leaderboard', view: leaderBoard },
	{ path: '/profile/:id', view: profilePage },
];
