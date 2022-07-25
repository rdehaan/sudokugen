"""
Module with functionality to generate interface puzzles using ASP encodings
"""

from ..instances import BasicInterfaceSudoku
from .deduction import DeductionRule


def select_input_cell() -> str:
    """
    Encoding that requires that an input cell is selected.
    """

    # Require that there is exactly one input cell, and that it is empty
    # in the puzzle
    asp_code = """
        1 { input_cell(C) : cell(C) } 1.
        #show input_cell/1.

        :- input_cell(C), not erase(C).
    """

    return asp_code


def input_cell_semantically_undeducible(
        num_alternative_values=1,
        enforce_uniqueness=False,
    ) -> str:
    """
    Encoding that requires that the input cell can be filled in with other
    values to yield another solution to the puzzle (that can be required to be
    unique for each alternative value for the input cell).
    """

    asp_code = f"""
        #const num_icsu_alt_solutions={num_alternative_values}.
        icsu_alt_solution(1..num_icsu_alt_solutions).

        1 {{ icsu_alt_solution(I,C,W) : value(W) }} 1 :-
            icsu_alt_solution(I), cell(C).
        icsu_alt_solution(I,C,W) :-
            icsu_alt_solution(I), cell(C), solution(C,W), not erase(C).
        :- icsu_alt_solution(I,C1,W), icsu_alt_solution(I,C2,W),
            icsu_alt_solution(I), cell(C1), cell(C2), share_group(C1,C2).

        :- icsu_alt_solution(I1), icsu_alt_solution(I2), I1 < I2,
            input_cell(C),
            icsu_alt_solution(I1,C,W1), icsu_alt_solution(I2,C,W2), W2 >= W1.
        :- icsu_alt_solution(I,C,V), icsu_alt_solution(I),
            input_cell(C), solution(C,V).
    """

    if enforce_uniqueness:
        asp_code += """
            %%% Use saturation
            :- not icsu_saturate(I), icsu_alt_solution(I).
            icsu_alt_other(I,C,V) :- icsu_alt_solution(I),
                cell(C), value(V), icsu_saturate(I).

            %%% Choose at least one V for every cell X,Y
            icsu_alt_other(I,C,V) : value(V) :-
                icsu_alt_solution(I),
                cell(C).

            %%% Filter out choices that don't agree with non-erased cells
            icsu_saturate(I) :-
                icsu_alt_solution(I),
                cell(C), solution(C,V1), not erase(C),
                icsu_alt_other(I,C,V2), different_values(V1,V2).

            %%% Filter out the choice that corresponds to the solution
            icsu_saturate(I) :- icsu_alt_solution(I),
                icsu_alt_other(I,C,V) : icsu_alt_solution(I,C,V).

            %%% Filter out choices that don't agree with the chosen value
            %%% in the input cell
            icsu_saturate(I) :-
                icsu_alt_solution(I), icsu_alt_solution(I,C,V1),
                input_cell(C), icsu_alt_other(I,C,V2),
                different_values(V1,V2).

            %%% Filter out choices that don't satisfy the constraints
            icsu_saturate(I) :- icsu_alt_solution(I),
                icsu_alt_other(I,C1,V),
                icsu_alt_other(I,C2,V),
                cell(C1), cell(C2), value(V),
                share_group(C1,C2).
        """

    # # Require that for each possible value in the input cell,
    # # there is a solution that agrees with the puzzle
    # asp_code = """
    #     1 { alt_solution(V,C,W) : value(W) } 1 :-
    #         value(V), cell(C).
    #     alt_solution(V,C,W) :-
    #         value(V), cell(C), solution(C,W), not erase(C).
    #     :- alt_solution(V,C1,W), alt_solution(V,C2,W),
    #         value(V), cell(C1), cell(C2), share_group(C1,C2).
    #     alt_solution(V,C,V) :- input_cell(C), value(V).
    #     alt_solution(V,C,W) :-
    #         cell(C), solution(C,W),
    #         input_cell(D), solution(D,V).
    # """

    return asp_code


def full_semantic_undeducibility() -> str:
    """
    Encoding that enforces that no empty cell in the puzzle has a unique value
    that fits with the non-empty cells in the puzzle.
    """

    asp_code = f"""
        fsu_alt_solution(D) :- cell(D), erase(D).

        1 {{ fsu_alt_solution(D,C,W) : value(W) }} 1 :-
            fsu_alt_solution(D), cell(C).
        fsu_alt_solution(D,C,W) :-
            fsu_alt_solution(D), cell(C), solution(C,W), not erase(C).
        :- fsu_alt_solution(D,C1,W), fsu_alt_solution(D,C2,W),
            fsu_alt_solution(D), cell(C1), cell(C2), share_group(C1,C2).

        :- fsu_alt_solution(D,D,V), fsu_alt_solution(D),
            cell(D), solution(D,V).
    """

    return asp_code


def fix_location_of_input_cell(
        instance: BasicInterfaceSudoku,
        col: int,
        row: int,
    ) -> str:
    """
    Encoding that requires that the input cell is at a particular location.
    """

    input_cell = (col,row)
    asp_code = f"""
        input_cell({instance.cell_encoding(input_cell)}).
    """

    return asp_code


def fix_solution_at_input_cell(
        value: int
    ) -> str:
    """
    Encoding that requires that the input cell has a particular value in the
    solution.
    """

    asp_code = f"""
        solution(C,{value}) :- input_cell(C).
    """

    return asp_code


def select_output_cell() -> str:
    """
    Encoding that requires that an output cell is selected.
    """

    # Require that there is exactly one output cell, and that it is empty
    # in the puzzle
    asp_code = """
        1 { output_cell(C) : cell(C) } 1.
        #show output_cell/1.

        :- output_cell(C), not erase(C).
    """

    return asp_code


def fix_location_of_output_cell(
        instance: BasicInterfaceSudoku,
        col: int,
        row: int,
    ) -> str:
    """
    Encoding that requires that the output cell is at a particular location.
    """

    output_cell = (col,row)
    asp_code = f"""
        output_cell({instance.cell_encoding(output_cell)}).
    """

    return asp_code


def fix_solution_at_output_cell(
        value: int
    ) -> str:
    """
    Encoding that requires that the output cell has a particular value in the
    solution.
    """

    asp_code = f"""
        solution(C,{value}) :- output_cell(C).
    """

    return asp_code


def forbid_solution_at_output_cell(
        value: int
    ) -> str:
    """
    Encoding that requires that the output cell does not have a particular
    value in the solution.
    """

    asp_code = f"""
        :- solution(C,{value}), output_cell(C).
    """

    return asp_code


reveal_input_cell = DeductionRule(
    "reveal_input_cell",
    """
    derivable(Mode,solution(C,V)) :-
        deduction_mode(Mode), use_technique(Mode,reveal_input_cell),
        input_cell(C), solution(C,V).
    """
)

output_cell_derivable = DeductionRule(
    "output_cell_derivable",
    """
    :- deduction_mode(Mode), use_technique(Mode,output_cell_derivable),
        output_cell(C), solution(C,V),
        not derivable(Mode,solution(C,V)).
    """
)

output_cell_not_derivable = DeductionRule(
    "output_cell_not_derivable",
    """
    :- deduction_mode(Mode), use_technique(Mode,output_cell_not_derivable),
        output_cell(C), solution(C,V),
        derivable(Mode,solution(C,V)).
    """
)
