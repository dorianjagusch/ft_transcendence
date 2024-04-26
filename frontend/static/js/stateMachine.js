import showLandingPage from "./pages/landingPage.js";
import showLoginPage from "./pages/loginPage.js";
import showRegisterPage from "./pages/registerPage.js";
import showFriendsPage from "./pages/friendsPage.js";
// import showDashboardPage from "./pages/dashboardPage.js";
// import showProfilePage from "./pages/profilePage.js";

const machineConfig = {
  initialState: "landing",
  states: {
    landing: {},
    register: {},
    login: {},
    loggedIn: {
      leaderboard: {},
      dashboard: {},
      friends: {},
      play: {},
      settings: {},
    },
    loggedOut: {},
  },
  transitions: {
    landing: {
      goToRegister: "register",
      goToLogin: "login",
	  goToLanding: "landing",
    },
    register: {
      goToLanding: "landing",
      goToLogin: "login",
    },
    login: {
      goToLanding: "landing",
      goToRegister: "register",
      goToLoggedIn: "loggedIn",
    },
    loggedIn: {
      goToLoggedOut: "loggedOut",
      goToLeaderboard: "leaderboard",
      goToDashboard: "dashboard",
      goToFriends: "friends",
      goToPlay: "play",
      goToSettings: "settings",
    },
    loggedOut: {
      goToLogin: "login",
    },
  },
};

const stateMachine = {
  currentState: machineConfig.initialState,
  transition: function (action) {
    const nextState = machineConfig.transitions[this.currentState][action];
    if (nextState) {
      this.currentState = nextState;
      this.executeAction(action);
    }
  },
  executeAction: function (action) {
    const actions = {
      goToRegister: () => {
        // Remove event listeners from current page
        showRegisterPage();
      },
      goToLogin: () => {
        // Remove event listeners from current page

        showLoginPage();
      },
      goToLanding: () => {
        // Remove event listeners from current page

        showLandingPage();
      },
      goToLoggedIn: () => {
        // Remove event listeners from current page

        showFriendsPage();
      },
    //   goToLoggedOut: () => {
    //     // Remove event listeners from current page
    //     showLoggedOutPage();
    //   },
    //   // Define other actions here
    };

    const actionFunction = actions[action];
    if (actionFunction) {
      actionFunction();
    }
  },
};

export default stateMachine;