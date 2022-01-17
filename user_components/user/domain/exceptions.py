class UserExists(Exception):
    pass


class USER_DOES_NOT_EXIST(Exception):
    pass


class INVALID_EMAIL_PASSWORD(Exception):
    pass


class UsMISSING_PARAMSerExists(Exception):
    pass


class DATA_NOT_FOUND(Exception):
    pass


class USER_NOT_ACTIVE(Exception):
    pass


class PASSWORD_INCORRECT(Exception):
    pass


class PASSWORD_MISMATCHED(Exception):
    pass


class REDIS_CONNECTION_NOT_ESTABLISHED(Exception):
    pass


class OTP_NOT_FOUND(Exception):
    pass


class OTP_MISMATCHED(Exception):
    pass


class DuplicationSellerId(Exception):
    pass


class DuplicationSellerName(Exception):
    pass


class DuplicationPhone(Exception):
    pass


class DuplicationCompanyName(Exception):
    pass


class DuplicationCompanySymbol(Exception):
    pass


class DuplicationShareholderName(Exception):
    pass


class DuplicationCRNNumber(Exception):
    pass


class InvalidPhoneNumber(Exception):
    pass
