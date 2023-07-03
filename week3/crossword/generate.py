import sys
from copy import deepcopy
from random import randrange, choice

from crossword import *

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

import time


class CrosswordCreator:
    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterates over every variable v.
        for v in self.crossword.variables:
            # Creates a set of inconsistencies.
            inconsistent = set([x for x in self.domains[v] if len(x) != v.length])
            # Then removes them from v's domain, if any.
            if inconsistent:
                self.domains[v] = self.domains[v] - inconsistent

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Gets the ith, jth positions of the overlap for respective variables.
        try:
            i, j = self.crossword.overlaps[x, y]
        except TypeError:
            # No overlap, no revision made.
            return False

        # Creates a set of inconsistencies in x's domain given y's domain.
        y_domain = [yw[j] for yw in self.domains[y]]
        inconsistent = set([xw for xw in self.domains[x] if xw[i] not in y_domain])

        # Then removes them from x's domain, if any.
        if inconsistent:
            self.domains[x] = self.domains[x] - inconsistent
            return True

        # No inconsistencies, no revision.
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs is none, arcs set to initial list of arcs.
        if not arcs:
            arcs = [
                (x, y)
                for x in self.domains
                for y in self.domains
                if x != y and self.crossword.overlaps[x, y] is not None
            ]

        # Removes inverse duplicates.
        for x, y in arcs:
            if (y, x) in arcs:
                arcs.remove((y, x))

        # Iterates oveer every arc.
        while arcs:
            # Selects any arc.
            x, y = arcs.pop(randrange(len(arcs)))

            # Revises selected arc.
            if self.revise(x, y):
                # No more possible values, impossible to solve.
                if not self.domains[x]:
                    return False

                # If successufuly revised, extends queue with new arcs.
                arcs.extend(
                    [
                        (z, x)
                        for z in self.crossword.neighbors(x)
                        if z != y and ((z, x) not in arcs or (x, z) not in arcs)
                    ]
                )

        # Arc consistency enforced.
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(v in assignment for v in self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        checked = list()
        for v1 in assignment:
            # Checks conflicting length
            if len(assignment[v1]) != v1.length:
                return False

            # Checks conflicting characters on overlaps
            for neighbour in self.crossword.neighbors(v1):
                if neighbour not in assignment or neighbour in checked:
                    continue

                i, j = self.crossword.overlaps[v1, neighbour]
                if assignment[v1][i] != assignment[neighbour][j]:
                    return False

            # Checks conflicting words
            for v2 in assignment:
                if v1 is v2 or v2 in checked:
                    continue
                if assignment[v1] == assignment[v2]:
                    return False

            checked.append(v1)
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Copies var's domain, excluding variables already assigned
        domain = [v for v in self.domains[var] if v not in assignment]

        # Creates a dictionary of value: quantity of affected neighbours pairs
        values = {
            value: len(
                [
                    neighbour
                    for neighbour in self.crossword.neighbors(var)
                    if value in self.domains[neighbour]
                ]
            )
            for value in domain
        }

        # Sorts dictionary by values and returns it's keys as a list
        return [item[0] for item in sorted(values.items(), key=lambda item: item[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Gets unassigned variables
        unassigned = [var for var in self.crossword.variables if var not in assignment]

        # Gets variable's domain lengths and filters by MRV
        remaining = [len(self.domains[var]) for var in unassigned]
        unassigned = [
            unassigned[index]
            for index in [i for i, j in enumerate(remaining) if j == min(remaining)]
        ]

        # Gets variable's degrees and filters by degree
        degrees = [len(self.crossword.neighbors(var)) for var in unassigned]
        unassigned = [
            unassigned[index]
            for index in [i for i, j in enumerate(degrees) if j == max(degrees)]
        ]

        # Picks randomly from filtered variables.
        return choice(unassigned)

    def inference(self, assignment, var):
        """
        Updates the domain and current assignment via inference,
        enforcing arc and node consistency, given a  variable `var`
        and a uncompleted assignment `assignment`.

        Returns the updated `assignment` and the `inferences` made.
        """
        # 1. Enforces arc consistency
        # Creates empty inferences list
        inferences = list()

        # Creates a list of arcs of var and it's neighbours then enforces arc consistency
        arcs = [(neighbour, var) for neighbour in self.crossword.neighbors(var)]
        self.ac3(arcs)

        # 2. Enforces node consistency
        # Iterates over every variable in the domain
        for v in self.domains:
            # Checks for possible values
            if len(self.domains[v]) == 1:
                # If only one, assigns it to assignment and deletes from domain
                assignment[v] = self.domains[v].pop()
                inferences.append(v)

        # Returns updated assignment and inferences
        return (assignment, inferences)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Returns completed assignment
        if self.assignment_complete(assignment):
            return assignment
        
        # Selects an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Orders the var's domain by least constraining value and then iterates over it
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            inferences = []
            if self.consistent(assignment):
                # Updates domain and assignment via inference
                assignment, inferences = self.inference(assignment, var)

                # Backtracks with current assignment
                result = self.backtrack(assignment)
                if result:
                    return result

            # If now inconsistent, deletes variable and inferences from assignment
            del assignment[var]
            for inference in inferences:
                del assignment[inference]

        # No satisfying assignment is possible
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)

    t0 = time.time()
    assignment = creator.solve()
    print("--- solved in %0.5f seconds ---" % (time.time() - t0))

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
