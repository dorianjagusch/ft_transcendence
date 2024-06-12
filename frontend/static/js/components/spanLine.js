const SpanLine = (text, id) => {
	const spanLine = document.createElement('p');
	spanLine.textContent = text + ': ';
	const span = document.createElement('span');
	span.id = id;
	spanLine.appendChild(span);
	return spanLine;
};

export default SpanLine;