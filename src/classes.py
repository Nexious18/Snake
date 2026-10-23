import random
import curses
from collections import deque

class Snake:
    __slots__ = ('size', 'color', 'cords', 'directions', 'path', 'last_cord')

    def __init__(self, color, size=5, path=('y', -1, ord('s'))):
        # Size - how many parts does the snake include
        self.size = size
        # Color of the snake
        self.color = color
        # Current snake's parts cords
        self.cords = deque([(15, 30),
                      (16, 30),
                      (17, 30),
                      (18, 30),
                      (19, 30)])

        # All available directions
        self.directions = {ord('w'): ('y', -1, ord('s')), ord('a'): ('x', -1, ord('d')),
                      ord('s'): ('y', 1, ord('w')), ord('d'): ('x', 1, ord('a'))}

        # Current path of the snake
        self.path = path
        # Last snakes cord, for covering it with ' ' symbol
        self.last_cord = self.cords[-1]



    def change_path(self, key):
        """Func for changing the current path"""
        if key in self.directions:
            if key == self.path[2]:
                pass
            else:
                self.path = self.directions[key]


    def change_cords(self, max_y, max_x, apple_cord):
        """Func for changing the current cords"""
        first_cord = self.cords[0]

        if self.path[0] == 'y':
            new_cord = (first_cord[0] + self.path[1], first_cord[1])
        else:
            new_cord = (first_cord[0], first_cord[1] + self.path[1])

        if new_cord != apple_cord:
            self.last_cord = self.cords.pop()

        if new_cord in self.cords:
            return False
        elif (new_cord[0] > max_y or new_cord[0] < 0) or (new_cord[1] > max_x or new_cord[1] < 0):
            return False
        else:
            self.cords.appendleft(new_cord)
            return True



    def draw(self, screen):
        """Func for drawing all parts of the snake"""
        screen.addstr(self.last_cord[0], self.last_cord[1], ' ')

        for i, j in self.cords:
            screen.addch(i, j, '#', self.color)

        return True


class Apple:
    __slots__ = ('cords', 'color', 'symbol', 'is_eaten')

    def __init__(self, color, symbol='@'):
        self.color = color
        self.cords = None
        self.symbol = symbol
        self.is_eaten = False

    def draw_apple(self, screen):
        '''Func for drawing a random apple'''
        screen.addch(self.cords[0], self.cords[1], '#', self.color)

    def generate_apple(self, max_y, max_x, snake_cords, screen):
        '''Function for generating a random apple location'''
        free = [(i, j)
                for i in range(max_y + 1)
                for j in range(max_x + 1)
                if (i, j) not in snake_cords]

        if not free:
            return False

        self.cords = random.choice(free)
        self.draw_apple(screen)
        self.is_eaten = False

        return True