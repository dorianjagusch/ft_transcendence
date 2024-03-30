import { routes } from './Routes.js';

export const handleLocation = async () => {
    const path = window.location.pathname;
    const route = routes[path] || routes["404"];
    const html = await fetch(route).then(data => data.text());
    document.getElementById("content-container").innerHTML = html;
}

window.onpopstate = handleLocation;

