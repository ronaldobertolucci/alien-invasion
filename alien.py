import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe para representar um alien em uma frota"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carregue a imagem do alien e defina o rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Comece com cada alien perto do canto superior esquerdo
        # Medida feita pelas características da imagem
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Marca a posição horizontal exata do alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Retorna True se o alien atingiu a extremidade da tela"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Mova o alien para direita ou esquerda"""
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x
