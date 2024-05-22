from rest_framework.throttling import UserRateThrottle


class CustomThrottle(UserRateThrottle):
    rate = '10/minute'