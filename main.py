import pygame
from math import sin, pi, hypot
import os, sys
from random import randint, choice

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen_width = 450
screen_height = 500

# region CLASSES

class Background():
    def __init__(self):
        self.hexlength = 10
        self.color_topleft = (randint(0,255), randint(0,255), randint(0,255))
        self.color_topright = (randint(0,255), randint(0,255), randint(0,255))
        self.color_bottomleft = (randint(0,255), randint(0,255), randint(0,255))
        self.color_bottomright = (randint(0,255), randint(0,255), randint(0,255))

    def draw(self):
        screen.fill((60,60,60))
        indent = False
        for y in range(0, screen_height, round(self.hexlength * sin(pi/3))):
            if indent: x_start = round(3 * self.hexlength / 2); indent = False
            else: x_start = 0; indent = True
            for x in range(x_start, screen_width, round(3 * self.hexlength)):
                p1 = (round(x), round(y))
                p2 = (round(x + self.hexlength / 2), round(y - self.hexlength * sin(pi/3)))
                p3 = (round(x + 3 * self.hexlength / 2), round(y - self.hexlength * sin(pi/3)))
                p4 = (round(x + 2 * self.hexlength), round(y))
                p5 = (round(x + 3 * self.hexlength / 2), round(y + self.hexlength * sin(pi/3)))
                p6 = (round(x + self.hexlength / 2), round(y + self.hexlength * sin(pi/3)))
                pygame.draw.polygon(screen, self.weighted_color(x,y), (p1, p2, p3, p4, p5, p6), 1)
        pygame.draw.rect(screen, (60,60,60), (0, 0, screen_width, 90))
        pygame.draw.line(screen, self.color_topleft, (0, 90), (screen_width, 90), 2)
        if gamestate.scene == 'game':
            pygame.draw.line(screen, self.color_topleft, (75, 0), (75, 90), 2)
            pygame.draw.line(screen, self.color_topleft, (0, 30), (75, 30), 2)
            pygame.draw.line(screen, self.color_topleft, (375, 0), (375, 90), 2)
            pygame.draw.line(screen, self.color_topleft, (375, 30), (450, 30), 2)
            screen.blit(pygame.font.Font("freesansbold.ttf", 26).render("X", True, board.xcolor), (27,4))
            screen.blit(pygame.font.Font("freesansbold.ttf", 26).render("O", True, board.ocolor), (402,4))
            screen.blit(pygame.font.Font("freesansbold.ttf", 40).render(f"{board.score['X']:02d}", True, board.xcolor), (12, 43))
            screen.blit(pygame.font.Font("freesansbold.ttf", 40).render(f"{board.score['O']:02d}", True, board.ocolor), (390,43))
            screen.blit(pygame.font.Font("freesansbold.ttf", 16).render(msglog.message, True, (255, 255, 255)), (100, 33))

    def weighted_color(self, x, y):
        d1 = hypot(x, y)
        d2 = hypot(screen_width - x, y)
        d3 = hypot(x, screen_height - y)
        d4 = hypot(screen_width - x, screen_height - y)
        if d1 == 0: return self.color_topleft
        elif d2 == 0: return self.color_topright
        elif d3 == 0: return self.color_bottomleft
        elif d4 == 0: return self.color_bottomright
        weight = 1/d1 + 1/d2 + 1/d3 + 1/d4
        r = (self.color_topleft[0]/d1 + self.color_topright[0]/d2 + self.color_bottomleft[0]/d3 + self.color_bottomright[0]/d4) / weight
        g = (self.color_topleft[1] / d1 + self.color_topright[1] / d2 + self.color_bottomleft[1] / d3 +
             self.color_bottomright[1] / d4) / weight
        b = (self.color_topleft[2] / d1 + self.color_topright[2] / d2 + self.color_bottomleft[2] / d3 +
             self.color_bottomright[2] / d4) / weight
        return (r,g,b)

    def change_colors(self):
        self.color_topleft = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_topright = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottomleft = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottomright = (randint(0, 255), randint(0, 255), randint(0, 255))

