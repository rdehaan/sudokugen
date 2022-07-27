"""
Module with ASP encodings for different deduction rules
"""

from typing import List, Optional
from dataclasses import dataclass
import itertools

from ..instances import SquareSudoku

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
    :- deduction_mode(Mode), use_technique(Mode,ss_solved),
        cell(C), solution(C,V),
        not derivable(Mode,solution(C,V)).
    """
)

stable_state_unsolved = DeductionRule(
    "ss_unsolved",
    """
    :- deduction_mode(Mode), use_technique(Mode,ss_unsolved),
        derivable(Mode,solution(C,V)) : solution(C,V).
    """
)

stable_state_no_derivable = DeductionRule(
    "ss_no_derivable",
    """
    :- deduction_mode(Mode), use_technique(Mode,ss_no_derivable),
        cell(C), solution(C,V), erase(C),
        derivable(Mode,solution(C,V)).
    """
)

stable_state_unsolved_naked_pairs = DeductionRule(
    "ss_unsolved_naked_pairs",
    """
    :- use_technique(Mode,ss_unsolved_naked_pairs),
        not counterexample(Mode,ss_unsolved_naked_pairs).
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
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
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

### TODO: develop this
stable_state_unsolved_hidden_pairs = DeductionRule(
    "ss_unsolved_hidden_pairs",
    """
    %TODO
    """
)

### TODO: develop this
stable_state_unsolved_naked_triples = DeductionRule(
    "ss_unsolved_naked_triples",
    """
    %TODO
    """
)

### TODO: develop this
stable_state_unsolved_hidden_triples = DeductionRule(
    "ss_unsolved_hidden_triples",
    """
    %TODO
    """
)

### TODO: develop this
stable_state_unsolved_locked_candidates = DeductionRule(
    "ss_unsolved_locked_candidates",
    """
    %TODO
    """
)

closed_under_naked_singles = DeductionRule(
    "closed_under_naked_singles",
    """
    :- use_technique(Mode,closed_under_naked_singles),
        cell(C), value(V), solution(C,V),
        derivable(Mode,strike(C,W)) : value(W), V != W;
        not certainly_not_erased(C), erase(C).
    """
)

closed_under_hidden_singles = DeductionRule(
    "closed_under_hidden_singles",
    """
    :- use_technique(Mode,closed_under_hidden_singles),
        deduction_mode(Mode), value(V), cell(C1),
        full_group(G), active_group(Mode,G), in_group(C1,G),
        derivable(Mode,strike(C2,V)) : in_group(C2,G), different_cells(C1,C2);
        not certainly_not_erased(C1), erase(C1).
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

    %%% Redundant rules: connection between derivable statements and the puzzle
    :- not solution(C,V),
        deduction_mode(Mode),
        derivable(Mode,solution(C,V)).
    :- solution(C,V),
        deduction_mode(Mode),
        derivable(Mode,strike(C,V)).
    """
)

naked_singles = DeductionRule(
    "naked_singles",
    """
    derivable(Mode,solution(C,V1)) :-
        use_technique(Mode,naked_singles),
        deduction_mode(Mode), value(V1),
        cell(C), not certainly_not_erased(C),
        derivable(Mode,strike(C,V2)) : different_values(V1,V2).
    """
)

