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
        for i in range(3):
            for j in range(3):
                if self.UScoreBoard[i][j] == 'p':
                    self.UScoreBoard[i][j] = '-'
        if 0 <= r < 3 and 0 <= c < 3 and self.UScoreBoard[r][c] == '-':
            self.UScoreBoard[r][c] = 'p'
        else:
            for i in range(3):
                for j in range(3):
                    if self.UScoreBoard[i][j] == '-':
                        self.UScoreBoard[i][j] = 'p'
                        return

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

    def PlayerMove(self):
        r, c = self.GetPlayingBoardPos()
        print(f"Player is playing in small board ({r}, {c}).")
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                if self.ValidMove(row, col):
                    self.UBoard[r][c][row][col] = 'o'
                    next_r, next_c = row, col
                    if self.UScoreBoard[next_r][next_c] == '-':
                        self.SetCurrPlayingBoard(next_r, next_c)
                    else:
                        self.SetCurrPlayingBoard(-1, -1)
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter numbers between 0 and 2.")

    def AIMove(self):
        r, c = self.GetPlayingBoardPos()
        print(f"AI is making a move in small board ({r}, {c}).")
        moves = self.GetAvailableMoves(r, c)
        if not moves:
            print("No valid moves available for AI!")
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
            next_r, next_c = i, j
            if self.UScoreBoard[next_r][next_c] == '-':
                self.SetCurrPlayingBoard(next_r, next_c)
            else:
                self.SetCurrPlayingBoard(-1, -1)
            print(f"AI placed 'X' at ({i}, {j}) in small board ({r}, {c}).")

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