import pygame
import random
pygame.init()
WHITE = (255, 255, 255)

done = False


def create_meteor():
	meteor = Meteor(width, height)
	meteor_group.add(meteor)
	all_sprites_group.add(meteor)

def distance(screen):
    """Show how far the rocketship has travelled."""
    # Get time since init was called
    time = pygame.time.get_ticks()
    # Convert milliseconds to seconds, 1 second = 1 km
    travel_distance = round(time/1000, 2)
    font = pygame.font.SysFont ("transistor", 25, True, False)
    travel_text = font.render("You've travelled " + str(travel_distance) + " kms", True, WHITE)
    screen.blit(travel_text, (HW-100, HH))

def collison():
	# Check to see if player has collided with meteor
	meteor_hit_list = pygame.sprite.spritecollide(player, meteor_group, True)
	# Event if player collides with meteor 
	for item in meteor_hit_list:
		print("Shuttle hit")
		create_meteor()

class Player(pygame.sprite.Sprite):
	def __init__(self,PLAYER_SURFACE, HW, HH):
		super().__init__()
		self.image = PLAYER_SURFACE            
		self.rect = pygame.rect.Rect(((HW - (PLAYER_SURFACE.get_width())), HH), self.image.get_size())

		# Gravity
		self.dy = 0 

	def ignite(self):
		self.dy = -400

	def update(self, dt):

        # Apply gravity
		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt
     
        # What happens if go to border of screen
		if self.rect.top <= 0:   # Top
			self.rect.y = 0
			self.dy = -4
		elif self.rect.bottom >= height:   # Bottom
			self.rect.y = 526-self.rect.height

class Meteor(pygame.sprite.Sprite):
	def __init__(self, width, height):
		super().__init__()
		self.image = random.choice(METEOR_IMAGES)	
		self.rect = self.image.get_rect()

		# Random starting location
		self.rect.x = random.randrange(width, (width + 300))
		self.rect.y = random.randrange(0, height)
            
		# Random movement to the left
		self.change_x = random.randrange(-10,-5)
		self.change_y = random.randrange(-4,3)

	def reset_pos(self, screen):
		self.image = random.choice(METEOR_IMAGES)
		self.rect = self.image.get_rect()

		self.rect.x = random.randrange(width, (width + 100))
		self.rect.y = random.randrange(0, height)

		# Random movement to the left
		self.change_x = random.randrange(-10,-5)
		self.change_y = random.randrange(-4,3)

	
	def update(self): 
		# Move meteor
		self.rect.x += self.change_x
		self.rect.y += self.change_y
	
		# Reset if falls off screen
		if self.rect.right < 0:
			self.reset_pos(screen)
		if self.rect.top > height:
			self.reset_pos(screen)
		if self.rect.bottom < 0:
			self.reset_pos(screen)

clock = pygame.time.Clock()


background = pygame.image.load("assets/background.png")

# Get dimensions of background
width = background.get_width()
height = background.get_height() 
HW, HH = width/2, height/2
screen = pygame.display.set_mode((width,height))
background = background.convert()
x = 0 

PLAYER_SURFACE = pygame.image.load("assets/player.png").convert_alpha()
METEOR_IMAGES = []
METEOR_LIST = [
	"assets/meteors/meteor1.png",
	"assets/meteors/meteor2.png",
	"assets/meteors/meteor3.png",
	"assets/meteors/meteor4.png",
	"assets/meteors/meteor5.png",
	"assets/meteors/meteor6.png",
	"assets/meteors/meteor7.png",
	"assets/meteors/meteor8.png",
	"assets/meteors/meteor9.png",
	"assets/meteors/meteor10.png",
	"assets/meteors/meteor11.png",
	"assets/meteors/meteor12.png"
]
for image in METEOR_LIST:
	METEOR_IMAGES.append(pygame.image.load(image).convert_alpha())

pygame.display.set_caption("")

all_sprites_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# Create spaceship 
player = Player(PLAYER_SURFACE, HW, HH)
all_sprites_group.add(player)

# Create meteor sprites on the screen     
for i in range(4):
    create_meteor()

#-----Main Program Loop 
while not done:
	dt = clock.tick(30)
	# Main event Loop 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			player.ignite()
			
#-----Game Logic 

	# Draw background and move to the left
	rel_x = x % width
	screen.blit(background, (rel_x - width, 0))
	if rel_x < width:
		screen.blit(background, (rel_x, 0))
	x -= 2
	
	distance(screen)
	all_sprites_group.draw(screen)
	

	meteor_group.update()
	player.update(dt/1000)
	collison()

	pygame.display.flip()

# Make sure to quit 
pygame.quit()
