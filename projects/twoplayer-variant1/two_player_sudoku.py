"""Functionality for creating two-player sudoku's."""

import os
import sys
import subprocess
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )
    )
)

from sudokugen import instances, generate_puzzle, encodings, \
    masks # pylint: disable=E0401,C0413,unused-import


def construct_basic_interface_sudoku_from_dict(
        input_dict
    ):
    """
    Takes a dictionary that specifies a basic interface sudoku and creates a
    BasicInterfaceSudoku instance from it.
    """

    puzzle=input_dict["puzzle"]
    input_cell=input_dict["input_cell"]
    input_cell_solution=input_dict["input_cell_solution"]
    input_decoy_value=input_dict["input_decoy_value"]
    output_cell=input_dict["output_cell"]
    output_cell_solution=input_dict["output_cell_solution"]
    output_decoy_value=input_dict["output_decoy_value"]

    instance = instances.BasicInterfaceSudoku(9)
    constraints = [
        encodings.use_mask(
            instance,
            puzzle
        ),
        #
        encodings.select_input_cell(),
        encodings.fix_location_of_input_cell(
            instance,
            input_cell[0],
            input_cell[1]
        ),
        encodings.fix_solution_at_input_cell(input_cell_solution),
        encodings.fix_input_decoy_value(input_decoy_value),
        #
        encodings.select_output_cell(),
        encodings.fix_location_of_output_cell(
            instance,
            output_cell[0],
            output_cell[1]
        ),
        encodings.fix_solution_at_output_cell(output_cell_solution),
        encodings.fix_output_decoy_value(output_decoy_value),
        #
    ]

    # Generate the puzzle
    found_solution = generate_puzzle(
        instance,
        constraints,
        timeout=30,
        verbose=False,
    )

    return found_solution


def instance_to_latex(instance):
    """
    Provides a LaTeX representation of a BasicInterfaceSudoku.
    """

    latex_repr = "\\begin{tikzpicture}[scale=0.6]\n"
    for (col, row) in instance.cells:
        latex_repr += f"\\node[anchor=center] at ({col-0.5},{9.5-row})"
        latex_repr += f" {{\\Large {instance.puzzle[(col, row)]}}};\n"
    latex_repr += """
        \\draw[ultra thick, scale=3] (0, 0) grid (3, 3);
        \\draw (0, 0) grid (9, 9);
        \\end{tikzpicture}%
    """
    return latex_repr


def make_pdf(
        filename,
        instance_dict,
        puzzle_id,
        directory=None,
        executable="pdflatex"
    ):
    """
    Creates a PDF of the puzzle (using LaTeX).
    """

    #
    if directory:
        cwd = os.path.abspath(directory)
    else:
        cwd = os.path.abspath('.')

    # Remove all aux files
    for ext in ["aux", "fdb_latexmk", "fls", "log"]:
        try:
            os.remove(os.path.join(cwd, f"{filename}.{ext}"))
        except FileNotFoundError:
            pass

    # Construct LaTeX source
    latex_source = ""
    with open("template.tex", 'r', encoding="utf-8") as file:
        latex_source = "".join(file.readlines())

    latex_source = latex_source.replace(
        "%%%[PUZZLE ID HERE]%%%",
        f"{puzzle_id}%"
    )

    for player in ["A", "B"]:
        for level in [1,2,3]:
            latex_source = latex_source.replace(
                f"%%%[PUZZLE HERE: PLAYER {player}, LEVEL {level}]%%%",
                f"{instance_to_latex(instance_dict[(player, level)])}%"
            )

    # Save LaTeX representation to [filename].tex
    filepath = os.path.join(cwd, f"{filename}.tex")
    with open(filepath, 'w', encoding="utf-8") as file:
        file.write(latex_source)
    # Call pdflatex
    with subprocess.Popen(
            [executable, f"{filename}.tex"],
            cwd=directory,
            stdout=subprocess.PIPE,
            universal_newlines=True
        ) as proc:
        proc.communicate()
    # Remove all aux files
    for ext in ["aux", "fdb_latexmk", "fls", "log"]:
        try:
            os.remove(os.path.join(cwd, f"{filename}.{ext}"))
        except FileNotFoundError:
            pass


def load_puzzle(puzzle):
    """
    Takes a 9x9 puzzle as a mask, and creates an instance from it.
    """

    instance = instances.RegularSudoku(9)
    constraints = [
        encodings.use_mask(
            instance,
            puzzle
        )
    ]

    # Generate the puzzle
    found_solution = generate_puzzle(
        instance,
        constraints,
        timeout=30,
        verbose=True,
        cl_arguments=["--parallel-mode=4"],
    )

    return found_solution


def print_puzzle_info(instance):
    """
    Prints some information about a given instance.
    """

    puzzle = instance.repr_short()
    try:
        input_cell = instance.input_cell
    except AttributeError:
        input_cell = None
    try:
        input_cell_solution = instance.solution[input_cell]
    except KeyError:
        input_cell_solution = None
    try:
        input_decoy_value = instance.input_decoy_value
    except AttributeError:
        input_decoy_value = None
    try:
        output_cell = instance.output_cell
    except AttributeError:
        output_cell = None
    try:
        output_cell_solution = instance.solution[output_cell]
    except KeyError:
        output_cell_solution = None
    try:
        output_decoy_value = instance.output_decoy_value
    except AttributeError:
        output_decoy_value = None

    print(instance.repr_pretty())
    print(f"puzzle = {puzzle}")
    print(f"num cells filled = {81-puzzle.count('0')}")
    print(f"output_cell = {output_cell} ", end="")
    print(f"with solution {output_cell_solution} ", end="")
    print(f"and decoy {output_decoy_value}")
    print(f"input_cell = {input_cell} ", end="")
    print(f"with solution {input_cell_solution} ", end="")
    print(f"and decoy {input_decoy_value}")
