"""
Module with classes to represent instances of different types of Sudoku-like
puzzles
"""

from abc import abstractmethod
import itertools
import math
import random

class Instance:
    """
    Class to represent instances of the generic template of a Sudoku puzzle.
    """

    def __init__(self):
        self.cells = []
        self.values = []
        self.groups = []

        self.solution = None
        self.puzzle = None

        self.outputs = {}

    @property
    def num_cells(self):
        return len(self.cells)

    def repr_basic(self) -> str:
        """
        Provides a basic string representation of the instance.
        """
        output = f"Cells: {self.cells}\n"
        output += f"Values: {self.values}\n"
        output += f"Groups: {self.groups}\n"
        output += f"Solution: {self.solution}\n"
        output += f"Puzzle: {self.puzzle}\n"
        return output

    def repr_pretty(self) -> str:
        """
        Provides a pretty representation of the puzzle of the instance.

        Should be implemented for subclasses
        """
        return self.repr_basic()

    @abstractmethod
    def cell_encoding(self, cell) -> str:
        """
        Provides the term to represent a cell in the ASP encoding.
        """

    def value_encoding(self, value) -> str: # pylint: disable=R0201
        """
        Provides the term to represent a value in the ASP encoding.
        """
        return str(value)

    def extract_from_answer_set(self, model):
        """
        Extracts the solution and puzzle members from an answer set.
        """

        self.outputs = {}

        for atom in model.symbols(atoms=True):
            if atom.name == "output":
                key = str(atom.arguments[0])
                value = str(atom.arguments[1])
                if key not in self.outputs:
                    self.outputs[key] = []
                self.outputs[key] = self.outputs[key] + [value]

    def swap_values(self, value1, value2):
        """
        Swaps two values in the puzzle and solution.
        """

        def val_permutation(value):
            if value == value1:
                return value2
            if value == value2:
                return value1
            return value

        # Apply permutation
        new_puzzle = {
            (i,j): val_permutation(self.puzzle[(i,j)])
            for (i,j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i,j): val_permutation(self.solution[(i,j)])
            for (i,j) in self.solution
        }
        self.solution = new_solution


