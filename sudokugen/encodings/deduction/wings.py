"""
Module with ASP encodings for different wing deduction rules
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

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

xy_wing_proper_chained = DeductionRule(
    "xy_wing_proper_chained",
    """
    derivable(Mode,xy_wing_or(0,C,V1,C,V2)) :-
        use_technique(Mode,xy_wing_proper_chained), deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2),
        cell(C), not certainly_not_erased(C),
        derivable(Mode,strike(C,V)) :
            value(V), different_values(V,V1), different_values(V,V2);
        not derivable(Mode,strike(C,V1)),
        not derivable(Mode,strike(C,V2)).
    derivable(Mode,xy_wing_or(D,C1,V1,C2,V2)) :-
        derivable(Mode,xy_wing_or(D,C2,V2,C1,V1)).
    derivable(Mode,xy_wing_or(1,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing_proper_chained), deduction_mode(Mode),
        derivable(Mode,xy_wing_or(0,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3.
    derivable(Mode,xy_wing_or(2,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing_proper_chained), deduction_mode(Mode),
        derivable(Mode,xy_wing_or(1,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3, V1 = V4.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,xy_wing_proper_chained), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V),
        derivable(Mode,xy_wing_or(2,C1,V,C2,V)),
        share_group(C,C1), share_group(C,C2).

    :- derivable(_,xy_wing_or(_,C1,V1,C2,V2)),
        not solution(C1,V1), not solution(C2,V2).
    """
)

xy_wing_forced_shot_chained = DeductionRule(
    "xy_wing_forced_shot_chained",
    """
    1 { choice(Mode,xy_wing_value1(V)) : value(V) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xy_wing_value2(V)) : value(V) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xy_wing_value3(V)) : value(V) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    :- choice(Mode,xy_wing_value1(V)), choice(Mode,xy_wing_value2(V)).
    :- choice(Mode,xy_wing_value1(V)), choice(Mode,xy_wing_value3(V)).
    :- choice(Mode,xy_wing_value2(V)), choice(Mode,xy_wing_value3(V)).
    :- choice(Mode,xy_wing_value2(V2)), choice(Mode,xy_wing_value3(V3)),
        V3 > V2.
    1 { choice(Mode,xy_wing_cell1(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xy_wing_cell2(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xy_wing_cell3(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xy_wing_target_cell(C)) : cell(C),
        not certainly_not_erased(C) } :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode).

    :- choice(Mode,xy_wing_cell1(C)), choice(Mode,xy_wing_cell2(C)).
    :- choice(Mode,xy_wing_cell1(C)), choice(Mode,xy_wing_cell3(C)).
    :- choice(Mode,xy_wing_cell2(C)), choice(Mode,xy_wing_cell3(C)).
    :- choice(Mode,xy_wing_cell1(C)), choice(Mode,xy_wing_target_cell(C)).
    :- choice(Mode,xy_wing_cell2(C)), choice(Mode,xy_wing_target_cell(C)).
    :- choice(Mode,xy_wing_cell3(C)), choice(Mode,xy_wing_target_cell(C)).

    :- choice(Mode,xy_wing_cell1(C1)), choice(Mode,xy_wing_cell2(C2)),
        not share_active_group(Mode,C1,C2).
    :- choice(Mode,xy_wing_cell2(C2)), choice(Mode,xy_wing_cell3(C3)),
        not share_active_group(Mode,C2,C3).
    :- choice(Mode,xy_wing_cell1(C1)), choice(Mode,xy_wing_cell3(C3)),
        share_active_group(Mode,C1,C3).
    :- choice(Mode,xy_wing_cell1(C1)), choice(Mode,xy_wing_target_cell(C)),
        not share_active_group(Mode,C1,C).
    :- choice(Mode,xy_wing_cell3(C3)), choice(Mode,xy_wing_target_cell(C)),
        not share_active_group(Mode,C3,C).

    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell1(C1)),
        choice(Mode,xy_wing_value1(V1)),
        derivable(Mode,strike(C1,V1)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell1(C1)),
        choice(Mode,xy_wing_value2(V2)),
        derivable(Mode,strike(C1,V2)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell1(C1)),
        choice(Mode,xy_wing_value1(V1)),
        choice(Mode,xy_wing_value2(V2)),
        value(V), different_values(V,V1), different_values(V,V2),
        not derivable(Mode,strike(C1,V)).

    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell2(C2)),
        choice(Mode,xy_wing_value2(V2)),
        derivable(Mode,strike(C2,V2)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell2(C2)),
        choice(Mode,xy_wing_value3(V3)),
        derivable(Mode,strike(C2,V3)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell2(C2)),
        choice(Mode,xy_wing_value2(V2)),
        choice(Mode,xy_wing_value3(V3)),
        value(V), different_values(V,V2), different_values(V,V3),
        not derivable(Mode,strike(C2,V)).

    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell3(C3)),
        choice(Mode,xy_wing_value1(V1)),
        derivable(Mode,strike(C3,V1)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell3(C3)),
        choice(Mode,xy_wing_value3(V3)),
        derivable(Mode,strike(C3,V3)).
    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_cell3(C3)),
        choice(Mode,xy_wing_value1(V1)),
        choice(Mode,xy_wing_value3(V3)),
        value(V), different_values(V,V1), different_values(V,V3),
        not derivable(Mode,strike(C3,V)).

    :- use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_target_cell(C)),
        choice(Mode,xy_wing_value1(V1)),
        derivable(Mode,strike(C,V1)).

    derivable(Mode,pre_strike(C,V1)) :-
        use_technique(Mode,xy_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xy_wing_target_cell(C)),
        choice(Mode,xy_wing_value1(V1)).
    """
)

xy_wing_not_applicable_chained = DeductionRule(
    "xy_wing_not_applicable_chained",
    """
    derivable(Mode,xy_wing_or(0,C,V1,C,V2)) :-
        use_technique(Mode,xy_wing_not_applicable_chained),
        deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2),
        cell(C), not certainly_not_erased(C),
        derivable(Mode,strike(C,V)) :
            value(V), different_values(V,V1), different_values(V,V2);
        not derivable(Mode,strike(C,V1)),
        not derivable(Mode,strike(C,V2)).
    derivable(Mode,xy_wing_or(D,C1,V1,C2,V2)) :-
        derivable(Mode,xy_wing_or(D,C2,V2,C1,V1)).
    derivable(Mode,xy_wing_or(1,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing_not_applicable_chained),
        deduction_mode(Mode),
        derivable(Mode,xy_wing_or(0,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3.
    derivable(Mode,xy_wing_or(2,C1,V1,C4,V4)) :-
        use_technique(Mode,xy_wing_not_applicable_chained),
        deduction_mode(Mode),
        derivable(Mode,xy_wing_or(1,C1,V1,C2,V2)),
        derivable(Mode,xy_wing_or(0,C3,V3,C4,V4)),
        share_group(C2,C3), V2 = V3, V1 = V4.
    :- use_technique(Mode,xy_wing_not_applicable_chained),
        deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        value(V),
        derivable(Mode,xy_wing_or(2,C1,V,C2,V)),
        share_group(C,C1), share_group(C,C2),
        not derivable(Mode,strike(C,V)).

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
    derivable(Mode,pre_strike(C,V2)) :-
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

xyz_wing_forced_shot_chained = DeductionRule(
    "xyz_wing_forced_shot_chained",
    """
    1 { choice(Mode,xyz_wing_value1(V)) : value(V) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xyz_wing_value2(V)) : value(V) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xyz_wing_value3(V)) : value(V) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    :- choice(Mode,xyz_wing_value1(V)), choice(Mode,xyz_wing_value2(V)).
    :- choice(Mode,xyz_wing_value1(V)), choice(Mode,xyz_wing_value3(V)).
    :- choice(Mode,xyz_wing_value2(V)), choice(Mode,xyz_wing_value3(V)).
    :- choice(Mode,xyz_wing_value2(V2)), choice(Mode,xyz_wing_value3(V3)),
        V3 > V2.
    1 { choice(Mode,xyz_wing_cell1(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xyz_wing_cell2(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xyz_wing_cell3(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,xyz_wing_target_cell(C)) : cell(C),
        not certainly_not_erased(C) } :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode).

    :- choice(Mode,xyz_wing_cell1(C)), choice(Mode,xyz_wing_cell2(C)).
    :- choice(Mode,xyz_wing_cell1(C)), choice(Mode,xyz_wing_cell3(C)).
    :- choice(Mode,xyz_wing_cell2(C)), choice(Mode,xyz_wing_cell3(C)).
    :- choice(Mode,xyz_wing_cell1(C)), choice(Mode,xyz_wing_target_cell(C)).
    :- choice(Mode,xyz_wing_cell2(C)), choice(Mode,xyz_wing_target_cell(C)).
    :- choice(Mode,xyz_wing_cell3(C)), choice(Mode,xyz_wing_target_cell(C)).

    :- choice(Mode,xyz_wing_cell1(C1)), choice(Mode,xyz_wing_cell2(C2)),
        not share_active_group(Mode,C1,C2).
    :- choice(Mode,xyz_wing_cell2(C2)), choice(Mode,xyz_wing_cell3(C3)),
        not share_active_group(Mode,C2,C3).
    :- choice(Mode,xyz_wing_cell1(C1)), choice(Mode,xyz_wing_cell3(C3)),
        share_active_group(Mode,C1,C3).
    :- choice(Mode,xyz_wing_cell1(C1)), choice(Mode,xyz_wing_target_cell(C)),
        not share_active_group(Mode,C1,C).
    :- choice(Mode,xyz_wing_cell2(C2)), choice(Mode,xyz_wing_target_cell(C)),
        not share_active_group(Mode,C2,C).
    :- choice(Mode,xyz_wing_cell3(C3)), choice(Mode,xyz_wing_target_cell(C)),
        not share_active_group(Mode,C3,C).

    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell1(C1)),
        choice(Mode,xyz_wing_value1(V1)),
        derivable(Mode,strike(C1,V1)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell1(C1)),
        choice(Mode,xyz_wing_value2(V2)),
        derivable(Mode,strike(C1,V2)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell1(C1)),
        choice(Mode,xyz_wing_value1(V1)),
        choice(Mode,xyz_wing_value2(V2)),
        value(V), different_values(V,V1), different_values(V,V2),
        not derivable(Mode,strike(C1,V)).

    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell2(C2)),
        choice(Mode,xyz_wing_value1(V1)),
        derivable(Mode,strike(C2,V1)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell2(C2)),
        choice(Mode,xyz_wing_value2(V2)),
        derivable(Mode,strike(C2,V2)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell2(C2)),
        choice(Mode,xyz_wing_value3(V3)),
        derivable(Mode,strike(C2,V3)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell2(C2)),
        choice(Mode,xyz_wing_value1(V1)),
        choice(Mode,xyz_wing_value2(V2)),
        choice(Mode,xyz_wing_value3(V3)),
        value(V), different_values(V,V1),
        different_values(V,V2), different_values(V,V3),
        not derivable(Mode,strike(C2,V)).

    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell3(C3)),
        choice(Mode,xyz_wing_value1(V1)),
        derivable(Mode,strike(C3,V1)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell3(C3)),
        choice(Mode,xyz_wing_value3(V3)),
        derivable(Mode,strike(C3,V3)).
    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_cell3(C3)),
        choice(Mode,xyz_wing_value1(V1)),
        choice(Mode,xyz_wing_value3(V3)),
        value(V), different_values(V,V1), different_values(V,V3),
        not derivable(Mode,strike(C3,V)).

    :- use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_target_cell(C)),
        choice(Mode,xyz_wing_value1(V1)),
        derivable(Mode,strike(C,V1)).

    derivable(Mode,pre_strike(C,V1)) :-
        use_technique(Mode,xyz_wing_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,xyz_wing_target_cell(C)),
        choice(Mode,xyz_wing_value1(V1)).
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

x_wing_not_applicable_chained = DeductionRule(
    "x_wing_not_applicable_chained",
    """
    derivable(Mode,(x_wing_snyder(V,C1,C3,G3);x_wing_snyder(V,C2,C4,G4))) :-
        use_technique(Mode,x_wing_not_applicable_chained),
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
    :- use_technique(Mode,x_wing_not_applicable_chained),
        deduction_mode(Mode), value(V),
        group(G), active_group(Mode,G),
        cell(C1), cell(C2), in_group(C1,G), in_group(C2,G),
        derivable(Mode,x_wing_snyder(V,C1,C2,G)),
        different_cells(C,C1), different_cells(C,C2),
        cell(C), in_group(C,G), not certainly_not_erased(C),
        not derivable(Mode,strike(C,V)).
    """
)

# w_wing = DeductionRule(
#     "w_wing",
#     """
#     derivable(Mode,w_wing_or(V2,C1,C4)) :-
#         deduction_mode(Mode), use_technique(Mode,w_wing),
#         value(V1), value(V2), V1 != V2,
#         cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         C1 < C4,
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,strike(C1,V)) :
#             value(V), V != V1, V != V2;
#         derivable(Mode,strike(C4,V)) :
#             value(V), V != V1, V != V2;
#         active_group(Mode,G),
#         in_group(C2,G), in_group(C3,G),
#         derivable(Mode,strike(D,V1)) :
#             cell(D), in_group(D,G),
#             different_cells(C2,D), different_cells(C3,D);
#         share_active_group(Mode,C1,C2),
#         share_active_group(Mode,C3,C4),
#         not share_group(C1,C3),
#         not share_group(C2,C4),
#         not share_group(C1,C4).
#     derivable(Mode,strike(C,V)) :-
#         use_technique(Mode,w_wing),
#         deduction_mode(Mode), value(V),
#         derivable(Mode,w_wing_or(V,C1,C2)),
#         cell(C), not certainly_not_erased(C),
#         different_cells(C,C1),
#         different_cells(C,C2),
#         share_active_group(Mode,C,C1),
#         share_active_group(Mode,C,C2).
#
#     :- derivable(_,w_wing_or(V,C1,C2)),
#         not solution(C1,V), not solution(C2,V).
#     """
# )

w_wing = DeductionRule(
    "w_wing",
    """
    derivable(Mode,w_wing_wsw(V,C1,C4)) :-
        deduction_mode(Mode), use_technique(Mode,w_wing),
        value(V),
        cell(C1), cell(C2), cell(C3), cell(C4),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        different_cells(C3,C4),
        C1 < C4,
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        active_group(Mode,G),
        in_group(C2,G), in_group(C3,G),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G),
            different_cells(C2,D), different_cells(C3,D);
        share_active_group(Mode,C1,C2),
        share_active_group(Mode,C3,C4),
        not share_group(C1,C3),
        not share_group(C2,C4),
        not share_group(C1,C4).
    derivable(Mode,w_wing_or(V2,C1,C2)) :-
        deduction_mode(Mode), use_technique(Mode,w_wing),
        value(V1), value(V2), V1 != V2,
        cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        derivable(Mode,w_wing_wsw(V1,C1,C2)),
        derivable(Mode,strike(C1,V)) :
            value(V), V != V1, V != V2;
        derivable(Mode,strike(C2,V)) :
            value(V), V != V1, V != V2.
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,w_wing),
        deduction_mode(Mode), value(V),
        derivable(Mode,w_wing_or(V,C1,C2)),
        cell(C), not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).

    :- derivable(_,w_wing_or(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)

w_wing_proper_chained = DeductionRule(
    "w_wing_proper_chained",
    """
    derivable(Mode,w_wing_wsw(V,C1,C4)) :-
        deduction_mode(Mode), use_technique(Mode,w_wing_proper_chained),
        value(V),
        cell(C1), cell(C2), cell(C3), cell(C4),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        different_cells(C3,C4),
        C1 < C4,
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        active_group(Mode,G),
        in_group(C2,G), in_group(C3,G),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G),
            different_cells(C2,D), different_cells(C3,D);
        share_active_group(Mode,C1,C2),
        share_active_group(Mode,C3,C4),
        not share_group(C1,C3),
        not share_group(C2,C4),
        not share_group(C1,C4),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        not derivable(Mode,strike(C3,V)),
        not derivable(Mode,strike(C4,V)).
    derivable(Mode,w_wing_or(V2,C1,C2)) :-
        deduction_mode(Mode), use_technique(Mode,w_wing_proper_chained),
        value(V1), value(V2), V1 != V2,
        cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        derivable(Mode,w_wing_wsw(V1,C1,C2)),
        derivable(Mode,strike(C1,V)) :
            value(V), V != V1, V != V2;
        derivable(Mode,strike(C2,V)) :
            value(V), V != V1, V != V2;
        not derivable(Mode,strike(C1,V2)),
        not derivable(Mode,strike(C2,V2)).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,w_wing_proper_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,w_wing_or(V,C1,C2)),
        cell(C), not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).

    :- derivable(_,w_wing_or(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)

# w_wing_not_applicable_chained = DeductionRule(
#     "w_wing_not_applicable_chained",
#     """
#     derivable(Mode,w_wing_or(V2,C1,C4)) :-
#         deduction_mode(Mode), use_technique(Mode,w_wing_not_applicable_chained),
#         value(V1), value(V2), V1 != V2,
#         cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         C1 < C4,
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,strike(C1,V)) :
#             value(V), V != V1, V != V2;
#         derivable(Mode,strike(C4,V)) :
#             value(V), V != V1, V != V2;
#         active_group(Mode,G),
#         in_group(C2,G), in_group(C3,G),
#         derivable(Mode,strike(D,V1)) :
#             cell(D), in_group(D,G),
#             different_cells(C2,D), different_cells(C3,D);
#         share_active_group(Mode,C1,C2),
#         share_active_group(Mode,C3,C4),
#         not share_group(C1,C3),
#         not share_group(C2,C4),
#         not share_group(C1,C4).
#     :- use_technique(Mode,w_wing_not_applicable_chained),
#         deduction_mode(Mode), value(V),
#         derivable(Mode,w_wing_or(V,C1,C2)),
#         cell(C), not certainly_not_erased(C),
#         share_active_group(Mode,C,C1),
#         share_active_group(Mode,C,C2),
#         not derivable(Mode,strike(C,V)).
#
#     :- derivable(_,w_wing_or(V,C1,C2)),
#         not solution(C1,V), not solution(C2,V).
#     """
# )

w_wing_not_applicable_chained = DeductionRule(
    "w_wing_not_applicable_chained",
    """
    derivable(Mode,w_wing_wsw(V,C1,C4)) :-
        deduction_mode(Mode),
        use_technique(Mode,w_wing_not_applicable_chained),
        value(V),
        cell(C1), cell(C2), cell(C3), cell(C4),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        different_cells(C3,C4),
        C1 < C4,
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        active_group(Mode,G),
        in_group(C2,G), in_group(C3,G),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G),
            different_cells(C2,D), different_cells(C3,D);
        share_active_group(Mode,C1,C2),
        share_active_group(Mode,C3,C4),
        not share_group(C1,C3),
        not share_group(C2,C4),
        not share_group(C1,C4),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        not derivable(Mode,strike(C3,V)),
        not derivable(Mode,strike(C4,V)).
    derivable(Mode,w_wing_or(V2,C1,C2)) :-
        deduction_mode(Mode),
        use_technique(Mode,w_wing_not_applicable_chained),
        value(V1), value(V2), V1 != V2,
        cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        derivable(Mode,w_wing_wsw(V1,C1,C2)),
        derivable(Mode,strike(C1,V)) :
            value(V), V != V1, V != V2;
        derivable(Mode,strike(C2,V)) :
            value(V), V != V1, V != V2;
        not derivable(Mode,strike(C1,V2)),
        not derivable(Mode,strike(C2,V2)).
    :- use_technique(Mode,w_wing_not_applicable_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,w_wing_or(V,C1,C2)),
        cell(C), not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        not derivable(Mode,strike(C,V)).

    :- derivable(_,w_wing_or(V,C1,C2)),
        not solution(C1,V), not solution(C2,V).
    """
)
