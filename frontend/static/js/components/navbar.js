const setNavbar = (isLoggedOut) => {
	const navPartitions = document.querySelectorAll('.nav-partition');
	navPartitions.forEach((partition) => {
		const isVisible = partition.classList.contains('logged-out')
			? isLoggedOut
			: !isLoggedOut;
		partition.setAttribute('data-visible', isVisible);
	});
	document.querySelector('#user').innerHTML = localStorage.getItem('username');
};

export default setNavbar;
