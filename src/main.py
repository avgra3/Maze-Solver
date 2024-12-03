from tkinter import Tk, BOTH, Canvas
from constants import (
    HEIGHT,
    WIDTH,
    TITLE,
    MAZE_TOP_LEFT,
    CELL_SIZE_X,
    CELL_SIZE_Y,
    MAX_ROWS,
    MAX_COLUMNS,
    MAX_SLEEP_TIME,
)
import time
from typing import Union, Tuple


class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_one: Point, point_two: Point):
        self.point_one = point_one
        self.point_two = point_two

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point_one.x,
            self.point_one.y,
            self.point_two.x,
            self.point_two.y,
            fill=fill_color,
            width=2,
        )


class Window:
    def __init__(self, width: int = WIDTH, height: int = HEIGHT, title: str = TITLE):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = title
        self.__root.geometry(f"{self.width}x{self.height}")
        self.canvas = Canvas(self.__root)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(canvas=self.canvas, fill_color=fill_color)


class Cell:
    def __init__(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
        win: Window = None,
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def __repr__(self):
        class_name = "Cell"
        return (
            f"{class_name}=(x1={self._x1}, y1={self._y1}, x2={self._y2}, y2={self._y2})"
        )

    def draw(self):
        if self.has_left_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill="white"
            )
        if self.has_right_wall:
            self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2)
        else:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill="white"
            )
        if self.has_top_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill="white"
            )
        if self.has_bottom_wall:
            self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill="white"
            )

    def draw_move(self, to_cell, undo: bool = False):
        color = "gray"
        if undo is False:
            color = "red"

        current_xy = self._calculate_center(
            x1=self._x1, x2=self._x2, y1=self._y1, y2=self._y2
        )

        new_xy = self._calculate_center(
            x1=to_cell._x1, x2=to_cell._x2, y1=to_cell._y1, y2=to_cell._y2
        )

        center_current = Point(x=current_xy[0], y=current_xy[1])
        center_new = Point(x=new_xy[0], y=new_xy[1])

        connection = Line(point_one=center_current, point_two=center_new)
        connection.draw(canvas=self._win.canvas, fill_color=color)

    def _calculate_center(
        x1: Union[int, float],
        x2: Union[int, float],
        y1: Union[int, float],
        y2: Union[int, float],
    ) -> Tuple[float, float]:
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (x, y)


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._cells = []

        self._create_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        for i in range(self.num_cols):
            temp = []
            for j in range(self.num_rows):
                x_position = self.x1 + (j * self.cell_size_x)
                y_position = self.y1 + (i * self.cell_size_y)
                new_cell = Cell(
                    x1=x_position,
                    y1=y_position,
                    x2=x_position + self.cell_size_x,
                    y2=y_position + self.cell_size_y,
                    win=self.win,
                )
                temp.append(new_cell)
            self._cells.append(temp)

        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        current_cell = self._cells[i][j]
        if self.win:
            current_cell.draw()
            self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(MAX_SLEEP_TIME)

    def _break_entrance_and_exit(self):
        # Will always be at the top left cell
        # and the exit will always be at the bottom right cell
        self._cells[0][0].has_top_wall = False
        self._draw_cell(i=0, j=0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(i=-1, j=-1)


def main():
    win = Window(width=WIDTH, height=HEIGHT, title=TITLE)

    # point_one = Point(x=10, y=10)
    # point_two = Point(x=100, y=150)
    # point_three = Point(x=100, y=250)
    # point_four = Point(x=300, y=500)

    # line_one = Line(point_one=point_one, point_two=point_two)
    # line_two = Line(point_one=point_three, point_two=point_four)

    # fill_color = "red"

    # win.draw_line(line=line_one, fill_color=fill_color)
    # win.draw_line(line=line_two, fill_color=fill_color)

    # Cells
    """
    cell_one = Cell(
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
        x1=20,
        x2=60,
        y1=20,
        y2=60,
        win=win,
    )
    cell_one.draw()

    cell_two = Cell(
        has_left_wall=False,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
        x1=point_one.x,
        y1=point_one.y,
        x2=point_two.x,
        y2=point_two.y,
        win=win,
    )

    cell_two.draw()

    cell_three = Cell(
        has_left_wall=True,
        has_right_wall=False,
        has_top_wall=False,
        has_bottom_wall=True,
        x1=point_three.x,
        y1=point_three.y,
        x2=point_four.x,
        y2=point_four.y,
        win=win,
    )

    cell_three.draw()

    cell_one.draw_move(to_cell=cell_three)
    cell_two.draw_move(to_cell=cell_three, undo=True)
    """
    # Our Maze
    Maze(
        x1=MAZE_TOP_LEFT[0],
        y1=MAZE_TOP_LEFT[1],
        num_rows=MAX_ROWS,
        num_cols=MAX_COLUMNS,
        cell_size_x=CELL_SIZE_X,
        cell_size_y=CELL_SIZE_Y,
        win=win,
    )

    # Needs to be the last line
    win.wait_for_close()


if __name__ == "__main__":
    main()
