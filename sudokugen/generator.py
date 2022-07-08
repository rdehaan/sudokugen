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
        verbose: Optional[bool] = None,
        cl_arguments: Optional[List[str]] = None,
        custom_encoding: Optional[str] = None
    ) -> Optional[Instance]:
    """
    Takes a Sudoku instance, and generates a solution and puzzle if possible.
    """

    new_instance = deepcopy(instance)

    # Put together the basic encoding with any additional constraints given
    asp_code = generate_basic(new_instance)
    asp_code += "".join(constraints)

    # Add any custom encoding that is present
    if custom_encoding:
        asp_code += custom_encoding

    ### FOR DEBUGGING:
    # with open("encoding.lp", "w", encoding="utf-8") as file:
    #     file.write(asp_code)

    # Call the ASP solver on the encoding,
    # and let the instance deal with answer sets
    if verbose:
        print("Grounding..")
    control = clingo.Control(arguments=cl_arguments)
    control.add("base", [], asp_code)
    control.ground([("base", [])])

    control.configuration.solve.opt_mode = "optN" # pylint: disable=no-member
    control.configuration.solve.models = 1 # pylint: disable=no-member

    if verbose:
        if not timeout:
            print("Solving..")
        else:
            print(f"Solving (with timeout {timeout}s)..")

    handle = control.solve(on_model=new_instance.extract_from_answer_set,
                           async_=True)
    if timeout:
        handle.wait(timeout)
    else:
        handle.wait()

    if verbose:
        # pylint: disable=E1136
        try:
            total_time = control.statistics['summary']['times']['total']
            print(f"Total time: {total_time:.2f}s")
            solving_time = control.statistics['summary']['times']['solve']
            print(f"Solving took: {solving_time:.2f}s")
        except RuntimeError:
            pass

    if new_instance.puzzle: # pylint: disable=R1705
        return new_instance
    else:
        return None
