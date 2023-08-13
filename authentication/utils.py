import random
from django.core.cache import cache
from config.envs import STACK


def generate_otp(length: int = 6) -> int:
    return random.randint(10 ** (length - 1), (10**length) - 1)


def create_auth_otp(key: str, otp_length: int, timeout: int = 300) -> tuple[int, int]:
    """Generates and stores an OTP for authentication.

    Args:
        key (str): The key used to store the OTP in the cache.
        timeout (int, optional): The timeout value for the OTP in seconds. Defaults to 300.

    Returns:
        tuple[int, int]: A tuple containing the generated OTP and the timeout value.
    """
    otp = int("".join([str(i) for i in range(1, otp_length + 1)])) if STACK == "development" else generate_otp(otp_length)

    cache.set(key, otp, timeout)
    return otp, timeout
