import { handleLocation } from "./handleLocation.js";

export const route = (event) => {
    event = event || window.event;
    if (event.preventDefault){
        event.preventDefault();
    };
    const destination = event.target && event.target.href ?  event.target.href : event;
    window.history.pushState({}, "", destination);
    handleLocation();
}

window.route = route;
