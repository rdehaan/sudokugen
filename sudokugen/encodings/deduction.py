"""
Module with ASP encodings for different deduction rules
"""

from typing import List, Optional
from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class DeductionRule:
    """
    Data class to represent the ASP encoding of a single deduction rule
    """
    name: str
    encoding: str


@dataclass
class SolvingStrategy:
    """
    Data class to represent a solving strategy

    Specifies which deduction rules are to be used in the strategy,
    possibly a restricted set of groups in the puzzle on which the deduction
    rules may only be applied.
    """
    rules: List[DeductionRule]
    groups: Optional[List[str]] = None


stable_state_solved = DeductionRule(
    "ss_solved",
    """
    stable_state(Mode) :-
        all_derived(Mode), use_technique(Mode,ss_solved).
    all_derived(Mode) :-
        deduction_mode(Mode), use_technique(Mode,ss_solved),
        derivable(Mode,solution(C,V)) : solution(C,V).
    """
)

stable_state_unsolved = DeductionRule(
    "ss_unsolved",
    """
    stable_state(Mode) :-
        not all_derived(Mode), use_technique(Mode,ss_unsolved).
    all_derived(Mode) :-
        deduction_mode(Mode), use_technique(Mode,ss_unsolved),
        derivable(Mode,solution(C,V)) : solution(C,V).
    """
)

basic_deduction = DeductionRule(
    "basic_deduction",
    """
    %%% Fill in the solution for the last remaining cell in a full group
    derivable(Mode,solution(C1,V1)) :-
        deduction_mode(Mode),
        value(V1), cell(C1), solution(C1,V1),
        full_group(G), active_group(Mode,G),
        in_group(C1,G),
        derivable(Mode,solution(C2,V2)) :
            in_group(C2,G),
            different_cells(C1,C2),
            solution(C2,V2).

    %%% Derive all clues given in the puzzle
    derivable(Mode,solution(C,V)) :-
        deduction_mode(Mode), solution(C,V), not erase(C).

    %%% Define share_active_group/3
    share_active_group(Mode,C1,C2) :-
        deduction_mode(Mode),
        active_group(Mode,G), group(G),
        cell(C1), in_group(C1,G),
        cell(C2), in_group(C2,G),
        different_cells(C1,C2).

    %%% Erase pencil marks for corresponding derived values in the same group
    derivable(Mode,strike(C1,V)) :-
        deduction_mode(Mode),
        cell(C1), cell(C2), different_cells(C1,C2),
        derivable(Mode,solution(C2,V)), share_active_group(Mode,C1,C2).

    %%% Erase other pencil marks when the solution for that cell is derived
    derivable(Mode,strike(C,V1)) :-
        deduction_mode(Mode), cell(C), derivable(Mode,solution(C,V2)),
        value(V1), value(V2), different_values(V1,V2).

    %%% Declare when the entire solution has been derived
    %all_derivable(Mode) :-
    %    deduction_mode(Mode),
    %    derivable(Mode,solution(C,V)) : solution(C,V).
    """
)

lone_singles = DeductionRule(
    "lone_singles",
    """
    derivable(Mode,solution(C,V1)) :-
        use_technique(Mode,lone_singles),
        deduction_mode(Mode), value(V1), cell(C),
        derivable(Mode,strike(C,V2)) : different_values(V1,V2).
    """
)

hidden_singles = DeductionRule(
    "hidden_singles",
    """
    derivable(Mode,solution(C1,V)) :-
        use_technique(Mode,hidden_singles),
        deduction_mode(Mode), value(V), cell(C1),
        full_group(G), active_group(Mode,G), in_group(C1,G),
        derivable(Mode,strike(C2,V)) : in_group(C2,G), different_cells(C1,C2).
    """
)

### TODO: add active_group/2 to this rule
naked_pairs = DeductionRule(
    "naked_pairs",
    """
    different_cells_in_group_ordered(C1,C2,G) :-
        group(G), cell(C1), cell(C2),
        in_group(C1,G), in_group(C2,G), C1 < C2.
    naked_pairs_setting(C1,C2,C3) :-
        group(G),
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        different_cells_in_group_ordered(C2,C3,G),
        different_cells(C1,C2), different_cells(C1,C3).
    value_in_pair(V1,V1,V2) :-
        value(V1), value(V2), V1 < V2.
    value_in_pair(V2,V1,V2) :-
        value(V1), value(V2), V1 < V2.

    derivable(Mode,naked_pair(C,V1,V2)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode), cell(C), value(V1), value(V2), V1 < V2,
        derivable(Mode,strike(C,W)) : value(W),
            %different_values(V1,W), different_values(V2,W).
            V1 != W, V2 != W.
    derivable(Mode,solution(C,V1)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode), cell(C),
        value(V1), value(V2), V1 < V2,
        derivable(Mode,naked_pair(C,V1,V2)),
        derivable(Mode,strike(C,V2)).
    derivable(Mode,solution(C,V2)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode), cell(C),
        value(V1), value(V2), V1 < V2,
        derivable(Mode,naked_pair(C,V1,V2)),
        derivable(Mode,strike(C,V1)).
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode), value(V),
        naked_pairs_setting(C1,C2,C3),
        derivable(Mode,naked_pair(C2,V1,V2)),
        derivable(Mode,naked_pair(C3,V1,V2)),
        value_in_pair(V,V1,V2).
    """
)

### WORK IN PROGRESS! :-)
naked_triples = DeductionRule(
    "naked_triples",
    """
    different_cells_in_group_ordered(C1,C2,C3,G) :-
        group(G), cell(C1), cell(C2), cell(C3)
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        C1 < C2, C2 < C3.
    naked_pairs_setting(C1,C2,C3,C4) :-
        group(G),
        in_group(C1,G), in_group(C2,G), in_group(C3,G), in_group(C4,G),
        different_cells_in_group_ordered(C2,C3,C4,G),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4).
    value_in_triple(V1,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
    value_in_triple(V2,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
    value_in_triple(V3,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.

    derivable(Mode,naked_triple(C,V1,V2,V3)) :-
        use_technique(Mode,naked_triples),
        deduction_mode(Mode), cell(C), value(V1), value(V2), value(V3),
        V1 < V2, V2 < V3,
        derivable(Mode,strike(C,W)) : value(W),
            different_values(V1,W),
            different_values(V2,W),
            different_values(V3,W).
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,naked_triples),
        deduction_mode(Mode), value(V),
        naked_triples_setting(C1,C2,C3,C4),
        derivable(Mode,naked_triple(C2,V1,V2,V3)),
        derivable(Mode,naked_triple(C3,V1,V2,V3)),
        derivable(Mode,naked_triple(C4,V1,V2,V3)),
        value_in_pair(V,V1,V2,V3).
    """
)
