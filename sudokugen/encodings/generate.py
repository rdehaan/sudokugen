"""
Module with functionality to generate puzzles using ASP encodings
"""

from typing import List

from .deduction import SolvingStrategy, basic_deduction
from ..instances import Instance, SquareSudoku


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
    for groupnum, (_, group) in enumerate(instance.groups):
        asp_code += f"group({groupnum}).\n"
        if len(group) == len(instance.values):
            asp_code += f"full_group({groupnum}).\n"
        for cell in group:
            asp_code += \
                f"in_group({instance.cell_encoding(cell)},{groupnum}).\n"

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
            asp_code += """
                erase(cell({col1},{row})) :- erase(cell({col2},{row})).
                erase(cell({col2},{row})) :- erase(cell({col1},{row})).
            """.format(col1=col, col2=instance.size+1-col, row=row)

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
            asp_code += """
                erase(cell({col},{row1})) :- erase(cell({col},{row2})).
                erase(cell({col},{row2})) :- erase(cell({col},{row1})).
            """.format(row1=row, row2=instance.size+1-row, col=col)

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
            asp_code += """
                erase(cell({col1},{row1})) :- erase(cell({col2},{row2})).
                erase(cell({col2},{row2})) :- erase(cell({col1},{row1})).
            """.format(row1=row, row2=instance.size+1-row,
                       col1=col, col2=instance.size+1-col)

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

    asp_code = """
        solution({cell_enc},{value_enc}).
        :- erase({cell_enc}).
    """.format(
        cell_enc=instance.cell_encoding(cell),
        value_enc=value
    )

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
