from rest_framework.exceptions import APIException


class ScraperException(APIException):
    status_code = 400

class ServiceUnavailableException(ScraperException):
    pass


class NoDataForGivenAddressException(ScraperException):
    pass


class BadInputDataException(ScraperException):
    pass


class AddressAlreadyCheckedException(ScraperException):
    pass
