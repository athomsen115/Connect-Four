#Graphical Version of Connect Four

import numpy as np
import pygame
import math
import sys
import random

ROW_COUNT = 6
COLUMN_COUNT=7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
EMPTY = 0

pygame.init()
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)
screen = pygame.display.set_mode(size)


def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))
    
def winning_move(board, piece):
    #Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True;
            
    #Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True;     
            
    #Check positively sloped diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True;
    
    #Check negatively sloped diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True;
       
def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
        
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4
    return score

def score_position(board, piece):
    score = 0
    #Score center
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 6
    
    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)  
                
    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)
    
    #Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+1][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    #Score negatively sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)
    
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_columns(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_columns(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, AI_PIECE)
            new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else: # minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, PLAYER_PIECE)
            new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
        

def get_valid_columns(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):   
    valid_locations = get_valid_columns(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col           


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range (ROW_COUNT):        
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)  
    pygame.display.update()

def main():
    global turn, board
    board = create_board()
    game_over = False
    print_board(board)
    
    draw_board(board)
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 70)
    turn = random.randint(PLAYER, AI)
    
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                #else:
                    #pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                #Ask for player 1 input
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
            
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                
                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Player 1 Wins!!!", 1, RED)
                            screen.blit(label, (30, 10))
                            game_over = True
                            turn = 1
                        
                        print_board(board)
                        draw_board(board)
            
                        turn += 1
                        turn = turn % 2
            
        
        #Ask for player 2 input
        if turn == AI and not game_over:
            #aiCol = random.randint(0, COLUMN_COUNT - 1)
            #aiCol = pick_best_move(board, AI_PIECE)
            #aiCol, minimax_score = minimax(board, 4, True)
            aiCol, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
            
            if is_valid_location(board, aiCol):
                pygame.time.wait(500)
                row = get_next_open_row(board, aiCol)
                drop_piece(board, row, aiCol, AI_PIECE)
        
                if winning_move(board, AI_PIECE):
                    label = myfont.render("Player 2 Wins!!!", 1, YELLOW)
                    screen.blit(label, (30, 10))
                    game_over = True
                
        
                print_board(board)
                draw_board(board)
    
                turn += 1
                turn = turn % 2
                
        if game_over:
            pygame.time.wait(3000)
            
            
def AIMainMenu():
    global aiCol
    run = True
    click = False
    radius = 75
    while run:
        screen.fill(BLACK)
        title = pygame.image.load("title.png")
        screen.blit(title, (0,0))
        
        buttonFont = pygame.font.SysFont('comicsans', 30)
        posx, posy = pygame.mouse.get_pos()
        
        button1 = pygame.draw.circle(screen, YELLOW, (200, 400), radius)
        easy = buttonFont.render("Easy", 1, RED)
        screen.blit(easy, (200 - easy.get_width()/2, 400 - easy.get_height()/2))
        button2 = pygame.draw.circle(screen, RED, (500, 400), radius)
        medium = buttonFont.render("Medium", 1, YELLOW)
        screen.blit(medium, (500 - medium.get_width()/2, 400 - medium.get_height()/2))
        button3 = pygame.draw.circle(screen, RED, (200, 600), radius)
        hard = buttonFont.render("Hard", 1, YELLOW)
        screen.blit(hard, (200 - hard.get_width()/2, 600 - hard.get_height()/2))
        button4 = pygame.draw.circle(screen, YELLOW, (500, 600), radius)
        impossible = buttonFont.render("Impossible", 1, RED)
        screen.blit(impossible, (500 - impossible.get_width()/2, 600 - impossible.get_height()/2))
        pygame.display.update()
        
        #aiCol = random.randint(0, COLUMN_COUNT - 1)
        #aiCol = pick_best_move(board, AI_PIECE)
        #aiCol, minimax_score = minimax(board, 4, True)
        #aicol, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
        
        if button1.collidepoint(posx, posy):
            if click:
                screen.fill(BLACK)
                aiCol = random.randint(0, COLUMN_COUNT - 1)
                main()
                click = False
        if button2.collidepoint(posx, posy):
            if click:
                screen.fill(BLACK)
                aiCol = pick_best_move(board, AI_PIECE)
                main()
                click = False
        if button3.collidepoint(posx, posy):
            if click:
                screen.fill(BLACK)
                aiCol, minimax_score = minimax(board, 4, True)
                main()
                click = False
        if button4.collidepoint(posx, posy):
            if click:
                screen.fill(BLACK)
                aicol, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
                main()
                click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update
            
if __name__ == '__main__':
    mainMenu()
            