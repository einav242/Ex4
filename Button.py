import pygame
from pygame import display, RESIZABLE


class Button:

    def __init__(self, text, width, height, pos, screen, font):
        self.screen = screen
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (255, 0, 0)
        FONT = font
        self.text_surf = FONT.render(text, True, (255,255,255))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

