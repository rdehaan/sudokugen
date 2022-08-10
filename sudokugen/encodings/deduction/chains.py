"""
Module with ASP encodings for different chain deduction rules
"""
# pylint: disable=too-many-lines

from .basic import DeductionRule

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
)

x_chain_proper_chained = DeductionRule(
    "x_chain_proper_chained",
    """
    derivable(Mode,x_chain_strong_link(V,C1,C2)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), different_cells(C1,C2),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        group(G), active_group(Mode,G),
        in_group(C1,G), in_group(C2,G),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        derivable(Mode,strike(C,V)) :
            cell(C), in_group(C,G),
            different_cells(C,C1), different_cells(C,C2).
    derivable(Mode,x_chain_weak_link(V,C1,C2)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3), different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        in_group(C1,G), in_group(C2,G), in_group(C3,G),
        not derivable(Mode,strike(C1,V)),
        not derivable(Mode,strike(C2,V)),
        not derivable(Mode,strike(C3,V)).

    derivable(Mode,x_chain_sw(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_strong_link(V,C1,C2)),
        derivable(Mode,x_chain_weak_link(V,C2,C3)).
    derivable(Mode,x_chain_ws(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_weak_link(V,C1,C2)),
        derivable(Mode,x_chain_strong_link(V,C2,C3)).

    derivable(Mode,x_chain_ss(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_sw(V,C1,C2)),
        derivable(Mode,x_chain_strong_link(V,C2,C3)).
    derivable(Mode,x_chain_ss(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_strong_link(V,C1,C2)),
        derivable(Mode,x_chain_ws(V,C2,C3)).

    derivable(Mode,x_chain_ww(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_strong_link(V,C1,C2)),
        derivable(Mode,x_chain_sw(V,C2,C3)).
    derivable(Mode,x_chain_ww(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_weak_link(V,C1,C2)),
        derivable(Mode,x_chain_sw(V,C2,C3)).
    derivable(Mode,x_chain_ww(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_ws(V,C1,C2)),
        derivable(Mode,x_chain_weak_link(V,C2,C3)).
    derivable(Mode,x_chain_ww(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_ws(V,C1,C2)),
        derivable(Mode,x_chain_strong_link(V,C2,C3)).

    derivable(Mode,x_chain_sw(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_strong_link(V,C1,C2)),
        derivable(Mode,x_chain_ww(V,C2,C3)).
    derivable(Mode,x_chain_sw(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_ss(V,C1,C2)),
        derivable(Mode,x_chain_strong_link(V,C2,C3)).
    derivable(Mode,x_chain_sw(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_ss(V,C1,C2)),
        derivable(Mode,x_chain_weak_link(V,C2,C3)).

    derivable(Mode,x_chain_ws(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_weak_link(V,C1,C2)),
        derivable(Mode,x_chain_ss(V,C2,C3)).
    derivable(Mode,x_chain_ws(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_strong_link(V,C1,C2)),
        derivable(Mode,x_chain_ss(V,C2,C3)).
    derivable(Mode,x_chain_ws(V,C1,C3)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        value(V), cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,x_chain_ww(V,C1,C2)),
        derivable(Mode,x_chain_strong_link(V,C2,C3)).

    derivable(Mode,pre_strike(C,V)) :-
        use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
        cell(C), not certainly_not_erased(C),
        cell(C1), not certainly_not_erased(C1),
        cell(C2), not certainly_not_erased(C2),
        value(V),
        derivable(Mode,x_chain_ss(V,C1,C2)),
        share_group(C,C1), share_group(C,C2),
        different_cells(C,C1),
        different_cells(C,C2),
        different_cells(C1,C2).
    """
)

