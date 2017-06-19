#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2016-2017 CEA
#
# This software is governed by the CeCILL license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty and the software's author, the holder of the
# economic rights, and the successive licensors have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading, using, modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean that it is complicated to manipulate, and that also
# therefore means that it is reserved for developers and experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and, more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""Generate codes to pseudonymize Stratify data.

The algorithm used here is certainly brain-dead. This is not reusable code
but is good enough for a one-shot run. I spent 10 minutes writing and it
took ~ 3 days to generate PSC1 codes for the Stratify project.

Notes
-----
.. Damerau–Levenshtein distance
   https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance

.. Lexicographic code
   https://en.wikipedia.org/wiki/Lexicographic_code

"""

from re import findall
from random import shuffle
from jellyfish import damerau_levenshtein_distance
from damm import encode


DIGITS = 5
MIN_DISTANCE = 3
PREFIXES = {
    '21': 600,
    '20': 400,
    '31': 600,
    '30': 400,
}


def code_generator(prefixes, digits, min_distance):
    """Generate distant enough numeric codes (Damerau-Levenshtein distance).

    The numeric codes are made of:
    - a prefix made from one of the `prefixes`
    - a main code made of `digits` digits
    - a Damm check digit as a suffix

    Parameters
    ----------
    prefix : dict
        Keys are the expected prefixes - strings made of digits.
        Values represent the expected number of codes for each prefix.

    digits : int
        Number of digits the main code is made of.

    min_distance : int
        Minimal Damerau-Levenshtein distance between generated strings.

    Returns
    -------
    dict
        Keys are the expected prefixes - strings made of digits.
        Values represent the egenerated codes for each prefix.

    """
    lexicode = set()
    result = {x: [] for x in prefixes.keys()}

    # avoid numbers starting with 0
    # for example for 5 digits, choose numbers between 9999 + 1 and 99999
    min_value = 0
    i = 1
    while i < digits:
        min_value = min_value * 10 + 9
        i += 1
    max_value = min_value * 10 + 9
    min_value += 1

    # avoid more than 2 repeated consecutive characters
    candidates = list(x for x in range(min_value, max_value + 1)
                      if not findall(r'((\w)\2{2,})', str(x)))

    shuffle(candidates)

    for i in candidates:
        i = str(i)
        for prefix, n in prefixes.items():
            if len(result[prefix]) < n:
                # prepend prefix, append Damm decimal check digit
                code = i + str(encode(prefix + i))
                # ignore prefix when calculating distance to previous codes
                if not lexicode or min(damerau_levenshtein_distance(code, l)
                                       for l in lexicode) >= min_distance:
                    lexicode.add(code)
                    result[prefix].append(code)
                    break  # from current inner loop over prefix

    return result


def main():
    result = code_generator(PREFIXES, DIGITS, MIN_DISTANCE)
    for prefix, codes in result.items():
        for code in codes:
            print(prefix + code)


if __name__ == '__main__':
    main()