class SquareSudoku(Instance):
    """
    Class to represent square sudoku instances.
    """

    def __init__(self, size: int = 9):
        super().__init__()
        self.size = size
        self.cells = list(itertools.product(range(1, size+1), repeat=2))
        self.values = list(range(1, size+1))
        rows = [("row", [(c, r) for c in range(1, size+1)])
                for r in range(1, size+1)]
        self.groups.extend(rows)
        cols = [("column", [(c, r) for r in range(1, size+1)])
                for c in range(1, size+1)]
        self.groups.extend(cols)

    def cell_encoding(self, cell) -> str:
        """
        Provides the term to represent a cell in the ASP encoding.
        """
        return f"cell({cell[0]},{cell[1]})"

    def extract_from_answer_set(self, model):
        """
        Extracts the solution and puzzle members from an answer set.
        """

        super().extract_from_answer_set(model)

        self.solution = {}
        self.puzzle = {}
        erase_set = set()

        for atom in model.symbols(shown=True):
            if atom.name == "solution":
                col = atom.arguments[0].arguments[0].number
                row = atom.arguments[0].arguments[1].number
                value = atom.arguments[1].number
                self.solution[(col, row)] = value
            elif atom.name == "erase":
                col = atom.arguments[0].arguments[0].number
                row = atom.arguments[0].arguments[1].number
                erase_set.add((col, row))

        for cell in self.cells:
            if cell in erase_set:
                self.puzzle[cell] = 0
            else:
                self.puzzle[cell] = self.solution[cell]

    def repr_pretty(self):
        """
        Provides a pretty representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return "[Not yet generated]"

        output = ""
        for row in range(1, self.size+1):
            for col in range(1, self.size+1):
                output += f"{self.puzzle[(col, row)]} "
            output += "\n"
        return output[:-1]

    def repr_list(self):
        """
        Provides a list representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return None

        output_list = []
        for row in range(1, self.size+1):
            row_list = []
            for col in range(1, self.size+1):
                row_list.append(self.puzzle[(col, row)])
            output_list.append(row_list)
        return output_list

    def repr_short(self):
        """
        Provides a short representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return "[Not yet generated]"

        output = ""
        for row in range(1, self.size + 1):
            for col in range(1, self.size + 1):
                output += f"{self.puzzle[(col, row)]}"
        return output


class RectangleBlockSudoku(SquareSudoku):
    """
    Class to represent square sudoku instances with rectangular blocks
    """

    def __init__(self, block_width: int = 3, block_height: int = 3):
        self._block_width = block_width
        self._block_height = block_height
        size = block_width * block_height
        super().__init__(size=size)

        # Add blocks as groups
        for outside_col, outside_row in itertools.product(
                range(0, self._block_height),
                range(0, self._block_width)
        ):
            self.groups.append(("block", [
                (outside_col * self._block_width + inside_col,
                 outside_row * self._block_height + inside_row)
                for inside_col, inside_row in itertools.product(
                    range(1, self._block_width + 1),
                    range(1, self._block_height + 1)
                )
            ]))

    def repr_pretty(self):
        """
        Provides a pretty representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return "[Not yet generated]"

        output = ""
        for row in range(1, self.size + 1):
            for col in range(1, self.size + 1):
                output += f"{self.puzzle[(col, row)]} "
                if col % self._block_width == 0:
                    output += " "
            output += "\n"
            if row % self._block_height == 0:
                output += "\n"
        return output[:-2]

    def shuffle(self):
        """
        Randomly permutes the rows, columns and values of the instance,
        and randomly transposes the instance if the blocks are squares.
        """
        self.shuffle_orientation()
        self.shuffle_values()

    def shuffle_orientation(self):
        """
        Randomly permutes the rows, columns of the instance,
        and randomly transposes the instance if the blocks are squares.
        """

        # Construct column permutation
        col_indices = [
            [(j*self._block_width)+i for i in range(1,self._block_width+1)]
            for j in range(self._block_height)
        ]
        for sublist in col_indices:
            random.shuffle(sublist)
        random.shuffle(col_indices)
        col_indices = [index for sublist in col_indices for index in sublist]
        def col_permutation(index):
            return col_indices[index-1]

        # Construct row permutation
        row_indices = [
            [(j*self._block_height)+i for i in range(1,self._block_height+1)]
            for j in range(self._block_width)
        ]
        for sublist in row_indices:
            random.shuffle(sublist)
        random.shuffle(row_indices)
        row_indices = [index for sublist in row_indices for index in sublist]
        def row_permutation(index):
            return row_indices[index-1]

        # Decide whether to transpose
        transpose = False
        if self._block_width == self._block_height:
            transpose = random.choice([True, False])
        def flip_if_transposed(i,j):
            if transpose:
                return (j,i)
            return (i,j)

        # Apply permutations
        new_puzzle = {
            (i,j): self.puzzle[flip_if_transposed(
                        col_permutation(i),
                        row_permutation(j))]
            for (i,j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i,j): self.solution[flip_if_transposed(
                        col_permutation(i),
                        row_permutation(j))]
            for (i,j) in self.solution
        }
        self.solution = new_solution

    def shuffle_values(self):
        """
        Randomly permutes the values of the instance.
        """

        # Construct and apply value permutation
        value_list = list(range(1,self.size+1))
        random.shuffle(value_list)
        self.apply_value_permutation(value_list)

    def apply_value_permutation(self, value_list):
        """
        Applies a given value permutation to the instance.
        """

        # Construct value permutation
        def val_permutation(value):
            if value == 0:
                return 0
            return value_list[value-1]

        # Apply permutation
        new_puzzle = {
            (i,j): val_permutation(self.puzzle[(i,j)])
            for (i,j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i,j): val_permutation(self.solution[(i,j)])
            for (i,j) in self.solution
        }
        self.solution = new_solution


class RegularSudoku(RectangleBlockSudoku):
    """
    Class to represent regular sudoku instances
    """

    def __init__(self, size: int = 9):
        if size != math.sqrt(size) ** 2:
            raise ValueError("size should be a squared number")
        block_size = int(math.sqrt(size))
        super().__init__(block_width=block_size, block_height=block_size)


class XSudoku(RegularSudoku):
    """
    Class to represent X sudoku instances (of different sizes).
    """

    def __init__(self, size: int = 9):
        super().__init__(size=size)

        # Add the X as groups
        diagonal1 = ("x", [(col, col) for col in range(1, size + 1)])
        self.groups.append(diagonal1)
        diagonal2 = ("x", [(col, size + 1 - col) for col in range(1, size + 1)])
        self.groups.append(diagonal2)


