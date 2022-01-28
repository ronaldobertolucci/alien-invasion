import pygame
from pygame.sprite import Sprite

class Rocket(Sprite):
    """Uma classe para gerenciar um foguete."""

    def __init__(self, ai_game):
        """Inicializa um foguete e determina sua posição inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # carrega a imagem do foguete e determina seu rect.
        self.image = pygame.image.load('images/rocket.bmp')
        self.image = pygame.transform.scale(self.image, (36, 92))

        self.rect = self.image.get_rect()

        # inicia o foguete no meio da tela
        self.rect.midbottom = self.screen_rect.midbottom

        # transforma a posição horizontal em float (importante para o setting)
        self.x = float(self.rect.x)



        # flag para o movimento
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Update the rocket's position based on the movement flag."""
        # atualiza a posição em x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.rocket_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.rocket_speed

        # atualiza a posição em definitivo
        self.rect.x = self.x


    def blitme(self):
        """Leva o foguete para a tela."""
        self.screen.blit(self.image, self.rect)

    def center_rocket(self):
        """Centraliza o foguete na tela"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
