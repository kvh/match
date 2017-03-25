import datetime
import re

from dateutil import parser
import phonenumbers

from .utils import memoize
from .similarity import DiceCoefficientSimilarity


class DataType(object):
    super_types = []

    def __init__(self, **kwargs):
        pass

    def score_similarity(self, s1, s2):
        return -1

    def score_type_match(self, s):
        return -1

    def parse(self, s, to_object=False):
        obj = self.parse_to_object(s)
        if obj is None:
            return None
        if to_object:
            return obj
        return self.to_string(obj)

    def to_string(self, obj):
        return str(obj)


class StringDataType(DataType):

    default_similarity_measure = DiceCoefficientSimilarity(grams=3)

    def __init__(self, **kwargs):
        self.similarity_measure = kwargs.get('similarity_measure',
                                             self.default_similarity_measure)

    def score_similarity(self, s1, s2):
        return self.similarity_measure.similarity(s1, s2)

    def score_type_match(self, s):
        return 0

# https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup
# class FullNameType(StringDataType):
#     super_types = [StringDataType]


# Address
# https://github.com/openvenues/libpostal, https://github.com/openvenues/pypostal


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


"""
Phone
"""

class PhoneNumberType(StringDataType):
    super_types = [StringDataType]

    # TODO: locale support
    default_region = "US"

    def to_string(self, obj):
        return phonenumbers.format_number(obj,
                                          phonenumbers.PhoneNumberFormat.E164)

    def parse_to_object(self, number):
        """Returns None if not a valid phone number"""
        if not number:
            return None
        if isinstance(number, int):
            number = str(number)
        try:
            parsed_number = phonenumbers.parse(number, self.default_region)
            if not phonenumbers.is_valid_number(parsed_number):
                return None
            return parsed_number
        except phonenumbers.NumberParseException:
            return None

    def score_type_match(self, s):
        return int(self.parse(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.parse(s1) == self.parse(s2))


"""
Email
"""

email_regex = re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')

class EmailType(StringDataType):
    super_types = [StringDataType]

    def parse_to_object(self, address):
        """Returns None if not a valid email"""
        if not address:
            return None
        # Emails are case insensitive (in practice)
        address = address.lower()
        try:
            local, host = address.split('@')
        except:
            return None
        local = local.split('+')[0]  # Most providers ignore after '+'
        # Gmail ignores dots
        if host == 'gmail.com':
            local = local.replace('.', '')
        return local + '@' + host

    def score_type_match(self, s):
        return int(email_regex.match(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.parse(s1) == self.parse(s2))


"""
DateTime
"""

def to_datetime(s):
    """s can be epoch seconds, ms, or date string"""
    try:
        secs = int(s)
    except ValueError:
        return parser.parse(s)
    if secs < 1000000000000:
        return datetime.datetime.fromtimestamp(secs)
    return datetime.datetime.fromtimestamp(secs / 1000)


class DateTimeType(StringDataType):
    super_types = [StringDataType]

    def to_string(self, obj):
        return obj.isoformat()

    def parse_to_object(self, s):
        return to_datetime(s)

    # def score_type_match(self, s):
        # return int(email_regex.match(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.parse(s1) == self.parse(s2))


datatype_lookup = {
    # Generic
    'string': StringDataType,

    # Entities
    'phonenumber': PhoneNumberType,
    # 'fullname': FullNameType,
    'datetime': DateTimeType,
}
ALL_TYPES = list(datatype_lookup.values())
DEFAULT_DATATYPE = StringDataType

def get_datatype(dtype_ish):
    if isinstance(dtype_ish, DataType):
        return dtype_ish
    if issubclass(dtype_ish, DataType):
        return dtype_ish()
    return datatype_lookup[dtype_ish]()
