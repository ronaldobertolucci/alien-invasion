import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Uma classe para gerenciar balas atiradas pelo foguete"""

    def __init__(self, ai_game):
        """Cria uma bala na posição atual do foguete"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Cria um rect para bala em (0,0) e determina a posição
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.rocket.rect.midtop

        # guarda a posição da bala em decimais
        self.y = float(self.rect.y)

    def update(self):
        """Move a bala na tela"""
        # Atualiza a posição decimal da bala
        self.y -= self.settings.bullet_speed
        # Atualiza a posição do retângulo
        self.rect.y = self.y

    def draw_bullet(self):
        """Leva as balas para a tela."""
        pygame.draw.rect(self.screen, self.color, self.rect)
