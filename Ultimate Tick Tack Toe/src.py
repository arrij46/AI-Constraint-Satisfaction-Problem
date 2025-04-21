# Arrij Fawad
# I220755 CS C

import copy
import math
import random

from collections import deque
class Variable:
    def __init__(self, r, c, i, j):
        self.board_pos = (r, c)  
        self.cell_pos = (i, j) 
        self.domain = ['x', 'o', ' ']  

class UltimateBoard:
    def __init__(self):
        self.UBoard = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.UScoreBoard = [['-' for _ in range(3)] for _ in range(3)]
        self.Uwinner = None
        self.CurrPlayer = 'x'
        self.PrevPlayer = 'x'
        self.GameOver = False 
        self.Smoves = 0

    def SetCurrPlayingBoard(self, r, c):
        self.UScoreBoard[r][c] = 'p'

    def GetPlayingBoardPos(self):
        for i in range(3):
            for j in range(3): 
                if self.UScoreBoard[i][j] == 'p':
                    return (i, j)
        return (-1, -1)

    def SDisplay(self, r, c):
        print(f"Small Board ({r}, {c}):")
        for i in range(3):
            row = " | ".join(self.UBoard[r][c][i])
            print(row)
            if i < 2:
                print("-" * 9)
        print()

    def UDisplay(self):
        print("Ultimate Board:")
        for Urow in range(3):
            for Srow in range(3):
                row_str = ""
                for Ucol in range(3):
                    row_str += " | ".join(self.UBoard[Urow][Ucol][Srow]) + " || "
                print(row_str[:-4])
            if Urow < 2:
                print("=" * 29)
        print()

    def ScoreBoardDisplay(self):
        print("Score Board:")
        for i in range(3):
            print(" | ".join(self.UScoreBoard[i]))
            if i < 2:
                print("-" * 9)
        print()

    def ValidMove(self, r, c):
        x, y = self.GetPlayingBoardPos()
        if x == -1 and y == -1:
            return False
        if 0 <= r < 3 and 0 <= c < 3 and self.UBoard[x][y][r][c] == ' ':
            return True
        return False

    def CheckSBoardWin(self, r, c):
        for i in range(3):
            if self.UBoard[r][c][i][0] == self.UBoard[r][c][i][1] == self.UBoard[r][c][i][2] != ' ':
                self.UScoreBoard[r][c] = self.UBoard[r][c][i][0]
                return self.UBoard[r][c][i][0]
            if self.UBoard[r][c][0][i] == self.UBoard[r][c][1][i] == self.UBoard[r][c][2][i] != ' ':
                self.UScoreBoard[r][c] = self.UBoard[r][c][0][i]
                return self.UBoard[r][c][0][i]

        if self.UBoard[r][c][0][0] == self.UBoard[r][c][1][1] == self.UBoard[r][c][2][2] != ' ':
            self.UScoreBoard[r][c] = self.UBoard[r][c][0][0]
            return self.UBoard[r][c][0][0]
        if self.UBoard[r][c][0][2] == self.UBoard[r][c][1][1] == self.UBoard[r][c][2][0] != ' ':
            self.UScoreBoard[r][c] = self.UBoard[r][c][0][2]
            return self.UBoard[r][c][0][2]

        # Check for draw
        for i in range(3):
            for j in range(3):
                if self.UBoard[r][c][i][j] == ' ':
                    return 'p'
 
        self.UScoreBoard[r][c] = 'd'
        return 'd'

    def CheckUBoardWin(self):
        for i in range(3):
            if self.UScoreBoard[i][0] == self.UScoreBoard[i][1] == self.UScoreBoard[i][2] != '-':
                return self.UScoreBoard[i][0]
            if self.UScoreBoard[0][i] == self.UScoreBoard[1][i] == self.UScoreBoard[2][i] != '-':
                return self.UScoreBoard[0][i]

        if self.UScoreBoard[0][0] == self.UScoreBoard[1][1] == self.UScoreBoard[2][2] != '-':
            return self.UScoreBoard[0][0]
        if self.UScoreBoard[0][2] == self.UScoreBoard[1][1] == self.UScoreBoard[2][0] != '-':
            return self.UScoreBoard[0][2]
 
        for i in range(3):
            for j in range(3):
                if self.UScoreBoard[i][j] == '-':
                    return 'p'
        return 'd'

    def GetAvailableMoves(self, r, c):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.UBoard[r][c][i][j] == ' ':
                    moves.append((i, j))
        return moves
    def ForwardChecking(self, move):
        r, c, i, j = move
        target_r, target_c = i, j  
        for cell in self.get_empty_cells(target_r, target_c):
            if 'X' in cell.domain: 
                cell.domain.remove('X')
    def PlayerMove(self):
        r, c = self.GetPlayingBoardPos()
        print(f"Player is playing in small board ({r}, {c}).")
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                if self.ValidMove(row, col):
                    self.UBoard[r][c][row][col] = 'o'
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter numbers between 0 and 2.")
    def AIMove(self):
        r, c = self.GetPlayingBoardPos()

        if r == -1 and c == -1:
            best_score = -math.inf
            best_board = None
            for i in range(3):
                for j in range(3):
                    if self.UScoreBoard[i][j] == '-':
                        temp_board = copy.deepcopy(self)
                        temp_board.SetCurrPlayingBoard(i, j)
                        score = self.EvaluateBoard(temp_board, is_global=True)
                        if score > best_score:
                            best_score = score
                            best_board = (i, j)
            if best_board:
                r, c = best_board
                self.SetCurrPlayingBoard(r, c)
                print(f"AI selected small board ({r}, {c}).")

        print(f"AI is making a move in small board ({r}, {c})...")
        moves = self.GetAvailableMoves(r, c)
        if not moves:
            print("No valid moves available for AI!")
            return

        for move in moves:
            temp = copy.deepcopy(self)
            temp.UBoard[r][c][move[0]][move[1]] = 'x'
            if temp.CheckSBoardWin(r, c) == 'x':
                self.UBoard[r][c][move[0]][move[1]] = 'x'
                print(f"AI placed 'X' at ({move[0]}, {move[1]}) in small board ({r}, {c}) WIN")
                return

        for move in moves:
            temp = copy.deepcopy(self)
            temp.UBoard[r][c][move[0]][move[1]] = 'o'
            if temp.CheckSBoardWin(r, c) == 'o':
                self.UBoard[r][c][move[0]][move[1]] = 'x'
                print(f"AI placed 'X' at ({move[0]}, {move[1]}) in small board ({r}, {c}) BLOCK")
                return

        best_score = -math.inf
        best_move = None
        for move in moves:
            temp_board = copy.deepcopy(self)
            temp_board.UBoard[r][c][move[0]][move[1]] = 'x'
            score = self.Minimax(temp_board, depth=3, alpha=-math.inf, beta=math.inf, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            i, j = best_move
            self.UBoard[r][c][i][j] = 'x'
            print(f"AI placed 'X' at ({i}, {j}) in small board ({r}, {c}) MINIMAX")
        
    def AIMove1(self):
        r, c = self.GetPlayingBoardPos()
        if r == -1 and c == -1:
            best_score = -math.inf
            best_board = None

            for i in range(3):
                for j in range(3):
                    if self.UScoreBoard[i][j] == '-': 
                        temp_board = copy.deepcopy(self)
                        temp_board.SetCurrPlayingBoard(i, j)
                        score = self.EvaluateBoard(temp_board, is_global=True)
                        if score > best_score:
                            best_score = score
                            best_board = (i, j)

            if best_board:
                r, c = best_board
                self.SetCurrPlayingBoard(r, c)
                print(f"AI selected small board ({r}, {c}).")

        print(f"AI is making a move in small board ({r}, {c})")
        best_score = -math.inf
        best_move = None
        moves = self.GetAvailableMoves(r, c)

        if not moves:
            print("No valid moves available for AI!")
            return

        for move in moves:
            i, j = move
            temp_board = copy.deepcopy(self)
            temp_board.UBoard[r][c][i][j] = 'x'  
            score = self.Minimax(temp_board, depth=3, alpha=-math.inf, beta=math.inf, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move

        if best_move:
            i, j = best_move
            self.UBoard[r][c][i][j] = 'x'
            print(f"AI placed 'X' at ({i}, {j}) in small board ({r}, {c}).")
    def ValidMove(self, r, c):
        x, y = self.GetPlayingBoardPos()
        if x == -1 and y == -1:
            return False
        if 0 <= r < 3 and 0 <= c < 3 and self.UBoard[x][y][r][c] == ' ':
            return True
        return False

    def GetPlayingBoardPos(self):
        for i in range(3):
            for j in range(3):
                if self.UScoreBoard[i][j] == 'p':
                    return (i, j)
        return (-1, -1) 
    
    def get_empty_cells(self, r, c):
        cells = []
        for i in range(3):
            for j in range(3):
                if self.UBoard[r][c][i][j] == ' ':
                    cells.append(Variable(r, c, i, j))
        return cells

    def get_csp_valid_moves(self):
        r, c = self.GetPlayingBoardPos()
        moves = []
        for var in self.get_empty_cells(r, c):
            moves.append((var.board_pos[0], var.board_pos[1], var.cell_pos[0], var.cell_pos[1]))
        return moves

    def would_win_small_board(self, move):
        r, c, i, j = move
        temp = copy.deepcopy(self)
        temp.UBoard[r][c][i][j] = 'x'
        result = temp.CheckSBoardWin(r, c)
        return result == 'x'

    def would_block_opponent(self, move):
        r, c, i, j = move
        temp = copy.deepcopy(self)
        temp.UBoard[r][c][i][j] = 'x'
        for x in range(3):
            for y in range(3):
                if self.UBoard[r][c][x][y] == ' ' and (x, y) != (i, j):
                    temp2 = copy.deepcopy(temp)
                    temp2.UBoard[r][c][x][y] = 'o'
                    if temp2.CheckSBoardWin(r, c) == 'o':
                        return True
        return False

    def constraints(self):
        r, c = self.GetPlayingBoardPos()
        variables = self.get_empty_cells(r, c)
        pairs = []
        for v1 in variables:
            for v2 in variables:
                if v1 is not v2:
                    i1, j1 = v1.cell_pos
                    i2, j2 = v2.cell_pos
                    if i1 == i2 or j1 == j2 or (i1 == j1 and i2 == j2) or (i1 + j1 == 2 and i2 + j2 == 2):
                        pairs.append((v1, v2))
        return pairs

    def get_neighbors(self, var):
        r, c = var.board_pos
        i, j = var.cell_pos
        neighbors = []
        for v in self.get_empty_cells(r, c):
            if v is not var:
                x, y = v.cell_pos
                if x == i or y == j or (x == y and i == j) or (x + y == 2 and i + j == 2):
                    neighbors.append(v)
        return neighbors

    def empty_cells(self):
        r, c = self.GetPlayingBoardPos()
        return self.get_empty_cells(r, c)

    def count_constraints(self, variable, value):
        count = 0
        for neighbor in self.get_neighbors(variable):
            if value in neighbor.domain:
                count += 1
        return count


    def hybrid_ai_move(self):
        csp_moves = self.get_csp_valid_moves() 
        best_move = None
        best_score = -math.inf

        for move in csp_moves:
            temp_board = copy.deepcopy(self)
            temp_board.make_move(move, 'x')  
            score = self.Minimax(temp_board, depth=3, alpha=-math.inf, beta=math.inf, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move
    
    def evaluate_move(self, move):
        score = 0
        if self.would_win_small_board(move):
            score += 100 
        elif self.would_block_opponent(move):
            score += 50 
        return score
    
    def EvaluateBoard(self, board, is_global=False):
        score = 0

        if is_global:
            for i in range(3):
                for j in range(3):
                    if board.UScoreBoard[i][j] == 'x':
                        score += 50 
                    elif board.UScoreBoard[i][j] == 'o':
                        score -= 50 

        r, c = board.GetPlayingBoardPos()
        for i in range(3):
            for j in range(3):
                if board.UBoard[r][c][i][j] == 'x':
                    if (i, j) == (1, 1):
                        score += 3
                    elif (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                        score += 2
                    else:
                        score += 1
                elif board.UBoard[r][c][i][j] == 'o':
                    if (i, j) == (1, 1):
                        score -= 3
                    elif (i, j) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                        score -= 2
                    else:
                        score -= 1

        return score

    def Minimax(self, board, depth, alpha, beta, is_maximizing):
        
        ultimate_result = board.CheckUBoardWin()
        if ultimate_result == 'x':
            return 100   
        elif ultimate_result == 'o':
            return -100 
        elif ultimate_result == 'd' or depth == 0:
            return self.EvaluateBoard(board)  

        r, c = board.GetPlayingBoardPos()
        moves = board.GetAvailableMoves(r, c)

        if is_maximizing:
            max_eval = -math.inf
            for move in moves:
                i, j = move
                temp_board = copy.deepcopy(board)
                temp_board.UBoard[r][c][i][j] = 'x'  
                eval = self.Minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  
            return max_eval
        else:
            min_eval = math.inf
            for move in moves:
                i, j = move
                temp_board = copy.deepcopy(board)
                temp_board.UBoard[r][c][i][j] = 'o'  
                eval = self.Minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  
            return min_eval

    def ac3(self):
        queue = deque([(v1, v2) for v1, v2 in self.constraints])
        while queue:
            (v1, v2) = queue.popleft()
            if self.revise(v1, v2):
                if not v1.domain:
                    return False
                for v3 in self.get_neighbors(v1):
                    queue.append((v3, v1))
        return True

    def revise(self, v1, v2):
        revised = False
        for x in v1.domain:
            if not any(self.satisfies_constraints(x, y) for y in v2.domain):
                v1.domain.remove(x)
                revised = True
        return revised
    def select_variable_mrv(self):
        return min(self.empty_cells, key=lambda v: len(v.domain))

    def order_values_lcv(self, variable):
        return sorted(variable.domain, key=lambda value: self.count_constraints(variable, value))

# Main
def main():
    b = UltimateBoard()
    b.ScoreBoardDisplay()

    print("You are 'O'\nAI Agent is 'X'\nBest of Luck!")
    b.GameOver = False

    while not b.GameOver:
        if b.CurrPlayer == 'o':
            b.ScoreBoardDisplay()
            r, c = b.GetPlayingBoardPos()
            if r == -1 and c == -1:
                print("Player, choose a small board.")
                while True:
                    try:
                        r = int(input("Enter row of the small board (0-2): "))
                        c = int(input("Enter column of the small board (0-2): "))
                        if 0 <= r < 3 and 0 <= c < 3 and b.UScoreBoard[r][c] == '-':
                            b.SetCurrPlayingBoard(r, c)
                            break
                        else:
                            print("Invalid board selection. Try again.")
                    except ValueError:
                        print("Invalid input. Enter numbers between 0 and 2.")
            b.SDisplay(r, c)
            b.PlayerMove()
            b.CurrPlayer = 'x'

        elif b.CurrPlayer == 'x':
            r, c = b.GetPlayingBoardPos()
            if r == -1 and c == -1:
                print("AI is choosing a small board...")
                available_boards = [(i, j) for i in range(3) for j in range(3) if b.UScoreBoard[i][j] == '-']
                if available_boards:
                    r, c = random.choice(available_boards)
                    b.SetCurrPlayingBoard(r, c)
                    print(f"AI selected small board ({r}, {c}).")
            b.SDisplay(r, c)
            b.AIMove()
            b.CurrPlayer = 'o'

        r, c = b.GetPlayingBoardPos()
        small_board_result = b.CheckSBoardWin(r, c)
        if small_board_result in ['x', 'o', 'd']:
            print(f"Small board ({r}, {c}) result: {small_board_result.upper()}")

        ultimate_result = b.CheckUBoardWin()
        if ultimate_result in ['x', 'o', 'd']:
            if ultimate_result == 'x':
                print("AI wins the Ultimate Board!")
            elif ultimate_result == 'o':
                print("Player wins the Ultimate Board!")
            else:
                print("The Ultimate Board is a draw!")
            b.GameOver = True

'''
if __name__ == "__main__":
    main()
'''

import pygame

CELL_SIZE = 50
BOARD_MARGIN = 20
SMALL_BOARD_GAP = 10
SMALL_BOARD_SIZE = 3 * CELL_SIZE + 2 * SMALL_BOARD_GAP
BIG_BOARD_SIZE = 3 * SMALL_BOARD_SIZE + 2 * SMALL_BOARD_GAP
WINDOW_SIZE = BIG_BOARD_SIZE + 2 * BOARD_MARGIN

PURPLE = (80, 0, 120)
BLACK = (20, 20, 20)
PINK = (255, 80, 180)
BLUE = (80, 180, 255)
WHITE = (240, 240, 240)
AI_WIN = (255, 200, 230)
PLAYER_WIN = (180, 220, 255)
DRAW = (180, 180, 180)

def draw_board(screen, board: UltimateBoard, font):
    screen.fill(PURPLE)
    for br in range(3):
        for bc in range(3):
            x0 = BOARD_MARGIN + bc * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
            y0 = BOARD_MARGIN + br * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
            winner = board.UScoreBoard[br][bc]
            if winner == 'x':
                pygame.draw.rect(screen, AI_WIN, (x0-2, y0-2, SMALL_BOARD_SIZE+4, SMALL_BOARD_SIZE+4), border_radius=8)
            elif winner == 'o':
                pygame.draw.rect(screen, PLAYER_WIN, (x0-2, y0-2, SMALL_BOARD_SIZE+4, SMALL_BOARD_SIZE+4), border_radius=8)
            elif winner == 'd':
                pygame.draw.rect(screen, DRAW, (x0-2, y0-2, SMALL_BOARD_SIZE+4, SMALL_BOARD_SIZE+4), border_radius=8)
            else:
                pygame.draw.rect(screen, BLACK, (x0-2, y0-2, SMALL_BOARD_SIZE+4, SMALL_BOARD_SIZE+4), border_radius=8)
            for i in range(3):
                pygame.draw.line(screen, WHITE, (x0, y0 + i*CELL_SIZE), (x0 + SMALL_BOARD_SIZE, y0 + i*CELL_SIZE), 2)
                pygame.draw.line(screen, WHITE, (x0 + i*CELL_SIZE, y0), (x0 + i*CELL_SIZE, y0 + SMALL_BOARD_SIZE), 2)
            for sr in range(3):
                for sc in range(3):
                    val = board.UBoard[br][bc][sr][sc]
                    cx = x0 + sc*CELL_SIZE + CELL_SIZE//2
                    cy = y0 + sr*CELL_SIZE + CELL_SIZE//2
                    if val == 'x':
                        pygame.draw.circle(screen, PINK, (cx, cy), CELL_SIZE//2 - 6, 0)
                    elif val == 'o':
                        pygame.draw.circle(screen, BLUE, (cx, cy), CELL_SIZE//2 - 6, 0)
    pr, pc = board.GetPlayingBoardPos()
    if pr != -1 and pc != -1:
        x0 = BOARD_MARGIN + pc * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
        y0 = BOARD_MARGIN + pr * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
        pygame.draw.rect(screen, WHITE, (x0-4, y0-4, SMALL_BOARD_SIZE+8, SMALL_BOARD_SIZE+8), 4, border_radius=10)
    winner = board.CheckUBoardWin()
    if winner in ['x', 'o', 'd']:
        msg = "AI Wins!" if winner == 'x' else ("Player Wins!" if winner == 'o' else "Draw!")
        text = font.render(msg, True, WHITE)
        screen.blit(text, (WINDOW_SIZE//2 - text.get_width()//2, 10))

def run_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Ultimate Tic Tac Toe")
    font = pygame.font.SysFont("Arial", 32)
    board = UltimateBoard()
    running = True
    player_turn = True
    clock = pygame.time.Clock()

    while running:
        draw_board(screen, board, font)
        pygame.display.flip()
        clock.tick(30)
        winner = board.CheckUBoardWin()
        if winner in ['x', 'o', 'd']:
            pygame.time.wait(2000)
            running = False
            continue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif player_turn and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for br in range(3):
                    for bc in range(3):
                        x0 = BOARD_MARGIN + bc * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
                        y0 = BOARD_MARGIN + br * (SMALL_BOARD_SIZE + SMALL_BOARD_GAP)
                        if x0 <= mx < x0 + SMALL_BOARD_SIZE and y0 <= my < y0 + SMALL_BOARD_SIZE:
                            pr, pc = board.GetPlayingBoardPos()
                            if pr == -1 or pc == -1:
                                if board.UScoreBoard[br][bc] == '-':
                                    board.SetCurrPlayingBoard(br, bc)
                                    pr, pc = br, bc
                                else:
                                    continue
                            if pr == br and pc == bc and board.UScoreBoard[pr][pc] == 'p':
                                for sr in range(3):
                                    for sc in range(3):
                                        cx = x0 + sc*CELL_SIZE
                                        cy = y0 + sr*CELL_SIZE
                                        if cx <= mx < cx+CELL_SIZE and cy <= my < cy+CELL_SIZE:
                                            if board.UBoard[pr][pc][sr][sc] == ' ':
                                                board.UBoard[pr][pc][sr][sc] = 'o'
                                                player_turn = False
        if not player_turn:
            pygame.time.wait(400)
            board.CurrPlayer = 'x'
            board.AIMove()
            board.CurrPlayer = 'o'
            player_turn = True
            
            pr, pc = board.GetPlayingBoardPos()
            board.CheckSBoardWin(pr, pc)
    pygame.quit()


if __name__ == "__main__":
    run_pygame()