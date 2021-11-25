from random import randint
from math import sin, pi, hypot
import pygame
import settings


class Background:

    def __init__(self, hex_length=10):
        self.hex_length = hex_length
        self.color_top_left = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_top_right = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottom_left = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottom_right = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.bg_color = (60, 60, 60)

    def draw(self, screen: pygame.display.set_mode):
        # fill canvass will color
        screen.fill(self.bg_color)

        # draw all hexagons
        indent = False
        for y in range(0, settings.SCREEN_HEIGHT, round(self.hex_length * sin(pi / 3))):

            # indent or un-indent hexagons
            if indent:
                x_start = round(3 * self.hex_length / 2)
                indent = False
            else:
                x_start = 0
                indent = True

            # draw a row of hexagons
            for x in range(x_start, settings.SCREEN_WIDTH, round(3 * self.hex_length)):
                p1 = (round(x), round(y))
                p2 = (round(x + self.hex_length / 2), round(y - self.hex_length * sin(pi / 3)))
                p3 = (round(x + 3 * self.hex_length / 2), round(y - self.hex_length * sin(pi / 3)))
                p4 = (round(x + 2 * self.hex_length), round(y))
                p5 = (round(x + 3 * self.hex_length / 2), round(y + self.hex_length * sin(pi / 3)))
                p6 = (round(x + self.hex_length / 2), round(y + self.hex_length * sin(pi / 3)))
                pygame.draw.polygon(screen, self.weighted_color(x, y), (p1, p2, p3, p4, p5, p6), 1)

        # draw heading / score board background
        pygame.draw.rect(screen, (60, 60, 60), (0, 0, settings.SCREEN_WIDTH, 90))
        pygame.draw.line(screen, self.color_top_left, (0, 90), (settings.SCREEN_WIDTH, 90), 2)

    def weighted_color(self, x, y):
        # get distances from all screen corners
        d1 = hypot(x, y)
        d2 = hypot(settings.SCREEN_WIDTH - x, y)
        d3 = hypot(x, settings.SCREEN_HEIGHT - y)
        d4 = hypot(settings.SCREEN_WIDTH - x, settings.SCREEN_HEIGHT - y)

        # base case: point is a corner
        if d1 == 0:
            return self.color_top_left
        elif d2 == 0:
            return self.color_top_right
        elif d3 == 0:
            return self.color_bottom_left
        elif d4 == 0:
            return self.color_bottom_right

        # get inverse distance weight
        weight = (1 / d1) + (1 / d2) + (1 / d3) + (1 / d4)
        r = (self.color_top_left[0]/d1 + self.color_top_right[0]/d2 + self.color_bottom_left[0]/d3 + self.color_bottom_right[0]/d4) / weight
        g = (self.color_top_left[1] / d1 + self.color_top_right[1] / d2 + self.color_bottom_left[1] / d3 +
             self.color_bottom_right[1] / d4) / weight
        b = (self.color_top_left[2] / d1 + self.color_top_right[2] / d2 + self.color_bottom_left[2] / d3 +
             self.color_bottom_right[2] / d4) / weight

        # return weighted color
        return r, g, b

    def change_colors(self):
        self.color_top_left = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_top_right = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottom_left = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.color_bottom_right = (randint(0, 255), randint(0, 255), randint(0, 255))