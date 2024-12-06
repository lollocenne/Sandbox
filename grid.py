"""
cells values:
    0: stone
    1: sand
    2: water left
    3: water right
    4: air

THIS ORDER IS IMPORTANT: the top one is heavier then the one below
"""

class Grid:
    def __init__(self):
        LIST_ELEMENTS: tuple[str] = ("stone", "sand", "waterLeft", "waterRight", "air")
        self.elements: dict[str, int] = {LIST_ELEMENTS[num] : num for num in range(len(LIST_ELEMENTS))}
        
        self.PIXEL_SIZE: int = 10
        SCREEN_SIZE: tuple[int, int] = (60, 30)   # replace with the screen size
        
        self.GRID_SIZE: tuple[int, int] = (SCREEN_SIZE[0] // self.PIXEL_SIZE, SCREEN_SIZE[1] // self.PIXEL_SIZE)
        self.grid: list[list[int]] = [[self.elements["air"] for _ in range(self.GRID_SIZE[0])] for _ in range(self.GRID_SIZE[1])]     # [y][x]
    
    # given the screen coordinates, it returns the grid coordinates
    def toGridCoords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] // self.PIXEL_SIZE, coords[1] // self.PIXEL_SIZE)
    
    # given the greed coordinates, it returns the screen coordinates
    def toScreenCoords(self, coords: tuple[int, int]) -> tuple[int, int]:
        return (coords[0] * self.PIXEL_SIZE, coords[1] * self.PIXEL_SIZE)
    
    # given the screen coordinates return the cell in the grid
    def getCellFromScreen(self, coords: tuple[int, int]) -> int:
        return self.getCellFromGrid(self.toGridCoords(coords))
    
    # given the coordinates return the cell in the grid
    def getCellFromGrid(self, coords: tuple[int, int]) -> int:
        return self.grid[coords[1]][coords[0]]
    
    def updateGrid(self) -> None:
        grid = self.grid    # just for readability
        
        for y in range(self.GRID_SIZE[1] - 1, -1, -1):
            for x in range(self.GRID_SIZE[0]):
                # reset the -1 to a waterRight
                if grid[y][x] == -1:
                    grid[y][x] = self.elements["waterRight"]
                    continue
                if grid[y][x] == self.elements["air"] or grid[y][x] == self.elements["stone"]: continue     # air and stone does not move
                # check if it can go down, down-left or down-right
                if y != self.GRID_SIZE[1] - 1:
                    for d in (0, -1, 1):
                        if x + d == self.GRID_SIZE[0] or x + d == -1: continue
                        if grid[y][x] < grid[y+1][x+d]:
                            grid[y][x], grid[y+1][x+d] = grid[y+1][x+d], grid[y][x]
                            break
                
                # water will move left and right untill it find somewhere to fall
                # check if water can go left, if not, it will try to go right
                if grid[y][x] == self.elements["waterLeft"]:
                    if x == 0 or grid[y][x] >= grid[y][x-1]:
                        grid[y][x] = self.elements["waterRight"]
                    else:
                        grid[y][x], grid[y][x-1] = grid[y][x-1], grid[y][x]
                        continue
                
                if grid[y][x] == self.elements["waterRight"]:
                    if x == self.GRID_SIZE[0] - 1 or grid[y][x] >= grid[y][x+1]:
                        grid[y][x] = self.elements["waterLeft"]
                    else:
                        grid[y][x], grid[y][x+1] = grid[y][x+1], -1     # set it to -1 to avoid moving it
    
    def __str__(self):
        grid = ""
        for row in self.grid:
            for cell in row:
                grid += str(cell)
            grid += "\n"
        return grid


if __name__ == "__main__":
    import time
    
    grid = Grid()
    print(grid)
    while True:
        time.sleep(0.5)
        grid.updateGrid()
        print(grid)