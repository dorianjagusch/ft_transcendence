from enum import Enum

class FriendShipStatus(Enum):
	NONE = 'none'
	FRIEND = 'friend'
	NOTFRIEND = 'not-friend'
	PENDINGSENT = 'pending-sent'
	PENDINGRECEIVED = 'pending-received'
