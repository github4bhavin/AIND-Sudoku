import solution
import unittest

class TestConstraints(unittest.TestCase):

    def setUp(self):
        self.board = solution.cross( solution.alphas, solution.digits)
        diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        solution.solve(diag_sudoku_grid)

    def test_col_constraints(self):
        for cell in self.board:
            self.assertEqual(len(solution.cols[cell]), 8 ,"cell:{}".format(cell))

    def test_row_constraints(self):
        for cell in self.board:
            self.assertEqual(len(solution.rows[cell]), 8 ,"cell:{}".format(cell))

    def test_box_constraints(self):
        for cell in self.board:
            self.assertEqual(len(solution.boxes[cell]), 8 ,"cell:{}".format(cell))

    def test_diagonal_constraints(self):
        for cell in solution.diagonals:
            if cell!= 'E5':
                self.assertEqual(len(solution.diagonals[cell]), 8 ,"cell:{}".format(cell))
            if cell == 'E5':
                self.assertEqual(len(solution.diagonals[cell]), 16, "cell:{}".format(cell))

if __name__ == '__main__':
    unittest.main(verbosity=3)