# x_chain_proper_chained = DeductionRule(
#     "x_chain_proper_chained",
#     """
#     derivable(Mode,x_chain_strong_link(V,C1,C2)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), different_cells(C1,C2),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         group(G), active_group(Mode,G),
#         in_group(C1,G), in_group(C2,G),
#         not derivable(Mode,strike(C1,V)),
#         not derivable(Mode,strike(C2,V)),
#         derivable(Mode,strike(C,V)) :
#             cell(C), in_group(C,G),
#             different_cells(C,C1), different_cells(C,C2).
#     derivable(Mode,x_chain_weak_link(V,C1,C2)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), cell(C3),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C2,C3),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         in_group(C1,G), in_group(C2,G), in_group(C3,G),
#         not derivable(Mode,strike(C1,V)),
#         not derivable(Mode,strike(C2,V)),
#         not derivable(Mode,strike(C3,V)).
#
#     derivable(Mode,x_chain_ss(V,C1,C4)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,x_chain_strong_link(V,C1,C2)),
#         derivable(Mode,x_chain_strong_link(V,C2,C3)),
#         derivable(Mode,x_chain_strong_link(V,C3,C4)).
#     derivable(Mode,x_chain_ss(V,C1,C4)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,x_chain_strong_link(V,C1,C2)),
#         derivable(Mode,x_chain_weak_link(V,C2,C3)),
#         derivable(Mode,x_chain_strong_link(V,C3,C4)).
#
#     derivable(Mode,x_chain_ss(V,C1,C4)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,x_chain_ss(V,C1,C2)),
#         derivable(Mode,x_chain_strong_link(V,C2,C3)),
#         derivable(Mode,x_chain_strong_link(V,C3,C4)).
#     derivable(Mode,x_chain_ss(V,C1,C4)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         value(V), cell(C1), cell(C2), cell(C3), cell(C4),
#         different_cells(C1,C2), different_cells(C1,C3), different_cells(C1,C4),
#         different_cells(C2,C3), different_cells(C2,C4),
#         different_cells(C3,C4),
#         not certainly_not_erased(C1),
#         not certainly_not_erased(C2),
#         not certainly_not_erased(C3),
#         not certainly_not_erased(C4),
#         derivable(Mode,x_chain_ss(V,C1,C2)),
#         derivable(Mode,x_chain_weak_link(V,C2,C3)),
#         derivable(Mode,x_chain_strong_link(V,C3,C4)).
#
#     derivable(Mode,pre_strike(C,V)) :-
#         use_technique(Mode,x_chain_proper_chained), deduction_mode(Mode),
#         cell(C), not certainly_not_erased(C),
#         cell(C1), not certainly_not_erased(C1),
#         cell(C2), not certainly_not_erased(C2),
#         value(V),
#         derivable(Mode,x_chain_ss(V,C1,C2)),
#         share_group(C,C1), share_group(C,C2),
#         different_cells(C,C1),
#         different_cells(C,C2),
#         different_cells(C1,C2).
#     """
#     # """
#     # :- derivable(_,x_chain_or(C1,no(V),C2,no(V))),
#     #     solution(C1,V), solution(C2,V).
#     # :- derivable(_,x_chain_or(C1,yes(V),C2,yes(V))),
#     #     not solution(C1,V), not solution(C2,V).
#     # :- derivable(_,x_chain_or(C1,no(V),C2,yes(V))),
#     #     solution(C1,V), not solution(C2,V).
#     # :- derivable(_,x_chain_or(C1,yes(V),C2,no(V))),
#     #     not solution(C1,V), solution(C2,V).
#     # """
# )

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
    derivable(Mode,pre_strike(C,V)) :-
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

remote_pairs_chained = DeductionRule(
    "remote_pairs_chained",
    """
    derivable(Mode,rp_odd(V1,V2,C1,C2)) :-
        use_technique(Mode,remote_pairs_chained), deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), different_cells(C1,C2), C1 < C2,
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        derivable(Mode,strike(C1,V)) :
            different_values(V,V1), different_values(V,V2);
        derivable(Mode,strike(C2,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C1,C2),
        not derivable(Mode,strike(C1,V1)),
        not derivable(Mode,strike(C1,V2)),
        not derivable(Mode,strike(C2,V1)),
        not derivable(Mode,strike(C2,V2)).

    derivable(Mode,rp_odd(V1,V2,C1,C2)) :-
        derivable(Mode,rp_odd(V1,V2,C2,C1)).
    derivable(Mode,rp_even(V1,V2,C1,C2)) :-
        derivable(Mode,rp_even(V1,V2,C2,C1)).

    derivable(Mode,rp_even(V1,V2,C1,C3)) :-
        use_technique(Mode,remote_pairs_chained), deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,rp_odd(V1,V2,C1,C2)),
        derivable(Mode,strike(C3,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C2,C3),
        not derivable(Mode,strike(C3,V1)),
        not derivable(Mode,strike(C3,V2)).
    derivable(Mode,rp_odd(V1,V2,C1,C3)) :-
        use_technique(Mode,remote_pairs_chained), deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,rp_even(V1,V2,C1,C2)),
        derivable(Mode,strike(C3,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C2,C3),
        not derivable(Mode,strike(C3,V1)),
        not derivable(Mode,strike(C3,V2)).

    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,remote_pairs_chained), deduction_mode(Mode),
        value(V), cell(C),
        derivable(Mode,rp_odd(V,_,C1,C2)),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        different_cells(C,C1),
        different_cells(C,C2).
    derivable(Mode,strike(C,V)) :-
        use_technique(Mode,remote_pairs_chained), deduction_mode(Mode),
        value(V), cell(C),
        derivable(Mode,rp_odd(_,V,C1,C2)),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        different_cells(C,C1),
        different_cells(C,C2).

    :- derivable(_,rp_even(V1,V2,C1,C2)),
        solution(C1,V1), solution(C2,V2).
    :- derivable(_,rp_even(V1,V2,C1,C2)),
        solution(C1,V2), solution(C2,V1).
    :- derivable(_,rp_odd(V1,V2,C1,C2)),
        solution(C1,V1), solution(C2,V1).
    :- derivable(_,rp_odd(V1,V2,C1,C2)),
        solution(C1,V2), solution(C2,V2).
    """
)

