import os
from random import random
from uuid import uuid4
from typing import Tuple, Iterable

# Type hints
Position = Tuple[int, int]


class Cell:
    def __init__(self):
        self._id: str = uuid4().hex
        self._position: Position
        self._state: bool
        self._neighbours: Iterable[str]
        self._live_neighbours: int

    def __str__(self):
        return f"{self.id}, {self.state}"

    @property
    def id(self):
        return self._id

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: Position):
        self._position = position

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state: bool):
        self._state = state

    @property
    def neighbours(self):
        return self._neighbours

    @neighbours.setter
    def neighbours(self, neighbours: Iterable[str]):
        self._neighbours = neighbours

    @property
    def live_neighbours(self):
        return self._live_neighbours

    @live_neighbours.setter
    def live_neighbours(self, live_neighbours: int):
        self._live_neighbours = live_neighbours


class Grid:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._cells = self.generate_cells()
        self.update_cell_neighbours()

    @property
    def cells(self):
        return self._cells

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def generate_cells(self) -> Iterable[Cell]:
        cells = []

        for h in range(self.height):
            for w in range(self.width):
                cell = Cell()
                cell.state = True if random() > 0.90 else False
                cell.position = (w, h)
                cells.append(cell)

        return cells

    def update_cell_neighbours(self) -> None:
        max_x = max([c.position[0] for c in self.cells])
        max_y = max([c.position[1] for c in self.cells])

        def check_distance(cell: Cell, target: Cell) -> bool:
            x, y = cell.position
            tx, ty = target.position

            xArr = [x, x - 1, x + 1]
            if (x + 1 > max_x):
                xArr.append(0)

            if (x - 1 < 0):
                xArr.append(max_x)

            yArr = [y, y - 1, y + 1]
            if (y + 1 > max_y):
                yArr.append(0)

            if (y - 1 < 0):
                yArr.append(max_y)

            if (tx in xArr) and (ty in yArr):
                return True if (tx, ty) != (x, y) else False
            else:
                return False

        for cell in self.cells:
            neighbours: Iterable[str] = []
            _n = list(filter(lambda t: check_distance(cell, t), self.cells))
            _n = [cell.id for cell in _n]
            neighbours += _n
            cell.neighbours = neighbours

    def update_cells_state(self):
        def count_live_neighbours(neighbours: Iterable[str]) -> int:
            def fn(target: Cell) -> bool:
                if (target.id in neighbours) and (target.state):
                    return True
                else:
                    return False

            live_neighbours = list(filter(fn, self.cells))

            return len(live_neighbours)

        def calculate_state(state: bool, count: int) -> bool:
            switcher = {
                True: {
                    2: True,
                    3: True
                },
                False: {
                    3: True
                }
            }

            result = switcher[state].get(count, False)

            return result

        for cell in self.cells:
            count = count_live_neighbours(cell.neighbours)
            cell.live_neighbours = count
            cell.state = calculate_state(cell.state, count)

    def render_grid(self) -> None:
        grid: str = ""

        for h in range(self.height):
            row = list(filter(lambda r: r.position[1] == h, self.cells))
            grid += "".join(
                [str(r.live_neighbours)
                 if r.state
                 else " "
                 for r in row]
            )
            grid += "\n"

        os.system('cls')
        print(grid)


def main():
    grid = Grid(24, 24)

    while(True):
        grid.update_cells_state()
        grid.render_grid()


if (__name__ == "__main__"):
    main()
