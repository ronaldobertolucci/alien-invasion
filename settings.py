class Settings:
    """Uma classe para gerenciar todos os settings de Alien Invasion."""

    def __init__(self):
        """Inicializa os settings do jogo"""
        # settings da tela
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (208, 239, 255)

        # settings do foguete
        self.rocket_speed = 1.5
        self.rocket_limit = 3

        # settings da Bala
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # settings do Alien
        self.alien_speed = 1
        self.fleet_drop_speed = 7
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Quão rápido a velocidade aumenta
        self.speedup_scale = 1.1

        # Quão rápido a pontuação aumenta
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa os settings que mudam durante o game"""
        self.rocket_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1
        self.alien_points = 50
        self.fleet_direction = 1

    def increase_speed(self):
        """Aumenta a velocidade e a pontuação"""
        self.rocket_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
