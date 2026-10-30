from collections import deque
import curses
from curses import wrapper

COLORS = [
    curses.COLOR_BLACK,
    curses.COLOR_RED,
    curses.COLOR_GREEN,
    curses.COLOR_YELLOW,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_CYAN,
    curses.COLOR_WHITE,
]

#Func for creating all available color pairs in curses
def init_colors():
    curses.start_color()
    for i, color in enumerate(COLORS, 1):
        curses.init_pair(i, color, curses.COLOR_BLACK)


class Settings:
    """Class for storaging all data"""
    def __init__(self, screen, logo, main_color=8):
        self.screen = screen
        self.max_y, self.max_x = screen.getmaxyx()
        self.stack = [] # Stack of classes functions
        self.colors = 8 # All available menu colors

        #Menu
        self.menu_logo = logo
        self.main_color = main_color

        #Snake
        self.snake_color = self.main_color # snake's color
        self.snake_size = 5 # number of snake parts
        self.snake_cords = deque([(15, 30), # Snake parts cords, in future create a option to change start values
                      (16, 30),
                      (17, 30),
                      (18, 30),
                      (19, 30)])

        self.snake_path = ('y', -1, ord('s')) # Snake's start path

        #Apple
        self.apple_color = 2
        self.apple_symbol = '@'
        self.apple_cord = None
        self.apple_is_eaten = True

class Menu:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.options = [{'name': 'Play', 'action': None, 'position': None},
                        {'name': 'Options', 'action': None, 'position': None},
                        {'name': 'Exit', 'action': 'exit', 'position': None}]

        if self.options:
            self.crosshair_indx = 0 # current option
        else:
            self.crosshair_indx = None

    def draw_menu(self, key=None):
        """Func for drawing menu and it's options"""

        settings = self.settings
        logo_pos_y = settings.max_y // 4
        logo_pos_x = settings.max_x//2 - len(settings.menu_logo[0])//2

        settings.screen.erase()

        # Creating menu's logo
        for i, line in enumerate(settings.menu_logo):
            settings.screen.addstr(logo_pos_y+i, logo_pos_x, line, curses.color_pair(settings.main_color))

        # Positions for options buttons
        options_pos_y = logo_pos_y+len(settings.menu_logo)
        options_pos_x = logo_pos_x

        # Creating menu's options
        for option in self.options:
            options_pos_y += 2
            settings.screen.addstr(options_pos_y, options_pos_x, option['name'], curses.color_pair(settings.main_color))
            option['position'] = (options_pos_y, options_pos_x)

        # Part for crosshair
        if key == ord('w'):
            self.crosshair_indx -= 1
        elif key == ord('s'):
            self.crosshair_indx += 1

         # Drawing cursor
        indx = self.crosshair_indx % len(self.options)
        self.croshair_indx = indx
        settings.screen.addstr(self.options[indx]['position'][0], self.options[indx]['position'][1] + 15, '<<<', curses.color_pair(settings.main_color))

        # For debugging
        settings.screen.addstr(0, 0, f'{key}')

    def run(self):
        """Func for running the menu"""
        settings = self.settings

        while True:
            key = settings.screen.getch()
            self.draw_menu(key)

            # Output to main
            if key == 10:
                action = self.options[self.crosshair_indx]['action']
                return action

            elif key == 3:
                return exit




