class GameStats:
    """Acompanha as estatísticas para Alien Invasion"""

    def __init__(self, ai_game):
        """Inicializa as estatísticas"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0

        # Comece Alien Invasion no estado ativo
        self.game_active = False

    def reset_stats(self):
        """Inicializa as estatísticas que podem mudar durante o jogo"""
        self.rockets_left = self.settings.rocket_limit
        self.score = 0
        self.level = 1
