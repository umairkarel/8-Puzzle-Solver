""" 
    Created on Thu June 20 2021

    @author: umairkarel
"""

import random
import pygame

pygame.font.init()
fnt = pygame.font.SysFont("comicsans", 60)

class Puzzle:
    def __init__(self, n, width, height, screen):
        """
        Initializes the Puzzle object with the provided dimensions and screen parameters.

        Parameters:
            n (int): The number of rows and columns in the puzzle.
            width (int): The width of the puzzle.
            height (int): The height of the puzzle.
            screen: The screen object to display the puzzle.

        Returns:
            None
        """
        self.rows = n
        self.cols = n
        self.width = width
        self.height = height
        self.screen = screen
        self.model = [[0 for i in range(self.rows)] for j in range(self.cols)]
        self.is_win = False
        self.set_model()

    def set_model(self):
        self.is_win = False
        nums = [i for i in range((self.rows * self.cols))]
        random.shuffle(nums)

        while not self.isSolvable(nums):
            random.shuffle(nums)

        self.model = [[nums[i * self.cols + j] for j in range(self.cols)] for i in range(self.rows)]

    def isSolvable(self, board):
        inv_count = 0
        x = 0

        for i in range(len(board)-1):

            for j in range(i+1, len(board)):
                if board[i] > 0 and board[j] > 0 and board[i] > board[j]:
                    inv_count += 1
                elif board[j] == 0:
                    x = j // self.cols

        if self.rows%2 != 0:
            return (inv_count % 2 == 0)
        else: 
            if (self.rows-x)%2 == 0:
                return inv_count%2 != 0
            else:
                return inv_count%2 == 0

    def check_win(self):
        num = 1
        rows = self.rows
        cols = self.cols
        model = self.model

        for i in range(rows):
            for j in range(cols):
                if model[i][j] != num:
                    if i == rows-1 and j == cols-1 and model[i][j] == 0:
                        self.is_win = True
                        return
                    self.is_win = False
                    return 
                num += 1

        self.is_win = True

    def draw(self):
        gap = self.width // self.rows
        text_pos = gap
        linecolor = (0,0,0) if not self.is_win else (0,255,0)

        for i in range(self.rows+1):
            pygame.draw.line(self.screen, linecolor, (0,i*gap), (self.width,i*gap), 1)
            pygame.draw.line(self.screen, linecolor, (i*gap,0), (i*gap,self.height), 1)

        for x in range(self.rows):
            for y in range(self.cols):
                char = ' ' if self.model[x][y] == 0 else str(self.model[x][y])
                text = fnt.render(char, 1, (0, 0, 0))
                self.screen.blit(text, (y*gap + (gap/2 - text.get_width()/2), x*gap + (gap/2 - text.get_height()/2)))

    def place(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width // self.rows
            x = pos[1] // gap
            y = pos[0] // gap

            if self.model[x][y] == 0:
                return False
            
            move = self.check_if_valid_move(x,y)
            if move:
                a,b = move
                self.model[x][y], self.model[a][b] = self.model[a][b], self.model[x][y]

                return True

        return False

    def check_if_valid_move(self,x,y):
        if (y != 0 and self.model[x][y-1] == 0):
            return (x,y-1)
        if (y != self.cols-1 and self.model[x][y+1] == 0):
            return (x,y+1)
        if (x != 0 and self.model[x-1][y] == 0):
            return (x-1,y)
        if (x != self.rows-1 and self.model[x+1][y] == 0):
            return (x+1,y)

        return False