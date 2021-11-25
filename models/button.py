from . import Text
import pygame


class Button:

    def __init__(self, name: str, left: int, top: int, width: int, height: int, text: Text,
                 border_color=(150, 150, 150), border_width=3, bg_color=(100, 100, 240), bg_shadow=(30, 30, 170)):
        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_width = border_width
        self.bg_color = bg_color
        self.bg_shadow = bg_shadow

        # self.text = Text(self.left, self.top, self.height // 2)
        self.text = text

    def draw(self, screen: pygame.display.set_mode):
        pygame.draw.rect(screen, self.bg_color, (self.left, self.top, self.width, self.height))
        pygame.draw.rect(screen, self.bg_shadow, (self.left, (self.top + self.height//2), self.width, self.height // 2))
        pygame.draw.rect(screen, self.border_color, (self.left, self.top, self.width, self.height), self.border_width)
        self.text.draw(screen=screen)

    def set_text_location(self, left: int, top: int):
        self.text.left = self.left + left
        self.text.top = self.top + top

    def glow(self):
        self.border_color = (255, 255, 255)
        self.border_color = (30, 100, 30)
        self.bg_color = (100, 240, 100)
        self.bg_shadow = (30, 170, 30)
        self.text.color = (155, 15, 155)
        self.text.color = (50, 50, 50)

    def unglow(self):
        self.border_color = (150, 150, 150)
        self.bg_color = (100, 100, 240)
        self.bg_shadow = (30, 30, 170)
        self.text.color = (255, 255, 255)

    def is_over(self, pos):
        return True if (self.left < pos[0] < self.left + self.width and self.top < pos[1] < self.top + self.height) else False
