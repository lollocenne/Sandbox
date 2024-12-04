class Grid:
    def __init__(self):
        PIXEL_SIZE: int = 10
        SCREEN_SIZE: tuple[int, int] = (50, 100)   # sostituire con la grandezza dello schermo
        GRID_SIZE: tuple[int, int] = (SCREEN_SIZE[0] // PIXEL_SIZE, SCREEN_SIZE[1] // PIXEL_SIZE)
        self.grid = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]     #[y][x]
    
    def __str__(self):
        string = ""
        for row in self.grid:
            for cell in row:
                string += str(cell)
            string += "\n"
        return string


if __name__ == "__main__":
    grid = Grid()
    print(grid)