remote_pairs_not_applicable_chained = DeductionRule(
    "remote_pairs_not_applicable_chained",
    """
    derivable(Mode,rp_odd(V1,V2,C1,C2)) :-
        use_technique(Mode,remote_pairs_not_applicable_chained),
        deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), different_cells(C1,C2), C1 < C2,
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        derivable(Mode,strike(C1,V)) :
            different_values(V,V1), different_values(V,V2);
        derivable(Mode,strike(C2,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C1,C2),
        not derivable(Mode,strike(C1,V1)),
        not derivable(Mode,strike(C1,V2)),
        not derivable(Mode,strike(C2,V1)),
        not derivable(Mode,strike(C2,V2)).

    derivable(Mode,rp_odd(V1,V2,C1,C2)) :-
        derivable(Mode,rp_odd(V1,V2,C2,C1)).
    derivable(Mode,rp_even(V1,V2,C1,C2)) :-
        derivable(Mode,rp_even(V1,V2,C2,C1)).

    derivable(Mode,rp_even(V1,V2,C1,C3)) :-
        use_technique(Mode,remote_pairs_not_applicable_chained),
        deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,rp_odd(V1,V2,C1,C2)),
        derivable(Mode,strike(C3,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C2,C3),
        not derivable(Mode,strike(C3,V1)),
        not derivable(Mode,strike(C3,V2)).
    derivable(Mode,rp_odd(V1,V2,C1,C3)) :-
        use_technique(Mode,remote_pairs_not_applicable_chained),
        deduction_mode(Mode),
        value(V1), value(V2), different_values(V1,V2), V1 < V2,
        cell(C1), cell(C2), cell(C3),
        different_cells(C1,C2), different_cells(C1,C3),
        different_cells(C2,C3),
        not certainly_not_erased(C1),
        not certainly_not_erased(C2),
        not certainly_not_erased(C3),
        derivable(Mode,rp_even(V1,V2,C1,C2)),
        derivable(Mode,strike(C3,V)) :
            different_values(V,V1), different_values(V,V2);
        share_active_group(Mode,C2,C3),
        not derivable(Mode,strike(C3,V1)),
        not derivable(Mode,strike(C3,V2)).

    :- use_technique(Mode,remote_pairs_not_applicable_chained),
        deduction_mode(Mode),
        value(V), cell(C),
        derivable(Mode,rp_odd(V,_,C1,C2)),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        different_cells(C,C1),
        different_cells(C,C2),
        not derivable(Mode,strike(C,V)).
    :- use_technique(Mode,remote_pairs_not_applicable_chained),
        deduction_mode(Mode),
        value(V), cell(C),
        derivable(Mode,rp_odd(_,V,C1,C2)),
        share_active_group(Mode,C,C1),
        share_active_group(Mode,C,C2),
        different_cells(C,C1),
        different_cells(C,C2),
        not derivable(Mode,strike(C,V)).

    :- derivable(_,rp_even(V1,V2,C1,C2)),
        solution(C1,V1), solution(C2,V2).
    :- derivable(_,rp_even(V1,V2,C1,C2)),
        solution(C1,V2), solution(C2,V1).
    :- derivable(_,rp_odd(V1,V2,C1,C2)),
        solution(C1,V1), solution(C2,V1).
    :- derivable(_,rp_odd(V1,V2,C1,C2)),
        solution(C1,V2), solution(C2,V2).
    """
)

remote_pairs_protection_chained = DeductionRule(
    "remote_pairs_protection_chained",
    """
    derivable(Mode,pair_left(V1,V2,C)) :-
        deduction_mode(Mode),
        use_technique(Mode,remote_pairs_protection_chained),
        value(V1), value(V2), V1 < V2,
        cell(C),
        not derivable(Mode,strike(C,V1)),
        not derivable(Mode,strike(C,V2)),
        derivable(Mode,strike(C,V)) : value(V),
            different_values(V,V1), different_values(V,V2).

    :- deduction_mode(Mode),
        use_technique(Mode,remote_pairs_protection_chained),
        value(V1), value(V2), V1 < V2,
        4 { derivable(Mode,pair_left(V1,V2,C)) :
            derivable(Mode,pair_left(V1,V2,C)), cell(C) }.
    """
)

remote_pairs_requirement_chained = DeductionRule(
    "remote_pairs_requirement_chained",
    """
    derivable(Mode,rp_pair_left(V1,V2,C)) :-
        deduction_mode(Mode),
        use_technique(Mode,remote_pairs_requirement_chained),
        value(V1), value(V2), V1 < V2,
        cell(C),
        not derivable(Mode,strike(C,V1)),
        not derivable(Mode,strike(C,V2)),
        derivable(Mode,strike(C,V)) : value(V),
            different_values(V,V1), different_values(V,V2).

    derivable(Mode,rp_requirement_met(V1,V2)) :-
        deduction_mode(Mode),
        use_technique(Mode,remote_pairs_requirement_chained),
        value(V1), value(V2), V1 < V2,
        not 4 { derivable(Mode,rp_pair_left(V1,V2,C)) :
            derivable(Mode,pair_left(V1,V2,C)), cell(C) }.
    :- deduction_mode(Mode),
        use_technique(Mode,remote_pairs_requirement_chained),
        not derivable(Mode,rp_requirement_met(V1,V2)) :
            value(V1), value(V2), V1 < V2.
    """
)
