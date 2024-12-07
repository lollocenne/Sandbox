import sys
import pygame
from grid import Grid


def main():
    pygame.init()
    screenSize = (600, 300)
    screen = pygame.display.set_mode(screenSize)
    grid = Grid(screenSize)
    clock = pygame.time.Clock()
    
    colors = {
        grid.elements["stone"]: (128, 128, 128),
        grid.elements["sand"]: (194, 178, 128),
        grid.elements["waterLeft"]: (0, 0, 255),
        grid.elements["waterRight"]: (0, 0, 255),
        grid.elements["air"]: (0, 0, 0),
    }
    
    def drawGrid():
        for y in range(grid.GRID_SIZE[1]):
            for x in range(grid.GRID_SIZE[0]):
                cell = grid.grid[y][x]
                color = getColor(cell)
                screenX, screenY = grid.toScreenCoords((x, y))
                rect = pygame.Rect(screenX, screenY, grid.PIXEL_SIZE, grid.PIXEL_SIZE)
                pygame.draw.rect(screen, color, rect)

    def getColor(cell):
        return colors[cell]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        grid.updateGrid()
        screen.fill((0, 0, 0))
        drawGrid()
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()