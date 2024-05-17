const scrollContainer = (elements, callback, orientation = 'row', ...classNames) => {

	if (!elements) {
		return;
	}

	const outerScroller = document.createElement('section');
	outerScroller.classList.add('scroll-container');

	const innerScroller = document.createElement('ul');
	innerScroller.classList.add('snaps-inline',
		`${orientation}-scroll`,
		...classNames);

	elements.forEach((element) => {
		const currentCard = callback(element);
		currentCard.classList.add('scroll-element');
		innerScroller.appendChild(currentCard);
	});

	outerScroller.appendChild(innerScroller);

	return outerScroller;
};

export { scrollContainer };
