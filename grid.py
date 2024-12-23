"""
Cells values:
    0: stone
    1: sand
    2: water
    3: air

THIS ORDER IS IMPORTANT: the top one can replace the one below
"""

from random import choice


class Grid:
    def __init__(self, screenSize: tuple[int, int]):
        self.LIST_ELEMENTS: tuple[str] = ("stone", "sand", "water", "air")
        self.elements: dict[str, int] = {self.LIST_ELEMENTS[num] : num for num in range(len(self.LIST_ELEMENTS))}
        
        # Get the smallest pixel size for the screen starting from a min size
        def getMinSize(min, num):
            while num % min != 0: min += 1
            return min
        self.PIXEL_SIZE: int = getMinSize(10, screenSize[1])
        
        self.GRID_SIZE: tuple[int, int] = self.toGridCoords(screenSize)
        self.grid: list[list[int]] = [[self.elements["air"] for _ in range(self.GRID_SIZE[0])] for _ in range(self.GRID_SIZE[1])]     # [y][x]
    
    # Given the screen coordinates, it returns the grid coordinates
    def toGridCoords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] // self.PIXEL_SIZE, coords[1] // self.PIXEL_SIZE)
    
    # Given the greed coordinates, it returns the screen coordinates
    def toScreenCoords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] * self.PIXEL_SIZE, coords[1] * self.PIXEL_SIZE)
    
    # Add the cells to the grid using the brush
    def addCells(self, center: tuple[int, int], size: tuple[int, int], cell: int) -> None:
        """
        centerCoords: center of the brush
        size: length, height of the brush
        cell: value for each cell
        """
        center = self.toGridCoords(center)
        for y in range(-size // 2 + 1, size // 2 + 1):
            if y + center[1] < 0: continue
            if y + center[1] >= self.GRID_SIZE[1]: return
            for x in range(-size // 2 + 1, size // 2 + 1):
                if x + center[0] < 0: continue
                if x + center[0] >= self.GRID_SIZE[0]: break
                self.grid[y + center[1]][x + center[0]] = cell
    
    # Physics
    def updateGrid(self) -> None:
        grid = self.grid    # Just for readability
        canUpdate: bool = True    # False if it needs to skip some updates (usuali water set it to False)
        
        updateToRight: bool = True    # True if the rows are updated from left to right, it switch for each row
        for y in range(self.GRID_SIZE[1] - 1, -1, -1):
            updateToRight = not updateToRight   # Switch the update direction
            canUpdate = True
            row = range(self.GRID_SIZE[0]) if updateToRight else range(self.GRID_SIZE[0] - 1, -1, -1)
            for x in row:
                if not canUpdate:
                    canUpdate = True
                    continue
                if grid[y][x] == self.elements["air"] or grid[y][x] == self.elements["stone"]: continue     # Air and stone does not move
                # Check if it can go down, down-left or down-right
                if y != self.GRID_SIZE[1] - 1:
                    for d in (0,) + choice([(-1, 1), (1, -1)]):
                        if x + d == self.GRID_SIZE[0] or x + d == -1: continue
                        if grid[y][x] < grid[y+1][x+d]:
                            grid[y][x], grid[y+1][x+d] = grid[y+1][x+d], grid[y][x]
                            break
                
                # Check where water can go and chooses randomly where to go
                if grid[y][x] == self.elements["water"]:
                    possibleMoves = [-1, 1]
                    if x + 1 == self.GRID_SIZE[0] or grid[y][x] >= grid[y][x + 1]:  # Check if it can go right
                        possibleMoves.pop()
                    if x == 0 or grid[y][x] >= grid[y][x - 1]:  # Check if it can go left
                        possibleMoves.pop(0)
                    
                    # Randomly choose a direction
                    if possibleMoves:
                        move = choice(possibleMoves)
                    else:
                        continue
                    
                    # Move and avoid getting updated angain
                    grid[y][x], grid[y][x + move] = grid[y][x + move], grid[y][x]
                    if move == 1:
                        if updateToRight: canUpdate = False
                    elif move == -1:
                        if not updateToRight: canUpdate = False
    
    def __str__(self):
        grid = ""
        for row in self.grid:
            for cell in row:
                grid += str(cell)
            grid += "\n"
        return grid


if __name__ == "__main__":
    import time
    
    grid = Grid((60, 30))
    print(grid)
    while True:
        time.sleep(0.5)
        grid.updateGrid()
        print(grid)