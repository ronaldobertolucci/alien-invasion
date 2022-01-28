import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """Inicializa os atributos do botão"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Determina as dimensões e propriedades
        self.width, self.height = 500, 60
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Constroi o rect do botão e centraliza-o
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # A mensagem do botão
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Transforma o texto em uma imagem renderizada"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Leva o botão para a tela"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
