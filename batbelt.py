#!/usr/bin/python
# -*-coding:Utf-8 -*

"""
Useful functions for miscellanous tasks
"""

import re
import unidecode
import datetime
from dateutil.parser import parse
from dateutil import relativedelta
import numpy as np
from typing import List, Set, Tuple, Optional
import _io


def sizeof(nbr: float, unit: str = "o", rounded: int = 1) -> str:

    """sizeof

    Args:
        nbr (float): number of bytes
        unit (str): what unit to use. o for octet, iB for binary bytes
        rounded (int): nbr of decimals

    Returns:
        str: a formatted string with the proper unit

    http://www.fevrierdorian.com/blog/post/2011/06/26/Taille-d-un-fichier-humainement-comprehensible-en-Python
    """

    if unit == "o":

        if nbr < 1000.0:
            return "{0} {1}".format(round(nbr, rounded), "octets")

        for x in ["ko", "Mo", "Go", "To"]:
            if nbr < 1000.0:
                return "{0} {1}".format(round(nbr, rounded), x)
            else:
                nbr /= 1000.0

    elif unit == "iB":

        if nbr < 1024.0:
            return "{0} {1}".format(round(nbr, rounded), "bytes")

        for x in ["KiB", "MiB", "GiB", "TiB"]:
            if nbr < 1024.0:
                return "{0} {1}".format(round(nbr, rounded), x)
            else:
                nbr /= 1024.0


def simple_char(entry: str) -> str:

    """simple_char

    Args:
        entry (str): string to be simplified

    Returns:
        str: the simplified string, lower case and without accents

    http://www.siteduzero.com/forum-83-810635-p1-sqlite-recherche-avec-like-insensible-a-la-casse.html#r7767300
    """

    # Nouvelle fct de renommage, qui prend aussi les chiffres
    # http://stackoverflow.com/questions/5574042/string-slugification-in-python
    entry = unidecode.unidecode(entry).lower()
    return re.sub(r"\W+", " ", entry)


def recent(date: str, days: int = 1) -> bool:

    """recent

    Args:
        date (str): date formatted as a string
        days (int): numbers of days to compare to date

    Returns:
        bool: if date is older than now + days, return False. Else return True
    """

    now = datetime.datetime.now()
    date = parse(date)

    if now - relativedelta.relativedelta(days=+days) < date:
        return True
    else:
        return False


def strByteToOctet(size: str) -> Tuple[str, int]:

    """strByteToOctet

    Args:
        size (str): a size in binary bytes. ex: 300 MiB

    Returns:
        Tuple[str, int]: the size in octet, human readable, and the size in octet
    """

    nbr, unit = size.split(" ")
    nbr = float(nbr)

    if unit == "MiB":
        nbr *= 2 ** 20
    elif unit == "GiB":
        nbr *= 2 ** 30

    nbr_octets = nbr

    for x in ["o", "Ko", "Mo", "Go", "To"]:
        if nbr < 1000.0:
            return "{0} {1}".format(round(nbr, 1), x), int(round(nbr_octets, 0))
        nbr /= 1000.0


def frange(start: float, end: Optional[float] = None, inc: float = 1.0) -> List[float]:

    """frange
    A range function, that accepts float increments
    if end is not provided, use start as the end

    Args:
        start (float): start of the list
        end (Optional[float]): end of the range
        inc (float): increment. Default to 0.1

    Returns:
        List[float]: list of the floats incremented
    """

    if end is None:
        end = start + 0.0
        start = 0.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L


def red_chisq(
    ydata: np.array, ymod: np.array, deg: int, sd: np.array = None
) -> np.array:

    """
    http://astropython.blogspot.fr/2012/02/computing-chi-squared-and-reduced-chi.html
    Returns the reduced Chi² of a data set.
    ydata is the y observed values
    ymod is the y model values
    deg is the number of parameters
    sd is the standard deviation
    """

    if sd is None:
        chisq: np.array = np.sum((ydata - ymod) ** 2)
    else:
        chisq: np.array = np.sum(((ydata - ymod) / sd) ** 2)

    nu: int = len(ydata) - 1 - deg

    return chisq / nu


def droite(x, a, b):

    y = a * x + b

    return y


def strip_tags(input_str: str) -> str:

    """strip_tags

    Args:
        input_str (str): input string, with html tags

    Returns:
        str: stripped string, no more html tags
    """

    return re.sub("<[^>]*>", "", input_str)


def remove_dup_order(seq: List[str]) -> List[str]:

    """remove_dup_order

    Args:
        seq (List[str]): A list of elements (str) to un-duplicate

    Returns:
        List[str]: list of elements without duplicates
    """

    seen: Set[str] = set()

    # Update append a sequence to a set. If an element of the sequence is duplicate,
    # it will be added only once to the set
    seen.update(seq)

    return list(seen)


def fread(fid: _io.TextIOWrapper, nelements: int, dtype: str) -> np.array:

    """fread
    Equivalent for Matlab fread function

    Args:
        fid (_io.TextIOWrapper): file, opened before
        nelements (int): number of elements to read
        dtype (str): type of the element to read

    Returns:
        np.array: elements read
    """

    if dtype is np.str:
        dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
    else:
        dt = dtype

    data_array = np.fromfile(fid, dt, nelements)
    data_array.shape = (nelements, 1)

    return data_array


if __name__ == "__main__":
    # print(strByteToOctet("300 MiB"))
    # print(frange(10, inc=0.5))
    pass
