from . import Text, Button, Board, Background, ScoreBoard
import pygame
import sys


# define menu objects
menu_button_width = 250
menu_button_height = 50
menu_button_text_size = 16
menu_texts = [
    Text(name="game title", left=25, top=10, size=52, label="TIC - TAC - TOE", color=(255, 255, 255)),
    Text(name="sub title", left=160, top=65, size=14, label="by: Jobo Fernandez", color=(255, 255, 255)),
]
menu_buttons = [
    Button(name="player vs player", left=100, top=150, width=menu_button_width, height=menu_button_height,
           text=Text(name="txt player vs player", left=100+42, top=150+18, size=menu_button_text_size, color=(205, 205, 50), label="PLAYER VS PLAYER")),
    Button(name="player vs ai easy", left=100, top=225, width=menu_button_width, height=menu_button_height,
           text=Text(name="txt player vs ai easy", left=100+33, top=225+18, size=menu_button_text_size, color=(205, 205, 50), label="PLAYER VS AI (EASY)")),
    Button(name="ai easy vs player", left=100, top=300, width=menu_button_width, height=menu_button_height,
           text=Text(name="txt ai easy vs player", left=100+33, top=300+18, size=menu_button_text_size, color=(205, 205, 50), label="PLAYER VS AI (HARD)")),
    Button(name="exit", left=100, top=425, width=menu_button_width, height=menu_button_height,
           text=Text(name="txt exit", left=100+105, top=425+18, size=menu_button_text_size, color=(205, 205, 50), label="EXIT")),
]

# define in-game objects
in_game_button_width = 100
in_game_button_height = 25
in_game_buttons = [
    Button(name="back to menu", left=38, top=460, width=in_game_button_width, height=in_game_button_height,
           text=Text(name="txt back to menu", left=38+33, top=460+6, label="MENU")),
    Button(name="reset game", left=175, top=460, width=in_game_button_width, height=in_game_button_height,
           text=Text(name="txt reset game", left=175+31, top=460+6, label="RESET")),
    Button(name="exit", left=313, top=460, width=in_game_button_width, height=in_game_button_height,
           text=Text(name="txt exit", left=313+37, top=460+6, label="EXIT")),
]

# define major objects
background = Background()
score_board = ScoreBoard(line_color=background.color_top_left)
board = Board(left=75, top=120, width=300)


class GameManager:

    def __init__(self):
        self.game_state = 'main_menu'
        self.event_handler = {
            "main_menu": self.handle_event_main_menu,
            "in_game": self.handle_event_in_game,
        }

    def handle_event(self, event: pygame.event.Event, pos: tuple):
        self.event_handler[self.game_state](event=event, pos=pos)

    def handle_event_main_menu(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.MOUSEMOTION:
            # handle button mouse-over effects
            for button in menu_buttons:
                button.glow() if button.is_over(pos) else button.unglow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # handle exit
            if menu_buttons[3].is_over(pos):
                pygame.quit()
                sys.exit()

            # handle game options
            if menu_buttons[0].is_over(pos):
                board.start(p1='PLAYER 1', p2='PLAYER 2', score_board=score_board)
            elif menu_buttons[1].is_over(pos):
                board.start(p1='PLAYER 1', p2='AI-EASY', score_board=score_board)
            elif menu_buttons[2].is_over(pos):
                board.start(p1='PLAYER 1', p2='AI-HARD', score_board=score_board)

            # background and game state adjustments
            background.change_colors()
            self.game_state = 'in_game'

    def handle_event_in_game(self, event: pygame.event.Event, pos: tuple):
        if event.type == pygame.MOUSEMOTION:
            # handle button mouse-over effects
            for button in in_game_buttons:
                button.glow() if button.is_over(pos=pos) else button.unglow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # handle exit
            if in_game_buttons[2].is_over(pos=pos):
                pygame.quit()
                sys.exit()

            # handle menu option
            if in_game_buttons[0].is_over(pos=pos):
                background.change_colors()
                self.game_state = 'main_menu'

            # handle game reset option
            elif in_game_buttons[1].is_over(pos=pos):
                board.reset(score_board=score_board)
                background.change_colors()
                score_board.update_line_color(line_color=background.color_top_left)

            # handle game input option
            else:
                board.set_mark(pos=pos, mark=board.on_play.mark, score_board=score_board)
                board.set_ai_move(score_board=score_board)

    def draw(self, screen: pygame.display.set_mode, cursor_pos: tuple):
        # draw background
        background.draw(screen=screen)

        # draw major objects
        objects = []
        if self.game_state == "main_menu":
            objects = menu_buttons + menu_texts
        elif self.game_state == "in_game":
            score_board.draw(screen=screen)
            board.draw(screen=screen)
            board.draw_cursor(screen=screen, pos=cursor_pos)
            objects = in_game_buttons

        # draw minor objects (texts and buttons)
        for obj in objects:
            obj.draw(screen=screen)

        # update display
        pygame.display.update()
