"""
Module with ASP encodings for different deduction rules that don't fit in any
other category
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

empty_rectangle = DeductionRule(
    "empty_rectangle",
    """
    derivable(Mode,eri(V,C,Block)) :-
        use_technique(Mode,empty_rectangle),
        deduction_mode(Mode),
        value(V),
        group(Block), group_type(Block,block),
        group(Row), group_type(Row,row),
        group(Col), group_type(Col,column),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,Block),
            not in_group(D,Row), not in_group(D,Col);
        cell(C), in_group(C,Block),
        in_group(C,Row), in_group(C,Col).
    derivable(Mode,strike(C1,V)) :-
        use_technique(Mode,empty_rectangle),
        deduction_mode(Mode),
        value(V),
        cell(C1), cell(C2), cell(C3), cell(C4),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        different_cells(C3,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        group(G1), in_group(C1,G1), in_group(C2,G1),
        group_type(G1,(row;column)),
        derivable(Mode,eri(V,C2,Block)), in_group(C2,Block),
        not in_group(C1,Block),
        not in_group(C3,Block),
        not in_group(C4,Block),
        group(G2), in_group(C2,G2), in_group(C3,G2),
        group_type(G2,(row;column)),
        group(G3), in_group(C3,G3), in_group(C4,G3),
        group_type(G3,(row;column)),
        derivable(Mode,strike(D,V)) : cell(D), in_group(D,G3),
            different_cells(D,C3), different_cells(D,C4);
        group(G4), in_group(C1,G4), in_group(C4,G4),
        group_type(G4,(row;column)).
    """
)

empty_rectangle_not_applicable_chained = DeductionRule(
    "empty_rectangle_not_applicable_chained",
    """
    derivable(Mode,eri(V,C,Block)) :-
        use_technique(Mode,empty_rectangle_not_applicable_chained),
        deduction_mode(Mode),
        value(V),
        group(Block), group_type(Block,block),
        group(Row), group_type(Row,row),
        group(Col), group_type(Col,column),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,Block),
            not in_group(D,Row), not in_group(D,Col);
        cell(C), in_group(C,Block),
        in_group(C,Row), in_group(C,Col).
    :- use_technique(Mode,empty_rectangle_not_applicable_chained),
        deduction_mode(Mode),
        value(V),
        cell(C1), cell(C2), cell(C3), cell(C4),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        different_cells(C3,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        group(G1), in_group(C1,G1), in_group(C2,G1),
        group_type(G1,(row;column)),
        derivable(Mode,eri(V,C2,Block)), in_group(C2,Block),
        not in_group(C1,Block),
        not in_group(C3,Block),
        not in_group(C4,Block),
        group(G2), in_group(C2,G2), in_group(C3,G2),
        group_type(G2,(row;column)),
        group(G3), in_group(C3,G3), in_group(C4,G3),
        group_type(G3,(row;column)),
        derivable(Mode,strike(D,V)) : cell(D), in_group(D,G3),
            different_cells(D,C3), different_cells(D,C4);
        group(G4), in_group(C1,G4), in_group(C4,G4),
        group_type(G4,(row;column)),
        not derivable(Mode,strike(C1,V)).
    """
)

bug1_protection_chained = DeductionRule(
    "bug1_protection_chained",
    """
    2 { non_binary_cell(Mode,C) : cell(C) } 2 :-
        deduction_mode(Mode),
        use_technique(Mode,bug1_protection_chained).
    :- deduction_mode(Mode),
        use_technique(Mode,bug1_protection_chained),
        non_binary_cell(Mode,C), cell(C),
        not 3 { not derivable(Mode,strike(C,W)) :
            not derivable(Mode,strike(C,W)), value(W) }.
    """
)
