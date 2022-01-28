import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from rocket import Rocket
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Classe geral para gerenciar os assets e o comportamento do jogo."""

    def __init__(self):
        """Inicializa o jogo e seus atributos."""
        pygame.init()
        self.settings = Settings()
        pygame.mouse.set_visible(False)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Cria uma instância para guardar as estatísticas do jogo
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Botão Play
        self.play_button = Button(self, "Pressione ESPAÇO para Jogar")

    def run_game(self):
        """Começa o loop principal do jogo."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.rocket.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Responda aos keypresses."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._fire_bullet()

    def _check_keydown_events(self, event):
        """Responda aos keypresses."""
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_d:
            self.rocket.moving_right = True
        elif event.key == pygame.K_a:
            self.rocket.moving_left = True
        if event.key == pygame.K_w:
            self.rocket.moving_up = True
        elif event.key == pygame.K_s:
            self.rocket.moving_down = True
        if event.key == pygame.K_SPACE:
            self._check_play_button()

    def _check_play_button(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_rockets()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.rocket.center_rocket()

    def _check_keyup_events(self, event):
        """Responda aos keypresses."""
        if event.key == pygame.K_d:
            self.rocket.moving_right = False
        elif event.key == pygame.K_a:
            self.rocket.moving_left = False
        if event.key == pygame.K_w:
            self.rocket.moving_up = False
        elif event.key == pygame.K_s:
            self.rocket.moving_down = False

    def _check_fleet_edges(self):
        """Responda apropriadamente se qualquer alien atingir a borda"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Muda a direção da frota"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Cria uma nova bala e adiciona-a ao grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Atualiza as imagens na tela e dá o flip"""
        self.screen.fill(self.settings.bg_color)
        self.rocket.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        # Botão play quando game está inativo
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _create_fleet(self):
        """Cria uma frota de aliens"""
        # Espaçamento entre cada alien é o comprimento de um alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # dois aliens, pois são duas margens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine o número de linhas de aliens que cabem na tela
        rocket_height = self.rocket.rect.height
        available_space_y = (self.settings.screen_height -
                                (4 * alien_height) - rocket_height)
        number_rows = available_space_y // (2 * alien_height)

        # Criar a frota completa
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Cria um alien e o coloca na linha de aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_bullets(self):
        """Atualiza a posição das balas e remove balas antigas"""
        self.bullets.update()

        # desaparece com as balas que atingem o topo
        # copiar os items (para que todos fiquem na nova lista)
        # remover aqueles que atingem o topo (bottom do rect = 0)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Responde as colisões bala-alien"""
        # Remove qualquer bala e alien que colidiram
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroi as balas existentes e cria uma nova frota
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Aumenta o nível do foguete
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Atualiza a posição de todos os aliens na frota"""
        self._check_fleet_edges()
        self.aliens.update()

        # Procure por colisões alien-rocket
        if pygame.sprite.spritecollideany(self.rocket, self.aliens):
            self._rocket_hit()

        # Procura por colisões com o final da tela
        self._check_aliens_bottom()

    def _rocket_hit(self):
        """Responde a colisão alien-rocket"""
        if self.stats.rockets_left > 0:
            self.stats.rockets_left -= 1
            self.sb.prep_rockets()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.rocket.center_rocket()
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        """Verifica se qualquer alien atingiu o final da tela"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._rocket_hit()
                break

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
