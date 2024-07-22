const populateInnerScroller = (elements, innerScroller, callback) => {

	if (!callback){
		return;
	}
		elements.forEach((element) => {
			const currentCard = callback(element);
			currentCard.classList.add('scroll-element');
			innerScroller.appendChild(currentCard);
		});
	}

const scrollContainer = (elements, callback, orientation = 'row', ...classNames) => {

	if (!elements || !callback) {
		return;
	}

	const outerScroller = document.createElement('section');
	outerScroller.classList.add('scroll-container');

	const innerScroller = document.createElement('ul');
	innerScroller.classList.add('snaps-inline',
		`${orientation}-scroll`,
		...classNames);

	populateInnerScroller(elements, innerScroller, callback);

	outerScroller.appendChild(innerScroller);

	return outerScroller;
};

export { scrollContainer, populateInnerScroller };
