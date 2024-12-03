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
import random


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
        self.visited = False

    def __repr__(self):
        class_name = "Cell"
        return f"{class_name}=(x1={self._x1}, y1={self._y1}, x2={self._y2}, y2={self._y2}, has_top={self.has_top_wall}, has_bottom={self.has_bottom_wall}, has_left={self.has_left_wall}, has_right={self.has_right_wall}"

    def draw(self):
        no_wall_color = "red"
        if self.has_left_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x1, self._y2, fill=no_wall_color
            )
        if self.has_right_wall:
            self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2)
        else:
            self._win.canvas.create_line(
                self._x2, self._y1, self._x2, self._y2, fill=no_wall_color
            )
        if self.has_top_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1)
        else:
            self._win.canvas.create_line(
                self._x1, self._y1, self._x2, self._y1, fill=no_wall_color
            )
        if self.has_bottom_wall:
            self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2)
        else:
            self._win.canvas.create_line(
                self._x1, self._y2, self._x2, self._y2, fill=no_wall_color
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
        seed=None,
    ):
        if seed is not None:
            random.seed(seed)
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
        self._break_walls_r(i=0, j=0)
        self._reset_cells_visited()
        if win is not None:
            self.win.redraw()

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
        # print(f"Cell at ({i}, {j}) ==> {self._cells[i][j]}")
        if self.win:
            current_cell.draw()
            self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(MAX_SLEEP_TIME)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(i=0, j=0)
        self._cells[-1][-1].has_bottom_wall = False
        self._draw_cell(i=-1, j=-1)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                current = self._cells[i][j]
                current.visited = False
                self._cells[i][j] = current

    def _break_walls_r(self, i: int, j: int):
        self._cells[i][j].visited = True

        # print(f"Breaking walls at cell ({i}, {j})")
        # print(f"Current cell walls: {self._cells[i][j].walls}")

        while True:
            # print(f"Checking for unvisited neighbors at ({i}, {j})")
            to_visit = {}

            # print(
            #    f"Checking neighbor: N({i-1},{j}), S({i+1},{j}), E({i},{j+1}), W({i},{j-1})"
            # )
            # print(
            #    f"Their visited states:",
            #    {
            #        "N": self._cells[i - 1][j].visited if i > 0 else "wall",
            #        "S": (
            #            self._cells[i + 1][j].visited
            #           if i < self.num_rows - 1
            #            else "wall"
            #        ),
            #        "E": (
            #            self._cells[i][j + 1].visited
            #            if j < self.num_cols - 1
            #            else "wall"
            #        ),
            #        "W": self._cells[i][j - 1].visited if j > 0 else "wall",
            #    },
            # )
            if i - 1 >= 0 and not self._cells[i-1][j].visited:
                to_visit["up"] = {
                        "coords": (i - 1, j),
                        "cell": self._cells[i - 1][j],
                    }

            if i + 1 < len(self._cells) and not self._cells[i + 1][j].visited:
                to_visit["down"] = {
                        "coords": (i + 1, j),
                        "cell": self._cells[i + 1][j],
                    }
            if j - 1 >= 0 and not self._cells[i][j - 1].visited:
                to_visit["left"] = {
                        "coords": (i, j - 1),
                        "cell": self._cells[i][j - 1],
                    }

            if j + 1 < len(self._cells[0]) and not self._cells[i][j + 1].visited:
                to_visit["right"] = {
                        "coords": (i, j + 1),
                        "cell": self._cells[i][j + 1],
                    }

            # print(f"Found {len(to_visit)} unvisited neighbors")
            # print(f"cell ({i}, {j}) has {len(to_visit)} unvisited neighbors")

            if len(to_visit) == 0:
                #    print(f"We should be drawing at ({i}, {j})")
                #    self._draw_cell(i=i, j=j)
                return

            random_direction = random.choice(list(to_visit.keys()))
            new_i, new_j = to_visit[random_direction]["coords"]
            wall_map = {
                "up": ("top", "bottom"),
                "down": ("bottom", "top"),
                "left": ("left", "right"),
                "right": ("right", "left"),
            }
            current_wall, next_wall = wall_map[random_direction]
            current_cell = self._cells[i][j]
            next_cell = self._cells[new_i][new_j]
            if current_wall == "top":
                current_cell.has_top_wall = False
                next_cell.has_bottom_wall = False
            elif current_wall == "down":
                current_cell.has_bottom_wall = False
                next_cell.has_top_wall = False
            elif current_wall == "left":
                current_cell.has_left_wall = False
                next_cell.has_right_wall = False
            elif current_wall == "right":
                current_cell.has_right_wall = False
                next_cell.has_left_wall = False

            self._cells[i][j] = current_cell
            self._cells[new_i][new_j] = next_cell

            # self._cells[i][j].walls[current_wall] = False
            # self._cells[new_i][new_j].walls[next_wall] = False

            self._draw_cell(i=i, j=j)
            self._draw_cell(i=new_i, j=new_j)
            self._break_walls_r(i=new_i, j=new_j)
            to_visit.pop(random_direction)
            # print(f"Returned to ({i}, {j}) after visitng ({new_i}, {new_j})")


def main():
    win = Window(width=WIDTH, height=HEIGHT, title=TITLE)

    # Our Maze
    Maze(
        x1=MAZE_TOP_LEFT[0],
        y1=MAZE_TOP_LEFT[1],
        num_rows=MAX_ROWS,
        num_cols=MAX_COLUMNS,
        cell_size_x=CELL_SIZE_X,
        cell_size_y=CELL_SIZE_Y,
        win=win,
        seed=0,
    )

    # Needs to be the last line
    win.wait_for_close()


if __name__ == "__main__":
    main()
