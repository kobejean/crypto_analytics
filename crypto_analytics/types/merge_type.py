""" Contains merge type definitions """
from enum import Enum

class MergeType(Enum):
    INTERSECT = 'intersect'
    UNION = 'union'

    def to_merge_how(self):
        if self == MergeType.UNION:
            return 'outer'
        elif self == MergeType.INTERSECT:
            return 'inner'
        return None
