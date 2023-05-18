import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH = 833
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon & Dragons")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (36, 12, 44)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# bag
coins = 0
coin_width = 9
coin_height = 17
coin_x = 0
coin_y = 0
coin_taken = False

coins_array = []

font = pygame.font.Font('freesansbold.ttf', 16)
text_space = font.render('Press SPACE to attack', True, WHITE, BLACK)
text_r = font.render('Press R to invoque an enemy', True, WHITE, BLACK)

# Define the character
character_width = 30
character_height = 50
character_x=0.0
character_y=0.0
character_x = WIDTH // 2 - character_width // 2
character_y = HEIGHT // 2 - character_height // 2
character_speed = 3
character_health = 100
character_damage= 50

# Load the character image
character_image = pygame.image.load("assets/knight.png")
character_image = pygame.transform.scale(character_image, (character_width, character_height))

# Define the room
room_width = WIDTH * .9
room_height = HEIGHT * .9
room_x = WIDTH // 2 - room_width // 2
room_y = HEIGHT // 2 - room_height // 2

# define separation of the window to the room
separation_x = WIDTH * .085
separation_y = HEIGHT * .14

# Load the room image
room_image = pygame.image.load("assets/room.png")
room_image = pygame.transform.scale(room_image, (room_width, room_height))

# Define the enemy
enemy_width = 30
enemy_height = 50
enemy_speed = .3
enemy_x = random.randint(round(separation_x, 0), round((room_width - separation_x), 0))
enemy_y = random.randint(round(separation_y, 0), round((room_height - separation_y), 0))
enemy_power = 1
enemy_direction_x = ''
enemy_direction_y = ''
enemy_push = 5
enemy_health = 100

# Load the enemy image
enemy_image = pygame.image.load("assets/skeleton.png")
enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))


# Define the coin
coin_width = 30
coin_height = 50

# Load the coin image
coin_image = pygame.image.load("assets/coin.png")
coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))

# Function to handle character movement
def character_behavior(keys):
    global character_x, character_y

    if keys[pygame.K_a]:
        character_x -= character_speed
    if keys[pygame.K_d]:
        character_x += character_speed
    if keys[pygame.K_w]:
        character_y -= character_speed
    if keys[pygame.K_s]:
        character_y += character_speed

# Function to handle enemy movement
def move_enemy():
    global enemy_x, enemy_y, enemy_direction_x, enemy_direction_y

    if enemy_x < character_x:
        enemy_x += enemy_speed
        enemy_direction_x = 'right'
    else:
        enemy_x -= enemy_speed
        enemy_direction_x = 'left'

    if enemy_y < character_y:
        enemy_y += enemy_speed
        enemy_direction_y = 'bottom'
    else:
        enemy_y -= enemy_speed
        enemy_direction_y = 'top'

# Function to handle collisions
def check_collision():
    global character_x, character_y, character_health, enemy_direction_x, enemy_direction_y, enemy_push

    if character_x < (room_x + separation_x):
        character_x = (room_x + separation_x)
    elif character_x + character_width > (room_x - separation_x) + room_width:
        character_x = (room_x - separation_x) + room_width - character_width

    if character_y < (room_y + separation_y):
        character_y = (room_y + separation_y)
    elif character_y + character_height > (room_y - separation_y) + room_height:
        character_y = (room_y - separation_y) + room_height - character_height

    # Check for collision with the enemy
    if (
        character_x < enemy_x + enemy_width
        and character_x + character_width > enemy_x
        and character_y < enemy_y + enemy_height
        and character_y + character_height > enemy_y
    ):
        # Game over scenario
        if(enemy_health <= 0):
            return

        character_health -= enemy_power

        if(enemy_direction_x == 'left'):
            for i in range(0, enemy_push, 1):
                character_x -= i
        else:
            for i in range(0, enemy_push, 1):
                character_x += i
        
        if(enemy_direction_y == 'top'):
            for i in range(0, enemy_push, 1):
                character_y -= i
        else:
            for i in range(0, enemy_push, 1):
                character_y += i

        if (character_health <= 0):
            print("Game Over")
            pygame.quit()
            quit()

# Function to update the game screen
def update_screen():
    screen.fill(PURPLE)
    screen.blit(room_image, (room_x, room_y, room_width, room_height))
    screen.blit(character_image, (character_x, character_y, character_width, character_height))
    text_health = font.render(('Health:' + str(character_health)), True, WHITE, BLACK)
    screen.blit(text_health, (10, 10))
    text_coins = font.render(('Coins:' + str(coins)), True, WHITE, BLACK)
    screen.blit(text_coins, (10, 40))
    screen.blit(text_space, (10, HEIGHT - 20))
    screen.blit(text_r, (10, HEIGHT - 40))
    if(enemy_health <= 0):
        coin_x = enemy_x
        coin_y = enemy_y
        if(coin_taken == False):
            screen.blit(coin_image, (coin_x, coin_y, coin_width, coin_height))
    else: 
        screen.blit(enemy_image, (enemy_x, enemy_y, enemy_width, enemy_height))

    pygame.display.flip()

def spawn_random_enemy():
    global enemy_width, enemy_height, enemy_speed, enemy_x, enemy_y, enemy_power, enemy_push, enemy_health, enemy_image
    enemy_images = ["assets/skeleton.png", "assets/dark-knight.png", "assets/witcher.png"]
    enemy_widths = [30, 43, 50]
    enemy_heights = [53, 73, 75]
    enemy_speeds = [.3, .5, .7]
    enemy_powers = [5, 25, 34]
    enemy_pushes = [5, 7, 10]
    enemy_healths = [100, 120, 150]

    random_number = random.randint(0,2)
    enemy_width = enemy_widths[random_number]
    enemy_height = enemy_heights[random_number]
    enemy_speed = enemy_speeds[random_number]
    enemy_x = random.randint(round(separation_x, 0), round((room_width - separation_x), 0))
    enemy_y = random.randint(round(separation_y, 0), round((room_height - separation_y), 0))
    enemy_power = enemy_powers[random_number]
    enemy_push = enemy_pushes[random_number]
    enemy_health = enemy_healths[random_number]
    
    enemy_image = pygame.image.load(enemy_images[random_number])
    enemy_speed = .3
    enemy_image = pygame.transform.scale(enemy_image, (enemy_width, enemy_height))

def level_up():
    global character_health, character_damage, enemy_speed
    character_damage *= 1.03

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    # print(character_x,enemy_x)
    if(coin_taken == False):
        if(abs(character_x - enemy_x) <= 10 and abs(character_y - enemy_y) <= 10 ):
            coin_taken = True
            coins += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_r): 
                if(enemy_health <= 0):
                    # Spawn an enemy
                    coin_taken = False
                    spawn_random_enemy()
            if event.key == pygame.K_SPACE:
                if(abs(enemy_x - character_x) <= 50 and abs(enemy_y - character_y) <= 50):
                    # Delete the enemy
                    enemy_health -= character_damage
                    if(enemy_health <= 0):
                        enemy_speed = 0
                        level_up()


    keys = pygame.key.get_pressed()
    character_behavior(keys)
    move_enemy()
    # drop_random_item()
    check_collision()
    update_screen()

pygame.quit()
