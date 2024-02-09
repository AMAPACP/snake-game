import pygame
import snakeSquare as snSq
import numpy as np
import theSnake as Snk
import time


def define_squares(window):
    blocks = np.empty((50, 30), dtype=snSq.Square)  # Where the states of all the blocks are stored
    for y in range(30):
        for x in range(50):
            current_square = snSq.Square(21 * x + 1, 21 * y + 1, window)
            blocks[x, y] = current_square
    return blocks


def update_score(window, length, font):
    pygame.draw.rect(window, (0, 0, 0), [0, 632, 500, 100])
    score = (length - 3) * 10
    current_score = font.render("Score: " + str(score), True, (255, 255, 255))
    # Above line creates the text to be put onto the screen
    window.blit(current_score, (50, 671))
    # Above line actually puts the text onto the screen


def initialize_high_score(file, font, window):
    with open(file) as f:
        high_score = f.read()
    score = font.render("High Score: " + str(high_score), True, (255, 255, 255))
    window.blit(score, (600, 671))


def update_high_score(file, length, font, window):
    score = (length - 3) * 10
    with open(file) as f:
        old_score = f.read()
    old_score = int(old_score)
    if old_score < score:
        pygame.draw.rect(window, (0, 0, 0), [600, 632, 400, 98])
        high_score = font.render("High Score: " + str(score), True, (255, 255, 255))
        with open(file, "r+") as f:
            f.truncate(0)
            f.write(str(score))
        window.blit(high_score, (600, 671))


def print_hi():
    hs_loc = "/Users/seanhayes/PycharmProjects/messingAround/venv/high_score.txt"
    pygame.init()  # Needed to use pygame functionality
    font = pygame.font.Font("freesansbold.ttf", 32)  # Creates a font object for us to use
    dis = pygame.display.set_mode((1051, 731))  # Makes the display
    pygame.display.set_caption("Snake")  # Makes the window title snake
    pygame.display.update()
    the_squares = define_squares(dis)  # Makes the squares and their objects
    pygame.display.update()
    initialize_high_score(hs_loc, font, dis)
    the_snake = Snk.Snake()  # Initializes the snake object
    new_apple = Snk.Apple()  # Initializes the apple object
    new_apple.update_location(the_snake.snake_blocks, the_snake.length, the_squares, dis)
    while True:
        the_snake.move(dis, the_squares, new_apple)
        update_score(dis, the_snake.length, font)
        update_high_score(hs_loc, the_snake.length, font, dis)
        for event in pygame.event.get():  # Gets the key presses of the user
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT:
                    the_snake.turn(False)
                if event.key == pygame.K_RIGHT:
                    the_snake.turn(True)
        time.sleep(0.09)


if __name__ == '__main__':
    print_hi()
