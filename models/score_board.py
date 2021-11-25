import pygame


class ScoreBoard:

    def __init__(self, line_color=(0, 0, 0)):
        self.line_color = line_color
        self.x_color = (0, 0, 0)
        self.o_color = (0, 0, 0)
        self.x_score = 0
        self.o_score = 0
        self.message_log = ''

    def update_score(self, players: list):
        for player in players:
            if player.mark == "X":
                self.x_score = player.score
            else:
                self.o_score = player.score

    def update_player_colors(self, players: list):
        for player in players:
            if player.mark == "X":
                self.x_color = player.color
            else:
                self.o_color = player.color

    def update_line_color(self, line_color: tuple):
        self.line_color = line_color

    def draw(self, screen: pygame.display.set_mode):
        pygame.draw.line(screen, self.line_color, (75, 0), (75, 90), 2)
        pygame.draw.line(screen, self.line_color, (0, 30), (75, 30), 2)
        pygame.draw.line(screen, self.line_color, (375, 0), (375, 90), 2)
        pygame.draw.line(screen, self.line_color, (375, 30), (450, 30), 2)
        screen.blit(pygame.font.Font("freesansbold.ttf", 26).render("X", True, self.x_color), (27, 4))
        screen.blit(pygame.font.Font("freesansbold.ttf", 26).render("O", True, self.o_color), (402, 4))
        screen.blit(pygame.font.Font("freesansbold.ttf", 40).render(f"{self.x_score:02d}", True, self.x_color), (12, 43))
        screen.blit(pygame.font.Font("freesansbold.ttf", 40).render(f"{self.o_score:02d}", True, self.o_color), (390, 43))
        screen.blit(pygame.font.Font("freesansbold.ttf", 16).render(self.message_log, True, (255, 255, 255)), (100, 33))