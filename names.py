
from enum import Enum

class EnumNAT(Enum):
    def __str__(self):
        return self.value[1]

class Restrictiveness(EnumNAT):
    undetermined   = (-1, 'Undetermined')
    permissive     = ( 0, 'Permissive')
    ipRestricted   = ( 1, 'IP restricted')
    portRestricted = ( 2, 'Port restricted')

class Sensitivity(EnumNAT):
	undetermined  = (-1, 'Undetermined')
	insensitive   = ( 0, 'Insensitive')
	ipSensitive   = ( 1, 'IP sensitive')
	portSensitive = ( 2, 'Port sensitive')
