"""
Module with example functions that can be used to interactively generate
Sudoku puzzles
"""

from .. import instances, generate_puzzle, encodings, masks


def initial_xyz_wing(
        maximize_filled_cells=True,
        max_num_repeat=4,
        timeout=600,
        num_filled_cells_in_random_mask=40,
        sym_breaking=True,
        verbose=True,
    ):
    """
    Function to generate a Sudoku puzzle that requires the solving technique
    XYZ-wing to solve.
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
