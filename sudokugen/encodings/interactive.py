"""
Module with functionality to generate puzzles using ASP encodings
"""

from typing import List
import uuid

from .deduction import DeductionRule


def select_single_highlight_strike() -> str:
    """
    Encoding that requires that a combination of cell and value is selected
    as a 'highlight'.
    """

    asp_code = """
        1 { highlight_strike(C,V) : cell(C), value(V) } 1.
    """

    return asp_code


def output_highlight_strikes() -> str:
    """
    Encoding that expresses that highlight strikes are being output.
    """

    asp_code = """
        output(highlight_strike,strike(C,V)) :- highlight_strike(C,V).
    """

    return asp_code

highlight_strikes_derivable = DeductionRule(
    "highlight_strikes_derivable",
    """
    :- deduction_mode(Mode), use_technique(Mode,highlight_strikes_derivable),
        highlight_strike(C,V),
        not derivable(Mode,strike(C,V)).
    """
)

highlight_strikes_not_derivable = DeductionRule(
    "highlight_strikes_not_derivable",
    """
    :- deduction_mode(Mode), use_technique(Mode,highlight_strikes_not_derivable),
        highlight_strike(C,V),
        derivable(Mode,strike(C,V)).
    """
)

reveal_highlight_strikes = DeductionRule(
    "reveal_highlight_strikes",
    """
    derivable(Mode,strike(C,V)) :-
        deduction_mode(Mode), use_technique(Mode,reveal_highlight_strikes),
        highlight_strike(C,V).
    """
)

select_non_derivable_strikes_as_highlight = DeductionRule(
    "select_non_derivable_strikes_as_highlight",
    """
    highlight_strike(C,V) :-
        deduction_mode(Mode),
        use_technique(Mode,select_non_derivable_strikes_as_highlight),
        cell(C), value(V),
        not derivable(Mode,strike(C,V)),
        not solution(C,V).
    """
)

def forbid_strings_derivable(
        conclusions: List[str]
    ) -> DeductionRule:
    """
    DeductionRule that expresses that the given strings may not be derivable.
    """

    rule_uuid = str(uuid.uuid4()).replace('-', '')

    asp_code = ""
    for conclusion in conclusions:
        asp_code += f"""
            :- deduction_mode(Mode),
                use_technique(Mode,forbid_strings_derivable(r{rule_uuid})),
                derivable(Mode,{conclusion}).
        """

    deduction_rule = DeductionRule(
        f"forbid_strings_derivable(r{rule_uuid})",
        asp_code
    )
    return deduction_rule
