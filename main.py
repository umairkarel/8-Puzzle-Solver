""" 
    Created on Thu June 20 2021

    @author: umairkarel
"""

import pygame
from board import Puzzle, fnt
from solver import solve
from constants import WIDTH, HEIGHT, WHITE


# Pygame Constants
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Board Vars
BOARD_LENGTH = 3
MOVES_TAKEN = 0
GAME_BOARD = Puzzle(BOARD_LENGTH, WIDTH, HEIGHT - 50, screen)
SOLUTION = None
i = 0


def show_moves():
    """
    Display the number of moves taken on the screen.
    """
    # Render the text onto the screen
    text = fnt.render(f"Moves: {MOVES_TAKEN}", 1, (0, 0, 255))

    # Blit the text onto the screen at the specified coordinates
    screen.blit(text, (20, HEIGHT - 40))


def draw():
    """
    A function that updates the game state.
    """
    global SOLUTION, i, MOVES_TAKEN, FPS

    if SOLUTION and i < len(SOLUTION):
        MOVES_TAKEN = i
        GAME_BOARD.model = SOLUTION[i].data
        i += 1
        FPS = 1.5
    else:
        SOLUTION = None
        FPS = 60
        i = 0

    GAME_BOARD.check_win()
    GAME_BOARD.draw()
    show_moves()


RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not SOLUTION:
                    # Solve Puzzle
                    SOLUTION = solve(GAME_BOARD.model, heuristic_func="manhattan")

            if event.key == pygame.K_SPACE:
                if not SOLUTION:
                    GAME_BOARD.set_model()
                    MOVES_TAKEN = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not SOLUTION:
                pos = pygame.mouse.get_pos()

                if GAME_BOARD.place(pos):
                    MOVES_TAKEN += 1

    pygame.display.flip()
    screen.fill(WHITE)
    draw()

    clock.tick(FPS)


pygame.quit()
