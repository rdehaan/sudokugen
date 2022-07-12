"""
Module with functionality to generate puzzles using ASP encodings
"""

import itertools
from typing import List

from .deduction import SolvingStrategy, basic_deduction
from ..instances import Instance, SquareSudoku, RectangleBlockSudoku


def generate_basic(instance: Instance) -> str:
    """
    Returns base encoding for generating a puzzle instance
    """

    asp_code = ""

    # Declare the cells
    for cell in instance.cells:
        asp_code += f"cell({instance.cell_encoding(cell)}).\n"

    # Declare the values
    for value in instance.values:
        asp_code += f"value({instance.value_encoding(value)}).\n"

    # Declare the (full) groups and their member cells
    for group_num, (group_type, group) in enumerate(instance.groups):
        asp_code += f"group({group_num}).\n"
        asp_code += f"group_type({group_num},{group_type}).\n"
        if len(group) == len(instance.values):
            asp_code += f"full_group({group_num}).\n"
        for cell in group:
            asp_code += \
                f"in_group({instance.cell_encoding(cell)},{group_num}).\n"

    # Declare predicate that captures when cells are different
    asp_code += """
        different_cells(C1,C2) :-
            cell(C1), cell(C2), C1 != C2.
    """

    # Declare predicate that captures when cells share a group
    asp_code += """
        share_group(C1,C2) :-
            group(G),
            cell(C1), in_group(C1,G),
            cell(C2), in_group(C2,G),
            different_cells(C1,C2).
    """

    # Declare predicate that captures when values are different
    asp_code += """
        different_values(V1,V2) :-
            value(V1), value(V2), V1 != V2.
    """

    # Define what a solution should look like
    asp_code += """
        1 { solution(C,V) : value(V) } 1 :- cell(C).
        :- share_group(C1,C2), solution(C1,V), solution(C2,V).
        { erase(C) } :- cell(C).
    """

    #
    asp_code += """
        different_cells_in_group_ordered(C1,C2,G) :-
            group(G), cell(C1), cell(C2),
            in_group(C1,G), in_group(C2,G), C1 < C2.
        value_in_pair(V1,V1,V2) :-
            value(V1), value(V2), V1 < V2.
        value_in_pair(V2,V1,V2) :-
            value(V1), value(V2), V1 < V2.
    """

    # Declare what to show
    asp_code += """
        #show solution/2.
        #show erase/1.
    """

    return asp_code


def unique_solution() -> str:
    """
    Returns the encoding that requires the puzzle to have a (semantically)
    unique solution
    """

    asp_code = """
        %%% Use saturation
        :- not w.
        choose(C,V) :- cell(C), value(V), w.

        %%% Choose at least one V for every cell X,Y
        choose(C,V) : value(V) :- cell(C).

        %%% Filter out choices that don't agree with non-erased cells
        w :-
            cell(C), solution(C,V1), not erase(C),
            choose(C,V2), different_values(V1,V2).

        %%% Filter out the choice that corresponds to the solution
        w :- choose(C,V) : solution(C,V).

        %%% Filter out choices that don't satisfy the constraints
        w :- choose(C1,V), choose(C2,V), cell(C1), cell(C2), value(V),
            share_group(C1,C2).
    """
    return asp_code


def maximize_num_filled_cells() -> str:
    """
    Returns the encoding that maximizes the number of non-empty cells in the
    puzzle
    """

    asp_code = """
        #minimize { 1,erase(C) : erase(C) }.
    """
    return asp_code


def minimize_num_filled_cells() -> str:
    """
    Returns the encoding that minimizes the number of non-empty cells in the
    puzzle
    """

    asp_code = """
        #maximize { 1,erase(C) : erase(C) }.
    """
    return asp_code


def constrain_num_filled_cells(
        instance: Instance,
        minimum: int,
        maximum: int
    ) -> str:
    """
    Returns the encoding that puts lower and upper bounds on the number of
    non-empty cells in the puzzle
    """
    minimum_erase = instance.num_cells - maximum
    maximum_erase = instance.num_cells - minimum
    if minimum == 0 and maximum == instance.num_cells: # pylint: disable=R1705
        return ""
    elif minimum_erase == 0: #
        return f"{{ erase(C) : erase(C) }} {maximum_erase}.\n"
    elif maximum_erase == instance.num_cells:
        return f"{minimum_erase} {{ erase(C) : erase(C) }}.\n"
    else:
        return f"{minimum_erase} {{ erase(C) : erase(C) }} {maximum_erase}.\n"


