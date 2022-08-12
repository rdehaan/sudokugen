"""
Module with ASP encodings for different fish deduction rules
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

turbot_fish = DeductionRule(
    "turbot_fish",
    """
    derivable(Mode,(turbot_fish_or(V,C2,C4))) :-
        use_technique(Mode,turbot_fish),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 != G2, G1 != G3,
        G2 != G3,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,turbot_fish),
        deduction_mode(Mode), value(V),
        derivable(Mode,turbot_fish_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).
    """
)

turbot_fish_proper_chained = DeductionRule(
    "turbot_fish_proper_chained",
    """
    derivable(Mode,(turbot_fish_or(V,C2,C4))) :-
        use_technique(Mode,turbot_fish_proper_chained),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 != G2, G1 != G3,
        G2 != G3,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        not derivable(Mode,strike(C3,V)),
        not derivable(Mode,strike(C4,V)).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,turbot_fish_proper_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,turbot_fish_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).
    """
)

turbot_fish_forced_shot_chained = DeductionRule(
    "turbot_fish_forced_shot_chained",
    """
    1 { choice(Mode,turbot_fish_value(V)) : value(V) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_cell1(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_cell2(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_cell3(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_cell4(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_target_cell(C)) : cell(C),
        not certainly_not_erased(C) } :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_group1(G)) : group(G) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_group2(G)) : group(G) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,turbot_fish_group3(G)) : group(G) } 1 :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode).

    :- choice(Mode,turbot_fish_cell1(C)), choice(Mode,turbot_fish_cell2(C)).
    :- choice(Mode,turbot_fish_cell1(C)), choice(Mode,turbot_fish_cell3(C)).
    :- choice(Mode,turbot_fish_cell1(C)), choice(Mode,turbot_fish_cell4(C)).
    :- choice(Mode,turbot_fish_cell2(C)), choice(Mode,turbot_fish_cell3(C)).
    :- choice(Mode,turbot_fish_cell2(C2)), choice(Mode,turbot_fish_cell4(C4)),
        C2 >= C4.
    :- choice(Mode,turbot_fish_cell3(C)), choice(Mode,turbot_fish_cell4(C)).
    :- choice(Mode,turbot_fish_cell1(C)),
        choice(Mode,turbot_fish_target_cell(C)).
    :- choice(Mode,turbot_fish_cell2(C)),
        choice(Mode,turbot_fish_target_cell(C)).
    :- choice(Mode,turbot_fish_cell3(C)),
        choice(Mode,turbot_fish_target_cell(C)).
    :- choice(Mode,turbot_fish_cell4(C)),
        choice(Mode,turbot_fish_target_cell(C)).

    :- choice(Mode,turbot_fish_group1(G)), choice(Mode,turbot_fish_group2(G)).
    :- choice(Mode,turbot_fish_group1(G)), choice(Mode,turbot_fish_group3(G)).
    :- choice(Mode,turbot_fish_group2(G)), choice(Mode,turbot_fish_group3(G)).

    :- choice(Mode,turbot_fish_cell1(C1)), choice(Mode,turbot_fish_group1(G1)),
        not in_group(C1,G1).
    :- choice(Mode,turbot_fish_cell2(C2)), choice(Mode,turbot_fish_group1(G1)),
        not in_group(C2,G1).
    :- choice(Mode,turbot_fish_cell1(C1)), choice(Mode,turbot_fish_group2(G2)),
        not in_group(C1,G2).
    :- choice(Mode,turbot_fish_cell3(C3)), choice(Mode,turbot_fish_group2(G2)),
        not in_group(C3,G2).
    :- choice(Mode,turbot_fish_cell3(C3)), choice(Mode,turbot_fish_group3(G3)),
        not in_group(C3,G3).
    :- choice(Mode,turbot_fish_cell4(C4)), choice(Mode,turbot_fish_group3(G3)),
        not in_group(C4,G3).

    :- choice(Mode,turbot_fish_cell2(C2)),
        choice(Mode,turbot_fish_target_cell(C)),
        not share_active_group(Mode,C2,C).
    :- choice(Mode,turbot_fish_cell4(C4)),
        choice(Mode,turbot_fish_target_cell(C)),
        not share_active_group(Mode,C4,C).

    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell1(C1)),
        choice(Mode,turbot_fish_value(V)),
        derivable(Mode,strike(C1,V)).
    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell2(C2)),
        choice(Mode,turbot_fish_value(V)),
        derivable(Mode,strike(C2,V)).
    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell3(C3)),
        choice(Mode,turbot_fish_value(V)),
        derivable(Mode,strike(C3,V)).
    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell4(C4)),
        choice(Mode,turbot_fish_value(V)),
        derivable(Mode,strike(C4,V)).

    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell1(C1)),
        choice(Mode,turbot_fish_cell2(C2)),
        choice(Mode,turbot_fish_group1(G1)),
        choice(Mode,turbot_fish_value(V)),
        cell(C), in_group(C,G1),
        different_cells(C,C1), different_cells(C,C2),
        not derivable(Mode,strike(C,V)).
    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell3(C3)),
        choice(Mode,turbot_fish_cell4(C4)),
        choice(Mode,turbot_fish_group3(G3)),
        choice(Mode,turbot_fish_value(V)),
        cell(C), in_group(C,G3),
        different_cells(C,C3), different_cells(C,C4),
        not derivable(Mode,strike(C,V)).

    :- use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_target_cell(C)),
        choice(Mode,turbot_fish_value(V)),
        derivable(Mode,strike(C,V)).

    derivable(Mode,pre_strike(C,V)) :-
        use_technique(Mode,turbot_fish_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,turbot_fish_cell2(C2)),
        choice(Mode,turbot_fish_cell4(C4)),
        choice(Mode,turbot_fish_value(V)),
        cell(C),
        share_active_group(Mode,C,C2),
        share_active_group(Mode,C,C4),
        different_cells(C,C2), different_cells(C,C4).
    """
)

turbot_fish_not_applicable_chained = DeductionRule(
    "turbot_fish_not_applicable_chained",
    """
    derivable(Mode,(turbot_fish_or(V,C2,C4))) :-
        use_technique(Mode,turbot_fish_not_applicable_chained),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 != G2, G1 != G3,
        G2 != G3,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        %not share_active_group(Mode,C2,C4), %%%
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        not derivable(Mode,strike(C3,V)),
        not derivable(Mode,strike(C4,V)).
    :- use_technique(Mode,turbot_fish_not_applicable_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,turbot_fish_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        not derivable(Mode,strike(C,V)).
    """
)

skyscraper = DeductionRule(
    "skyscraper",
    """
    derivable(Mode,(skyscraper_or(V,C2,C4))) :-
        use_technique(Mode,skyscraper),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 < G2, G1 != G3,
        G2 != G3,
        group_type(G1,T1), group_type(G2,T1), T1 != block,
        group_type(G3,T2), T2 != block, T1 != T2,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
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

skyscraper_forced_shot_chained = DeductionRule(
    "skyscraper_forced_shot_chained",
    """
    1 { choice(Mode,skyscraper_value(V)) : value(V) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_cell1(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_cell2(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_cell3(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_cell4(C)) : cell(C),
        not certainly_not_erased(C) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_target_cell(C)) : cell(C),
        not certainly_not_erased(C) } :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_group1(G)) : group(G) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_group2(G)) : group(G) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).
    1 { choice(Mode,skyscraper_group3(G)) : group(G) } 1 :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode).

    :- choice(Mode,skyscraper_cell1(C)), choice(Mode,skyscraper_cell2(C)).
    :- choice(Mode,skyscraper_cell1(C)), choice(Mode,skyscraper_cell3(C)).
    :- choice(Mode,skyscraper_cell1(C)), choice(Mode,skyscraper_cell4(C)).
    :- choice(Mode,skyscraper_cell2(C)), choice(Mode,skyscraper_cell3(C)).
    :- choice(Mode,skyscraper_cell2(C2)), choice(Mode,skyscraper_cell4(C4)),
        C2 >= C4.
    :- choice(Mode,skyscraper_cell3(C)), choice(Mode,skyscraper_cell4(C)).
    :- choice(Mode,skyscraper_cell1(C)),
        choice(Mode,skyscraper_target_cell(C)).
    :- choice(Mode,skyscraper_cell2(C)),
        choice(Mode,skyscraper_target_cell(C)).
    :- choice(Mode,skyscraper_cell3(C)),
        choice(Mode,skyscraper_target_cell(C)).
    :- choice(Mode,skyscraper_cell4(C)),
        choice(Mode,skyscraper_target_cell(C)).

    :- choice(Mode,skyscraper_group1(G)), choice(Mode,skyscraper_group2(G)).
    :- choice(Mode,skyscraper_group1(G)), choice(Mode,skyscraper_group3(G)).
    :- choice(Mode,skyscraper_group2(G)), choice(Mode,skyscraper_group3(G)).
    :- choice(Mode,skyscraper_cell1(C1)), choice(Mode,skyscraper_group1(G1)),
        not in_group(C1,G1).
    :- choice(Mode,skyscraper_cell2(C2)), choice(Mode,skyscraper_group1(G1)),
        not in_group(C2,G1).
    :- choice(Mode,skyscraper_cell1(C1)), choice(Mode,skyscraper_group2(G2)),
        not in_group(C1,G2).
    :- choice(Mode,skyscraper_cell3(C3)), choice(Mode,skyscraper_group2(G2)),
        not in_group(C3,G2).
    :- choice(Mode,skyscraper_cell3(C3)), choice(Mode,skyscraper_group3(G3)),
        not in_group(C3,G3).
    :- choice(Mode,skyscraper_cell4(C4)), choice(Mode,skyscraper_group3(G3)),
        not in_group(C4,G3).

    :- choice(Mode,skyscraper_group1(G)), group_type(G,block).
    :- choice(Mode,skyscraper_group2(G)), group_type(G,block).
    :- choice(Mode,skyscraper_group3(G)), group_type(G,block).
    :- choice(Mode,skyscraper_group1(G1)),
        choice(Mode,skyscraper_group2(G2)),
        group_type(G1,T), group_type(G2,T).
    :- choice(Mode,skyscraper_group2(G2)),
        choice(Mode,skyscraper_group3(G3)),
        group_type(G2,T), group_type(G3,T).
    :- choice(Mode,skyscraper_cell2(C2)),
        choice(Mode,skyscraper_cell4(C4)),
        share_active_group(Mode,C2,C4).

    :- choice(Mode,skyscraper_cell2(C2)),
        choice(Mode,skyscraper_target_cell(C)),
        not share_active_group(Mode,C2,C).
    :- choice(Mode,skyscraper_cell4(C4)),
        choice(Mode,skyscraper_target_cell(C)),
        not share_active_group(Mode,C4,C).

    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell1(C1)),
        choice(Mode,skyscraper_value(V)),
        derivable(Mode,strike(C1,V)).
    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell2(C2)),
        choice(Mode,skyscraper_value(V)),
        derivable(Mode,strike(C2,V)).
    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell3(C3)),
        choice(Mode,skyscraper_value(V)),
        derivable(Mode,strike(C3,V)).
    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell4(C4)),
        choice(Mode,skyscraper_value(V)),
        derivable(Mode,strike(C4,V)).

    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell1(C1)),
        choice(Mode,skyscraper_cell2(C2)),
        choice(Mode,skyscraper_group1(G1)),
        choice(Mode,skyscraper_value(V)),
        cell(C), in_group(C,G1),
        different_cells(C,C1), different_cells(C,C2),
        not derivable(Mode,strike(C,V)).
    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell3(C3)),
        choice(Mode,skyscraper_cell4(C4)),
        choice(Mode,skyscraper_group3(G3)),
        choice(Mode,skyscraper_value(V)),
        cell(C), in_group(C,G3),
        different_cells(C,C3), different_cells(C,C4),
        not derivable(Mode,strike(C,V)).

    :- use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_target_cell(C)),
        choice(Mode,skyscraper_value(V)),
        derivable(Mode,strike(C,V)).

    derivable(Mode,pre_strike(C,V)) :-
        use_technique(Mode,skyscraper_forced_shot_chained),
        deduction_mode(Mode),
        choice(Mode,skyscraper_cell2(C2)),
        choice(Mode,skyscraper_cell4(C4)),
        choice(Mode,skyscraper_value(V)),
        cell(C),
        share_active_group(Mode,C,C2),
        share_active_group(Mode,C,C4),
        different_cells(C,C2), different_cells(C,C4).
    """
)

skyscraper_not_applicable_chained = DeductionRule(
    "skyscraper_not_applicable_chained",
    """
    derivable(Mode,(skyscraper_or(V,C2,C4))) :-
        use_technique(Mode,skyscraper_not_applicable_chained),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 < G2, G1 != G3,
        G2 != G3,
        group_type(G1,T1), group_type(G2,T1), T1 != block,
        group_type(G3,T2), T2 != block, T1 != T2,
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    :- use_technique(Mode,skyscraper_not_applicable_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,skyscraper_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        not derivable(Mode,strike(C,V)).
    """
)

two_string_kite = DeductionRule(
    "two_string_kite",
    """
    derivable(Mode,(two_string_kite_or(V,C2,C4))) :-
        use_technique(Mode,two_string_kite),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 < G2, G1 != G3,
        G2 != G3,
        group_type(G1,T1), group_type(G2,T2),
        T1 != block, T2 != block, T1 != T2,
        group_type(G3,block),
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        %not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,two_string_kite),
        deduction_mode(Mode), value(V),
        derivable(Mode,two_string_kite_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2).
    """
)

two_string_kite_not_applicable_chained = DeductionRule(
    "two_string_kite_not_applicable_chained",
    """
    derivable(Mode,(two_string_kite_or(V,C2,C4))) :-
        use_technique(Mode,two_string_kite_not_applicable_chained),
        deduction_mode(Mode), value(V),
        group(G1), active_group(Mode,G1),
        group(G2), active_group(Mode,G2),
        group(G3), active_group(Mode,G3),
        G1 < G2, G1 != G3,
        G2 != G3,
        group_type(G1,T1), group_type(G2,T2),
        T1 != block, T2 != block, T1 != T2,
        group_type(G3,block),
        in_group(C1,G1), in_group(C2,G1), different_cells(C1,C2),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G1),
            different_cells(D,C1), different_cells(D,C2);
        in_group(C3,G2), in_group(C4,G2), different_cells(C3,C4),
        derivable(Mode,strike(D,V)) :
            cell(D), in_group(D,G2),
            different_cells(D,C3), different_cells(D,C4);
        different_cells(C1,C3), different_cells(C1,C4),
        different_cells(C2,C3), different_cells(C2,C4),
        in_group(C1,G3), in_group(C3,G3),
        %not share_active_group(Mode,C2,C4),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        not certainly_not_erased(C4).
    :- use_technique(Mode,two_string_kite_not_applicable_chained),
        deduction_mode(Mode), value(V),
        derivable(Mode,two_string_kite_or(V,C1,C2)),
        not certainly_not_erased(C),
        different_cells(C,C1),
        different_cells(C,C2),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        not derivable(Mode,strike(C,V)).
    """
)
