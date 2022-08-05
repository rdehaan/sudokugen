"""
Module with ASP encodings for different fish deduction rules
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

skyscraper = DeductionRule(
    "skyscraper",
    """
    derivable(Mode,(skyscraper_or(V,C2,C4))) :-
        use_technique(Mode,skyscraper),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 != G2, G1 != G3,
        G2 != G3,
        group_type(G1,T1), group_type(G2,T1), T1 != block,
        group_type(G3,T2), T2 != block, T1 != T2,
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
        not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,skyscraper),
        deduction_mode(Mode), value(V),
        derivable(Mode,skyscraper_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).
    """
)