def deduction_constraint(
        instance: Instance,
        solving_strategies: List[SolvingStrategy]
    ) -> str:
    """
    Returns the encoding that requires that the puzzle (i) can or (ii) cannot
    be solved, using a given solving strategy, where the choice between (i) and
    (ii) is specified in the solving strategy
    """

    asp_code = ""
    all_rules = set([basic_deduction])

    for strategy_num, strategy in enumerate(solving_strategies):

        strategy_name = f"strategy({strategy_num})"

        asp_code += f"deduction_mode({strategy_name}).\n"

        asp_code += f":- not stable_state({strategy_name}).\n"

        all_rules.update(strategy.rules)

        for rule in strategy.rules:
            asp_code += f"use_technique({strategy_name},{rule.name}).\n"

        for groupnum, (groupname, _) in enumerate(instance.groups):
            if ((strategy.groups and groupname in strategy.groups)
                    or not strategy.groups):
                asp_code += f"active_group({strategy_name},{groupnum}).\n"

    for rule in all_rules:
        asp_code += rule.encoding

    return asp_code


def left_right_symmetry(
        instance: SquareSudoku
    ) -> str:
    """
    Returns the encoding that requires that the pattern of non-empty cells in
    the (square) puzzle instance is left-right symmetric
    """

    asp_code = ""
    for col in range(1, int(instance.size/2)+1):
        for row in range(1, instance.size+1):
            cell1 = (col,row)
            cell2 = (instance.size+1-col,row)
            asp_code += f"""
                erase({instance.cell_encoding(cell1)}) :-
                    erase({instance.cell_encoding(cell2)}).
                erase({instance.cell_encoding(cell2)}) :-
                    erase({instance.cell_encoding(cell1)}).
            """

    return asp_code


def top_bottom_symmetry(
        instance: SquareSudoku
    ) -> str:
    """
    Returns the encoding that requires that the pattern of non-empty cells in
    the (square) puzzle instance is top-bottom symmetric
    """

    asp_code = ""
    for col in range(1, instance.size+1):
        for row in range(1, int(instance.size/2)+1):
            cell1 = (col,row)
            cell2 = (col,instance.size+1-row)
            asp_code += f"""
                erase({instance.cell_encoding(cell1)}) :-
                    erase({instance.cell_encoding(cell2)}).
                erase({instance.cell_encoding(cell2)}) :-
                    erase({instance.cell_encoding(cell1)}).
            """

    return asp_code


def point_symmetry(
        instance: SquareSudoku
    ) -> str:
    """
    Returns the encoding that requires that the pattern of non-empty cells in
    the (square) puzzle instance is point symmetric
    """

    asp_code = ""
    for col in range(1, instance.size+1):
        for row in range(1, int(instance.size/2)+2):
            cell1 = (col,row)
            cell2 = (instance.size+1-col,instance.size+1-row)
            asp_code += f"""
                erase({instance.cell_encoding(cell1)}) :-
                    erase({instance.cell_encoding(cell2)}).
                erase({instance.cell_encoding(cell2)}) :-
                    erase({instance.cell_encoding(cell1)}).
            """

    return asp_code


def forbid_values(
        forbidden_values: List[int]
    ) -> str:
    """
    Returns the encoding that forbids the given values from appearing as
    non-empty cells in the puzzle
    """

    asp_code = ""

    for value in forbidden_values:
        asp_code += f"erase(C) :- cell(C), solution(C,{value}).\n"

    return asp_code


def fill_cell(
        instance: Instance,
        cell,
        value: int
    ) -> str:
    """
    Returns the encoding that states that a given value should appear in the
    puzzle in the given cell.
    """

    asp_code = f"""
        solution({instance.cell_encoding(cell)},{value}).
        :- erase({instance.cell_encoding(cell)}).
    """

    return asp_code


def open_cell(
        instance: Instance,
        cell
    ) -> str:
    """
    Returns the encoding that states that a given cell should be left open in
    the puzzle.
    """

    asp_code = f"erase({instance.cell_encoding(cell)}).\n"

    return asp_code


def sym_breaking_top_row(
        instance: SquareSudoku
    ) -> str:
    """
    Returns the symmetry breaking code that requires that the top row of the
    solution of the puzzle contains the values in order (i.e., 1, 2, 3, ...).
    """

    asp_code = ""
    row = 1
    for col in range(1, instance.size+1):
        cell = (col,row)
        asp_code += f"""
            :- not solution({instance.cell_encoding(cell)},{col}).
        """

    return asp_code


