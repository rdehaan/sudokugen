"""
Module with ASP encodings for different Snyder deduction rules
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

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
