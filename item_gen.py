"""Generate a number of random strings to use as items for the shuffler. Used mainly for development
and testing purposes."""

import random
import sys
import os


_DIGITS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

def _str(length: int) -> str:
    """Generate a random string with `length`.

    :param length: The desired length of the string.
    :type length: int
    :return: A random string of `length`.
    :rtype: str
    """

    return ''.join(str(random.choice(_DIGITS)) for _ in range(length))

def random_strs(num: int, length: int) -> list[str]:
    """Return a list of random strings.

    :param num: The desired number of strings.
    :type num: int
    :param length: The desired string length.
    :type length: int
    :return: A list of random strings.
    :rtype: list[str]
    """

    return [_str(length) for _ in range(num)]

if __name__ == '__main__':
    STRS = os.linesep.join(random_strs(num=int(sys.argv[1]), length=int(sys.argv[2])))
    with open('items.txt', 'wt', encoding='utf-8') as file:
        file.write(STRS)
