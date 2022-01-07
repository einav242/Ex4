import pygame
from pygame import display, RESIZABLE


class Rect_text:

    def __init__(self, text, width, height, pos, screen, font,text_color,rect_color):
        self.screen = screen
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = rect_color
        FONT = font
        self.text_surf = FONT.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

