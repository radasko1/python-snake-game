import pygame
from pygame.math import Vector2
import random


# TODO check colission

# Color Declaration
color_black = (0, 0, 0)
color_red = (255,50,80)
color_blue = (0, 255, 20)

# Window resolution
block_size = int(20)
window_width = block_size * 26
window_height = block_size * 26



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
        self.crashed = False

    def draw(self) -> None:
        """Draw snake body on 'canvas'"""
        for body_block in self.body:
            rect = pygame.Rect(body_block.x, body_block.y, block_size, block_size)
            # draw on canvas
            pygame.draw.rect(game_screen, color_blue, rect)

    def move(self) -> None:
        """Move snake"""
        # Move each segment except head to the position of the segment before it (from list_length to 1)
        for i in range(len(self.body) -1, 0, -1):
            # check if snaked crashed
            self.is_crashed(self.body[i])
            # body movement
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        # Move head based on direction
        self.body[0].x += self.direction_x * block_size
        self.body[0].y += self.direction_y * block_size
            
    def grow(self) -> None:
        """Grow snake by adding a new segment at the head"""
        snake_head = self.body[0] + Vector2(self.direction_x * block_size, self.direction_y * block_size)
        self.body.insert(0, snake_head)

    def is_crashed(self, body_part: Vector2) -> None:
        """Whether snaked crashed into his body"""
        crash_happened = body_part == self.body[0]
        if crash_happened: self.crashed = True

    def check_border(self) -> None:
        for i in range(0, len(self.body), 1):
            # left side border
            if self.body[i].x == (block_size * -1): 
                self.body[i] = Vector2(window_width, self.body[i].y)
            # top side border (NOT WORKING)
            elif self.body[i].y == (block_size * -1): 
                self.body[i] = Vector2(self.body[i].x, window_height)
            # right side border
            elif self.body[i].x == window_width: 
                self.body[i] = Vector2(0, self.body[i].y)
            # bottom side border
            elif self.body[i].y == window_height: 
                self.body[i] = Vector2(self.body[i].x, 0)

# FOOD class
class Food:
    def __init__(self) -> None:
        self.respawn()

    def draw(self) -> None:
        """Draw food on canvas"""
        pygame.draw.rect(game_screen, color_red, self.object)

    def respawn(self) -> None:
        """Change food position"""
        pos_x, pos_y = generate_food_position()
        self.object = pygame.Rect(pos_x, pos_y, block_size, block_size)        


# GAME class
class Game:
    def __init__(self) -> None: 
        self.score = int(0)
        self.running = True

    def add_score(self) -> None:
        """Add score points"""
        self.score += 10
        print('score:', self.score)

    def stop_game(self) -> None:
        """Stop game cycle"""
        self.running = False



def generate_food_position() -> tuple[int, int]:
    """Generate random number"""
    max_width = int(window_width / block_size)
    max_height = int(window_height / block_size)
    x = random.randrange(0, max_width, 1) * block_size
    y = random.randrange(0, max_height, 1) * block_size
    return (x, y)



def game():
    """Game loop"""
    snake = Snake()
    food = Food()
    game = Game()

    while game.running:
        # Events
        for event in pygame.event.get():
            # Key press event
            if (event.type == pygame.KEYDOWN):
                # Binded keys
                if (event.key == pygame.K_ESCAPE):
                    pygame.quit()
                elif (event.key == pygame.K_DOWN and snake.direction_x != 0):
                    snake.direction_x = 0
                    snake.direction_y = 1
                elif (event.key == pygame.K_UP and snake.direction_x != 0):
                    snake.direction_x = 0
                    snake.direction_y = -1
                elif (event.key == pygame.K_LEFT and snake.direction_y != 0):
                    snake.direction_x = -1
                    snake.direction_y = 0
                elif (event.key == pygame.K_RIGHT and snake.direction_y != 0):
                    snake.direction_x = 1
                    snake.direction_y = 0

         # Redraw screen background
        game_screen.fill(color_black)
        # Food
        food.draw()

        # Grow snake / Move snake
        if (food.object.x == snake.body[0].x and food.object.y == snake.body[0].y):
            snake.grow()
            food.respawn()
            game.add_score()
        else:
            snake.move()
        
        snake.check_border()

        # Check if snake crashed, then stop game
        if snake.crashed: 
            print('snake crashed')
            game.stop_game()

        # Draw snake 
        snake.draw()

        # Update screen
        pygame.display.update()   
        clock.tick(5)     
    

if __name__ == "__main__":
    game()
