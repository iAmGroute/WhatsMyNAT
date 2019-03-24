
from enum import Enum

class NatType(Enum):
    undetermined   = -1
    noNat          = 0
    fullCone       = 1
    ipRestricted   = 2
    portRestricted = 3
    symmetric      = 4
