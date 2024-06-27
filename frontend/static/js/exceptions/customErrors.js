import UnauthorizedException from './UnauthorizedException.js';
import ConflictException from './ConflictException.js';

const customErrors = {
	unauthorized_401: UnauthorizedException,
	conflict_409: ConflictException,
};

export default customErrors;