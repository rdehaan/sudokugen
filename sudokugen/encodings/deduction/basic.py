"""
Module with ASP encodings for different basic deduction rules
"""
# pylint: disable=too-many-lines

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
        deduction_mode(Mode), use_technique(Mode,basic_deduction),
        solution(C,V), not erase(C).

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

# naked_triples_perfect_chained = DeductionRule(
#     "naked_triples_perfect_chained",
#     """
#     different_cells_in_group_ordered(C1,C2,C3,G) :-
#         group(G), cell(C1), cell(C2), cell(C3),
#         in_group(C1,G), in_group(C2,G), in_group(C3,G),
#         C1 < C2, C2 < C3.
#     naked_triples_setting(Mode,C1,C2,C3,C4) :-
#         group(G), deduction_mode(Mode), active_group(Mode,G),
#         in_group(C1,G), in_group(C2,G), in_group(C3,G), in_group(C4,G),
#         different_cells_in_group_ordered(C2,C3,C4,G),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4).
#     value_in_triple(V1,V1,V2,V3) :-
#         value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
#     value_in_triple(V2,V1,V2,V3) :-
#         value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
#     value_in_triple(V3,V1,V2,V3) :-
#         value(V1), value(V2), value(V3), V1 < V2, V2 < V3.
#
#     derivable(Mode,naked_triple_perfect(C,V1,V2,V3)) :-
#         use_technique(Mode,naked_triples_perfect_chained),
#         deduction_mode(Mode),
#         cell(C), not certainly_not_erased(C),
#         value(V1), value(V2), value(V3),
#         V1 < V2, V2 < V3,
#         not derivable(Mode,strike(C,V1)),
#         not derivable(Mode,strike(C,V2)),
#         derivable(Mode,strike(C,V3)),
#         derivable(Mode,strike(C,W)) : value(W),
#             different_values(V1,W),
#             different_values(V2,W),
#             different_values(V3,W).
#     derivable(Mode,naked_triple_perfect(C,V1,V2,V3)) :-
#         use_technique(Mode,naked_triples_perfect_chained),
#         deduction_mode(Mode),
#         cell(C), not certainly_not_erased(C),
#         value(V1), value(V2), value(V3),
#         V1 < V2, V2 < V3,
#         not derivable(Mode,strike(C,V1)),
#         derivable(Mode,strike(C,V2)),
#         not derivable(Mode,strike(C,V3)),
#         derivable(Mode,strike(C,W)) : value(W),
#             different_values(V1,W),
#             different_values(V2,W),
#             different_values(V3,W).
#     derivable(Mode,naked_triple_perfect(C,V1,V2,V3)) :-
#         use_technique(Mode,naked_triples_perfect_chained),
#         deduction_mode(Mode),
#         cell(C), not certainly_not_erased(C),
#         value(V1), value(V2), value(V3),
#         V1 < V2, V2 < V3,
#         derivable(Mode,strike(C,V1)),
#         not derivable(Mode,strike(C,V2)),
#         not derivable(Mode,strike(C,V3)),
#         derivable(Mode,strike(C,W)) : value(W),
#             different_values(V1,W),
#             different_values(V2,W),
#             different_values(V3,W).
#     derivable(Mode,pre_strike(C1,V)) :-
#         use_technique(Mode,naked_triples_perfect_chained),
#         deduction_mode(Mode), value(V),
#         naked_triples_setting(Mode,C1,C2,C3,C4),
#         derivable(Mode,naked_triple_perfect(C2,V1,V2,V3)),
#         derivable(Mode,naked_triple_perfect(C3,V1,V2,V3)),
#         derivable(Mode,naked_triple_perfect(C4,V1,V2,V3)),
#         value_in_triple(V,V1,V2,V3).
#     """
# )

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
