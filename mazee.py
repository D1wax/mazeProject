# импорт пайгейм и рандома
import pygame
from random import choice


win = width, height = 1000, 600
tile = 50
#кол-во столбцов и рядов
cols, rows = width // tile, height // tile

pygame.init()
sc = pygame.display.set_mode(win)
clock = pygame.time.Clock()

c_border = (55,100,100)
class Cell:
    # объявление клетки и ее стен
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 
                      'right': True, 
                      'bottom': True, 
                      'left': True}
        self.visited = False
    # текущая клетка
    def draw_current_cell(self):
        x, y = self.x * tile, self.y * tile
        pygame.draw.rect(sc, (150,150,150), (x + 2, y + 2, tile - 2, tile - 2))
    # отрисовка клетки
    def draw(self):
        x, y = self.x * tile, self.y * tile
        if self.visited:
            pygame.draw.rect(sc, (10,10,10), (x, y, tile, tile))

        if self.walls['top']:
            pygame.draw.line(sc, c_border, (x, y), (x + tile, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, c_border, (x + tile, y), (x + tile, y + tile), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, c_border, (x + tile, y + tile), (x , y + tile), 3)
        if self.walls['left']:
            pygame.draw.line(sc, c_border, (x, y + tile), (x, y), 3)
    #проверка клетки по формуле нахождения индекса в одномерном массиве, зная координаты x,y в двумерном
    def check_index(self, x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[(x + y * cols)]
    #проверка на наличие соседних не посещенных клеток
    def check_neighbors(self):
        neighbors = []
        top = self.check_index(self.x, self.y - 1)
        right = self.check_index(self.x + 1, self.y)
        bottom = self.check_index(self.x, self.y + 1)
        left = self.check_index(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

#удаление стен
def del_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

#сетка с клетками
grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
#координата текущей клетки
current_cell = grid_cells[0]
stack = []
#цвет поля
color2 = 99,22,33

while True:
    sc.fill(color2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    for cell in grid_cells:
        cell.draw()
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        del_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(60)


