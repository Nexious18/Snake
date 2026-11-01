import random
import curses
from collections import deque

class Snake:
    """The snake itself"""
    def __init__(self, settings):
        # Snake related settings
        self.settings = settings
        # All available directions
        self.directions = {ord('w'): ('y', -1, ord('s')), ord('a'): ('x', -1, ord('d')),
                      ord('s'): ('y', 1, ord('w')), ord('d'): ('x', 1, ord('a'))}

        # Last snakes cord, for covering it with ' ' symbol
        self.last_cord = self.settings.snake_cords[-1]



    def change_path(self, key):
        """Func for changing the current path"""
        settings = self.settings

        if key in self.directions:
            #If the path is the same then pass
            if key == settings.snake_path[2]:
                pass
            else:
                settings.snake_path = self.directions[key]


    def change_cords(self):
        """Func for changing the current cords"""
        settings = self.settings
        first_cord = self.settings.snake_cords[0]

        # getting new cord
        if settings.snake_path[0] == 'y':
            new_cord = (first_cord[0] + settings.snake_path[1], first_cord[1])
        else:
            new_cord = (first_cord[0], first_cord[1] + settings.snake_path[1])

        # checking if new_cord == apple_cord, else keep 1 more snake part
        if new_cord != settings.apple_cord:
            self.last_cord = settings.snake_cords.pop()
        else:
            settings.apple_is_eaten = True
            settings.score += 1


        y, x = new_cord
        # checking if new_cord is valid
        if new_cord in settings.snake_cords:
            return False

        if (y < settings.field_top or y > settings.field_bottom or x < settings.field_left or x > settings.field_right):
                return False

        settings.snake_cords.appendleft(new_cord)
        return True



    def draw(self):
        """Func for drawing all parts of the snake"""
        settings = self.settings

        # deleting last part of snake
        settings.screen.addstr(self.last_cord[0], self.last_cord[1], ' ')

        for i, j in settings.snake_cords:
            settings.screen.addch(i, j, '#', curses.color_pair(settings.snake_color))


class Apple:
    def __init__(self, settings):
        self.settings = settings


    def generate_apple(self):
        """Function for creating a random apple"""
        settings = self.settings

        if settings.apple_is_eaten:
            free = [(i, j)
                    for i in range(settings.field_top, settings.field_bottom + 1)
                    for j in range(settings.field_left, settings.field_right + 1)
                    if (i, j) not in settings.snake_cords]

            if free:
                settings.apple_is_eaten = False
                settings.apple_cord = random.choice(free)
                settings.screen.addch(settings.apple_cord[0], settings.apple_cord[1], settings.apple_symbol, curses.color_pair(settings.apple_color))
            else:
                settings.win = True
