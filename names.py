
from enum import Enum

class Permissiveness(Enum):
    undetermined   = -1
    permissive     = 0
    ipRestricted   = 1
    portRestricted = 2

class Sensitivity(Enum):
	undetermined  = -1
	insensitive   = 0
	ipSensitive   = 1
	portSensitive = 2
