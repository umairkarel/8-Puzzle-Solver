""" 
    Created on Thu June 20 2021

    @author: umairkarel
"""

import pygame
from board import Puzzle, fnt
from solver import solve
# Color
white = (255,255,255)

# Const
width = 400
height = 450
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
FPS = 60

# Board Vars
n = 3
moves = 0
board = Puzzle(n, width, height-50, screen)
solution = None
i = 0

def show_moves():
    txt = "Moves: " + str(moves)
    text = fnt.render(txt, 1, (0, 0, 255))
    screen.blit(text, (20, height-40))

def draw():
    global solution, i, moves, FPS

    if solution and i < len(solution):
        moves = i
        board.model = solution[i].data
        i += 1
        FPS = 1.5
    else:
        solution = None
        FPS = 60
        i = 0

    board.check_win()
    board.draw()
    show_moves()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not solution:
                    # Solve Puzzle
                    solution = solve(board.model, heuristic_func='manhattan')

            if event.key == pygame.K_SPACE:
                if not solution:
                    board.set_model()
                    moves = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not solution:
                pos = pygame.mouse.get_pos()
                placed = board.place(pos)
                
                if placed:
                    moves += 1

    pygame.display.flip()
    screen.fill(white)
    draw()
    
    clock.tick(FPS)


pygame.quit()