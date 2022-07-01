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

stable_state_trivial = DeductionRule(
    "ss_trivial",
    """
    stable_state(Mode) :- use_technique(Mode,ss_trivial).
    """
)

stable_state_unsolved_naked_pairs = DeductionRule(
    "ss_unsolved_naked_pairs",
    """
    stable_state(Mode) :-
        use_technique(Mode,ss_unsolved_naked_pairs),
        counterexample(Mode,ss_unsolved_naked_pairs).
    different_cells_in_group_ordered(C1,C2,G) :-
        group(G), cell(C1), cell(C2),
        in_group(C1,G), in_group(C2,G), C1 < C2.
    value_in_pair(V1,V1,V2) :-
        value(V1), value(V2), V1 < V2.
    value_in_pair(V2,V1,V2) :-
        value(V1), value(V2), V1 < V2.
    counterexample(Mode,ss_unsolved_naked_pairs) :-
        use_technique(Mode,ss_unsolved_naked_pairs),
        cell(C), cell(C1), cell(C2), C != C1, C != C2,
        group(G), in_group(C,G), in_group(C1,G), in_group(C2,G),
        different_cells_in_group_ordered(C1,C2,G),
        value(V), value_in_pair(V,V1,V2),
        derivable(Mode,strike(C1,W)) : value(W), W != V1, W != V2;
        derivable(Mode,strike(C2,W)) : value(W), W != V1, W != V2;
        not derivable(Mode,strike(C1,V1)),
        not derivable(Mode,strike(C1,V2)),
        not derivable(Mode,strike(C2,V1)),
        not derivable(Mode,strike(C2,V2)),
        not derivable(Mode,strike(C,V)).
    """
)

closed_under_naked_singles = DeductionRule(
    "closed_under_naked_singles",
    """
    :- use_technique(Mode,closed_under_naked_singles),
        cell(C), value(V), solution(C,V),
        derivable(Mode,strike(C,W)) : value(W), V != W;
        erase(C).
    """
)

closed_under_hidden_singles = DeductionRule(
    "closed_under_hidden_singles",
    """
    :- use_technique(Mode,closed_under_hidden_singles),
        deduction_mode(Mode), value(V), cell(C1),
        full_group(G), active_group(Mode,G), in_group(C1,G),
        derivable(Mode,strike(C2,V)) : in_group(C2,G), different_cells(C1,C2);
        erase(C1).
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

naked_singles = DeductionRule(
    "naked_singles",
    """
    derivable(Mode,solution(C,V1)) :-
        use_technique(Mode,naked_singles),
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

naked_pairs = DeductionRule(
    "naked_pairs",
    """
    naked_pairs_setting(Mode,C1,C2,C3) :-
        group(G), deduction_mode(Mode), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        different_cells_in_group_ordered(C2,C3,G),
        different_cells(C1,C2), different_cells(C1,C3).

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
        naked_pairs_setting(Mode,C1,C2,C3),
        derivable(Mode,naked_pair(C2,V1,V2)),
        derivable(Mode,naked_pair(C3,V1,V2)),
        value_in_pair(V,V1,V2).
    """
)

naked_triples = DeductionRule(
    "naked_triples",
    """
    different_cells_in_group_ordered(C1,C2,C3,G) :-
        group(G), cell(C1), cell(C2), cell(C3),
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        C1 < C2, C2 < C3.
    naked_triples_setting(Mode,C1,C2,C3,C4) :-
        group(G), deduction_mode(Mode), active_group(Mode,G),
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
        naked_triples_setting(Mode,C1,C2,C3,C4),
        derivable(Mode,naked_triple(C2,V1,V2,V3)),
        derivable(Mode,naked_triple(C3,V1,V2,V3)),
        derivable(Mode,naked_triple(C4,V1,V2,V3)),
        value_in_triple(V,V1,V2,V3).
    """
)

hidden_pairs = DeductionRule(
    "hidden_pairs",
    """
    derivable(Mode,value_only_in_two_cells_in_group(V,C1,C2,G)) :-
        use_technique(Mode,hidden_pairs),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), cell(C2),
        different_cells_in_group_ordered(C1,C2,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) : in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,hidden_pairs),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), in_group(C1,G),
        cell(C2), in_group(C2,G),
        different_cells(C1,C2),
        value(V1), value(V2), V1 < V2,
        different_values(V,V1), different_values(V,V2),
        derivable(Mode,value_only_in_two_cells_in_group(V1,C1,C2,G)),
        derivable(Mode,value_only_in_two_cells_in_group(V2,C1,C2,G)).
    derivable(Mode,strike(C2,V)) :-
        use_technique(Mode,hidden_pairs),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), in_group(C1,G),
        cell(C2), in_group(C2,G),
        different_cells(C1,C2),
        value(V1), value(V2), V1 < V2,
        different_values(V,V1), different_values(V,V2),
        derivable(Mode,value_only_in_two_cells_in_group(V1,C1,C2,G)),
        derivable(Mode,value_only_in_two_cells_in_group(V2,C1,C2,G)).
    """
)

### TODO: develop this
hidden_triples = DeductionRule(
    "hidden_triples",
    """
        %TODO
    """
)

locked_candidate = DeductionRule(
    "locked_candidate",
    """
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,locked_candidate),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        in_group(C1,G2), not in_group(C1,G1),
        derivable(Mode,strike(C2,V)) :
            cell(C2), in_group(C2,G1), not in_group(C2,G2).
    """
)

### TODO: develop this
xy_wing = DeductionRule(
    "xy_wing",
    """
        %TODO
    """
)

### TODO: develop this
x_wing = DeductionRule(
    "x_wing",
    """
        %TODO
    """
)
