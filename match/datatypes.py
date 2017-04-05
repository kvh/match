import datetime
import re

from dateutil import parser
import phonenumbers

from .utils import memoize


class DataType(object):
    super_types = []
    SIMILARITY_MATCH_THRESHOLD = .95

    def __init__(self, **kwargs):
        pass

    def validate_and_clean(self, s):
        if not s:
            return None
        if not isinstance(s, str):
            s = str(s)
        return s.strip()

    def score_similarity(self, s1, s2):
        return -1

    def score_type_match(self, s):
        return -1

    def is_eligible(self, s):
        # First pass check. Purpose is to be much faster than parse
        return True

    def parse(self, s, to_object=False):
        s = self.validate_and_clean(s)
        if not s:
            return None
        if not self.is_eligible(s):
            return None
        obj = self.parse_to_object(s)
        if obj is None:
            return None
        if to_object:
            return obj
        return self.to_string(obj)

    def to_string(self, obj):
        return str(obj)

    def is_exact_match(self, s1, s2):
        if self.score_similarity(s1, s2) > self.SIMILARITY_MATCH_THRESHOLD:
            return True
        return False


class StringType(DataType):
    name = 'string'

    default_similarity_measure = 'jaro'

    def __init__(self, **kwargs):
        self.similarity_measure = kwargs.get('similarity_measure',
                                             self.default_similarity_measure)

    def score_similarity(self, s1, s2):
        return self.similarity_measure.similarity(s1, s2)

    def score_type_match(self, s):
        return 0


# https://github.com/carltonnorthern/nickname-and-diminutive-names-lookup
# class FullNameType(StringType):
#     super_types = [StringType]


# Address
# https://github.com/openvenues/libpostal, https://github.com/openvenues/pypostal


@memoize
def closest_common_type(t1, t2):
    t1 = get_datatype(t1)
    t2 = get_datatype(t2)
    if t1 == t2:
        return t1
    for t in t1.super_types:
        if t in t2.super_types:
            return t
    return None

def get_closest_common_type(s1, s2):
    score, s1_type = detect_type(s1)
    score, s2_type = detect_type(s2)
    dtype = closest_common_type(s1_type, s2_type)
    return dtype


def eligible_types(s):
    # TODO
    return ALL_TYPES


"""
Phone
"""

class PhoneNumberType(StringType):
    super_types = [StringType]
    name = 'phonenumber'

    # TODO: locale support
    default_region = "US"

    def is_eligible(self, s):
        return (len(s) > 6 and
                len(s) < 20)

    def to_string(self, obj):
        return phonenumbers.format_number(obj,
                                          phonenumbers.PhoneNumberFormat.E164)

    def parse_to_object(self, number):
        """Returns None if not a valid phone number"""
        if not number:
            return None
        number = number.strip()
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


class EmailType(StringType):
    super_types = [StringType]
    name = 'email'

    def is_eligible(self, s):
        return (len(s) > 4 and
                len(s) < 256 and
                '@' in s and
                '.' in s)

    def validate_and_clean(self, s):
        s = super(EmailType, self).validate_and_clean(s)
        # Emails are case insensitive (in practice)
        return s.lower()

    def parse_to_object(self, address):
        """Returns None if not a valid email"""

        # Is valid?
        if email_regex.match(address) is None:
            return None

        local, host = address.split('@')

        # Gmail ignores dots and after +
        if host == 'gmail.com':
            local = local.split('+')[0]
            local = local.replace('.', '')
        return local + '@' + host

    def score_type_match(self, s):
        return int(self.parse(s) is not None)

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
    if secs < 1000000000000000:
        return datetime.datetime.fromtimestamp(secs / 1000)
    return None


class DateTimeType(StringType):
    super_types = [StringType]
    name = 'datetime'

    def is_eligible(self, s):
        return (len(s) > 2 and
                len(s) < 48)

    def to_string(self, obj):
        return obj.isoformat()

    def parse_to_object(self, s):
        try:
            return to_datetime(s)
        except ValueError:
            return None

    def score_type_match(self, s):
        return int(self.parse(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.parse(s1) == self.parse(s2))


datatype_lookup = {
    # Generic
    'string': StringType,

    # Entities
    'phonenumber': PhoneNumberType,
    'email': EmailType,
    # 'fullname': FullNameType,
    'datetime': DateTimeType,
}
ALL_TYPES = list(datatype_lookup.keys())
DEFAULT_DATATYPE = 'string'


def get_datatype(dtype_ish, **kwargs):
    if isinstance(dtype_ish, DataType):
        return dtype_ish
    if isinstance(dtype_ish, type):
        if issubclass(dtype_ish, DataType):
            return dtype_ish(**kwargs)
    return datatype_lookup[dtype_ish](**kwargs)
