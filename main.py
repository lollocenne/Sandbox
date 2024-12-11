import sys
import pygame
from pygame._sdl2 import Window
from grid import Grid


def main():
    pygame.init()
    pygame.display.set_caption("Sendbox")
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    Window.from_display_module().maximize()
    grid = Grid(screen.get_size())
    clock = pygame.time.Clock()
    
    colors: dict[int: tuple[int, int, int]] = {
        grid.elements["stone"]: (128, 128, 128),
        grid.elements["sand"]: (194, 178, 128),
        grid.elements["water"]: (0, 0, 255),
        grid.elements["air"]: (0, 0, 0),
    }
    
    def getColor(cell: int) -> tuple[int, int, int]:
        return colors[cell]
    
    def drawGrid() -> None:
        for y in range(grid.GRID_SIZE[1]):
            for x in range(grid.GRID_SIZE[0]):
                cell: int = grid.grid[y][x]
                color = getColor(cell)
                screenX, screenY = grid.toScreenCoords((x, y))
                rect = pygame.Rect(screenX, screenY, grid.PIXEL_SIZE, grid.PIXEL_SIZE)
                pygame.draw.rect(screen, color, rect)
    
    def drawMouseSquare(x, y) -> None:
        length = size * grid.PIXEL_SIZE
        x, y = grid.toGridCoords((x, y))
        x -= size // 2
        y -= size // 2
        x, y = grid.toScreenCoords((x, y))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, length, length), width = 1)
    
    running: bool = True
    mousePressed: bool = False
    size: int = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePressed = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0 and size < max(grid.GRID_SIZE) + 1:
                    size += 2
                elif event.y < 0 and size > 1:
                    size -= 2
        
        mouseX, mouseY = pygame.mouse.get_pos()
        if mousePressed:
            touchX, touchY = mouseX, mouseY
            grid.addCells((touchX, touchY), size, 2)
        
        grid.updateGrid()
        screen.fill((0, 0, 0))
        drawGrid()
        drawMouseSquare(mouseX, mouseY)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()