class YSudoku(RegularSudoku):
    """
    Class to represent Y sudoku instances (of different odd sizes).
    """

    def __init__(self, size: int = 9):
        if (size % 2) == 0:
            raise ValueError("size should be an odd number")
        super().__init__(size=size)

        # Add the Y as groups
        middle = int((size + 1) / 2)
        bottom_of_y = [(middle, row) for row in range(middle, size + 1)]
        left_of_y = [(row, row) for row in range(1, middle)]
        right_of_y = [(size + 1 - row, row) for row in range(1, middle)]
        self.groups.append(("y", left_of_y + bottom_of_y))
        self.groups.append(("y", right_of_y + bottom_of_y))


class SSudoku(RegularSudoku):
    """
    Class to represent S sudoku instances (of size 9).
    """

    def __init__(self):
        size = 9
        super().__init__(size=size)

        # Add the S as groups
        blocks = [("s", group) for group in [
            [(1, 3), (2, 2), (3, 1), (4, 1), (5, 1),
             (6, 1), (7, 1), (8, 2), (9, 2)],
            [(1, 4), (2, 5), (3, 5), (4, 5), (5, 5),
             (6, 5), (7, 5), (8, 5), (9, 6)],
            [(1, 8), (2, 8), (3, 9), (4, 9), (5, 9),
             (6, 9), (7, 9), (8, 8), (9, 7)],
            [(1, 3), (2, 2), (3, 1), (1, 4), (2, 5),
             (3, 5), (1, 8), (2, 8), (3, 9)],
            [(4, 1), (5, 1), (3, 1), (6, 5), (5, 5),
             (6, 5), (4, 9), (5, 9), (6, 9)],
            [(7, 1), (8, 2), (3, 2), (9, 5), (8, 5),
             (9, 6), (7, 9), (8, 8), (9, 7)]
        ]]
        self.groups.extend(blocks)


class RokuDoku(RectangleBlockSudoku):
    """
    Class to represent roku doku instances
    """

    def __init__(self):
        super().__init__(block_width=3, block_height=2)


class DozenDoku(RectangleBlockSudoku):
    """
    Class to represent dozen doku instances
    """

    def __init__(self):
        super().__init__(block_width=4, block_height=3)


class FourSquareSudoku(RegularSudoku):
    """
    Class to represent four square sudoku instances
    """

    def __init__(self):
        size = 9
        super().__init__(size)
        squares = [("square", group) for group in [
            [(2, 2), (3, 2), (4, 2), (2, 3), (3, 3),
             (4, 3), (2, 4), (3, 4), (4, 4)],
            [(6, 2), (7, 2), (8, 2), (6, 3), (7, 3),
             (8, 3), (6, 4), (7, 4), (8, 4)],
            [(2, 6), (3, 6), (4, 6), (2, 7), (3, 7),
             (4, 7), (2, 8), (3, 8), (4, 8)],
            [(6, 6), (7, 6), (8, 6), (6, 7), (7, 7),
             (8, 7), (6, 8), (7, 8), (8, 8)]
        ]]
        self.groups.extend(squares)


