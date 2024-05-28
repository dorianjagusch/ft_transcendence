const setNavbar = () => {
	if (localStorage.getItem('isLoggedIn') === 'false') {
		return;
	}
	const navPartitions = document.querySelectorAll('.nav-partition');
	navPartitions.forEach((partition) => {
		const visibility = partition.getAttribute('data-visible');
		partition.setAttribute('data-visible', visibility === 'true' ? 'false' : 'true');
		document.querySelector('#user').innerHTML = localStorage.getItem('username');
	});
};

export default setNavbar;
