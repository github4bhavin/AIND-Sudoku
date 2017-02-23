import unittest
import solution

#'.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........'

class NorvigSudokuTest(unittest.TestCase):

    def setUp(self):
        self.grid = '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........'

    def test_try(self):
        values = solution.solve(self.grid)
        self.assertTrue(solution.is_solved(values))
        solution.display(values)


if __name__ == '__main__':
    unittest.main(verbosity=3)