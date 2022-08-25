import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	def __init__(self):
		pygame.init()
		self.settings = Settings()

		self.screen = pygame.display.set_mode(self.settings.screen_dimension_tuple)
		# FULL SCREEN SETTINGS - uncomment next three lines and comment out above line to make game full screen
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		# self.settings.screen_width = self.screen.get_rect().width
		# self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		# Create instance of game stats
		self.stats = GameStats(self)

		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()
		self.play_button = Button(self, "Play")

	def run_game(self):
		while True:
			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()

	def _check_events(self):
		"""Respond to kepyresses and mouse events."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			self.settings.initialize_dynamic_settings()

			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()

			self.aliens.empty()
			self.bullets.empty()

			self._create_fleet()
			self.ship.center_ship()

			pygame.mouse.set_visible(False)

	def _check_keydown_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False

	def _ship_hit(self):
		"""Respond to ship being hit"""
		if self.stats.ships_left > 0:
			# Decrement ships left
			self.stats.ships_left -= 1

			# Get rid of remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			# Create new fleet and center ship
			self._create_fleet()
			self.ship.center_ship()

			# Pause between tries
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _fire_bullet(self):
		"""Create new bullet anda add to bullets group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets"""
		# Update bullet positions
		self.bullets.update()


		# Get rid of bullets that disappeared at top of screen
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		"""Respond to bullet-alien collisions"""
		# Check for bullets that hit aliens and if so, get rid of bullet and alien
		collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

		if not self.aliens:
			# Destoy existing bullets and create new fleet
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			self.stats.level += 1
			self.sb.prep_level()

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.check_high_score()

	def _update_aliens(self):
		"""Check if fleet is at an edge, then update positions af all aliens"""
		self._check_fleet_edges()
		self.aliens.update()

		# Look for alien-ship collision
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Look for aliens hitting bottom of screen
		self._check_aliens_bottom()

	def _update_screen(self):
		"""Update images on the screen, and flip to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			# bullet.draw_bullet()
			bullet.blitme()
		self.aliens.draw(self.screen)

		self.sb.show_score()

		if not self.stats.game_active:
			self.play_button.draw_button()

		pygame.display.flip()

	def _create_fleet(self):
		"""Create fleet of aliens"""
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# Determine number of rows of aliens that fit screen
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Create full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		#Create alien and place in in row
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		alien.rect.y = alien_height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""Respond appropriately if any aliens have reached an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _check_aliens_bottom(self):
		"""Check of any aliens have reached bottom of screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treat same as if ship got hit
				self._ship_hit()
				break

	def _change_fleet_direction(self):
		"""Drop whole fleet and change direction"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

if __name__ == '__main__':
	ai = AlienInvasion()
	ai.run_game()



























