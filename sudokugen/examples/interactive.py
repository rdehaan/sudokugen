"""
Module with example functions that can be used to interactively generate
Sudoku puzzles
"""
# pylint: disable=too-many-lines

from .. import instances, generate_puzzle, encodings, masks


def initial_color_wrap(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    color wrap to solve.
    """
    # pylint: disable=too-many-arguments

    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add symmetry breaking constraints
        if sym_breaking:
            sym_breaking_constraints = [
                encodings.sym_breaking_top_row(instance),
                encodings.sym_breaking_left_column(instance),
            ]
        else:
            sym_breaking_constraints = []
        # Add deduction constraints
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_unsolved,
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.color_wrap,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_solved,
                        ]),
                ]
            ),
        ]
        # Add mask constraint
        mask_constraints = [
            encodings.use_mask(
                instance,
                masks.generate_randomly(instance, '?',
                    [(num_filled_cells_in_random_mask, '*')])
            ),
        ]

        constraints = \
            maximize_constraints + \
            sym_breaking_constraints + \
            deduction_constraints + \
            mask_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def initial_color_trap(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=600,
        num_filled_cells_in_random_mask=40,
        rule_out_xy_wing=True,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    color trap to solve.
    """
    # pylint: disable=too-many-arguments,too-many-locals

    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add symmetry breaking constraints
        if sym_breaking:
            sym_breaking_constraints = [
                encodings.sym_breaking_top_row(instance),
                encodings.sym_breaking_left_column(instance),
            ]
        else:
            sym_breaking_constraints = []
        # Add deduction constraints
        if rule_out_xy_wing:
            additional_non_solve = [
                encodings.xy_wing,
            ]
        else:
            additional_non_solve = []
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_unsolved
                        ] + additional_non_solve),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.color_trap_proper_chained,
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_solved
                        ]),
                ]
            ),
        ]
        # Add mask constraint
        mask_constraints = [
            encodings.use_mask(
                instance,
                masks.generate_randomly(instance, '?',
                    [(num_filled_cells_in_random_mask, '*')])
            ),
        ]

        constraints = \
            maximize_constraints + \
            sym_breaking_constraints + \
            deduction_constraints + \
            mask_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def initial_x_chain(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=600,
        num_filled_cells_in_random_mask=40,
        use_proper_encoding=True,
        rule_out_xy_wing=False,
        rule_out_color_trap=False,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    X-chain to solve.
    """
    # pylint: disable=too-many-arguments,too-many-locals

    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add symmetry breaking constraints
        if sym_breaking:
            sym_breaking_constraints = [
                encodings.sym_breaking_top_row(instance),
                encodings.sym_breaking_left_column(instance),
            ]
        else:
            sym_breaking_constraints = []
        # Add deduction constraints
        additional_non_solve = []
        if rule_out_xy_wing:
            additional_non_solve += [
                encodings.xy_wing,
            ]
        if rule_out_color_trap:
            additional_non_solve += [
                encodings.color_trap,
            ]
        if use_proper_encoding:
            x_chain_rules = [
                encodings.x_chain_proper_chained,
            ]
        else:
            x_chain_rules = [
                encodings.x_chain,
            ]
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_unsolved
                        ] + additional_non_solve),
                    encodings.SolvingStrategy(
                        rules=x_chain_rules),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_solved
                        ]),
                ]
            ),
        ]
        # Add mask constraint
        mask_constraints = [
            encodings.use_mask(
                instance,
                masks.generate_randomly(instance, '?',
                    [(num_filled_cells_in_random_mask, '*')])
            ),
        ]

        constraints = \
            maximize_constraints + \
            sym_breaking_constraints + \
            deduction_constraints + \
            mask_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def prepend_xy_wing(
        puzzle_to_derive,
        maximize_filled_cells=True,
        max_num_repeat=4,
        use_strong_connection=False,
        timeout=300,
        verbose=True,
    ):
    """
    Function to take a Sudoku puzzle and from it construct another that
    requires the solving technique XY-wing to get to the given puzzle.
    """
    # pylint: disable=too-many-arguments

    # If required, firstly determine what strikes cannot be derived from the
    # given puzzle in order to require that none of these can be derived in
    # the prepended puzzle
    if use_strong_connection:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.use_mask(
                instance,
                puzzle_to_derive
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.select_non_derivable_strikes_as_highlight,
                        ]
                    ),
                ]
            ),
            encodings.output_highlight_strikes(),
        ]

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=False,
        )

        # Store the strikes that we may not derive
        forbidden_strikes = found_solution.outputs['highlight_strike']

    # Now let's find our prepended puzzle..
    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add deduction constraints
        if use_strong_connection:
            forbidden_strike_rule = [
                encodings.forbid_strings_derivable(
                    forbidden_strikes
                )
            ]
        else:
            forbidden_strike_rule = []
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_mask_not_derived(
                                instance,
                                puzzle_to_derive
                            )
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.xy_wing,
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_derived(
                                instance,
                                puzzle_to_derive
                            ),
                        ] + forbidden_strike_rule),
                ]
            )
        ]

        constraints = \
            maximize_constraints + \
            deduction_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def prepend_locked_candidates(
        puzzle_to_derive,
        maximize_filled_cells=True,
        max_num_repeat=4,
        use_strong_connection=False,
        timeout=120,
        verbose=True,
    ):
    """
    Function to take a Sudoku puzzle and from it construct another that
    requires the solving technique locked candidates to get to the given puzzle.
    """
    # pylint: disable=too-many-arguments

    # If required, firstly determine what strikes cannot be derived from the
    # given puzzle in order to require that none of these can be derived in
    # the prepended puzzle
    if use_strong_connection:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.use_mask(
                instance,
                puzzle_to_derive
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.select_non_derivable_strikes_as_highlight,
                        ]
                    ),
                ]
            ),
            encodings.output_highlight_strikes(),
        ]

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=False,
        )

        # Store the strikes that we may not derive
        forbidden_strikes = found_solution.outputs['highlight_strike']

    # Now let's find our prepended puzzle..
    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add deduction constraints
        if use_strong_connection:
            forbidden_strike_rule = [
                encodings.forbid_strings_derivable(
                    forbidden_strikes
                )
            ]
        else:
            forbidden_strike_rule = []
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_mask_not_derived(
                                instance,
                                puzzle_to_derive
                            )
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.locked_candidates,
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_derived(
                                instance,
                                puzzle_to_derive
                            ),
                        ] + forbidden_strike_rule),
                ]
            )
        ]

        constraints = \
            maximize_constraints + \
            deduction_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def prepend_hidden_pairs(
        puzzle_to_derive,
        maximize_filled_cells=True,
        max_num_repeat=4,
        use_strong_connection=False,
        timeout=120,
        verbose=True,
    ):
    """
    Function to take a Sudoku puzzle and from it construct another that
    requires the solving technique hidden pairs to get to the given puzzle.
    """
    # pylint: disable=too-many-arguments

    # If required, firstly determine what strikes cannot be derived from the
    # given puzzle in order to require that none of these can be derived in
    # the prepended puzzle
    if use_strong_connection:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.use_mask(
                instance,
                puzzle_to_derive
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.select_non_derivable_strikes_as_highlight,
                        ]
                    ),
                ]
            ),
            encodings.output_highlight_strikes(),
        ]

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=False,
        )

        # Store the strikes that we may not derive
        forbidden_strikes = found_solution.outputs['highlight_strike']

    # Now let's find our prepended puzzle..
    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add deduction constraints
        if use_strong_connection:
            forbidden_strike_rule = [
                encodings.forbid_strings_derivable(
                    forbidden_strikes
                )
            ]
        else:
            forbidden_strike_rule = []
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_mask_not_derived(
                                instance,
                                puzzle_to_derive
                            )
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.hidden_pairs,
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_derived(
                                instance,
                                puzzle_to_derive
                            ),
                        ] + forbidden_strike_rule),
                ]
            )
        ]

        constraints = \
            maximize_constraints + \
            deduction_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def prepend_naked_pairs(
        puzzle_to_derive,
        maximize_filled_cells=True,
        max_num_repeat=4,
        use_strong_connection=False,
        timeout=120,
        verbose=True,
    ):
    """
    Function to take a Sudoku puzzle and from it construct another that
    requires the solving technique naked pairs to get to the given puzzle.
    """
    # pylint: disable=too-many-arguments

    # If required, firstly determine what strikes cannot be derived from the
    # given puzzle in order to require that none of these can be derived in
    # the prepended puzzle
    if use_strong_connection:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.use_mask(
                instance,
                puzzle_to_derive
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.select_non_derivable_strikes_as_highlight,
                        ]
                    ),
                ]
            ),
            encodings.output_highlight_strikes(),
        ]

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=False,
        )

        # Store the strikes that we may not derive
        forbidden_strikes = found_solution.outputs['highlight_strike']

    # Now let's find our prepended puzzle..
    puzzle = None

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        instance = instances.RegularSudoku(9)
        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add deduction constraints
        if use_strong_connection:
            forbidden_strike_rule = [
                encodings.forbid_strings_derivable(
                    forbidden_strikes
                )
            ]
        else:
            forbidden_strike_rule = []
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            #
                            encodings.stable_state_mask_not_derived(
                                instance,
                                puzzle_to_derive
                            )
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_pairs,
                        ]
                    ),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_derived(
                                instance,
                                puzzle_to_derive
                            ),
                        ] + forbidden_strike_rule),
                ]
            )
        ]

        constraints = \
            maximize_constraints + \
            deduction_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def initial_generic(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        pre_rules=None,
        chain_point_rules=None,
        additional_constraints=None,
        additional_nonsolve_branches=None,
        post_rules=None,
        instance=None,
        verbose=True,
    ):
    """
    Generic function to generate a Sudoku puzzle that requires a particular
    solving technique to solve.
    """
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches

    if not pre_rules:
        pre_rules = []
    if not chain_point_rules:
        chain_point_rules = []
    if not post_rules:
        post_rules = []
    if not additional_constraints:
        additional_constraints = []

    if not instance:
        instance = instances.RegularSudoku(9)

    puzzle = None
    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []

        # Add symmetry breaking constraints
        if sym_breaking:
            sym_breaking_constraints = [
                encodings.sym_breaking_top_row(instance),
                encodings.sym_breaking_left_column(instance),
            ]
        else:
            sym_breaking_constraints = []

        # Add deduction constraints
        chaining_pattern = [(0, 1), (1, 2)]
        additional_deduction_modes = []
        if additional_nonsolve_branches:
            additional_deduction_modes = [
                encodings.SolvingStrategy(
                    rules=[
                        encodings.basic_deduction,
                        encodings.naked_singles,
                        encodings.hidden_singles,
                        #
                        encodings.stable_state_unsolved,
                    ] + rule_set
                ) for rule_set in additional_nonsolve_branches
            ]
            chaining_pattern += [
                (0, 3+i) for i, _ in enumerate(additional_nonsolve_branches)
            ]

        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    # Pre chain point
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_unsolved,
                        ] + pre_rules
                    ),
                    # Chain point
                    encodings.SolvingStrategy(
                        rules=chain_point_rules
                    ),
                    # Post chain point
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_solved,
                        ] + post_rules
                    ),
                ] + additional_deduction_modes,
                chaining_pattern
            ),
        ]

        # Add mask constraint
        mask_constraints = [
            encodings.use_mask(
                instance,
                masks.generate_randomly(instance, '?',
                    [(num_filled_cells_in_random_mask, '*')])
            ),
        ]

        # Put together all the constraints
        constraints = \
            maximize_constraints + \
            sym_breaking_constraints + \
            deduction_constraints + \
            mask_constraints + \
            additional_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def initial_from_preset(
        preset_name,
        **kwargs
    ):
    """
    Function to generate a Sudoku puzzle that requires a particular
    solving technique to solve, using a list of preset values.
    """
    # pylint: disable=too-many-arguments,too-many-locals

    presets = {
        #
        "hidden pairs": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.hidden_pairs,
            ],
            "post_rules": [],
        },
        #
        "hidden pairs only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.naked_pairs_not_applicable_chained,
                encodings.locked_candidates_not_applicable_chained,
            ],
            "chain_point_rules": [
                encodings.hidden_pairs,
            ],
            "post_rules": [],
        },
        #
        "hidden triples": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 0,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.hidden_triples,
            ],
            "post_rules": [],
        },
        #
        "naked pairs": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 0,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.naked_pairs,
            ],
            "post_rules": [],
        },
        #
        "naked pairs only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 0,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.naked_pairs,
            ],
            "post_rules": [],
            "additional_nonsolve_branches": [
                [
                    encodings.hidden_pairs,
                    encodings.locked_candidates,
                ]
            ]
        },
        #
        "naked triples": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.naked_triples,
            ],
            "post_rules": [],
        },
        #
        "lc hp combo": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 20,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.naked_pairs,
            ],
            "chain_point_rules": [
                encodings.hidden_pairs,
                encodings.locked_candidates,
            ],
            "post_rules": [],
            "additional_nonsolve_branches": [
                [
                    encodings.closed_under_naked_singles,
                    encodings.closed_under_hidden_singles,
                    encodings.naked_pairs,
                    encodings.hidden_pairs,
                ],
                [
                    encodings.closed_under_naked_singles,
                    encodings.closed_under_hidden_singles,
                    encodings.naked_pairs,
                    encodings.locked_candidates,
                ],
            ]
        },
        #
        "snyder locked": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.snyder_basic,
                encodings.snyder_hidden_pairs,
                encodings.snyder_basic_locked,
            ],
            "chain_point_rules": [
                encodings.snyder_locked_candidates,
            ],
            "post_rules": [],
        },
        #
        "snyder locked full": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.snyder_basic,
                encodings.snyder_hidden_pairs,
                encodings.snyder_basic_locked,
                encodings.snyder_locked_candidates,
            ],
            "chain_point_rules": [
                encodings.locked_candidates,
            ],
            "post_rules": [],
        },
        #
        "snyder locked both": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "num_filled_cells_in_random_mask": 20,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.snyder_basic,
                encodings.snyder_hidden_pairs,
            ],
            "chain_point_rules": [
                encodings.snyder_basic,
                encodings.snyder_basic_locked,
                encodings.snyder_locked_candidates,
            ],
            "post_rules": [],
            "additional_nonsolve_branches": [
                [
                    encodings.closed_under_naked_singles,
                    encodings.closed_under_hidden_singles,
                    encodings.snyder_basic,
                    encodings.snyder_hidden_pairs,
                    encodings.snyder_basic_locked,
                ],
                [
                    encodings.closed_under_naked_singles,
                    encodings.closed_under_hidden_singles,
                    encodings.snyder_basic,
                    encodings.snyder_hidden_pairs,
                    encodings.snyder_locked_candidates,
                ],
            ]
        },
        #
        "snyder hidden pairs": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.snyder_basic,
                encodings.snyder_basic_locked,
                encodings.locked_candidates,
            ],
            "chain_point_rules": [
                encodings.snyder_hidden_pairs,
            ],
            "post_rules": [],
        },
        #
        "xy wing": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xy_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xy_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xy_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing only *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xy_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
        "xyz wing": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xyz_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xyz wing *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xyz_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
        "xyz wing only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 600,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.xy_wing_not_applicable_chained,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xyz_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xyz wing only *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 600,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.xy_wing_not_applicable_chained,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xyz_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
        "w wing": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.w_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "w wing only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.xy_wing_not_applicable_chained,
                encodings.turbot_fish_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.w_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "x wing": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.x_wing,
            ],
            "post_rules": [],
        },
        #
        "x wing only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.x_wing,
            ],
            "post_rules": [],
        },
        #
        "turbot fish": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.turbot_fish_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "turbot fish only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.x_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.turbot_fish_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "empty rectangle": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.empty_rectangle,
            ],
            "post_rules": [],
        },
        #
        "empty rectangle only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.empty_rectangle,
            ],
            "post_rules": [],
        },
        #
        "two string kite": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.two_string_kite,
            ],
            "post_rules": [],
        },
        "two string kite only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.x_wing_not_applicable_chained,
                encodings.skyscraper_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.two_string_kite,
            ],
            "post_rules": [],
        },
        #
        "skyscraper": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.skyscraper,
            ],
            "post_rules": [],
        },
        #
        "skyscraper only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.x_wing_not_applicable_chained,
                encodings.two_string_kite_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.skyscraper,
            ],
            "post_rules": [],
        },
        #
        "remote pairs": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                # encodings.remote_pairs_requirement_chained,
            ],
            "chain_point_rules": [
                encodings.remote_pairs_chained,
            ],
            "post_rules": [],
        },
        #
        "remote pairs only": { # not efficient (yet)
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
            ],
            "chain_point_rules": [
                encodings.remote_pairs_chained,
            ],
            "post_rules": [],
        },
        #
    }

    for argument in [
        "maximize_filled_cells",
        "max_num_repeat",
        "timeout",
        "num_filled_cells_in_random_mask",
        "sym_breaking",
        "pre_rules",
        "chain_point_rules",
        "post_rules",
        "additional_nonsolve_branches",
        "additional_constraints",
        "verbose",
        "instance",
    ]:
        if argument not in kwargs and argument in presets[preset_name]:
            kwargs[argument] = presets[preset_name][argument]

    return initial_generic(**kwargs)


def prepend_generic(
        puzzle_to_derive,
        use_strong_connection=False,
        strong_connection_rules=None,
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        pre_rules=None,
        chain_point_rules=None,
        additional_constraints=None,
        additional_nonsolve_branches=None,
        post_rules=None,
        instance=None,
        verbose=True,
    ):
    """
    Function to take a Sudoku puzzle and from it construct another that
    requires some particular solving techniques to get to the given puzzle.
    """
    # pylint: disable=too-many-arguments,too-many-branches,too-many-locals

    # If required, firstly determine what strikes cannot be derived from the
    # given puzzle in order to require that none of these can be derived in
    # the prepended puzzle
    if use_strong_connection:

        if not strong_connection_rules:
            strong_connection_rules = [
                encodings.basic_deduction,
                encodings.naked_singles,
                encodings.hidden_singles,
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
            ]

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.use_mask(
                instance,
                puzzle_to_derive
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=strong_connection_rules + [
                            encodings.select_non_derivable_strikes_as_highlight,
                        ]
                    ),
                ]
            ),
            encodings.output_highlight_strikes(),
        ]

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=False,
        )

        # Store the strikes that we may not derive
        forbidden_strikes = found_solution.outputs['highlight_strike']

    # Now let's find our prepended puzzle..
    puzzle = None
    if not instance:
        instance = instances.RegularSudoku(9)

    if not pre_rules:
        pre_rules = []
    if not chain_point_rules:
        chain_point_rules = []
    if not post_rules:
        post_rules = []
    if not additional_constraints:
        additional_constraints = []

    i = 0
    while not puzzle and i < max_num_repeat:
        i += 1

        # Add maximization constraint
        if maximize_filled_cells:
            maximize_constraints = [
                encodings.maximize_num_filled_cells(),
            ]
        else:
            maximize_constraints = []
        # Add deduction constraints
        if use_strong_connection:
            forbidden_strike_rule = [
                encodings.forbid_strings_derivable(
                    forbidden_strikes
                )
            ]
        else:
            forbidden_strike_rule = []
        # Add deduction constraints
        chaining_pattern = [(0, 1), (1, 2)]
        additional_deduction_modes = []
        if additional_nonsolve_branches:
            additional_deduction_modes = [
                encodings.SolvingStrategy(
                    rules=[
                        encodings.basic_deduction,
                        encodings.naked_singles,
                        encodings.hidden_singles,
                        #
                        encodings.stable_state_mask_not_derived(
                            instance,
                            puzzle_to_derive
                        )
                    ] + rule_set
                ) for rule_set in additional_nonsolve_branches
            ]
            chaining_pattern += [
                (0, 3+i) for i, _ in enumerate(additional_nonsolve_branches)
            ]
        deduction_constraints = [
            encodings.chained_deduction_constraint(
                instance,
                [
                    # Pre chain point
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_not_derived(
                                instance,
                                puzzle_to_derive
                            )
                        ] + pre_rules
                    ),
                    # Chain point
                    encodings.SolvingStrategy(
                        rules=chain_point_rules
                    ),
                    # Post chain point
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            #
                            encodings.stable_state_mask_derived(
                                instance,
                                puzzle_to_derive
                            ),
                        ] + post_rules + forbidden_strike_rule
                    ),
                ] + additional_deduction_modes,
                chaining_pattern
            ),
        ]

        constraints = \
            maximize_constraints + \
            deduction_constraints + \
            additional_constraints

        # Generate the puzzle
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=timeout,
            verbose=verbose,
            cl_arguments=["--parallel-mode=4"],
        )

        if found_solution:
            puzzle = found_solution.repr_short()
            if verbose:
                print(found_solution.repr_pretty())
                print(f"Puzzle = {puzzle}")
                print(f"Number of cells filled: {81-puzzle.count('0')}")
            return puzzle


def prepend_from_preset(
        preset_name,
        puzzle_to_derive,
        **kwargs
    ):
    """
    Function to generate a Sudoku puzzle that requires a particular
    solving technique to solve, using a list of preset values.
    """
    # pylint: disable=too-many-arguments,too-many-locals

    presets = {
        #
        "xy wing": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xy_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 180,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
            ],
            "chain_point_rules": [
                encodings.xy_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing only": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xy_wing_proper_chained,
            ],
            "post_rules": [],
        },
        #
        "xy wing only *": {
            "maximize_filled_cells": True,
            "max_num_repeat": 4,
            "timeout": 300,
            "num_filled_cells_in_random_mask": 40,
            "pre_rules": [
                encodings.naked_pairs,
                encodings.hidden_pairs,
                encodings.locked_candidates,
                encodings.closed_under_naked_singles,
                encodings.closed_under_hidden_singles,
                encodings.turbot_fish_not_applicable_chained,
                encodings.w_wing_not_applicable_chained,
                encodings.empty_rectangle_not_applicable_chained,
                encodings.bug1_protection_chained,
                encodings.remote_pairs_protection_chained,
            ],
            "chain_point_rules": [
                encodings.xy_wing_forced_shot_chained,
            ],
            "post_rules": [],
        },
        #
    }

    for argument in [
        "use_strong_connection",
        "strong_connection_rules",
        "maximize_filled_cells",
        "max_num_repeat",
        "timeout",
        "pre_rules",
        "chain_point_rules",
        "post_rules",
        "additional_nonsolve_branches",
        "additional_constraints",
        "verbose",
        "instance",
    ]:
        if argument not in kwargs and argument in presets[preset_name]:
            kwargs[argument] = presets[preset_name][argument]

    return prepend_generic(puzzle_to_derive, **kwargs)
