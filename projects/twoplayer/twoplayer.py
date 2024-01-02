"""Functionality for creating two-player sudoku's."""

import json
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


def store_instance_in_db(
        instance,
        category,
        db_filename,
        additional_data=None,
    ):
    """
    TODO
    """
    try:
        with open(db_filename, "r", encoding="utf-8") as db_file:
            database = json.load(db_file)
    except FileNotFoundError:
        database = {}

    def highest_category_id(database, category):
        highest_id = 0
        if category in database:
            highest_id = max([
                instance_dict["id"]
                for instance_dict in database[category]
            ])
        return highest_id

    def instance_to_dict(instance):
        instance_dict = {}
        instance_dict["puzzle"] = instance.repr_short()
        instance_dict["input_cell"] = instance.input_cell
        instance_dict["input_cell_solution"] = \
            instance.solution[instance.input_cell]
        instance_dict["input_decoy_value"] = \
            instance.input_decoy_value
        instance_dict["output_cell"] = instance.output_cell
        instance_dict["output_cell_solution"] = \
            instance.solution[instance.output_cell]
        instance_dict["output_decoy_value"] = \
            instance.output_decoy_value
        return instance_dict

    def add_to_db(database, category, instance_dict):
        if category not in database:
            database[category] = []
        database[category].append(instance_dict)

    highest_id = highest_category_id(database, category)
    instance_dict = instance_to_dict(instance)
    instance_dict["id"] = highest_id + 1
    if additional_data:
        for key in additional_data:
            instance_dict[key] = additional_data[key]
    add_to_db(database, category, instance_dict)

    with open(db_filename, "w", encoding="utf-8") as db_file:
        json.dump(database, db_file, indent=4)


def load_db(
        db_filename,
    ):
    """
    TODO
    """
    try:
        with open(db_filename, "r", encoding="utf-8") as db_file:
            database = json.load(db_file)
    except FileNotFoundError:
        database = {}
    return database


def select_instance_dict_from_db(
        database,
        category,
        puzzle_id,
    ):
    """
    TODO
    """
    return [
        instance_dict
        for instance_dict in database[category]
        if instance_dict["id"] == puzzle_id
    ][0]


def construct_instance_from_dict(
        instance_dict
    ):
    """
    Takes a dictionary that specifies a basic interface sudoku and creates a
    BasicInterfaceSudoku instance from it.
    """

    puzzle=instance_dict["puzzle"]
    input_cell=instance_dict["input_cell"]
    input_cell_solution=instance_dict["input_cell_solution"]
    input_decoy_value=instance_dict["input_decoy_value"]
    output_cell=instance_dict["output_cell"]
    output_cell_solution=instance_dict["output_cell_solution"]
    output_decoy_value=instance_dict["output_decoy_value"]

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
    solution = generate_puzzle(
        instance,
        constraints,
        timeout=30,
        verbose=False,
    )

    return solution


