import landingPage from "./pages/landingPage.js";
import loginPage from "./pages/loginPage.js";
import registerPage from "./pages/registerPage.js";
import friendsPage from "./pages/friendsPage.js";
import friendPage from "./pages/friendPage.js";
import show404Page from "./pages/404Page.js";

const pathToRegex = path => new RegExp('^' + path.replace(/\//g, '\\/').replace(/:\w+/g, '(.+)') + '$');

const getParams = match => {
	const values = match.result.slice(1);
	const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

	return Object.fromEntries(keys.map((key, i) => {
			return [key, values[i]];
		}
	))
}

const navigateTo = url => {
  history.pushState(null, null, url);
  router();
};

const router = async () => {
  const routes = [
	{ path: '/404', view: show404Page },
    { path: "/", view: landingPage },
    { path: "/login", view: loginPage },
    { path: "/register", view: registerPage },
    { path: "/friends", view: friendsPage },
    { path: '/friends/:id', view: friendPage },
  ];

  const potentialMatches = routes.map(route => {
    return {
      route: route,
      result: location.pathname.match(pathToRegex(route.path))
    };
  });

  let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);
  console.log(match);
  if (!match){
    match = {
      route: routes[0],
      result: [location.pathname]
    };
  }
  const view = new match.route.view(getParams(match));
  await view.getHTML();

};

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', e => {
    if (e.target.matches('[data-link]')){
      e.preventDefault();
	  console.log(e.target.href);
      navigateTo(e.target.href);
    }
  });

  router();
});

export { navigateTo };