import math
import sys

import numpy as np
import pygame
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_disk(board, row, column, disk):
    board[row][column] = disk


def is_valid_column(board, column):
    # 5 is the top row
    return board[ROW_COUNT - 1][column] == 0


def get_next_open_row(board, column):
    for r in range(ROW_COUNT):
        # Return the first instance of an empty row
        if board[r][column] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def win_game(board, disk):
    # Check horizontal rows for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == disk and board[r][c + 1] == disk and board[r][c + 2] == disk and board[r][c + 3] == disk:
                return True

    # Check vertical columns for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == disk and board[r + 1][c] == disk and board[r + 2][c] == disk and board[r + 3][c] == disk:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == disk and board[r + 1][c + 1] == disk and board[r + 2][c + 2] == disk and board[r + 3][
                c + 3] == disk:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == disk and board[r - 1][c + 1] == disk and board[r - 2][c + 2] == disk and board[r - 3][
                c + 3] == disk:
                return True


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARE_SIZE + SQUARE_SIZE / 2), (int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2))), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # Blacks out screen
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # print(event.pos)
            # Ask for Player 1 input
            if turn == 0:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_column(board, column):
                    row = get_next_open_row(board, column)
                    drop_disk(board, row, column, 1)

                if win_game(board, 1):
                    label = my_font.render("Player 1 wins!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

            # Ask for Player 2 input
            else:
                posx = event.pos[0]
                column = int(math.floor(posx / SQUARE_SIZE))

                if is_valid_column(board, column):
                    row = get_next_open_row(board, column)
                    drop_disk(board, row, column, 2)

                if win_game(board, 2):
                    label = my_font.render("Player 2 wins!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(3000)
