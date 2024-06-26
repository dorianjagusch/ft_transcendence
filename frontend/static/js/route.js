import landingPage from './pages/landingPage.js';
import loginPage from './pages/loginPage.js';
import logoutPage from './pages/logoutPage.js';
import registerPage from './pages/registerPage.js';
import dashboardPage from './pages/dashboardPage.js';
import friendsPage from './pages/friendsPage.js';
import profilePage from './pages/profilePage.js';
import playPage from './pages/playPage.js';
import pongPage from './pages/pongPage.js';
import leaderBoard from './pages/leaderboardPage.js';
import show404Page from './pages/404Page.js';

export default [
	{ path: '/404', view: show404Page },
	{ path: '/', view: landingPage },
	{ path: '/login', view: loginPage },
	{ path: '/logout', view: logoutPage },
	{ path: '/register', view: registerPage },
	{ path: '/dashboard', view: dashboardPage },
	{ path: '/friends', view: friendsPage },
	{ path: '/play', view: playPage },
	{ path: '/pong', view: pongPage },
	{ path: '/leaderboard', view: leaderBoard },
	{ path: '/profile/:id', view: profilePage },
];
