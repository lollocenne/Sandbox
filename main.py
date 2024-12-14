import sys
import pygame
import random
from pygame._sdl2 import Window
from grid import Grid


def main():
    pygame.init()
    pygame.display.set_caption("Sandbox")
    screen = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
    Window.from_display_module().maximize()
    screenLength, screenHeight = screen.get_size()
    buttonsAreaSize = (300, screenHeight)
    grid = Grid((screenLength - buttonsAreaSize[0], screenHeight))
    clock = pygame.time.Clock()
    
    colors: dict[int, tuple[int, int, int]] = {
        grid.elements["stone"]: (128, 128, 128),
        grid.elements["sand"]: (194, 178, 128),
        grid.elements["water"]: (0, 0, 255),
        grid.elements["air"]: (0, 0, 0),
    }
    
    # Colors based on the position
    def clamp(values, minVal, maxVal) -> list:  return [max(minVal, min(val, maxVal)) for val in values]
    def getColor(cell: int, x: int, y: int) -> tuple[int, int, int]:
        change = hash((x, y, y*2, x/(y + 1))) % 21 - 10
        R, G, B = colors[cell]
        return clamp((R + change, G + change, B + change), 0, 255)
    
    def drawGrid() -> None:
        for y in range(grid.GRID_SIZE[1]):
            for x in range(grid.GRID_SIZE[0]):
                cell: int = grid.grid[y][x]
                color = getColor(cell, x, y)
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
    
    def drawButtonsArea(mouseCoords: tuple[int, int]):
        nonlocal element
        buttons = grid.LIST_ELEMENTS
        font = pygame.font.Font(size = 30)
        buttonHeight, gap = 50, 70
        totalHeight = len(buttons) * buttonHeight + (len(buttons) - 1) * gap
        startY = (screenHeight - totalHeight) // 2
        
        for i, text in enumerate(buttons):
            buttonX = screenLength - buttonsAreaSize[0] // 2 - 100
            buttonY = startY + i * (buttonHeight + gap)
            buttonRect = pygame.Rect(buttonX, buttonY, 200, buttonHeight)
            pygame.draw.rect(screen, colors[grid.elements[text]], buttonRect)
            if element == grid.elements[text.lower()]:
                pygame.draw.rect(screen, (255, 255, 255), buttonRect, width=3)
            textSurface = font.render(text.upper(), True, (255, 255, 255))
            textRect = textSurface.get_rect(center=buttonRect.center)
            screen.blit(textSurface, textRect)
            
            if buttonRect.collidepoint(mouseCoords) and pygame.mouse.get_pressed()[0]:
                element = grid.elements[text.lower()]
    
    running: bool = True
    mousePressed: bool = False
    size: int = 5
    element: int = grid.elements["water"]
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
            grid.addCells((mouseX, mouseY), size, element)
        
        grid.updateGrid()
        screen.fill((30, 30, 35))
        drawGrid()
        drawMouseSquare(mouseX, mouseY)
        drawButtonsArea((mouseX, mouseY))
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()