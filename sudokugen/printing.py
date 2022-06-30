"""
Module with additional printing functionality (for regular 9x9 sudoku's)
"""

from .instances import Instance, RegularSudoku

def latex_preamble() -> str:
    """
    Returns the LaTeX preamble needed to print Sudoku instances in LaTeX
    """

    preamble = """
        \\usepackage{tikz}
        \\newcounter{row}
        \\newcounter{col}
        \\newcommand\\setrow[9]{
          \\setcounter{col}{1}
          \\foreach \\n in {#1, #2, #3, #4, #5, #6, #7, #8, #9} {
            \\edef\\x{\\value{col} - 0.5}
            \\edef\\y{9.5 - \\value{row}}
            \\node[anchor=center] at (\\x, \\y) {\\Large \\n};
            \\stepcounter{col}
          }
          \\stepcounter{row}
        }

        \\usepackage{ifthen}
        \\usepackage{substr}

        \\newcommand{\\pencilraw}[9]{%
        \\color{black!50}
        \\begin{tikzpicture}
          \\node[] at (-0.3,0.6) {\\scriptsize #1};
          \\node[] at (-0.3,0.3) {\\scriptsize #4};
          \\node[] at (-0.3,0) {\\scriptsize #7};
          \\node[] at (0,0.6) {\\scriptsize #2};
          \\node[] at (0,0.3) {\\scriptsize #5};
          \\node[] at (0,0) {\\scriptsize #8};
          \\node[] at (0.3,0.6) {\\scriptsize #3};
          \\node[] at (0.3,0.3) {\\scriptsize #6};
          \\node[] at (0.3,0) {\\scriptsize #9};
        \\end{tikzpicture}
        }
        \\newcommand{\\pencil}[1]{%
        \\pencilraw%
        {\\IfSubStringInString{1!}{#1}{\\color{red!50} \\sout{1}}{\\IfSubStringInString{1}{#1}{1}{\\phantom{1}}}}%
        {\\IfSubStringInString{2!}{#1}{\\color{red!50} \\sout{2}}{\\IfSubStringInString{2}{#1}{2}{\\phantom{2}}}}%
        {\\IfSubStringInString{3!}{#1}{\\color{red!50} \\sout{3}}{\\IfSubStringInString{3}{#1}{3}{\\phantom{3}}}}%
        {\\IfSubStringInString{4!}{#1}{\\color{red!50} \\sout{4}}{\\IfSubStringInString{4}{#1}{4}{\\phantom{4}}}}%
        {\\IfSubStringInString{5!}{#1}{\\color{red!50} \\sout{5}}{\\IfSubStringInString{5}{#1}{5}{\\phantom{5}}}}%
        {\\IfSubStringInString{6!}{#1}{\\color{red!50} \\sout{6}}{\\IfSubStringInString{6}{#1}{6}{\\phantom{6}}}}%
        {\\IfSubStringInString{7!}{#1}{\\color{red!50} \\sout{7}}{\\IfSubStringInString{7}{#1}{7}{\\phantom{7}}}}%
        {\\IfSubStringInString{8!}{#1}{\\color{red!50} \\sout{8}}{\\IfSubStringInString{8}{#1}{8}{\\phantom{8}}}}%
        {\\IfSubStringInString{9!}{#1}{\\color{red!50} \\sout{9}}{\\IfSubStringInString{9}{#1}{9}{\\phantom{9}}}}%
        }

        \\newcommand{\\drawrow}[9]{%
        \\setrow {#1}{#2}{#3}  {#4}{#5}{#6}  {#7}{#8}{#9}%
        }
        \\newcommand{\\drawsudoku}[9]{
        \\begin{tikzpicture}[scale=1]
          \\begin{scope}
            \\draw (0, 0) grid (9, 9);
            \\draw[ultra thick, scale=3] (0, 0) grid (3, 3);
            \\setcounter{row}{1}
            #1
            #2
            #3

            #4
            #5
            #6

            #7
            #8
            #9
          \\end{scope}
        \\end{tikzpicture}
        }
    """
    return preamble

def repr_latex(
        instance: Instance,
        show_pencil: bool = False
    ) -> str:
    """
    Returns the LaTeX code for a Sudoku instance

    Works only for RegularSudoku instances of size 9
    """
    # pylint: disable=too-many-branches

    if not isinstance(instance, RegularSudoku):
        raise TypeError(f"Wrong type found: {type(instance)}")
    if instance.size != 9:
        raise ValueError("RegularSudoku.size should be 9")

    latex_repr = "\\drawsudoku%\n"

    pencil = {}
    for row in range(1, 10):
        for col in range(1, 10):
            pencil[(col, row)] = list(range(1, 10))

    for _, group in instance.groups:
        for cell1 in group:
            value = instance.puzzle[cell1]
            if value != 0:
                for cell2 in group:
                    try:
                        pencil[cell2].remove(value)
                    except ValueError:
                        pass

    cell_fill = {}
    for row in range(1, 10):
        for col in range(1, 10):
            value = instance.puzzle[(col, row)]
            if value != 0:
                cell_fill[(col, row)] = value
            else:
                if show_pencil:
                    pencil_str = "".join(map(str, pencil[(col, row)]))
                    cell_fill[(col, row)] = f"\\pencil{{{pencil_str}}}"
                else:
                    cell_fill[(col, row)] = " "

    for row in range(1, 10):
        cells = [cell_fill[(col, row)] for col in range(1, 10)]
        latex_repr += ("{{\\drawrow " + \
            "{{{}}}{{{}}}{{{}}} " + \
            "{{{}}}{{{}}}{{{}}} " + \
            "{{{}}}{{{}}}{{{}}} }}\n").format(
                *cells
            )

    return latex_repr[:-1]
