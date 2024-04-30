import showLandingPage from "./pages/landingPage.js";
import showLoginPage from "./pages/loginPage.js";
import showRegisterPage from "./pages/registerPage.js";
import showFriendsPage from "./pages/friendsPage.js";
import showDashboardPage from "./pages/dashboardPage.js";
import { friendCard } from "./components/friendCard.js";
// import showProfilePage from "./pages/profilePage.js";

// const machineConfig = {
//   initialState: "landing",
//    states: {
//     // ... other states
//     register: {
//       states: {
//         idle: {},
//         processing: {},
//         error: {},
//       },
//       transitions: {
//         goToLanding: "landing",
//         goToLogin: "login",
//         fetchData: "processing",
//         onSuccess: "loggedIn",
//         onFailure: "error",
//       },
//     },
//     login: {
//       states: {
//         idle: {},
//         processing: {},
//         error: {},
//       },
//       transitions: {
//         goToLanding: "landing",
//         goToRegister: "register",
//         fetchData: "processing",
//         onSuccess: "dashboard",
//         onFailure: "error",
//       },
//     },
//     // ... other states
//   },
// }

const machineConfig = {
  initialState: "landing",
  states: {
    landing: {},
    register: {},
    login: {},
    leaderboard: {},
    dashboard: {},
    friends: {},
    play: {},
    settings: {},
    logginIn: {},
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
      goToLoggedIn: "loggedIn",
    },
    login: {
      goToLanding: "landing",
      goToRegister: "register",
      goToDashboard: "dashboard",
      goToFriends: "friends",
    },
    dashboard: {
      goToFriends: "friends",
    },
    friends: {
      goToDashboard: "dashboard",
    },
    loggedOut: {
      goToLogin: "login",
    },
  },
};

const stateMachine = {
  currentState: machineConfig.initialState,
  context: {
	username: ''
	},
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
      goToDashboard: () => {
        // Remove event listeners from current page

        showDashboardPage();
      },
      goToFriends: () => {
        // Remove event listeners from current page

		const navSections = document.querySelectorAll('.nav-partition');
		navSections.forEach(section => {
		  section.getAttribute('data-visible') === 'false' ? section.setAttribute('data-visible', 'true') : section.setAttribute('data-visible', 'false');
		});
		const userName = document.querySelector('#user');
		userName.textContent = this.context.username;
        showFriendsPage();
      },
      goToLoggedIn: () => {
        // Remove event listeners from current page
          const main = document.querySelector('main');
          main.innerHTML = '';


          const user = friendCard({username: 'User', status: 'online', img: 'https://via.placeholder.com/150'});

          // stateMachine.transition('goToDashboard');
        },
    };

    const actionFunction = actions[action];
    if (actionFunction) {
      actionFunction();
    }
  },
};


// const stateMachine = {
//   currentState: machineConfig.initialState,
//   subState: "idle", // Add this line to track the sub-state
//   transition: function (action) {
//     const nextState = machineConfig.transitions[this.currentState][action];
//     if (nextState) {
//       this.currentState = nextState;
//       this.subState = "idle"; // Reset the sub-state to 'idle' when transitioning to a new state
//       this.executeAction(action);
//     } else {
//       const nextSubState =
//         machineConfig.states[this.currentState].transitions[action];
//       if (nextSubState) {
//         this.subState = nextSubState; // Update the sub-state if the action is a sub-state transition
//         this.executeAction(action);
//       }
//     }
//   },
//   executeAction: function (action) {
//     const actions = {
//       // ... other actions
//       fetchData: () => {
//         // Add your code to fetch data here
//         // Once the data is fetched, call `this.transition('onSuccess')` or `this.transition('onFailure')` based on the result
//       },
//       onSuccess: () => {
//         // Add your code to handle successful data fetch here
//       },
//       onFailure: () => {
//         // Add your code to handle failed data fetch here
//       },
//       // ... other actions
//     };
//     // Execute the action if it exists
//     if (actions[action]) {
//       actions[action]();
//     }
//   },
// };

export default stateMachine;