def instance_to_latex(
        instance,
        input_color="red",
        input_pattern="north west",
        output_color="blue",
        output_pattern="horizontal",
    ):
    """
    Provides a LaTeX representation of a BasicInterfaceSudoku.
    """

    pattern_dict = {
        "horizontal":
            "{Lines[distance=1.5pt,yshift=0.85pt]}",
        "north west":
            "north west lines"
    }
    color_dict = {
        "blue": "NavyBlue!60",
        "red": "BrickRed!40",
    }

    input_pattern_str = "crosshatch"
    try:
        input_pattern_str = pattern_dict[input_pattern]
    except KeyError:
        pass
    input_color_str = "yellow"
    try:
        input_color_str = color_dict[input_color]
    except KeyError:
        pass
    output_pattern_str = "crosshatch"
    try:
        output_pattern_str = pattern_dict[output_pattern]
    except KeyError:
        pass
    output_color_str = "yellow"
    try:
        output_color_str = color_dict[output_color]
    except KeyError:
        pass

    latex_repr = "\\begin{tikzpicture}[scale=0.6]\n"
    for (col, row) in instance.cells:
        coloring_str = ""
        if (col, row) == instance.input_cell:
            coloring_str = ", minimum width=17pt, minimum height=17pt,"
            coloring_str += f" pattern={input_pattern_str},"
            coloring_str += f" pattern color={input_color_str}"
        if (col, row) == instance.output_cell:
            coloring_str = ", minimum width=17pt, minimum height=17pt,"
            coloring_str += f" pattern={output_pattern_str},"
            coloring_str += f" pattern color={output_color_str}"
        latex_repr += f"\\node[anchor=center{coloring_str}]"
        latex_repr += f" at ({col-0.5},{9.5-row})"
        cell_no = instance.puzzle[(col, row)]
        if cell_no != 0:
            latex_repr += f" {{\\Large {cell_no}}};\n"
        else:
            latex_repr += " {};\n"
    latex_repr += """
        \\draw[ultra thick, scale=3] (0, 0) grid (3, 3);
        \\draw (0, 0) grid (9, 9);
        \\end{tikzpicture}%
    """
    latex_repr += f"""
        % short form: {instance.repr_short()}
    """
    return latex_repr


def log(
        logstr,
        directory="output",
        logfile="output.log",
    ):
    """
    TODO
    """

    #
    if directory:
        cwd = os.path.abspath(directory)
    else:
        cwd = os.path.abspath('.')

    with open(os.path.join(cwd, logfile), 'a+', encoding="utf-8") as file:
        file.write(logstr)

def make_pdf(
        filename,
        instance_dict,
        meta_info,
        puzzle_set_id,
        two_page=True,
        directory="output",
        executable="pdflatex",
    ):
    """
    Creates a PDF of the puzzle (using LaTeX).
    """
    # pylint disable=too-many-arguments,too-many-locals

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
    if two_page:
        backside_source = ""
        with open("template-backside.tex", 'r', encoding="utf-8") as file:
            backside_source = "".join(file.readlines())

    latex_source = ""
    with open("template.tex", 'r', encoding="utf-8") as file:
        latex_source = "".join(file.readlines())

    for player in ["A", "B"]:
        latex_source = latex_source.replace(
            f"%%%[PUZZLE SET ID HERE: PLAYER {player}]%%%",
            f"{puzzle_set_id}-{player}%"
        )

    for player in ["A", "B"]:
        for puzzle_no in [1, 2, 3]:
            instance_str = instance_to_latex(
                instance_dict[(player, puzzle_no)],
                input_color=meta_info["deco"][player]["input color"],
                input_pattern=meta_info["deco"][player]["input pattern"],
                output_color=meta_info["deco"][player]["output color"],
                output_pattern=meta_info["deco"][player]["output pattern"],
            )
            latex_source = latex_source.replace(
                f"%%%[PUZZLE HERE: PLAYER {player}, NUMBER {puzzle_no}]%%%",
                f"{instance_str}%"
            )
            level = meta_info["level"][(player, puzzle_no)]
            level_str = f"\\textbf{{Level {level}}} "
            level_substr = "\\ ".join(["\\faGear"]*level)
            level_str += f"\\hfill {{{level_substr}}}"
            latex_source = latex_source.replace(
                f"%%%[LEVEL DESCRIPTION HERE: PLAYER {player}" + \
                f", NUMBER {puzzle_no}]%%%",
                f"{level_str}%"
            )

    if "subtitle" in meta_info:
        latex_source = latex_source.replace(
            "%%%[SUBTITLE HERE]%%%",
            meta_info["subtitle"]
        )

    if two_page:
        latex_source = latex_source.replace(
            "%%%[BACKSIDE HERE]%%%",
            backside_source
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
    solution = generate_puzzle(
        instance,
        constraints,
        timeout=30,
        verbose=True,
        cl_arguments=["--parallel-mode=4"],
    )

    return solution


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
