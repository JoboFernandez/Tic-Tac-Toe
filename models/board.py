from models import Player, ScoreBoard
from random import randint, choice
import pygame
import settings


class Board:

    def __init__(self, left: int, top: int, width: int, color=(0, 0, 0), line_width=5):
        self.left = left
        self.top = top
        self.width = width
        self.div = width // 3
        self.color = color
        self.line_width = line_width

        self.enabled = True
        self.marks = [['' for _ in range(3)] for _ in range(3)]
        self.players = []
        self.on_play = None

    def initialize_players(self, p1: str, p2: str):
        # set-up player mark and color randomization
        p1_mark = choice(["X", "O"])
        p2_mark = "O" if p1_mark == "X" else "X"
        p1_color = choice([(255, 0, 0), (0, 0, 255)])
        p2_color = (0, 0, 255) if p1_color == (255, 0, 0) else (255, 0, 0)

        # initializing attributes
        self.players = []
        self.players = [
            Player(type=p1, mark=p1_mark, color=p1_color),
            Player(type=p2, mark=p2_mark, color=p2_color),
        ]
        self.on_play = choice(self.players)

    def start(self, p1: str, p2: str, score_board: ScoreBoard):
        self.initialize_players(p1=p1, p2=p2)
        score_board.update_player_colors(players=self.players)
        score_board.update_score(players=self.players)
        self.reset(score_board=score_board)
        pygame.mouse.set_pos(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)

    def reset(self, score_board: ScoreBoard):
        # reset board conditions
        self.enabled = True
        self.marks = [['' for _ in range(3)] for _ in range(3)]
        score_board.message_log = f"Player {self.on_play.mark} GOES FIRST"

        # set first move if on_play is an AI
        if self.on_play.type in ['AI-EASY', 'AI-HARD']:
            ai_x, ai_y = (randint(0, 2), randint(0, 2))
            x = self.left + ai_x * self.div + self.div // 2
            y = self.top + ai_y * self.div + self.div // 2
            self.set_mark(pos=(x, y), mark=self.on_play.mark, score_board=score_board)

    def set_mark(self, pos: tuple, mark: str, score_board: ScoreBoard):
        # check if board is enabled and entry is inside the board
        if self.enabled and (self.left < pos[0] < self.left + self.width) and (self.top < pos[1] < self.top + self.width):
            c = (pos[0] - self.left) // self.div
            r = (pos[1] - self.top) // self.div

            # set mark if board cell is empty
            if self.marks[r][c] == '':
                self.marks[r][c] = mark
                winner = self.get_winner(self.marks)

                # no winner yet, continue game
                if winner == '':
                    self.change_on_play()
                    score_board.message_log = f"Player {self.on_play.mark}'s TURN"

                # game is draw
                elif winner == 'DRAW':
                    score_board.message_log = "DRAW GAME"
                    self.enabled = False

                # there is a winner
                else:
                    self.on_play.score += 1
                    score_board.update_score(players=self.players)
                    score_board.message_log = f"Player {self.on_play.mark} WINS!"
                    self.enabled = False

    def get_winner(self, board: list) -> str:
        # check for diagonal matches
        same_diagonal1 = (board[0][0] == board[1][1] and board[1][1] == board[2][2])
        same_diagonal2 = (board[2][0] == board[1][1] and board[1][1] == board[0][2])
        if board[1][1] != '' and (same_diagonal1 or same_diagonal2):
            return board[1][1]

        # check for horizontal and vertical matches
        else:
            for i in range(3):
                if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != '':
                    return board[i][0]
                if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != '':
                    return board[0][i]

        # check for draw
        for r in range(3):
            for c in range(3):
                if self.marks[r][c] == '':
                    return ''
        return 'DRAW'

    def change_on_play(self):
        self.on_play = self.players[0] if self.on_play == self.players[1] else self.players[1]

    def set_ai_move(self, score_board: ScoreBoard):
        if self.enabled:
            # apply randomization if AI is easy level
            if self.on_play.type == 'AI-EASY':
                self.random_ai(score_board=score_board)

            # apply minimax algorithm if AI is difficult level
            elif self.on_play.type == 'AI-HARD':
                board_copy = [row for row in self.marks]
                self.minimax_ai(board=board_copy, on_play=self.on_play.mark, score_board=score_board)

    def random_ai(self, score_board: ScoreBoard):
        while True:
            ai_x, ai_y = (randint(0, 2), randint(0, 2))
            if self.marks[ai_y][ai_x] == '':
                x = self.left + ai_x * self.div + self.div // 2
                y = self.top + ai_y * self.div + self.div // 2
                self.set_mark((x, y), self.on_play.mark, score_board=score_board)
                return

    def minimax_ai(self, board: list, on_play: str, score_board: ScoreBoard, depth=0):
        # locate empty cells
        blanks = [(c, r) for c in range(3) for r in range(3) if board[r][c] == '']

        # base case: all cells are filled, draw game
        if not blanks:
            return 0

        # collecting scores for all tree branches in a certain depth
        depth_scores = []
        next_player = 'X' if on_play == 'O' else 'O'
        brd_copy = [row for row in board]
        for blank in blanks:
            blank_col, blank_row = blank
            brd_copy[blank_row][blank_col] = on_play
            winner = self.get_winner(board=brd_copy)
            if winner == 'DRAW':
                depth_scores.append(0)
            elif winner != '':
                depth_scores.append(1 if depth % 2 == 0 else -1)
            else:
                depth_scores.append(self.minimax_ai(board=brd_copy, on_play=next_player, score_board=score_board, depth=depth+1))
            brd_copy[blank_row][blank_col] = ''

        # evaluating the final depth score, minimizing AI results while maximizing player results
        the_score = max(depth_scores) if depth % 2 == 0 else min(depth_scores)

        # return / apply result
        if depth == 0:
            x = self.left + blanks[depth_scores.index(the_score)][0] * self.div + self.div // 2
            y = self.top + blanks[depth_scores.index(the_score)][1] * self.div + self.div // 2
            self.set_mark((x, y), self.on_play.mark, score_board=score_board)
        else:
            return the_score

    def draw(self, screen: pygame.display.set_mode):
        # drawing the board
        cover = pygame.Surface((self.width, self.width))
        cover.fill((255, 255, 255))
        cover.set_alpha(64)
        screen.blit(cover, (self.left, self.top))
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left + self.div, self.top), (self.left + self.div, self.top + self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left + 2*self.div, self.top), (self.left + 2*self.div, self.top + self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left, self.top + self.div), (self.left + self.width, self.top + self.div), self.line_width)
        pygame.draw.line(screen, self.color, (self.left, self.top + 2*self.div), (self.left + self.width, self.top + 2*self.div), self.line_width)

        # drawing the entry markings
        player1 = self.players[0]
        player2 = self.players[1]
        for r in range(3):
            for c in range(3):
                marking = self.marks[r][c]
                color = player1.color if marking == player1.mark else player2.color if marking == player2.mark else (0, 0, 0)
                screen.blit(pygame.font.Font("freesansbold.ttf", 100).render(marking, True, color), (self.left + c * self.div + 13, self.top + r * self.div + 8))

    def draw_cursor(self, screen: pygame.display.set_mode, pos: tuple):
        mark = self.on_play.mark
        color = self.on_play.color
        screen.blit(pygame.font.Font("freesansbold.ttf", 24).render(mark, True, color), (pos[0] - 10, pos[1] - 10))