hidden_singles = DeductionRule(
    "hidden_singles",
    """
    derivable(Mode,solution(C1,V)) :-
        use_technique(Mode,hidden_singles),
        deduction_mode(Mode), value(V),
        cell(C1), not certainly_not_erased(C1),
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
        different_cells(C1,C2), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).

    derivable(Mode,naked_pair(C,V1,V2)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V1), value(V2), V1 < V2,
        derivable(Mode,strike(C,W)) : value(W),
            %different_values(V1,W), different_values(V2,W).
            V1 != W, V2 != W.
    derivable(Mode,solution(C,V1)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V1), value(V2), V1 < V2,
        derivable(Mode,naked_pair(C,V1,V2)),
        derivable(Mode,strike(C,V2)).
    derivable(Mode,solution(C,V2)) :-
        use_technique(Mode,naked_pairs),
        deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
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
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    value_in_triple(V1,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
    value_in_triple(V2,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
    value_in_triple(V3,V1,V2,V3) :-
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3.

    derivable(Mode,naked_triple(C,V1,V2,V3)) :-
        use_technique(Mode,naked_triples),
        deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V1), value(V2), value(V3),
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
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        different_cells_in_group_ordered(C1,C2,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) : in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    cell_in_pair(C1,C1,C2) :-
        cell(C1), cell(C2), C1 < C2.
    cell_in_pair(C2,C1,C2) :-
        cell(C1), cell(C2), C1 < C2.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,hidden_pairs),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), in_group(C1,G), not certainly_not_erased(C1),
        cell(C2), in_group(C2,G), not certainly_not_erased(C2),
        cell_in_pair(C,C1,C2),
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
    derivable(Mode,value_only_in_three_cells_in_group(V,C1,C2,C3,G)) :-
        use_technique(Mode,hidden_triples),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), cell(C2), cell(C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        different_cells_in_group_ordered(C1,C2,G),
        different_cells_in_group_ordered(C2,C3,G),
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        derivable(Mode,strike(C,V)) : in_group(C,G),
            different_cells(C,C1),
            different_cells(C,C2),
            different_cells(C,C3).
    cell_in_triple(C1,C1,C2,C3) :-
        cell(C1), cell(C2), cell(C3), C1 < C2, C2 < C3.
    cell_in_triple(C2,C1,C2,C3) :-
        cell(C1), cell(C2), cell(C3), C1 < C2, C2 < C3.
    cell_in_triple(C3,C1,C2,C3) :-
        cell(C1), cell(C2), cell(C3), C1 < C2, C2 < C3.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,hidden_triples),
        deduction_mode(Mode), value(V), group(G), active_group(Mode,G),
        cell(C1), in_group(C1,G), not certainly_not_erased(C1),
        cell(C2), in_group(C2,G), not certainly_not_erased(C2),
        cell(C3), in_group(C3,G), not certainly_not_erased(C3),
        cell_in_triple(C,C1,C2,C3),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C2,C3),
        value(V1), value(V2), value(V3), V1 < V2, V2 < V3,
        different_values(V,V1), different_values(V,V2), different_values(V,V3),
        derivable(Mode,value_only_in_three_cells_in_group(V1,C1,C2,C3,G)),
        derivable(Mode,value_only_in_three_cells_in_group(V2,C1,C2,C3,G)),
        derivable(Mode,value_only_in_three_cells_in_group(V3,C1,C2,C3,G)).
    """
)

locked_candidates = DeductionRule(
    "locked_candidates",
    """
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,locked_candidates),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        in_group(C1,G2), not in_group(C1,G1),
        not certainly_not_erased(C1),
        derivable(Mode,strike(C2,V)) :
            cell(C2), in_group(C2,G1), not in_group(C2,G2).
    """
)

xy_wing = DeductionRule(
    "xy_wing",
    """
    derivable(Mode,xy_wing_or(0,C,V1,C,V2)) :-
        use_technique(Mode,xy_wing), deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2),
        cell(C), not certainly_not_erased(C),
        derivable(Mode,strike(C,V)) :
            value(V), different_values(V,V1), different_values(V,V2).
    derivable(Mode,xy_wing_or(D,C1,V1,C2,V2)) :-
        derivable(Mode,xy_wing_or(D,C2,V2,C1,V1)).
    derivable(Mode,xy_wing_or(1,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing), deduction_mode(Mode),
        derivable(Mode,xy_wing_or(0,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3.
    derivable(Mode,xy_wing_or(2,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing), deduction_mode(Mode),
        derivable(Mode,xy_wing_or(1,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3, V1 = V4.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,xy_wing), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V),
        derivable(Mode,xy_wing_or(2,C1,V,C2,V)),
        share_group(C,C1), share_group(C,C2).

    :- derivable(_,xy_wing_or(_,C1,V1,C2,V2)),
        not solution(C1,V1), not solution(C2,V2).
    """
)

xyz_wing = DeductionRule(
    "xyz_wing",
    """
    derivable(Mode,strike(C,V2)) :-
        deduction_mode(Mode), use_technique(Mode, xyz_wing),
        cell(C1), cell(C2), cell(C3), cell(C), C1 < C3,
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C2,C3),
        different_cells(C,C1), different_cells(C,C2), different_cells(C,C3),
        value(V1), value(V2), value(V3),
        different_values(V1,V2),
        different_values(V1,V3),
        different_values(V2,V3),
        share_group(C,C1), share_group(C,C2), share_group(C,C3),
        share_group(C1,C2), share_group(C2,C3),
        derivable(Mode,strike(C1,V)) :
            value(V), different_values(V,V1), different_values(V,V2);
        derivable(Mode,strike(C2,V)) :
            value(V), different_values(V,V1), different_values(V,V2),
            different_values(V,V3);
        derivable(Mode,strike(C3,V)) :
            value(V), different_values(V,V2), different_values(V,V3).
    """
)

