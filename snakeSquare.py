import pygame


class Square:
    def __init__(self, x_pos, y_pos, window):
        self.state = 0
        self.x_pos = x_pos
        self.y_pos = y_pos
        pygame.draw.rect(window, (45, 68, 82), [x_pos, y_pos, 20, 20])

    def update_state(self, change, window):
        self.state = change
        if self.state == 0:  # State of 0 means that the square is empty
            pygame.draw.rect(window, (45, 68, 82), [self.x_pos, self.y_pos, 20, 20])
        if self.state == 1:  # State of 1 means it is food
            pygame.draw.rect(window, (15, 150, 130), [self.x_pos, self.y_pos, 20, 20])
        if self.state == 2:  # State of 2 means that the snake occupies the square
            pygame.draw.rect(window, (0, 255, 0), [self.x_pos, self.y_pos, 20, 20])
        pygame.display.update()
