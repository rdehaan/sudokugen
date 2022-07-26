"""
Module with functionality to generate interface puzzles using ASP encodings
"""

from ..instances import BasicInterfaceSudoku
from .deduction import DeductionRule


def select_input_cell() -> str:
    """
    Encoding that requires that an input cell is selected together with a decoy
    value.
    """

    # Require that there is exactly one input cell, and that it is empty
    # in the puzzle
    asp_code = """
        1 { input_cell(C) : cell(C) } 1.
        #show input_cell/1.

        :- input_cell(C), not erase(C).
    """

    # Require that a decoy value is selected, that is different from the
    # solution at the input cell.
    asp_code += """
        1 { input_decoy_value(V) : value(V) } 1.
        #show input_decoy_value/1.

        :- input_decoy_value(V), input_cell(C), solution(C,V).
    """

    return asp_code


def input_cell_semantically_undeducible(
        num_alternative_values=1,
        enforce_exclusivity=False,
        enforce_uniqueness=False,
    ) -> str:
    """
    Encoding that requires that the input cell can be filled in with other
    values to yield another solution to the puzzle (that can be required to be
    unique for each alternative value for the input cell).
    """
    # pylint: disable=invalid-name

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

        :- input_cell(C), input_decoy_value(V),
            V != W : icsu_alt_solution(_,C,W).
    """

    if enforce_exclusivity:
        asp_code += """
            icsu_value(V) :- icsu_alt_solution(I,C,V), input_cell(C).
            icsu_value(V) :- input_cell(C), solution(C,V).

            %%% Use saturation
            :- not icsu_saturate.
            icsu_other(C,V) :- cell(C), value(V), icsu_saturate.

            %%% Choose at least one value for every cell
            icsu_other(C,V) : value(V) :- cell(C).

            %%% Filter out choices that don't agree with non-erased cells
            icsu_saturate :-
                cell(C), solution(C,V1), not erase(C),
                icsu_other(C,V2), different_values(V1,V2).

            %%% Filter out choices that correspond to the selected values at
            %%% the input cell
            icsu_saturate :- icsu_other(C,V), input_cell(C), icsu_value(V).

            %%% Filter out choices that don't satisfy the constraints
            icsu_saturate :-
                icsu_other(C1,V),
                icsu_other(C2,V),
                cell(C1), cell(C2), value(V),
                share_group(C1,C2).
        """

    if enforce_uniqueness:
        asp_code += """
            %%% Use saturation
            :- not icsu_saturate(I), icsu_alt_solution(I).
            icsu_alt_other(I,C,V) :- icsu_alt_solution(I),
                cell(C), value(V), icsu_saturate(I).

            %%% Choose at least one value for every cell
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


def fix_input_decoy_value(
        value: int
    ) -> str:
    """
    Encoding that requires that the input decoy has a particular value.
    """

    asp_code = f"""
        input_decoy_value({value}).
    """

    return asp_code


def select_output_cell() -> str:
    """
    Encoding that requires that an output cell is selected together with a
    decoy value.
    """

    # Require that there is exactly one output cell, and that it is empty
    # in the puzzle
    asp_code = """
        1 { output_cell(C) : cell(C) } 1.
        #show output_cell/1.

        :- output_cell(C), not erase(C).
    """

    # Require that a decoy value is selected, that is different from the
    # solution at the output cell.
    asp_code += """
        1 { output_decoy_value(V) : value(V) } 1.
        #show output_decoy_value/1.

        :- output_decoy_value(V), output_cell(C), solution(C,V).
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


def fix_output_decoy_value(
        value: int
    ) -> str:
    """
    Encoding that requires that the output decoy has a particular value.
    """

    asp_code = f"""
        output_decoy_value({value}).
    """

    return asp_code


def io_solutions_and_decoys_alldiff() -> str:
    """
    Encoding that requires that the solutions of the input/output cells and
    the input/output decoy values are all different.
    """

    asp_code = f"""
        :- input_decoy_value(V), output_decoy_value(V).
        :- input_decoy_value(V), input_cell(C), solution(C,V).
        :- input_decoy_value(V), output_cell(C), solution(C,V).
        :- output_decoy_value(V), input_cell(C), solution(C,V).
        :- output_decoy_value(V), output_cell(C), solution(C,V).
        :- input_cell(C1), output_cell(C2), solution(C1,V), solution(C2,V).
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

reveal_output_value_or_decoy = DeductionRule(
    "reveal_output_value_or_decoy",
    """
    derivable(Mode,strike(C,V)) :- deduction_mode(Mode),
        use_technique(Mode,reveal_output_value_or_decoy),
        output_cell(C), solution(C,V1),
        output_decoy_value(V2),
        value(V),
        different_values(V,V1),
        different_values(V,V2).
    """
)

output_decoy_not_ruled_out = DeductionRule(
    "output_decoy_not_ruled_out",
    """
    :- deduction_mode(Mode), use_technique(Mode,output_decoy_not_ruled_out),
        output_cell(C), output_decoy_value(V),
        derivable(Mode,strike(C,V)).
    """
)
