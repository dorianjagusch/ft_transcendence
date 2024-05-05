const navigateTo = url => {
  history.pushState(null, null, url);
  router();
};

const router = async () => {
  const routes = [
    { path: '/', view: showLandingPage },
    { path: '', view: show404Page },
    { path: '/login', view: showLoginPage },
    { path: '/register', view: showRegisterPage },
    { path: '/friends', view: showFriendsPage },
    { path: 'friends/:id', view: showFriendPage }
  ];

  const potentialMatches = routes.map(route => {
    return {
      route: route,
      isMatch: location.pathname === route.path
    };
  });

  let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);
  if (!match){
    match = {
      route: routes[0],
      isMatch: true
    };
  }

  match.route.view();

};

window.addEventListener('popstate', router);

document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', e => {
    if (e.target.matches('[data-link]')){
      e.preventDefault();
      navigateTo(e.target.href);
    }
  });

  router();
});