xyz_wing_proper_chained = DeductionRule(
    "xyz_wing_proper_chained",
    """
    derivable(Mode,strike(C,V2)) :-
        deduction_mode(Mode), use_technique(Mode, xyz_wing_proper_chained),
        cell(C1), cell(C2), cell(C3), cell(C), C1 < C3,
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C2,C3),
        different_cells(C,C1), different_cells(C,C2), different_cells(C,C3),
        value(V1), value(V2), value(V3),
        different_values(V1,V2),
        different_values(V1,V3),
        different_values(V2,V3),
        share_group(C,C1), share_group(C,C2), share_group(C,C3),
        share_group(C1,C2), share_group(C2,C3),
        not derivable(Mode,strike(C1,V1)),
        not derivable(Mode,strike(C1,V2)),
        derivable(Mode,strike(C1,V)) :
            value(V), different_values(V,V1), different_values(V,V2);
        not derivable(Mode,strike(C2,V1)),
        not derivable(Mode,strike(C2,V2)),
        not derivable(Mode,strike(C3,V3)),
        derivable(Mode,strike(C2,V)) :
            value(V), different_values(V,V1), different_values(V,V2),
            different_values(V,V3);
        not derivable(Mode,strike(C3,V2)),
        not derivable(Mode,strike(C3,V3)),
        derivable(Mode,strike(C3,V)) :
            value(V), different_values(V,V2), different_values(V,V3).
    """
)

x_wing = DeductionRule(
    "x_wing",
    """
    derivable(Mode,(x_wing_snyder(V,C1,C3,G3);x_wing_snyder(V,C2,C4,G4))) :-
        use_technique(Mode,x_wing),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        group(G4), active_group(Mode,G4),
        G1 != G2, G1 != G3, G1 != G4,
        G2 != G3, G2 != G4,
        G3 != G4,
        group_type(G1,T1), group_type(G2,T1), T1 != block,
        group_type(G3,T2), group_type(G4,T2), T2 != block, T1 != T2,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2), C1 < C2,
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4), C1 < C3,
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        in_group(C2,G4), in_group(C4,G4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,x_wing),
        deduction_mode(Mode), value(V),
        group(G), active_group(Mode,G),
        cell(C1), cell(C2), in_group(C1,G), in_group(C2,G),
        derivable(Mode,x_wing_snyder(V,C1,C2,G)),
        different_cells(C,C1), different_cells(C,C2),
        cell(C), in_group(C,G), not certainly_not_erased(C).
    """
)

### Old encoding of x_wing
### (seems to lead to slightly smaller grounding times
###  but higher solving times)
# x_wing = DeductionRule(
#     "x_wing",
#     """
#     derivable(Mode,strike(C,V)) :-
#         use_technique(Mode,x_wing),
#         deduction_mode(Mode), value(V),
#         group(G1), active_group(Mode,G1),
#         group(G2), active_group(Mode,G2),
#         group(G3), active_group(Mode,G3),
#         group(G4), active_group(Mode,G4),
#         G1 != G2, G1 != G3, G1 != G4,
#         G2 != G3, G2 != G4,
#         G3 != G4,
#         group_type(G1,T1), group_type(G2,T1), T1 != block,
#         group_type(G3,T2), group_type(G4,T2), T2 != block, T1 != T2,
#         in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2), C1 < C2,
#         derivable(Mode,strike(D,V)) :
#             cell(D), in_group(D,G1),
#             different_cells(D,C1), different_cells(D,C2);
#         in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
#         derivable(Mode,strike(D,V)) :
#             cell(D), in_group(D,G2),
#             different_cells(D,C3), different_cells(D,C4);
#         different_cells(C1,C3), different_cells(C1,C4), C1 < C3,
#         different_cells(C2,C3), different_cells(C2,C4),
#         in_group(C1,G3), in_group(C3,G3),
#         in_group(C2,G4), in_group(C4,G4),
#         cell(C), in_group(C,(G3;G4)),
#         different_cells(C,C1), different_cells(C,C2),
#         different_cells(C,C3), different_cells(C,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4).
#     """
# )

