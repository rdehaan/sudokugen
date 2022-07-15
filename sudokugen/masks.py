"""
Module with different masks for Sudoku puzzles
"""

import re
import random
from typing import List, Tuple

from .instances import SquareSudoku

mask_library = {

    "pretty1":
        "*00*0*00*" + \
        "0*00*00*0" + \
        "00*000*00" + \
        "*00*0*00*" + \
        "0*00*00*0" + \
        "*00*0*00*" + \
        "00*000*00" + \
        "0*00*00*0" + \
        "*00*0*00*",

    "pretty2":
        "**00*00**" + \
        "*00*0*00*" + \
        "00*000*00" + \
        "0*00*00*0" + \
        "*00***00*" + \
        "0*00*00*0" + \
        "00*000*00" + \
        "*00*0*00*" + \
        "**00*00**",

    "18clue_rotational_1":
        "00*00000*" + \
        "000*000**" + \
        "00*0*0000" + \
        "00000*000" + \
        "00*000*00" + \
        "000*00000" + \
        "0000*0*00" + \
        "**000*000" + \
        "*00000*00",
}

def generate_uniformly(
        instance: SquareSudoku,
        filler: str
    ) -> str:
    """
    Generates a mask from an instance, by setting all elements in the mask to
    filler.
    """

    return filler*(instance.size**2)

def random_replacement(
        mask: str,
        regex_from: str,
        str_to: str,
        num_to_replace: int
    ):
    """
    Randomly replaces num_to_replace of the occurrences of regex_from in mask
    by str_to.
    """

    if len(re.findall(regex_from, mask)) <= num_to_replace:
        return re.sub(regex_from, str_to, mask)

    indices = [index.start() for index in re.finditer(regex_from, mask)]
    indices_to_replace = random.sample(indices, k=num_to_replace)
    new_mask = list(mask)
    for index in indices_to_replace:
        new_mask[index] = str_to
    new_mask = ''.join(new_mask)
    return new_mask

def generate_randomly(
        instance: SquareSudoku,
        filler: str,
        char_list: List[Tuple[int, str]],
    ) -> str:
    """
    Generates a random mask, starting with all entries as given by the filler,
    and then randomly replacing the fillers as indicated by the list, where
    each tuple (num, char) indicates that num of the fillers should be replaced
    by char.
    """

    mask = generate_uniformly(instance, filler)
    for num, char in char_list:
        mask = random_replacement(mask, re.escape(filler), char, num)
    return mask
