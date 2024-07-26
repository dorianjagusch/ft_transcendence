import backendURL from '../constants.js';7

const parseWStoMatchId = (wsURL) => {
	const regex = new RegExp(
		`^ws://${backendURL.location}pong\\/(\\w+)\\?token=`
	);
	const match = wsURL.match(regex);
	return match?.[1] ?? '';
};

export default parseWStoMatchId;
