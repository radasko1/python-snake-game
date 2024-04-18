import pygame
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

# Snake Game Object
class Snake:
    def __init__(self) -> None:
        self.pos_x = block_size
        self.pos_y = block_size
        self.velocity_x = 1
        self.velocity_y = 0
        # Head is first - on right side
        self.head = pygame.Rect(self.pos_x, self.pos_y, block_size, block_size)
        # Body is after head - from right to left
        self.body = [pygame.Rect(self.pos_x - block_size, self.pos_y, block_size, block_size)]
        self.colied = False

    def draw_head(self) -> None:
        """Draw snake head on 'canvas'"""
        pygame.draw.rect(game_screen, color_violet, self.head)

    def draw_body(self) -> None:
        """Draw snake body on 'canvas'"""
        for _body in self.body:
            pygame.draw.rect(game_screen, color_blue, _body)

    def redraw(self) -> None:
        """Redraw snake body parts on 'canvas'"""
        if self.is_collied():
            pygame.time.wait(9999999999)

        self.body.append(self.head)
        #
        for i in range(len(self.body) - 1):
            self.body[i].x = self.body[i + 1].x
            self.body[i].y = self.body[i + 1].y
        #
        self.head.x = self.head.x + (self.velocity_x * block_size)
        self.head.y = self.head.y + (self.velocity_y * block_size)
        #
        self.body.remove(self.head)

    def grow(self) -> None:
        """Add block on snake tail"""
        self.body.append(pygame.Rect(self.head.x, self.head.y, block_size, block_size))

    def is_collied(self) -> bool:
        """Whether snake has collied with head to the body"""
        colied = False
        #
        for body in self.body:
            if body.x == self.head.x and body.y == self.head.y:
                self.colied = True
                colied = True
                break
        #
        return colied

class Food:
    def __init__(self) -> None:
        self.respawn()
        #self.pos_x, self.pos_y = generate_food_position()
        #self.object = pygame.Rect(self.pos_x, self.pos_y, block_size, block_size)

    def update(self) -> None:
        """"""
        pygame.draw.rect(game_screen, color_red, self.object)

    def respawn(self):
        """Change food position"""
        self.pos_x, self.pos_y = generate_food_position()
        self.object = pygame.Rect(self.pos_x, self.pos_y, block_size, block_size)



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
                    snake.velocity_x = 0
                    snake.velocity_y = 1
                elif (event.key == pygame.K_UP):
                    snake.velocity_x = 0
                    snake.velocity_y = -1
                elif (event.key == pygame.K_LEFT):
                    snake.velocity_x = -1
                    snake.velocity_y = 0
                elif (event.key == pygame.K_RIGHT):
                    snake.velocity_x = 1
                    snake.velocity_y = 0

        # Redraw snake = moving
        snake.redraw()

        # Redraw screen background
        game_screen.fill(color_black)

        # Food
        food.update()

        # Draw snake 
        snake.draw_body()
        snake.draw_head()

        # Eat food => add tile to snake
        if (snake.head.x == food.pos_x and snake.head.y == food.pos_y):
            snake.grow()
            food.respawn()

        # Update screen
        pygame.display.update()   
        clock.tick(2)     
    

if __name__ == "__main__":
    game()
