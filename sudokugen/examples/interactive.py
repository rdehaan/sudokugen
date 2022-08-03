"""
Module with example functions that can be used to interactively generate
Sudoku puzzles
"""
# pylint: disable=too-many-lines

from .. import instances, generate_puzzle, encodings, masks


def initial_xyz_wing(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=600,
        num_filled_cells_in_random_mask=40,
        use_chained_encoding=False,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    XYZ-wing to solve.
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
        if use_chained_encoding:
            positive_deduction_constraint = [
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
                            ]),
                        encodings.SolvingStrategy(
                            rules=[
                                encodings.xyz_wing_proper_chained,
                            ]),
                        encodings.SolvingStrategy(
                            rules=[
                                encodings.basic_deduction,
                                encodings.naked_singles,
                                encodings.hidden_singles,
                                encodings.naked_pairs,
                                encodings.hidden_pairs,
                                encodings.locked_candidates,
                                #
                                encodings.stable_state_solved
                            ]),
                    ]
                ),
            ]
        else:
            positive_deduction_constraint = [
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
                                encodings.xyz_wing,
                                #
                                encodings.stable_state_solved
                            ]),
                    ]
                ),
            ]
        deduction_constraints = [
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
                            encodings.xy_wing,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
                        ]),
                ]
            ),
        ] + positive_deduction_constraint
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


def initial_x_wing(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    X-wing to solve.
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
                            encodings.x_wing,
                            encodings.stable_state_solved
                        ]),
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
                            encodings.stable_state_unsolved
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


def initial_xy_wing(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    XY-wing to solve.
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
                            encodings.xy_wing,
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
                            encodings.color_wrap,
                            encodings.stable_state_solved
                        ]),
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
                            encodings.stable_state_unsolved
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
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.color_trap_proper_chained,
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.locked_candidates,
                            #
                            encodings.stable_state_solved
                        ]),
                ]
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
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
                        ] + additional_non_solve),
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
        if use_proper_encoding:
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
                            ]),
                        encodings.SolvingStrategy(
                            rules=[
                                encodings.x_chain_proper_chained,
                            ]),
                        encodings.SolvingStrategy(
                            rules=[
                                encodings.basic_deduction,
                                encodings.naked_singles,
                                encodings.hidden_singles,
                                encodings.naked_pairs,
                                encodings.hidden_pairs,
                                encodings.locked_candidates,
                                #
                                encodings.stable_state_solved
                            ]),
                    ]
                ),
            ]
        else:
            deduction_constraints = [
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
                                encodings.x_chain,
                                #
                                encodings.stable_state_solved
                            ]),
                    ]
                ),
            ]
        if rule_out_xy_wing:
            deduction_constraints += [
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
                                encodings.xy_wing,
                                #
                                encodings.closed_under_naked_singles,
                                encodings.closed_under_hidden_singles,
                                encodings.stable_state_unsolved
                            ]),
                    ]
                ),
            ]
        else:
            deduction_constraints += [
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
                                encodings.closed_under_naked_singles,
                                encodings.closed_under_hidden_singles,
                                encodings.stable_state_unsolved
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


def initial_snyder_x_wing(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=60,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    Snyder-X-wing to solve.
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
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.snyder_locked_candidates,
                            encodings.snyder_x_wing,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.snyder_locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
                        ]),
                ]
            ),
        ]
        # Add mask constraint
        mask_constraints = [
            # encodings.use_mask(
            #     instance,
            #     masks.generate_randomly(instance, '?',
            #         [(num_filled_cells_in_random_mask, '*')])
            # ),
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


def initial_snyder_locked_full(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=60,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    locked candidates (not just the Snyder variant) to solve.
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
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.locked_candidates,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.snyder_locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
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


def initial_snyder_locked(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=60,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    locked candidates (the Snyder variant) to solve.
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
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.snyder_locked_candidates,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
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


def initial_snyder_hidden_pairs(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=60,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    Snyder hidden pairs to solve.
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
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_hidden_pairs,
                            encodings.snyder_basic_locked,
                            encodings.locked_candidates,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.naked_singles,
                            encodings.hidden_singles,
                            encodings.snyder_basic,
                            encodings.snyder_basic_locked,
                            encodings.locked_candidates,
                            #
                            encodings.closed_under_naked_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_unsolved
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


def initial_naked_triples(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        rule_out_hidden_triples=False,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    naked triples to solve.
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
        if rule_out_hidden_triples:
            additional_non_solve = [
                encodings.hidden_triples,
            ]
        else:
            additional_non_solve = []
        deduction_constraints = [
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
                            encodings.naked_triples,
                            #
                            encodings.stable_state_solved
                        ]),
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
                            encodings.stable_state_unsolved
                        ] + additional_non_solve),
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


def initial_hidden_triples(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=300,
        num_filled_cells_in_random_mask=0,
        sym_breaking=True,
        rule_out_naked_triples=False,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    hidden triples to solve.
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
        if rule_out_naked_triples:
            additional_non_solve = [
                encodings.naked_triples,
            ]
        else:
            additional_non_solve = []
        deduction_constraints = [
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
                            encodings.hidden_triples,
                            #
                            encodings.stable_state_solved
                        ]),
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
                            encodings.stable_state_unsolved
                        ] + additional_non_solve),
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