x_chain = DeductionRule(
    "x_chain",
    """
    derivable(Mode,x_chain_or(C1,yes(V),C2,yes(V))) :-
        use_technique(Mode,x_chain), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        group(G), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) :
            cell(C), in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,x_chain_or(C1,no(V),C2,no(V))) :-
        use_technique(Mode,x_chain), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        share_group(C1,C2).
    derivable(Mode,x_chain_or(C1,S1,C2,S2)) :-
        derivable(Mode,x_chain_or(C2,S2,C1,S1)).
    derivable(Mode,x_chain_or(C1,S1,C3,S3)) :-
        use_technique(Mode,x_chain), deduction_mode(Mode),
        derivable(Mode,x_chain_or(C1,S1,C2,yes(V))),
        derivable(Mode,x_chain_or(C2,no(V),C3,S3)),
        different_cells(C1,C2), different_cells(C2,C3),
        different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,x_chain), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V),
        derivable(Mode,x_chain_or(C1,yes(V),C2,yes(V))),
        share_group(C,C1), share_group(C,C2),
        different_cells(C1,C2).

    :- derivable(_,x_chain_or(C1,no(V),C2,no(V))),
        solution(C1,V), solution(C2,V).
    :- derivable(_,x_chain_or(C1,yes(V),C2,yes(V))),
        not solution(C1,V), not solution(C2,V).
    :- derivable(_,x_chain_or(C1,no(V),C2,yes(V))),
        solution(C1,V), not solution(C2,V).
    :- derivable(_,x_chain_or(C1,yes(V),C2,no(V))),
        not solution(C1,V), solution(C2,V).
    """
    # """
    # derivable(Mode,x_chain_or(C1,yes(V),C2,yes(V))) :-
    #     use_technique(Mode,x_chain), deduction_mode(Mode),
    #     value(V), cell(C1), cell(C2), different_cells(C1,C2),
    #     not certainly_not_erased(C1),
    #     not certainly_not_erased(C2),
    #     derivable(Mode,solution(C1,V)).
    # derivable(Mode,x_chain_or(C1,yes(V),C2,no(V))) :-
    #     use_technique(Mode,x_chain), deduction_mode(Mode),
    #     value(V), cell(C1), cell(C2), different_cells(C1,C2),
    #     not certainly_not_erased(C1),
    #     not certainly_not_erased(C2),
    #     derivable(Mode,solution(C1,V)).
    # derivable(Mode,x_chain_or(C1,no(V),C2,yes(V))) :-
    #     use_technique(Mode,x_chain), deduction_mode(Mode),
    #     value(V), cell(C1), cell(C2), different_cells(C1,C2),
    #     not certainly_not_erased(C1),
    #     not certainly_not_erased(C2),
    #     derivable(Mode,strike(C1,V)).
    # derivable(Mode,x_chain_or(C1,no(V),C2,no(V))) :-
    #     use_technique(Mode,x_chain), deduction_mode(Mode),
    #     value(V), cell(C1), cell(C2), different_cells(C1,C2),
    #     not certainly_not_erased(C1),
    #     not certainly_not_erased(C2),
    #     derivable(Mode,strike(C1,V)).
    # """
)

color_trap = DeductionRule(
    "color_trap",
    """
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        use_technique(Mode,color_trap), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        group(G), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) :
            cell(C), in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,unicolor_same(V,C1,C2)) :-
        derivable(Mode,unicolor_same(V,C2,C1)).
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        derivable(Mode,unicolor_diff(V,C2,C1)).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_trap), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_same(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_trap), deduction_mode(Mode),
        derivable(Mode,unicolor_diff(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_diff(V,C1,C3)) :-
        use_technique(Mode,color_trap), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,color_trap), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C), value(V),
        derivable(Mode,unicolor_diff(V,C1,C2)),
        share_group(C,C1), share_group(C,C2),
        different_cells(C1,C2).

    :- derivable(_,unicolor_same(V,C1,C2)),
        not solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_same(V,C1,C2)),
        solution(C1,V), not solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)

color_trap_proper_chained = DeductionRule(
    "color_trap_proper_chained",
    """
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        use_technique(Mode,color_trap_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        group(G), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) :
            cell(C), in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,unicolor_same(V,C1,C2)) :-
        derivable(Mode,unicolor_same(V,C2,C1)).
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        derivable(Mode,unicolor_diff(V,C2,C1)).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_trap_proper_chained), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_same(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_trap_proper_chained), deduction_mode(Mode),
        derivable(Mode,unicolor_diff(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_diff(V,C1,C3)) :-
        use_technique(Mode,color_trap_proper_chained), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,color_trap_proper_chained), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C), value(V),
        derivable(Mode,unicolor_diff(V,C1,C2)),
        share_group(C,C1), share_group(C,C2),
        different_cells(C1,C2),
        not derivable(Mode,unicolor_same(V,C,C1)),
        not derivable(Mode,unicolor_same(V,C,C2)).

    :- derivable(_,unicolor_same(V,C1,C2)),
        not solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_same(V,C1,C2)),
        solution(C1,V), not solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)

