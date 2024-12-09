"""
Cells values:
    0: stone
    1: sand
    2: water left
    3: water right
    4: air

THIS ORDER IS IMPORTANT: the top one can replace the one below
"""

from random import choice


class Grid:
    def __init__(self, screenSize: tuple[int, int]):
        LIST_ELEMENTS: tuple[str] = ("stone", "sand", "waterLeft", "waterRight", "air")
        self.elements: dict[str, int] = {LIST_ELEMENTS[num] : num for num in range(len(LIST_ELEMENTS))}
        
        self.PIXEL_SIZE: int = 10
        SCREEN_SIZE: tuple[int, int] = (screenSize[0], screenSize[1])
        
        self.GRID_SIZE: tuple[int, int] = (SCREEN_SIZE[0] // self.PIXEL_SIZE, SCREEN_SIZE[1] // self.PIXEL_SIZE)
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
            if y + center[1] < 0 or y + center[1] >= self.GRID_SIZE[1]: continue
            for x in range(-size // 2 + 1, size // 2 + 1):
                if x + center[0] < 0 or x + center[0] >= self.GRID_SIZE[0]: continue
                self.grid[y + center[1]][x + center[0]] = cell
    
    # Physics
    def updateGrid(self) -> None:
        grid = self.grid    # Just for readability
        canUpdate: bool = True    # False if it needs to skip some updates
        
        for y in range(self.GRID_SIZE[1] - 1, -1, -1):
            for x in choice([range(self.GRID_SIZE[0]), range(self.GRID_SIZE[0] - 1, -1, -1)]):
                if not canUpdate:
                    canUpdate = True
                    continue
                if grid[y][x] == self.elements["air"] or grid[y][x] == self.elements["stone"]: continue     # Air and stone does not move
                # Check if it can go down, down-left or down-right
                if y != self.GRID_SIZE[1] - 1:
                    for d in (0, -1, 1):
                        if x + d == self.GRID_SIZE[0] or x + d == -1: continue
                        if grid[y][x] < grid[y+1][x+d]:
                            grid[y][x], grid[y+1][x+d] = grid[y+1][x+d], grid[y][x]
                            break
                
                # Water will move left and right untill it find somewhere to fall
                # Check if water can go left, if not, it will try to go right
                if grid[y][x] == self.elements["waterLeft"]:
                    if x == 0 or grid[y][x] >= grid[y][x-1]:
                        grid[y][x] = self.elements["waterRight"]
                    else:
                        grid[y][x], grid[y][x-1] = grid[y][x-1], grid[y][x]
                        canUpdate = False   # It should not get updated
                        continue
                
                if grid[y][x] == self.elements["waterRight"]:
                    if x == self.GRID_SIZE[0] - 1 or grid[y][x] >= grid[y][x+1]:
                        grid[y][x] = self.elements["waterLeft"]
                    else:
                        grid[y][x], grid[y][x+1] = grid[y][x+1], grid[y][x]
                        canUpdate = False   # It should not get updated
    
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