import unittest
from main import Maze, Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(
            x1=0,
            y1=0,
            num_rows=num_rows,
            num_cols=num_cols,
            cell_size_x=10,
            cell_size_y=10,
        )
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)
        self.assertIsNone(m1.win)

        num_cols = 44
        num_rows = 10
        m2 = Maze(
            x1=1,
            y1=1,
            num_rows=num_rows,
            num_cols=num_cols,
            cell_size_x=100,
            cell_size_y=100,
        )
        self.assertEqual(len(m2._cells), num_cols)
        self.assertEqual(len(m2._cells[0]), num_rows)
        self.assertIsNone(m2.win)


if __name__ == "__main__":
    unittest.main()
