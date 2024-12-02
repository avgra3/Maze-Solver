from tkinter import Tk, BOTH, Canvas

HEIGHT = 800
WIDTH = 600


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
    def __init__(self, width: int = WIDTH, height: int = HEIGHT, title: str = None):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = title
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
        has_left_wall: bool = True,
        has_right_wall: bool = True,
        has_top_wall: bool = True,
        has_bottom_wall: bool = True,
        x1: int = 0,
        x2: int = 0,
        y1: int = 0,
        y2: int = 0,
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

    def draw(self):
        if self.has_left_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2)
        if self.has_right_wall:
            self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2)
        if self.has_top_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1)
        if self.has_bottom_wall:
            self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2)


def main():
    win = Window()

    point_one = Point(x=10, y=10)
    point_two = Point(x=100, y=150)
    point_three = Point(x=100, y=250)
    point_four = Point(x=300, y=500)

    # line_one = Line(point_one=point_one, point_two=point_two)
    # line_two = Line(point_one=point_three, point_two=point_four)

    fill_color = "red"

    # win.draw_line(line=line_one, fill_color=fill_color)
    # win.draw_line(line=line_two, fill_color=fill_color)

    # Cells
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

    # Needs to be the last line
    win.wait_for_close()


if __name__ == "__main__":
    main()
