"""
Module with examples for how to generate Sudoku puzzles
"""

from .. import instances, generate_puzzle, encodings

def generate_example(num=1):
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    # Example no. 1:
    # - Generate a regular 9x9 sudoku puzzle
    # - with a unique solution
    # - where exactly 10 cells are empty
    if num == 1:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                instance.num_cells-10,
                instance.num_cells-10
            ),
            encodings.unique_solution()
        ]
        found_solution = generate_puzzle(
            instance,
            constraints
        )

    # Example no. 2:
    # - Generate a RokuDoku (6x6) puzzle
    # - with a unique solution
    # - minimizing the number of filled in cells
    # - and where at least 10 cells are empty
    # - giving a timeout of 30 seconds for solving
    # - in verbose mode
    elif num == 2:

        instance = instances.RokuDoku()
        constraints = [
            encodings.minimize_num_filled_cells(),
            encodings.constrain_num_filled_cells(
                instance,
                0,
                instance.num_cells-10
            ),
            encodings.unique_solution()
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30,
            verbose=True
        )

    # Example no. 3:
    # - Generate a CrossDoku (5x5) puzzle
    # - with a unique solution
    # - where at least 10 cells are empty and at least 10 cells are filled in
    # - where the locations of empty cells are left-right and top-bottom
    #   symmetric
    # - giving a timeout of 10 seconds for solving
    elif num == 3:

        instance = instances.CrossDoku()
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                10,
                instance.num_cells-10
            ),
            encodings.unique_solution(),
            encodings.left_right_symmetry(instance),
            encodings.top_bottom_symmetry(instance)
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=10
        )

    # Example no. 4:
    # - Generate a TriangleDoku (6x6) puzzle
    # - with a unique solution
    # - where at least 15 cells are empty and at least 15 cells are filled in
    # - where the locations of empty cells are point symmetric
    # - giving a timeout of 10 seconds for solving
    elif num == 4:

        instance = instances.TriangleDoku()
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                15,
                instance.num_cells-15
            ),
            encodings.unique_solution(),
            encodings.point_symmetry(instance)
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=10
        )

    # Example no. 5:
    # - Generate a BombRokuDoku (6x6) puzzle
    # - with a unique solution
    # - minimizing the number of filled in cells
    # - giving a timeout of 30 seconds for solving
    elif num == 5:

        instance = instances.BombRokuDoku()
        constraints = [
            encodings.minimize_num_filled_cells(),
            encodings.unique_solution()
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30
        )

    # Example no. 6:
    # - Generate a regular 9x9 sudoku puzzle
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    # (- and thus has a unique solution)
    # - where at least 50 cells are empty
    # - giving a timeout of 10 seconds for solving
    elif num == 6:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.constrain_num_filled_cells(instance, 0, instance.num_cells-50),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.stable_state_solved
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=10
        )

    # Example no. 7:
    # - Generate a regular 9x9 sudoku puzzle
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    # (- and thus has a unique solution)
    # - and that is *not* solvable using only the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    # - maximizing the number of non-empty in cells
    # - giving a timeout of 30 seconds for solving
    elif num == 7:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.maximize_num_filled_cells(),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.stable_state_unsolved
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30
        )

    # Example no. 8:
    # - Generate a KnightRokuDoku (6x6) puzzle
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    # (- and thus has a unique solution)
    # - minimizing the number of filled in cells
    # - giving a timeout of 30 seconds for solving
    elif num == 8:

        instance = instances.KnightRokuDoku()
        constraints = [
            encodings.minimize_num_filled_cells(),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.stable_state_solved
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=30
        )

    # Example no. 9:
    # - Generate a KnightBombDozenDoku (12x12) puzzle
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    # (- and thus has a unique solution)
    # - and that is *not* solvable using only the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    # - where at least 110 cells are empty
    # - giving a timeout of 300 seconds for solving
    elif num == 9:

        instance = instances.KnightBombDozenDoku()
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                0,
                instance.num_cells-110
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.stable_state_unsolved
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=300
        )

    # Example no. 10:
    # - Generate a regular 9x9 sudoku puzzle
    # - that is closed under the deduction rules:
    #   * lone singles
    #   * hidden singles
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked triples
    # (- and thus has a unique solution)
    # - and that is *not* solvable using only the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    # - giving a timeout of 240 seconds for solving with 4 parallel threads
    elif num == 10:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                0,
                instance.num_cells-10
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.closed_under_lone_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_trivial
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_triples,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.stable_state_unsolved,
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=60,
            verbose=True,
            cl_arguments=["--parallel-mode=4"]
        )

    # Example no. 11:
    # - Generate a regular 9x9 sudoku puzzle
    # - that is closed under the deduction rules:
    #   * lone singles
    #   * hidden singles
    # - that is solvable using the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    #   * hidden pairs
    # (- and thus has a unique solution)
    # - and that is *not* solvable using only the deduction rules:
    #   * basic deduction
    #   * lone singles
    #   * hidden singles
    #   * naked pairs
    # - giving a timeout of 60 seconds for solving with 4 parallel threads
    elif num == 11:

        instance = instances.RegularSudoku(9)
        constraints = [
            encodings.constrain_num_filled_cells(
                instance,
                0,
                instance.num_cells-10
            ),
            encodings.deduction_constraint(
                instance,
                [
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.closed_under_lone_singles,
                            encodings.closed_under_hidden_singles,
                            encodings.stable_state_trivial
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.hidden_pairs,
                            encodings.stable_state_solved
                        ]),
                    encodings.SolvingStrategy(
                        rules=[
                            encodings.basic_deduction,
                            encodings.lone_singles,
                            encodings.hidden_singles,
                            encodings.naked_pairs,
                            encodings.stable_state_unsolved,
                        ])
                ]
            )
        ]
        found_solution = generate_puzzle(
            instance,
            constraints,
            timeout=60,
            verbose=True,
            cl_arguments=["--parallel-mode=4"]
        )

    else:
        print(f"Example #{num} not found")
        return

    if found_solution:
        print(found_solution.repr_pretty())
    else:
        print("No puzzle could be found")
