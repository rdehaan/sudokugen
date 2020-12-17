"""
Module with functionality to generate puzzle instances
"""

from copy import deepcopy
from typing import List, Optional
import clingo

from .instances import Instance
from .encodings import generate_basic

def generate_puzzle(
        instance: Instance,
        constraints: List[str],
        timeout: Optional[int] = None,
        verbose: Optional[bool] = None
    ) -> Optional[Instance]:
    """
    Takes a Sudoku instance, and generates a solution and puzzle if possible.
    """

    new_instance = deepcopy(instance)

    # Put together the basic encoding with any additional constraints given
    asp_code = generate_basic(new_instance)
    asp_code += "".join(constraints)

    ### FOR DEBUGGING:
    # with open("encoding.lp", "w") as file:
    #     file.write(asp_code)

    # Call the ASP solver on the encoding,
    # and let the instance deal with answer sets
    if verbose:
        print("Grounding..")
    control = clingo.Control()
    control.add("base", [], asp_code)
    control.ground([("base", [])])

    control.configuration.solve.opt_mode = "optN" # pylint: disable=no-member
    control.configuration.solve.models = 1 # pylint: disable=no-member

    if verbose:
        if not timeout:
            print("Solving..")
        else:
            print("Solving (with timeout {}s)..".format(timeout))

    handle = control.solve(on_model=new_instance.extract_from_answer_set,
                           async_=True)
    if timeout:
        handle.wait(timeout)
    else:
        handle.wait()

    if new_instance.puzzle: # pylint: disable=R1705
        return new_instance
    else:
        return None
