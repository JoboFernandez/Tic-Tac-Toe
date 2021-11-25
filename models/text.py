import pygame


class Text:

    def __init__(self, name: str, left: int, top: int, size=10, label='', color=(0, 0, 0)):
        self.name = name
        self.left = left
        self.top = top
        self.size = size
        self.label = label
        self.color = color

    def draw(self, screen: pygame.display.set_mode):
        screen.blit(pygame.font.Font("freesansbold.ttf", self.size).render(self.label, True, self.color), (self.left, self.top))
