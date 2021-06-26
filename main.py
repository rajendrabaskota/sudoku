import pygame

WIDTH = 450
HEIGHT = 500
RECT_SIZE = 50

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()
pygame.display.set_caption('Sudoku')


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("| " + str(board[i][j]) + " ", end="")
            elif j == 8:
                print(str(board[i][j]))
            else:
                print(str(board[i][j]) + " ", end="")


def empty_space(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j

    return None


def validity_check(board, row, col, value):
    # row_check
    for j in range(len(board[0])):
        if board[row][j] == value and j != col:
            return False

    # column_check
    for i in range(len(board)):
        if board[i][col] == value and i != row:
            return False

    # box_check
    row_modified = row // 3
    col_modified = col // 3
    for i in range(row_modified * 3, row_modified * 3 + 3):
        for j in range(col_modified * 3, col_modified * 3 + 3):
            if board[i][j] == value and (i, j) != (row, col):
                return False

    return True


def solve_board(board):
    empty_box = empty_space(board)
    if not empty_box:
        return True
    else:
        row, column = empty_box
    for i in range(1, 10):
        if validity_check(board, row, column, i):
            board[row][column] = i

            if solve_board(board):
                return True

            board[row][column] = 0

    return False


def redraw_window(board, board_guess, rect_colors, errors):
    font = pygame.font.SysFont('comicsans', 30)

    win.fill((200, 200, 200))
    pygame.draw.lines(win, (0, 0, 0), True, [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT - RECT_SIZE), (0, HEIGHT - RECT_SIZE)], 2)

    for i in range(9):
        for j in range(9):
            pygame.draw.rect(win, rect_colors[i][j], (j * RECT_SIZE, i * RECT_SIZE, RECT_SIZE, RECT_SIZE), 1)
            if j % 3 == 0 and j != 0:
                pygame.draw.line(win, (0, 0, 0), (j * RECT_SIZE, i * RECT_SIZE), (j * RECT_SIZE, i * RECT_SIZE + RECT_SIZE), 2)
            if i % 3 == 0:
                pygame.draw.line(win, (0, 0, 0), (j * RECT_SIZE, i * RECT_SIZE), (j * RECT_SIZE + RECT_SIZE, i * RECT_SIZE), 2)

            if board[i][j] != 0:
                text = font.render(str(board[i][j]), 1, (50, 50, 50))
                win.blit(text, (((j * RECT_SIZE) + (j * RECT_SIZE + RECT_SIZE)) / 2 - text.get_width() / 2, (i * RECT_SIZE) / 2 + (i * RECT_SIZE + RECT_SIZE) / 2 - text.get_height() / 2))

            if board_guess[i][j] != 0:
                font_guess = pygame.font.SysFont('comicsans', 25)
                text = font_guess.render(str(board_guess[i][j]), 1, (50, 50, 50))
                win.blit(text, (j * RECT_SIZE, i * RECT_SIZE))

    for i in range(errors):
        text = font.render('X', 1, (255, 0, 0))
        win.blit(text, (i * RECT_SIZE, 450))

    pygame.display.update()


def main():
    run = True
    errors = 0
    clock = pygame.time.Clock()
    board = [
        [0, 8, 0, 0, 0, 9, 1, 0, 0],
        [0, 0, 0, 0, 8, 7, 0, 0, 3],
        [0, 0, 0, 5, 4, 6, 0, 0, 0],
        [0, 0, 8, 0, 9, 0, 0, 0, 1],
        [0, 0, 2, 0, 0, 0, 7, 5, 0],
        [0, 0, 1, 0, 2, 0, 0, 0, 6],
        [3, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 3, 9, 0],
        [9, 0, 0, 0, 7, 0, 0, 2, 0]
    ]

    board_guess = [[0 for _ in range(9)] for _ in range(9)]

    board_answer = [
        [0, 8, 0, 0, 0, 9, 1, 0, 0],
        [0, 0, 0, 0, 8, 7, 0, 0, 3],
        [0, 0, 0, 5, 4, 6, 0, 0, 0],
        [0, 0, 8, 0, 9, 0, 0, 0, 1],
        [0, 0, 2, 0, 0, 0, 7, 5, 0],
        [0, 0, 1, 0, 2, 0, 0, 0, 6],
        [3, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 3, 9, 0],
        [9, 0, 0, 0, 7, 0, 0, 2, 0]
    ]

    rect_colors = [[(128, 128, 128) for _ in range(9)] for _ in range(9)]
    solve_board(board_answer)
    while run and errors < 5:
        clock.tick(30)
        redraw_window(board, board_guess, rect_colors, errors)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos_x, pos_y = pos
                col = pos_x // RECT_SIZE
                row = pos_y // RECT_SIZE

                if rect_colors[row][col] == (255, 0, 0):
                    rect_colors[row][col] = (128, 128, 128)
                else:
                    rect_colors = [[(128, 128, 128) for _ in range(9)] for _ in range(9)]
                    rect_colors[row][col] = (255, 0, 0)

            if event.type == pygame.KEYDOWN:
                if board[row][col] == 0:
                    if event.key == pygame.K_1:
                        board_guess[row][col] = 1
                    elif event.key == pygame.K_2:
                        board_guess[row][col] = 2
                    elif event.key == pygame.K_3:
                        board_guess[row][col] = 3
                    elif event.key == pygame.K_4:
                        board_guess[row][col] = 4
                    elif event.key == pygame.K_5:
                        board_guess[row][col] = 5
                    elif event.key == pygame.K_6:
                        board_guess[row][col] = 6
                    elif event.key == pygame.K_7:
                        board_guess[row][col] = 7
                    elif event.key == pygame.K_8:
                        board_guess[row][col] = 8
                    elif event.key == pygame.K_9:
                        board_guess[row][col] = 9

                    if event.key == pygame.K_RETURN:
                        if board_guess[row][col] == board_answer[row][col]:
                            board[row][col] = board_answer[row][col]
                            board_guess[row][col] = 0
                        else:
                            board_guess[row][col] = 0
                            errors += 1

                if event.key == pygame.K_SPACE:
                    board_guess = [[0 for _ in range(9)] for _ in range(9)]
                    board = board_answer


main()