color_wrap = DeductionRule(
    "color_wrap",
    """
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        use_technique(Mode,color_wrap), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        group(G), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) :
            cell(C), in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,unicolor_same(V,C1,C2)) :-
        derivable(Mode,unicolor_same(V,C2,C1)).
    derivable(Mode,unicolor_diff(V,C1,C2)) :-
        derivable(Mode,unicolor_diff(V,C2,C1)).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_wrap), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_same(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_same(V,C1,C3)) :-
        use_technique(Mode,color_wrap), deduction_mode(Mode),
        derivable(Mode,unicolor_diff(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,unicolor_diff(V,C1,C3)) :-
        use_technique(Mode,color_wrap), deduction_mode(Mode),
        derivable(Mode,unicolor_same(V,C1,C2)),
        derivable(Mode,unicolor_diff(V,C2,C3)),
        different_cells(C1,C2), different_cells(C2,C3), different_cells(C1,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3).
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,color_wrap), deduction_mode(Mode),
        value(V),
        derivable(Mode,unicolor_same(V,C1,C2)),
        share_group(C1,C2), different_cells(C1,C2).

    :- derivable(_,unicolor_same(V,C1,C2)),
        not solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_same(V,C1,C2)),
        solution(C1,V), not solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        solution(C1,V), solution(C2,V).
    :- derivable(_,unicolor_diff(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)

snyder_basic = DeductionRule(
    "snyder_basic",
    """
    derivable(Mode,snyder(V,C1,C2,G)) :-
        use_technique(Mode,snyder_basic),
        deduction_mode(Mode), value(V),
        group(G), active_group(Mode,G), group_type(G,block),
        cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        in_group(C1,G), in_group(C2,G),
        derivable(Mode,strike(C,V)) : in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,snyder_basic),
        deduction_mode(Mode),
        group(G), active_group(Mode,G), group_type(G,block),
        cell(C1), cell(C2), cell(C),
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        different_cells(C1,C2), different_cells(C1,C),
        different_cells(C2,C),
        in_group(C1,G), in_group(C2,G), in_group(C,G),
        derivable(Mode,snyder(V,C1,C2,G)).
    """
)

snyder_basic_locked = DeductionRule(
    "snyder_basic_locked",
    """
    derivable(Mode,snyder(V,C1,C2,G1)) :-
        use_technique(Mode,snyder_basic_locked),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1), group_type(G1,block),
        group(G2), active_group(Mode,G2), group_type(G2,(row;column)),
        cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        in_group(C1,G1), in_group(C2,G1),
        in_group(C1,G2), in_group(C2,G2),
        derivable(Mode,strike(C,V)) : in_group(C,G2),
            different_cells(C,C1), different_cells(C,C2).
    """
)

snyder_hidden_pairs = DeductionRule(
    "snyder_hidden_pairs",
    """
    cell_in_pair(C1,C1,C2) :-
        cell(C1), cell(C2), C1 < C2.
    cell_in_pair(C2,C1,C2) :-
        cell(C1), cell(C2), C1 < C2.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,snyder_hidden_pairs),
        deduction_mode(Mode), value(V),
        group(G), active_group(Mode,G), group_type(G,block),
        cell(C1), in_group(C1,G),
        cell(C2), in_group(C2,G),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        different_cells(C1,C2), C1 < C2,
        cell_in_pair(C,C1,C2),
        value(V1), value(V2), V1 < V2,
        different_values(V,V1), different_values(V,V2),
        derivable(Mode,snyder(V1,C1,C2,G)),
        derivable(Mode,snyder(V2,C1,C2,G)).
    """
)

snyder_locked_candidates = DeductionRule(
    "snyder_locked_candidates",
    """
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,snyder_locked_candidates),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1), group_type(G1,block),
        group(G2), active_group(Mode,G2), group_type(G2,(row;column)),
        cell(C1), cell(C2), cell(C),
        different_cells(C1,C2), different_cells(C1,C),
        different_cells(C2,C),
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        in_group(C1,G1), in_group(C2,G1),
        in_group(C1,G2), in_group(C2,G2), in_group(C,G2),
        derivable(Mode,snyder(V,C1,C2,G1)).
    """
)

snyder_x_wing = DeductionRule(
    "snyder_x_wing",
    """
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,snyder_x_wing),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1), group_type(G1,block),
        group(G2), active_group(Mode,G2), group_type(G2,block),
        G1 != G2,
        derivable(Mode,snyder(V,C1,C2,G1)), different_cells(C1,C2), C1 < C2,
        derivable(Mode,snyder(V,C3,C4,G2)), different_cells(C3,C4), C1 < C3,
        not certainly_not_erased(C),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        in_group(C1,G3), in_group(C3,G3), group_type(G3,T),
        in_group(C2,G4), in_group(C4,G4), group_type(G4,T), T != block,
        not in_group(C,G1), not in_group(C,G2),
        cell(C), in_group(C,(G3;G4)).
    """
)

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
    mask_pieces = [
        (j, i, mask[(i-1) * instance.size + j - 1])
        for (i, j) in itertools.product(range(1, instance.size+1), repeat=2)
    ]
    for (i, j, val) in mask_pieces:
        cell = instance.cell_encoding((i,j))
        if val == "0":
            asp_code += f"""
                :- deduction_mode(Mode),
                    use_technique(Mode,ss_mask_derived(m{mask})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    derivable(Mode,solution({cell},V)).
            """
        elif val == "*":
            asp_code += f"""
                :- deduction_mode(Mode),
                    use_technique(Mode,ss_mask_derived(m{mask})),
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
                        use_technique(Mode,ss_mask_derived(m{mask})),
                        cell({cell}),
                        solution({cell},{val}),
                        not derivable(Mode,solution({cell},{val})).
                """
            except ValueError:
                pass

    deduction_rule = DeductionRule(
        f"ss_mask_derived(m{mask})",
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
    mask_pieces = [
        (j, i, mask[(i-1) * instance.size + j - 1])
        for (i, j) in itertools.product(range(1, instance.size+1), repeat=2)
    ]
    for (i, j, val) in mask_pieces:
        cell = instance.cell_encoding((i,j))
        if val == "0":
            asp_code += f"""
                derivable(Mode,mask_not_derived({cell},m{mask})) :-
                    deduction_mode(Mode),
                    use_technique(Mode,ss_mask_not_derived(m{mask})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    derivable(Mode,solution({cell},V)).
            """
        elif val == "*":
            asp_code += f"""
                derivable(Mode,mask_not_derived({cell},m{mask})) :-
                    deduction_mode(Mode),
                    use_technique(Mode,ss_mask_not_derived(m{mask})),
                    cell({cell}), value(V),
                    solution({cell},V),
                    not derivable(Mode,solution({cell},V)).
            """
        else:
            try:
                val = int(val)
                asp_code += f"""
                    derivable(Mode,mask_not_derived({cell},m{mask})) :-
                        deduction_mode(Mode),
                        use_technique(Mode,ss_mask_not_derived(m{mask})),
                        cell({cell}),
                        not derivable(Mode,solution({cell},{val})).
                """
            except ValueError:
                pass

    asp_code += f"""
        derivable(Mode,mask_not_derived(m{mask})) :-
            deduction_mode(Mode),
            use_technique(Mode,ss_mask_not_derived(m{mask})),
            cell(C), derivable(Mode,mask_not_derived(C,m{mask})).
        :- deduction_mode(Mode),
            use_technique(Mode,ss_mask_not_derived(m{mask})),
            not derivable(Mode,mask_not_derived(m{mask})).
    """

    deduction_rule = DeductionRule(
        f"ss_mask_not_derived(m{mask})",
        asp_code
    )
    return deduction_rule
