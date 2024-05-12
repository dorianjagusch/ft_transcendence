from enum import Enum

class FriendShipStatus(Enum):
	NONE = 'None',
	REQUESTPENDING = 'RequestPending',
	WAITINGFORYOUACCEPTANCE = 'WaitingForYourAcceptance'
	ACCEPTED = 'Accepted'
