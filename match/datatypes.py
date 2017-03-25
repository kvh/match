import datetime
import re

from dateutil import parser
import phonenumbers

from .utils import memoize


class DataType(object):
    super_types = []

    def score_similarity(self, s1, s2):
        return -1

    def score_type_match(self, s):
        return -1


class StringDataType(DataType):

    def score_similarity(self, s1, s2):
        return int(s1 == s2)

    def score_type_match(self, s):
        return 0

class FullNameType(StringDataType):
    super_types = [StringDataType]


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

    def normalize(self, number):
        """Returns None if not a valid phone number"""
        if not number:
            return None
        if isinstance(number, int):
            number = str(number)
        try:
            parsed_number = phonenumbers.parse(number, self.default_region)
            if not phonenumbers.is_valid_number(parsed_number):
                return None
            return phonenumbers.format_number(parsed_number,
                                              phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            return None

    def score_type_match(self, s):
        return int(self.normalize(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.normalize(s1) == self.normalize(s2))


"""
Email
"""

email_regex = re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')

class EmailType(StringDataType):
    super_types = [StringDataType]

    def normalize(self, address):
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
        return int(self.normalize(s1) == self.normalize(s2))


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

    def normalize(self, s):
        dt = to_datetime(s)
        if dt:
            return dt.isoformat()
        return None

    # def score_type_match(self, s):
        # return int(email_regex.match(s) is not None)

    def score_similarity(self, s1, s2):
        return int(self.normalize(s1) == self.normalize(s2))


datatype_lookup = {
    # Generic
    'string': StringDataType,

    # Entities
    'phone_number': PhoneNumberType,
    'full_name': FullNameType,
    'datetime': DateTimeType,
}
ALL_TYPES = list(datatype_lookup.values())
DEFAULT_DATATYPE = StringDataType