class Board():
    def __init__(self, left, top, width):
        self.left = left
        self.top = top
        self.width = width
        self.div = width // 3
        self.color = (0, 0, 0)
        self.line_width = 5
        self.marks = [['' for _ in range(3)] for _ in range(3)]
        self.font = pygame.font.Font("freesansbold.ttf", self.width // 3)
        self.cursor = (0, 0)
        self.p1 = 'PLAYER 1'
        self.p2 = 'PLAYER 2'
        self.onplay = self.p1
        self.pmark = {self.p1: 'X', self.p2: 'O'}
        self.enabled = True
        self.score = {'X': 0, 'O': 0}
        self.xcolor = (255, 0, 0)
        self.ocolor = (0, 0, 255)

    def draw(self):
        cover = pygame.Surface((self.width, self.width))
        cover.fill((255, 255, 255))
        cover.set_alpha(64)
        screen.blit(cover, (self.left, self.top))
        pygame.draw.rect(screen, self.color, (self.left, self.top, self.width, self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left + self.div, self.top), (self.left + self.div, self.top + self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left + 2*self.div, self.top), (self.left + 2*self.div, self.top + self.width), self.line_width)
        pygame.draw.line(screen, self.color, (self.left, self.top + self.div), (self.left + self.width, self.top + self.div), self.line_width)
        pygame.draw.line(screen, self.color, (self.left, self.top + 2*self.div), (self.left + self.width, self.top + 2*self.div), self.line_width)
        for r in range(3):
            for c in range(3):
                color = (255,0,0) if self.marks[r][c] == 'X' else (0,0,255) if self.marks[r][c] == 'O' else (0,0,0)
                screen.blit(self.font.render(self.marks[r][c], True, color), (self.left + c * self.div + 13, self.top + r * self.div + 8))

    def get_mark(self, pos, mark):
        if self.left < pos[0] < self.left + self.width and self.top < pos[1] < self.top + self.width and self.enabled:
            c = (pos[0] - self.left) // self.div
            r = (pos[1] - self.top) // self.div
            if self.marks[r][c] == '':
                self.marks[r][c] = mark
                winner = self.check_winner(self.marks)
                if winner != '':
                    if winner == 'DRAW':
                        msglog.update("DRAW GAME")
                    else:
                        msglog.update(f"{self.onplay} ({winner}) WINS!")
                        self.score[winner] = self.score[winner] + 1
                    self.enabled = False
                else:
                    next1 = self.p1 if self.onplay == self.p2 else self.p2
                    next2 = 'X' if self.pmark[self.onplay] == 'O' else 'O'
                    msglog.update(f"{next1}'s {next2} TURN")
                self.change_player()

    def check_winner(self, brd):
        if (brd[0][0] == brd[1][1] and brd[1][1] == brd[2][2]) or \
                (brd[2][0] == brd[1][1] and brd[1][1] == brd[0][2]) and brd[1][1] != '':
            return brd[1][1]
        else:
            for i in range(3):
                if brd[i][0] == brd[i][1] and brd[i][1] == brd[i][2] and brd[i][0] != '':
                    return brd[i][0]
                if brd[0][i] == brd[1][i] and brd[1][i] == brd[2][i] and brd[0][i] != '':
                    return brd[0][i]
        if self.isFilled():
            return 'DRAW'
        return ''

    def isFilled(self):
        for r in range(3):
            for c in range(3):
                if self.marks[r][c] == '':
                    return False
        return True

    def reset(self):
        self.enabled = True
        self.marks = [['' for _ in range(3)] for _ in range(3)]
        msglog.update(f"{self.onplay} ({self.pmark[self.onplay]}) GOES FIRST")
        if self.onplay == 'AI-EASY' or self.onplay == 'AI-HARD':
            ai_selection = (randint(0,2), randint(0,2))
            x = self.left + ai_selection[0] * self.div + self.div // 2
            y = self.top + ai_selection[1] * self.div + self.div // 2
            self.get_mark((x, y), self.pmark[self.onplay])

    def start(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.onplay = choice([p1, p2])
        self.pmark[self.onplay] = choice(['X', 'O'])
        self.pmark[p1 if self.onplay == p2 else p2] = 'X' if self.pmark[self.onplay] == 'O' else 'O'
        self.reset()
        self.score['X'] = 0
        self.score['O'] = 0
        pygame.mouse.set_pos(screen_width // 2, screen_height // 2)

    def draw_cursor(self, pos):
        color = (255,0,0) if self.pmark[self.onplay] == 'X' else (0,0,255)
        screen.blit(pygame.font.Font("freesansbold.ttf", 24).render(self.pmark[self.onplay], True, color), (pos[0] - 10, pos[1] - 10))

    def change_player(self):
        self.onplay = self.p1 if self.onplay == self.p2 else self.p2

    def update(self):
        if self.enabled:
            if self.onplay == 'AI-EASY':
                while True:
                    ai_selection = (randint(0,2), randint(0,2))
                    if self.marks[ai_selection[1]][ai_selection[0]] == '':
                        x = self.left + ai_selection[0] * self.div + self.div // 2
                        y = self.top + ai_selection[1] * self.div + self.div // 2
                        self.get_mark((x,y), self.pmark[self.onplay])
                        break
            elif self.onplay == 'AI-HARD':
                board_copy = [row[:] for row in self.marks]
                self.tictactoe_counter(board_copy, self.pmark[self.onplay])

    def tictactoe_counter(self, brd, plyr, depth = 0):
        blanks = []
        for r in range(3):
            for c in range(3):
                if brd[r][c] == '':
                    blanks.append((c,r))

        if blanks:
            depth_score = []
            for blank in blanks:
                next = 'X' if plyr == 'O' else 'O'
                brd_copy = [row[:] for row in brd]
                brd_copy[blank[1]][blank[0]] = plyr
                winner = self.check_winner(brd_copy)
                if winner == 'DRAW': depth_score.append(0)
                elif winner != '': depth_score.append(1 if depth % 2 == 0 else -1)
                else: depth_score.append(self.tictactoe_counter(brd_copy, next, depth + 1))
            if depth % 2 == 0: the_score = max(depth_score)
            else: the_score = min(depth_score)
            if depth == 0:
                x = self.left + blanks[depth_score.index(the_score)][0] * self.div + self.div // 2
                y = self.top + blanks[depth_score.index(the_score)][1] * self.div + self.div // 2
                self.get_mark((x,y), plyr)
            else:
                return the_score
        else: return 0

class Button():
    def __init__(self, name, left, top, width, height):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = Text("txt" + self.name, self.left, self.top, self.height // 2)
        self.bordercolor = (150, 150, 150)
        self.borderwidth = 3
        self.bgcolor = (100, 100, 240)
        self.bgshadow = (30, 30, 170)

    def draw(self):
        pygame.draw.rect(screen, self.bgcolor, (self.left, self.top, self.width, self.height))
        pygame.draw.rect(screen, self.bgshadow, (self.left, (self.top + self.height//2), self.width, self.height // 2))
        pygame.draw.rect(screen, self.bordercolor, (self.left, self.top, self.width, self.height), self.borderwidth)
        self.text.draw()

    def set_text_location(self, left, top):
        self.text.left = self.left + left
        self.text.top = self.top + top

    def glow(self):
        self.bordercolor = (255, 255, 255)
        self.bordercolor = (30, 100, 30)
        self.bgcolor = (100, 240, 100)
        self.bgshadow = (30, 170, 30)
        self.text.color = (155, 15, 155)
        self.text.color = (50, 50, 50)

    def unglow(self):
        self.bordercolor = (150, 150, 150)
        self.bgcolor = (100, 100, 240)
        self.bgshadow = (30, 30, 170)
        self.text.color = (255, 255, 255)

    def isover(self, pos):
        return True if (self.left < pos[0] < self.left + self.width and self.top < pos[1] < self.top + self.height) else False

class MessageLog():
    def __init__(self):
        self.message = ''

    def update(self, msg):
        self.message = msg

class Text():
    def __init__(self, name, left, top, size):
        self.name = name
        self.left = left
        self.top = top
        self.size = size
        self.label = ''
        self.font = pygame.font.Font("freesansbold.ttf", self.size)
        self.color = (0,0,0)

    def draw(self):
        screen.blit(self.font.render(self.label, True, self.color), (self.left, self.top))

    def change_size(self, size):
        self.size = size
        self.font = pygame.font.Font("freesansbold.ttf", self.size)

class GameState():
    def __init__(self):
        self.scene = 'main_menu'

    def main_menu(self):
        pos = pygame.mouse.get_pos()
        # region EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for i in range(len(btns_menu)):
                    if btns_menu[i].isover(pos): btns_menu[i].glow()
                    else: btns_menu[i].unglow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_option1.isover(pos): board.start('PLAYER 1', 'PLAYER 2'); bg.change_colors(); self.scene = 'game'
                elif btn_option2.isover(pos): board.start('PLAYER 1', 'AI-EASY'); bg.change_colors(); self.scene = 'game'
                elif btn_option3.isover(pos): board.start('PLAYER 1', 'AI-HARD'); bg.change_colors(); self.scene = 'game'
                elif btn_option4.isover(pos): pygame.quit(); sys.exit()
        # endregion

        # region DRAWING
        bg.draw()

        for i in range(len(btns_menu)):
            btns_menu[i].draw()
        for i in range(len(txts_menu)):
            txts_menu[i].draw()
        pygame.display.update()
        # endregion

    def game(self):
        pos = pygame.mouse.get_pos()
        # region EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for i in range(len(btns_game)):
                    if btns_game[i].isover(pos): btns_game[i].glow()
                    else: btns_game[i].unglow()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_game_option1.isover(pos): bg.change_colors(); self.scene = 'main_menu'
                elif btn_game_option2.isover(pos): bg.change_colors(); board.reset()
                elif btn_game_option3.isover(pos): pygame.quit(); sys.exit()
                board.get_mark(pos, board.pmark[board.onplay])
        # endregion

        # region UPDATES
        board.update()
        # endregion

        # region DRAW
        bg.draw()
        board.draw()
        board.draw_cursor(pos)

        for i in range(len(btns_game)):
            btns_game[i].draw()

        pygame.display.update()
        # endregion

    def state_manager(self):
        if self.scene == 'main_menu':
            self.main_menu()
        elif self.scene == 'game':
            self.game()

# endregion

# region MAIN GAME

# region GAME ENVIRONMENT
screen = pygame.display.set_mode((screen_width, screen_height))
bg = Background()
gamestate = GameState()
# endregion

# region INITIALIZATIONS: MAIN MENU
game_title = Text("game title", 25, 10, 52)
game_title.label = "TIC - TAC - TOE"
game_title.color = (255, 255, 255)
sub_title = Text("sub title", 160, 65, 14)
sub_title.label = "by: ThePokerFaceVII"
sub_title.color = (255, 255, 255)

btn_option1 = Button("player vs player", 100, 150, 250, 50)
btn_option2 = Button("player vs ai easy", 100, 225, 250, 50)
btn_option3 = Button("ai easy vs player", 100, 300, 250, 50)
btn_option4 = Button("exit", 100, 425, 250, 50)

btns_menu = [btn_option1, btn_option2, btn_option3, btn_option4]
txts_menu = [game_title, sub_title]

btn_option1.text.label = "PLAYER VS PLAYER"
btn_option2.text.label = "PLAYER VS AI (EASY)"
btn_option3.text.label = "PLAYER VS AI (HARD)"
btn_option4.text.label = "EXIT"

btn_option1.set_text_location(42, 18)
btn_option2.set_text_location(33, 18)
btn_option3.set_text_location(33, 18)
btn_option4.set_text_location(105, 18)

for i in range(len(btns_menu)):
    btns_menu[i].text.change_size(16)
    btns_menu[i].text.color = (205, 205, 50)
# endregion

# region INITIALIZATION: GAME
board = Board(75, 120, 300)
msglog = MessageLog()

btn_game_option1 = Button("back to menu", 38, 460, 100, 25)
btn_game_option2 = Button("reset game", 175, 460, 100, 25)
btn_game_option3 = Button("exit", 313, 460, 100, 25)

btn_game_option1.text.label = "MENU"
btn_game_option2.text.label = "RESET"
btn_game_option3.text.label = "EXIT"

btn_game_option1.set_text_location(33,6)
btn_game_option2.set_text_location(31,6)
btn_game_option3.set_text_location(37,6)

btns_game = [btn_game_option1, btn_game_option2, btn_game_option3]
# endregion

while True:
    gamestate.state_manager()

# endregion