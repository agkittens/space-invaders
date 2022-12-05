import os
import pygame

class Window:

    def __init__(self):
        self.width = 1200
        self.height = 800
        self.background = os.path.join('assets', 'background.jpg')
        self.icon = os.path.join('assets', 'icon.png')
        self.caption = 'star wars: space invaders'
        self.fps = 120
        self.startText = pygame.font.Font(r'C:\Users\agkit\AppData\Local\Microsoft\Windows\Fonts\Monocraft.otf', 50)
        self.gameText = pygame.font.Font(r'C:\Users\agkit\AppData\Local\Microsoft\Windows\Fonts\Monocraft.otf', 20)


    def drawScreen(self):
        surface = pygame.display.set_mode((self.width, self.height))
        self.background = pygame.transform.scale(pygame.image.load(self.background), (self.width, self.height))
        icon = pygame.image.load(self.icon)
        surface.blit(self.background, (0, 0))
        pygame.display.set_caption(self.caption)
        pygame.display.set_icon(icon)
        return surface

