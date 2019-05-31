""" Contains merge type definitions """
from enum import Enum

class MergeType(Enum):
    """ An enum of merge types """
    INTERSECT = 'intersect'
    UNION = 'union'

    def to_merge_how(self):
        """ Converts merge type to a `how` parameter for using `pd.merge` """
        switch = {
            MergeType.UNION: 'outer',
            MergeType.INTERSECT: 'inner',
        }
        return switch[self]