def sym_breaking_row_col_ordering(
        instance: RectangleBlockSudoku
    ) -> str:
    """
    Returns the symmetry breaking code that enforces an ordering in the number
    of non-empty cells in the puzzle in the different rows and columns.
    """
    # pylint: disable=W0212,R0914
    block_width = instance._block_width
    block_height = instance._block_height

    asp_code = ""

    def encoding_rows_ordered(row1, row2):
        return f"""
             :- {{ erase({instance.cell_encoding(('C',row1))})
                 : cell({instance.cell_encoding(('C',row1))}) ;
                 not erase({instance.cell_encoding(('C',row2))})
                 : cell({instance.cell_encoding(('C',row2))}) }}
                 > {instance.size}.
        """

    def encoding_cols_ordered(col1, col2):
        return f"""
            :- {{ erase({instance.cell_encoding((col1,'R'))})
                : cell({instance.cell_encoding((col1,'R'))}) ;
                not erase({instance.cell_encoding((col2,'R'))})
                : cell({instance.cell_encoding((col2,'R'))}) }}
                > {instance.size}.
        """

    # Rows inside blocks
    for row_basis in range(block_width):
        for row1_basis in range(1, block_width+1):
            for row2_basis in range(1, block_height-row1_basis+1):
                basis = row_basis * block_height
                row1 = basis + row1_basis
                row2 = basis + row1_basis + row2_basis
                asp_code += encoding_rows_ordered(row1, row2)

    # Corresponding rows between blocks
    row_basis = 0
    for row1_basis in range(block_width):
        for row2_basis in range(1, block_width-row1_basis):
            basis = row_basis
            row1 = basis + row1_basis * block_height + 1
            row2 = basis + (row1_basis + row2_basis) * block_height + 1
            asp_code += encoding_rows_ordered(row1, row2)

    # Cols inside blocks
    for col_basis in range(block_height):
        for col1_basis in range(1, block_height+1):
            for col2_basis in range(1, block_width-col1_basis+1):
                basis = col_basis * block_width
                col1 = basis + col1_basis
                col2 = basis + col1_basis + col2_basis
                asp_code += encoding_cols_ordered(col1, col2)

    # Corresponding cols between blocks
    col_basis = 0
    for col1_basis in range(block_height):
        for col2_basis in range(1, block_height-col1_basis):
            basis = col_basis
            col1 = basis + col1_basis * block_width + 1
            col2 = basis + (col1_basis + col2_basis) * block_width + 1
            asp_code += encoding_cols_ordered(col1, col2)

    return asp_code


def sym_breaking_left_column(
        instance: RectangleBlockSudoku
    ) -> str:
    """
    Returns the symmetry breaking code that enforces increasing values in the
    leftmost column, both inside blocks and between the top rows of different
    blocks.
    """
    # pylint: disable=W0212,R0914
    block_width = instance._block_width
    block_height = instance._block_height

    asp_code = ""

    # Rows inside blocks
    for row_basis in range(block_width):
        for row1_basis in range(1, block_width+1):
            for row2_basis in range(1, block_height-row1_basis+1):
                basis = row_basis * block_height
                row1 = basis + row1_basis
                row2 = basis + row1_basis + row2_basis
                cell1 = (1,row1)
                cell2 = (1,row2)
                asp_code += f"""
                    :- solution({instance.cell_encoding(cell1)},V1),
                        solution({instance.cell_encoding(cell2)},V2),
                        V2 < V1.
                """

    # Corresponding rows between blocks
    row_basis = 0
    for row1_basis in range(block_width):
        for row2_basis in range(1, block_width-row1_basis):
            basis = row_basis
            row1 = basis + row1_basis * block_height + 1
            row2 = basis + (row1_basis + row2_basis) * block_height + 1
            cell1 = (1,row1)
            cell2 = (1,row2)
            asp_code += f"""
                :- solution({instance.cell_encoding(cell1)},V1),
                    solution({instance.cell_encoding(cell2)},V2),
                    V2 < V1.
            """

    return asp_code


def sym_breaking_at_most_one_hidden() -> str:
    """
    Returns the symmetry breaking code that enforces that there may not be two
    values that do not appear at all in the puzzle (as for many sudoku types
    this can never lead to a unique solution).
    """

    asp_code = """
        value_appears(V) :-
            value(V), cell(C), solution(C,V), not erase(C).
        :- value(V1), value(V2), different_values(V1,V2),
            not value_appears(V1), not value_appears(V2).
    """
    return asp_code


def use_mask(
        instance: SquareSudoku,
        mask: str
    ) -> str:
    """
    Use a mask to generate the puzzle, which consists of a string of characters,
    one per cell, going left-to-right and (then) top-to-bottom, where a "0"
    indicates an empty cell, a positive integer indicates a non-empty cell with
    this value, a "*" indicates a non-empty cell with an arbitrary value,
    and a "?" indicates free choice for the cell.
    """

    asp_code = ""
    mask_pieces = [
        (j, i, mask[(i-1) * instance.size + j - 1])
        for (i, j) in itertools.product(range(1, instance.size+1), repeat=2)
    ]
    for (i, j, val) in mask_pieces:
        if val == "0":
            asp_code += f"""
                :- not erase({instance.cell_encoding((i,j))}).
            """
        elif val == "*":
            asp_code += f"""
                :- erase({instance.cell_encoding((i,j))}).
                certainly_not_erased({instance.cell_encoding((i,j))}).
            """
        else:
            try:
                val = int(val)
                asp_code += f"""
                    :- erase({instance.cell_encoding((i,j))}).
                    :- not solution({instance.cell_encoding((i,j))},{val}).
                    certainly_not_erased({instance.cell_encoding((i,j))}).
                """
            except ValueError:
                pass
    return asp_code
