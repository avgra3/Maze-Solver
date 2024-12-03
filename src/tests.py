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

    def test_entrance_and_exit(self):
        num_cols, num_rows = 12, 10
        m1 = Maze(
            x1=0,
            y1=0,
            num_rows=num_rows,
            num_cols=num_cols,
            cell_size_x=10,
            cell_size_y=10,
        )

        top_left_cell = m1._cells[0][0]
        bottom_right_cell = m1._cells[-1][-1]

        self.assertEqual(top_left_cell.has_top_wall, False)
        self.assertEqual(bottom_right_cell.has_bottom_wall, False)


if __name__ == "__main__":
    unittest.main()
