import pygame
from pygame.math import Vector2
import random


# TODO 
# vykreslovani - posouva se dopredu o jeden blok, nejdriv telo, pak hlava, proto se v jednom momente mohou prekryvat, proto by byo dobre po snezeni jidla
# vynechat posun tela, dosadit dopredu dalsi block, a pak posunout hlavu
# TODO check colission

# Color Declaration
color_black = (0, 0, 0)
color_red = (255,50,80)
color_violet = (148, 0, 211)
color_blue = (0, 0, 255)

# Window resolution
window_width = int(600)
window_height = int(480)

# Snake variables
block_size = int(20)


# PyGame Initialization
pygame.init()

clock = pygame.time.Clock()

game_screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")


# SNAKE class
class Snake:
    def __init__(self) -> None:
        self.direction_x = 1
        self.direction_y = 0
        # Body using vector position - [head, body]
        self.body = [Vector2(block_size * 3, block_size * 3), Vector2(block_size * 2, block_size * 3)]

    def draw(self) -> None:
        """Draw snake body on 'canvas'"""
        for body_block in self.body:
            rect = pygame.Rect(body_block.x, body_block.y, block_size, block_size)
            # draw on canvas
            pygame.draw.rect(game_screen, color_blue, rect)

    def move(self):
        """Move snake"""
        # posunout indexy podle predchozich pozic - co bylo na [0] dat na [1], co bylo na [1] dat na [2], atd...
        # Move each segment except head to the position of the segment before it
        for i in range(len(self.body) -1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        # posunout [0] na vypoctenou pozici
        # Move head based on direction
        self.body[0].x += (self.direction_x * block_size)
        self.body[0].y += (self.direction_y * block_size)        
            
    def grow(self):
        """Grow snake by adding a new segment at the head"""
        new_head = self.body[0] + Vector2(self.direction_x * block_size, self.direction_y * block_size)
        self.body.insert(0, new_head)  # Insert at the head (index 0)


# FOOD class
class Food:
    def __init__(self) -> None:
        self.respawn()

    def draw(self):
        """Draw food on canvas"""
        pygame.draw.rect(game_screen, color_red, self.object)

    def respawn(self):
        """Change food position"""
        pos_x, pos_y = generate_food_position()
        self.object = pygame.Rect(pos_x, pos_y, block_size, block_size)        


def generate_food_position() -> tuple[int, int]:
    """Generate random number"""
    max_width = int(window_width / block_size)
    max_height = int(window_height / block_size)
    x = random.randrange(0, max_width, 1) * block_size
    y = random.randrange(0, max_height, 1) * block_size
    return (x, y)


def game():
    """Game loop"""
    game_running = True
    snake = Snake()
    food = Food()

    while game_running:
        # Events
        for event in pygame.event.get():
            # Key press event
            if (event.type == pygame.KEYDOWN):
                # Binded keys
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                elif (event.key == pygame.K_DOWN):
                    snake.direction_x = 0
                    snake.direction_y = 1
                elif (event.key == pygame.K_UP):
                    snake.direction_x = 0
                    snake.direction_y = -1
                elif (event.key == pygame.K_LEFT):
                    snake.direction_x = -1
                    snake.direction_y = 0
                elif (event.key == pygame.K_RIGHT):
                    snake.direction_x = 1
                    snake.direction_y = 0

         # Redraw screen background
        game_screen.fill(color_black)
        # Food
        food.draw()

        # Eat food
        if (food.object.x == snake.body[0].x and food.object.y == snake.body[0].y):
            snake.grow()
            food.respawn()
        else:
            snake.move()
            

        # Draw snake 
        snake.draw()

        # Update screen
        pygame.display.update()   
        clock.tick(10)     
    

if __name__ == "__main__":
    game()
