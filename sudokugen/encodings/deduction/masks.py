"""
Module with ASP encodings related to (not) deriving masks
"""
# pylint: disable=too-many-lines

import itertools

from .basic import DeductionRule
from ...instances import SquareSudoku

def stable_state_mask_derived(
        instance: SquareSudoku,
        mask: str
    ) -> str:
    """
    Given a mask, produce a deduction rule that states that this mask must be
    derived (in the deduction mode in which the rule is used): if the
    mask has a 0 for a cell, no solution may be derived for this cell, if the
    mask has a positive integer, this integer must be derived for this cell,
    if the mask has a "*", some solution must be derived for this cell,
    and if the mask has a "?", no constraints are posed on what may be derived
    for this cell.
    """

    asp_code = ""
    mask_id = mask.replace("?", "_")
    mask_pieces = [
        (j, i, mask[(i-1) * instance.size + j - 1])
        for (i, j) in itertools.product(range(1, instance.size+1), repeat=2)
    ]
    for (i, j, val) in mask_pieces:
        cell = instance.cell_encoding((i,j))
        if val == "0":
            asp_code += f"""
                :- deduction_mode(Mode),
                    use_technique(Mode,ss_mask_derived(m{mask_id})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    derivable(Mode,solution({cell},V)).
            """

        elif val == "*":
            asp_code += f"""
                :- deduction_mode(Mode),
                    use_technique(Mode,ss_mask_derived(m{mask_id})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    not derivable(Mode,solution({cell},V)).
            """

        else:
            try:
                val = int(val)
                asp_code += f"""
                    solution({cell},{val}).
                    :- deduction_mode(Mode),
                        use_technique(Mode,ss_mask_derived(m{mask_id})),
                        cell({cell}),
                        solution({cell},{val}),
                        not derivable(Mode,solution({cell},{val})).
                """
            except ValueError:
                pass

    deduction_rule = DeductionRule(
        f"ss_mask_derived(m{mask_id})",
        asp_code
    )
    return deduction_rule

def stable_state_mask_not_derived(
        instance: SquareSudoku,
        mask: str
    ) -> str:
    """
    Given a mask, produce a deduction rule that states that this mask must *NOT*
    be derived (in the deduction mode in which the rule is used). A mask is
    derived if the following conditions holds for all cells: if the mask
    mask has a 0 for a cell, no solution may be derived for this cell, if the
    mask has a positive integer, this integer must be derived for this cell,
    if the mask has a "*", some solution must be derived for this cell,
    and if the mask has a "?", no constraints are posed on what may be derived
    for this cell.
    """

    asp_code = ""
    mask_id = mask.replace("?", "_")
    mask_pieces = [
        (j, i, mask[(i-1) * instance.size + j - 1])
        for (i, j) in itertools.product(range(1, instance.size+1), repeat=2)
    ]
    for (i, j, val) in mask_pieces:
        cell = instance.cell_encoding((i,j))
        if val == "0":
            asp_code += f"""
                derivable(Mode,mask_not_derived({cell},m{mask_id})) :-
                    deduction_mode(Mode),
                    use_technique(Mode,ss_mask_not_derived(m{mask_id})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    derivable(Mode,solution({cell},V)).
            """
        elif val == "*":
            asp_code += f"""
                derivable(Mode,mask_not_derived({cell},m{mask_id})) :-
                    deduction_mode(Mode),
                    use_technique(Mode,ss_mask_not_derived(m{mask_id})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    not derivable(Mode,solution({cell},V)).
            """
        else:
            try:
                val = int(val)
                asp_code += f"""
                    derivable(Mode,mask_not_derived({cell},m{mask_id})) :-
                        deduction_mode(Mode),
                        use_technique(Mode,ss_mask_not_derived(m{mask_id})),
                        cell({cell}),
                        not derivable(Mode,solution({cell},{val})).
                """
            except ValueError:
                pass

    asp_code += f"""
        derivable(Mode,mask_not_derived(m{mask_id})) :-
            deduction_mode(Mode),
            use_technique(Mode,ss_mask_not_derived(m{mask_id})),
            cell(C), derivable(Mode,mask_not_derived(C,m{mask_id})).
        :- deduction_mode(Mode),
            use_technique(Mode,ss_mask_not_derived(m{mask_id})),
            not derivable(Mode,mask_not_derived(m{mask_id})).
    """

    deduction_rule = DeductionRule(
        f"ss_mask_not_derived(m{mask_id})",
        asp_code
    )
    return deduction_rule