class CrossDoku(SquareSudoku):
    """
    Class to represent cross doku instances
    """

    def __init__(self):
        super().__init__(size=5)

        # Add groups
        self.groups.extend([("block", group) for group in [
            [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2)],
            [(5, 1), (5, 1), (4, 2), (5, 2), (5, 3)],
            [(4, 4), (5, 4), (3, 5), (4, 5), (5, 5)],
            [(1, 3), (1, 4), (2, 4), (1, 5), (2, 5)],
            [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)]
        ]])

    def repr_pretty(self):
        """
        Provides a pretty representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return "[Not yet generated]"

        # pylint: disable=consider-using-f-string
        output = ""
        output += "-{} -{} -{} +{} +{}\n".format(
            *[self.puzzle[(col, 1)] for col in range(1, 6)]
        )
        output += "-{} -{} .{} +{} +{}\n".format(
            *[self.puzzle[(col, 2)] for col in range(1, 6)]
        )
        output += "+{} .{} .{} .{} +{}\n".format(
            *[self.puzzle[(col, 3)] for col in range(1, 6)]
        )
        output += "+{} +{} .{} -{} -{}\n".format(
            *[self.puzzle[(col, 4)] for col in range(1, 6)]
        )
        output += "+{} +{} -{} -{} -{}\n".format(
            *[self.puzzle[(col, 5)] for col in range(1, 6)]
        )
        return output[:-1]


class TriangleDoku(SquareSudoku):
    """
    Class to represent cross doku instances
    """

    def __init__(self):
        super().__init__(size=6)

        # Add groups
        self.groups.extend([("block", group) for group in [
            [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (1, 3)],
            [(4, 1), (5, 1), (6, 1), (5, 2), (6, 2), (6, 3)],
            [(3, 2), (4, 2), (2, 3), (3, 3), (4, 3), (5, 3)],
            [(1, 4), (1, 5), (2, 5), (1, 6), (2, 6), (3, 6)],
            [(2, 4), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5)],
            [(6, 4), (5, 5), (6, 5), (4, 6), (5, 6), (6, 6)]
        ]])

    def repr_pretty(self):
        """
        Provides a pretty representation of the puzzle of the instance.
        """

        if not self.puzzle:
            return "[Not yet generated]"

        # pylint: disable=consider-using-f-string
        output = ""
        output += "-{} -{} -{} +{} +{} +{}\n".format(
            *[self.puzzle[(col, 1)] for col in range(1, 7)]
        )
        output += "-{} -{} .{} .{} +{} +{}\n".format(
            *[self.puzzle[(col, 2)] for col in range(1, 7)]
        )
        output += "-{} .{} .{} .{} .{} +{}\n".format(
            *[self.puzzle[(col, 3)] for col in range(1, 7)]
        )
        output += "+{} ~{} ~{} ~{} ~{} -{}\n".format(
            *[self.puzzle[(col, 4)] for col in range(1, 7)]
        )
        output += "+{} +{} ~{} ~{} -{} -{}\n".format(
            *[self.puzzle[(col, 5)] for col in range(1, 7)]
        )
        output += "+{} +{} +{} -{} -{} -{}\n".format(
            *[self.puzzle[(col, 6)] for col in range(1, 7)]
        )
        return output[:-1]


class BombSudoku(SquareSudoku):
    """
    Class to represent bomb sudoku instances.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add small groups for the neighboring constraints
        for (col, row) in self.cells:
            neighbors = [
                (col, row+1),
                (col+1, row),
                (col+1, row+1),
                (col+1, row-1)
            ]
            for neighbor in neighbors:
                if neighbor in self.cells:
                    self.groups.append(("bomb", [(col, row), neighbor]))


class BombRegularSudoku(BombSudoku, RegularSudoku):
    """
    Class to represent bomb regular sudoku instances.
    """


class BombRokuDoku(BombSudoku, RokuDoku):
    """
    Class to represent bomb roku doku instances.
    """


class BombDozenDoku(BombSudoku, DozenDoku):
    """
    Class to represent bomb dozen doku instances.
    """


