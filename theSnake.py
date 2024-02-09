import numpy as np
import pygame


class Snake:
    def __init__(self):
        self.length = 3  # The current length of the snake
        self.direction = 0  # Up is 0, then going clockwise to four
        self.snake_blocks = np.empty((3, 3), dtype=np.int32)  # One row for each segment of the snake
        # One column for the row of the segment, one for the column of the segment, and one for the direction
        for x in range(3):
            self.snake_blocks[x][2] = self.direction  # Sets the direction of the segments
            self.snake_blocks[x][1] = 15 - x  # Sets the x values of the segments
            self.snake_blocks[x][0] = 15  # Sets the y values of the segments

    def move(self, window, grid, apple):
        # Grid has to be a two d array of squares from snakeSquare.py
        x_pos = self.snake_blocks[self.length-1][1]
        y_pos = self.snake_blocks[self.length-1][0]
        grid[x_pos, y_pos].update_state(0, window)
        # Above line removes the tail of the snake
        count = 0
        l = self.length - 1
        last_block = np.array([[self.snake_blocks[l][0], self.snake_blocks[l][1], self.snake_blocks[l][2]]])
        temp = self.direction
        for x in range(self.length):  # Checks how many direction changes there are
            if self.snake_blocks[x][2] != temp:
                count += 1
                temp = self.snake_blocks[x][2]
        for x in range(self.length):  # Updates the direction of the snake segments
            if x == 0:
                temp = self.direction
            break_count = 0
            if self.snake_blocks[x][2] != temp:
                temp, self.snake_blocks[x][2] = self.snake_blocks[x][2], temp
                break_count += 1
            if count == break_count:
                break  # Breaks the loop if the required number of direction changes have been performed
        for y in range(self.length):  # Updates the positions of the segments
            if self.snake_blocks[y][2] == 0:
                self.snake_blocks[y][1] += 1
            if self.snake_blocks[y][2] == 2:
                self.snake_blocks[y][1] += -1
            if self.snake_blocks[y][2] == 1:
                self.snake_blocks[y][0] += 1
            if self.snake_blocks[y][2] == 3:
                self.snake_blocks[y][0] += -1
        x_pos = self.snake_blocks[0][1]
        y_pos = self.snake_blocks[0][0]
        if self.check_collision():
            pygame.quit()
            quit()
        # Above line checks if the snake dies
        grid[x_pos, y_pos].update_state(1, window)
        # Above line creates the head of the snake
        self.check_apple(apple, grid, window, last_block)
        # Above line checks if the snake collided with the apple

    def turn(self, right):
        if right:
            self.direction = (self.direction + 1) % 4
        else:
            self.direction += -1
            if self.direction == -1:
                self.direction = 3

    def update_length(self):
        self.length += 1

    def check_apple(self, apple, grid, window, last_block):
        eat = False
        for x in range(self.length):  # Checks if the snake overlaps with the apple
            y_match = self.snake_blocks[x][0] == apple.apple_location[1]
            x_match = self.snake_blocks[x][1] == apple.apple_location[0]
            if x_match & y_match:
                eat = True
                break
        if eat:  # Updates everything if the snake eats the apple
            apple.update_location(self.snake_blocks, self.length, grid, window)
            self.extend_snake(last_block)

    def extend_snake(self, appended):  # Makes the snake appear longer if it eats
        self.snake_blocks = np.concatenate((self.snake_blocks, appended), axis=0)
        self.update_length()

    def check_collision(self):
        # First loop checks collision with the walls
        if (self.snake_blocks[0][0] > 29) | (self.snake_blocks[0][0] < 0):
            return True
        if (self.snake_blocks[0][1] > 49) | (self.snake_blocks[0][1] < 0):
            return True
        head_x = self.snake_blocks[0][1]
        head_y = self.snake_blocks[0][0]
        # Checks if the head has collided with the body at some point
        for x in range(1, self.length - 1):
            current_x = self.snake_blocks[x][1]
            current_y = self.snake_blocks[x][0]
            x_same = head_x == current_x
            y_same = head_y == current_y
            if x_same and y_same:
                return True
        return False


class Apple:
    def __init__(self):
        self.apple_location = np.empty(2)
        self.x_coord = np.random.randint(50)
        self.y_coord = np.random.randint(30)

    def update_location(self, snake_blocks, length, grid, window):
        good_loc = False
        while not good_loc:  # Finds a new location for the apple
            self.x_coord = np.random.randint(50)
            self.y_coord = np.random.randint(30)
            good_loc = True
            for x in range(length-1):  # Checks if the hypothetical apple overlaps with the snake
                if (snake_blocks[x][1] == self.x_coord) & (snake_blocks[x][0] == self.y_coord):
                    good_loc = False
                    break
        grid[self.x_coord][self.y_coord].update_state(2, window)
        self.apple_location[0] = self.x_coord
        self.apple_location[1] = self.y_coord
