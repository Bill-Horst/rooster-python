class Settings:

	def __init__(self):
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.screen_dimension_tuple = (self.screen_width, self.screen_height)
		self.bg_color = (0, 0, 0)

		# Ship settings
		self.ship_speed = 1.5
		self.ship_limit = 3

		# Bullet settings
		self.bullet_speed = 1.5
		self.bullet_width = 3
		self.bullet_height = 15
		# self.bullet_color = (60, 60, 60)
		self.bullet_color = (249, 249, 6)
		self.bullets_allowed = 99

		# Alien settings
		self.alien_speed = 1.0
		self.fleet_drop_speed = 10
		# fleet direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

		# How quickly game speeds up
		# self.speedup_scale = 1.1
		self.speedup_scale = 1.5
		self.score_scale = 2.0

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		self.ship_speed = 1.5
		self.bullet_speed = 3.0
		self.alien_speed = 1.0

		self.fleet_direction = 1

		self.alien_points = 50

	def increase_speed(self):
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)