class KnightSudoku(SquareSudoku):
    """
    Class to represent knight sudoku instances.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add small groups for the knight constraints
        for (col, row) in self.cells:
            neighbors = [
                (col+1, row-2),
                (col+2, row-1),
                (col+2, row+1),
                (col+1, row+2)
            ]
            for neighbor in neighbors:
                if neighbor in self.cells:
                    self.groups.append(("knight", [(col, row), neighbor]))


class KnightRegularSudoku(KnightSudoku, RegularSudoku):
    """
    Class to represent knight regular sudoku instances.
    """


class KnightRokuDoku(KnightSudoku, RokuDoku):
    """
    Class to represent knight roku doku instances.
    """


class KnightDozenDoku(KnightSudoku, DozenDoku):
    """
    Class to represent knight dozen doku instances.
    """


class KnightBombRegularSudoku(KnightSudoku, BombSudoku, RegularSudoku):
    """
    Class to represent knight bomb regular sudoku instances.
    """


class KnightBombDozenDoku(KnightSudoku, BombSudoku, DozenDoku):
    """
    Class to represent knight bomb dozen doku instances.
    """


class BasicInterfaceSudoku(RegularSudoku):
    """
    Class to represent 'interface' regular sudoku instances, with one output
    and one input cell.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.output_cell = None
        self.input_cell = None
        self.output_decoy_value = None
        self.input_decoy_value = None

    def extract_from_answer_set(self, model):
        """
        Extracts the solution and puzzle members from an answer set.
        """

        super().extract_from_answer_set(model)

        for atom in model.symbols(shown=True):
            if atom.name == "output_cell":
                col = atom.arguments[0].arguments[0].number
                row = atom.arguments[0].arguments[1].number
                self.output_cell = (col, row)
            if atom.name == "input_cell":
                col = atom.arguments[0].arguments[0].number
                row = atom.arguments[0].arguments[1].number
                self.input_cell = (col, row)
            if atom.name == "output_decoy_value":
                self.output_decoy_value = atom.arguments[0].number
            if atom.name == "input_decoy_value":
                self.input_decoy_value = atom.arguments[0].number

    def shuffle_orientation(self):
        """
        Randomly permutes the rows, columns of the instance,
        and randomly transposes the instance.
        """

        # Construct column permutation
        col_indices = [
            [(j*self._block_width)+i for i in range(1,self._block_width+1)]
            for j in range(self._block_height)
        ]
        for sublist in col_indices:
            random.shuffle(sublist)
        random.shuffle(col_indices)
        col_indices = [index for sublist in col_indices for index in sublist]
        def col_permutation(index):
            return col_indices[index-1]
        def col_permutation_inverse(index):
            return col_indices.index(index)+1

        # Construct row permutation
        row_indices = [
            [(j*self._block_height)+i for i in range(1,self._block_height+1)]
            for j in range(self._block_width)
        ]
        for sublist in row_indices:
            random.shuffle(sublist)
        random.shuffle(row_indices)
        row_indices = [index for sublist in row_indices for index in sublist]
        def row_permutation(index):
            return row_indices[index-1]
        def row_permutation_inverse(index):
            return row_indices.index(index)+1

        # Decide whether to transpose
        transpose = False
        if self._block_width == self._block_height:
            transpose = random.choice([True, False])
        def flip_if_transposed(col, row):
            if transpose:
                return (row, col)
            return (col, row)

        # Apply permutations
        new_puzzle = {
            (i, j): self.puzzle[flip_if_transposed(
                        col_permutation(i),
                        row_permutation(j))]
            for (i, j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i, j): self.solution[flip_if_transposed(
                        col_permutation(i),
                        row_permutation(j))]
            for (i, j) in self.solution
        }
        self.solution = new_solution

        if self.input_cell:
            (i, j) = flip_if_transposed(*self.input_cell)
            self.input_cell = (
                col_permutation_inverse(i),
                row_permutation_inverse(j)
            )

        if self.output_cell:
            (i, j) = flip_if_transposed(*self.output_cell)
            self.output_cell = (
                col_permutation_inverse(i),
                row_permutation_inverse(j)
            )

    def apply_value_permutation(self, value_list):
        """
        Applies a given value permutation to the instance.
        """

        def val_permutation(value):
            if value == 0:
                return 0
            return value_list[value-1]
        # def val_permutation_inverse(value):
        #     if value == 0:
        #         return 0
        #     return value_list.index(value)+1

        # Apply permutation
        new_puzzle = {
            (i, j): val_permutation(self.puzzle[(i, j)])
            for (i, j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i, j): val_permutation(self.solution[(i, j)])
            for (i, j) in self.solution
        }
        self.solution = new_solution
        if self.input_decoy_value:
            self.input_decoy_value = val_permutation(
                self.input_decoy_value
            )
        if self.output_decoy_value:
            self.output_decoy_value = val_permutation(
                self.output_decoy_value
            )

    def swap_values(self, value1, value2):
        """
        Swaps two values in the puzzle and solution.
        """

        def val_permutation(value):
            if value == value1:
                return value2
            if value == value2:
                return value1
            return value

        # Apply permutation
        new_puzzle = {
            (i,j): val_permutation(self.puzzle[(i,j)])
            for (i,j) in self.puzzle
        }
        self.puzzle = new_puzzle
        new_solution = {
            (i,j): val_permutation(self.solution[(i,j)])
            for (i,j) in self.solution
        }
        self.solution = new_solution
        if self.input_decoy_value:
            self.input_decoy_value = val_permutation(
                self.input_decoy_value
            )
        if self.output_decoy_value:
            self.output_decoy_value = val_permutation(
                self.output_decoy_value
            )
