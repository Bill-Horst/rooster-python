import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""Class to manage bullets fired from ship"""
	def __init__(self, ai_game):
		"""Create bullet object at ship's current position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		# self.color = self.settings.bullet_color

		# Create bullet rect at (0 ,0) then set correct position
		# self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
		# 	self.settings.bullet_height)
		# self.rect.midtop = ai_game.ship.rect.midtop


		self.image = pygame.image.load('images/corn_bullet.bmp')
		self.rect = self.image.get_rect()
		self.rect.midtop = ai_game.ship.rect.midtop


		# Store bullet's position as decimal value
		self.y = float(self.rect.y)

	def update(self):
		"""Move bullet up screen"""
		# Update decimal position of bullet
		self.y -= self.settings.bullet_speed
		self.rect.y = self.y

	def draw_bullet(self):
		"""Draw bullet to screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)

	def blitme(self):
		self.screen.blit(self.image, self.rect)