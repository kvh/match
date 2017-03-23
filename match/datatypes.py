import inspect
from .utils import memoize


class DataType(object):
    super_types = []

    def score_match(self, s1, s2):
        return 0

    def score_type(self, s):
        return 0

class StringDataType(DataType):

    def score(self, s1, s2):
        return int(s1 == s2)

class PhoneNumberType(StringDataType):
    super_types = [StringDataType]

class FullNameType(StringDataType):
    super_types = [StringDataType]


datatype_lookup = {
    # Generic
    'string': StringDataType,

    # Personal
    'phone_number': PhoneNumberType,
    'full_name': FullNameType,
}
ALL_TYPES = list(datatype_lookup.values())
DEFAULT_DATATYPE = StringDataType


@memoize
def closest_common_type(t1, t2):
    if t1 == t2:
        return t1
    for t in t1.super_types:
        if t in t2.super_types:
            return t
    return None


def eligible_types(s):
    # TODO
    return ALL_TYPES