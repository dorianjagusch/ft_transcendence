const arrayToElementsList = (array, className, callback) => {
	if (!array){
		return;
	}
	if (array.length === 0) {
		const noData = document.createElement(p)
		return noData.textContent = 'No elements to display';
	}

	const list = document.createElement('ul');
	list.classList.add(className);
	array.forEach((element) => {
		const listItem = callback(element);
		list.appendChild(listItem);
	});

	return list;
};

export default arrayToElementsList;