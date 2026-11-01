from collections import deque
import curses
from curses import wrapper
from game_classes import Apple, Snake
from time import sleep

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
        self.colors = (1, 2, 3, 4, 5, 6, 7, 8) # All available menu colors

        #Menu
        self.menu_logo = logo
        self.main_color = main_color

        #GameScreen
        self.score = 0

        self.border_sym = '#'
        self.border_color = 8
        self.field_h = 15
        self.field_w = 25

        self.field_top = None
        self.field_left = None
        self.field_bottom = None
        self.field_right = None

        #Snake
        self.snake_color = 3 # snake's color
        self.snake_size = 5 # number of snake parts
        self.snake_cords = deque([(15, 30), # Snake parts cords, in future create a option to change start values
                      (16, 30),
                      (17, 30),
                      (18, 30),
                      (19, 30)])

        self.snake_path = ('y', -1, ord('s')) # Snake's start path
        self.win = False

        #Apple
        self.apple_color = 2
        self.apple_symbol = '@'
        self.apple_cord = None
        self.apple_is_eaten = True



class GameScreen:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.snake = Snake(settings) # snake class
        self.apple = Apple(settings) # apple class


    def get_game_borders(self):
        """Func for creating borders for the game"""
        settings = self.settings

        max_y, max_x = settings.max_y, settings.max_x
        field_h, field_w = settings.field_h, settings.field_w

        top = (max_y - field_h) // 2
        left = (max_x - field_w) // 2

        settings.field_top = top + 1
        settings.field_left = left + 1
        settings.field_bottom = top + field_h - 2
        settings.field_right = left + field_w - 2

        color = curses.color_pair(settings.border_color)

        for x in range(left, left + field_w):
            settings.screen.addstr(top, x, settings.border_sym, curses.color_pair(color))
            settings.screen.addstr(top + field_h - 1, x, settings.border_sym, curses.color_pair(color))
        for y in range(top, top + field_h):
            settings.screen.addstr(y, left, settings.border_sym, curses.color_pair(color))
            settings.screen.addstr(y, left + field_w - 1, settings.border_sym, curses.color_pair(color))


    def reset_apple_snake_values(self):
        """Func for reseting the apple and snake values"""
        settings = self.settings
        center_y = (settings.field_top + settings.field_bottom) // 2
        center_x = (settings.field_left + settings.field_right) // 2

        #Score
        settings.score = 0

        #Apple
        settings.apple_cord = None
        settings.apple_is_eaten = True

        #Snake
        settings.snake_size = 5

        settings.snake_cords = deque([])
        for i in range(settings.snake_size):
            settings.snake_cords.append((center_y+i, center_x))

        settings.snake_path = ('y', -1, ord('s'))

    def lose_screen(self):
        """Func for drawing the lose screen"""
        settings = self.settings
        max_y, max_x = settings.max_y, settings.max_x

        settings.screen.erase()
        settings.screen.addstr(max_y//2, max_x//2, 'GAME OVER', curses.color_pair(2))
        settings.screen.refresh()
        sleep(2)

    def win_screen(self):
        """Func for drawing the win screen"""
        settings = self.settings
        max_y, max_x = settings.max_y, settings.max_x

        settings.screen.erase()
        settings.screen.addstr(max_y // 2, max_x // 2, 'YOU WIN', curses.color_pair(4))
        settings.screen.refresh()
        sleep(2)

    def run(self):
        """Func for running the game"""
        settings = self.settings
        snake = self.snake
        apple = self.apple

        self.get_game_borders()
        self.reset_apple_snake_values()

        text = 'Press "q" to quit'
        settings.screen.addstr(0, settings.max_x//2-len(text)//2, text)

        while True:
            key = settings.screen.getch()

            if key == ord('q'):
                return 'back'

            #Checking if snake occupies whole field
            if not settings.win:
                #Drawing score
                settings.screen.addstr(0, 0, f'Score: {settings.score}')

                # Generating apple
                apple.generate_apple()

                # getting key from user to change pass
                snake.change_path(key)
                # checking snake's status
                if snake.change_cords():
                    pass
                else:
                    self.lose_screen()
                    return 'back'

                snake.draw()
            else:
                #If snake occupies whole field
                self.win_screen()
                return 'back'


class Options:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.options = ({'name': 'Menu color:',   'action': self.settings.main_color,  'position': None, 'settings_name': 'main_color'},
                        {'name': 'Snake color:',  'action': self.settings.snake_color, 'position': None, 'settings_name': 'snake_color'},
                        {'name': 'Apples color:', 'action': self.settings.apple_color, 'position': None, 'settings_name': 'apple_color'},
                        {'name': 'Back',          'action': 'back',                    'position': None, 'settings_name': None})
        self.crosshair_indx = 0

        #Logo positions
        self.logo_pos_y = settings.max_y // 4
        self.logo_pos_x = settings.max_x // 2 - len(self.settings.menu_logo[0]) // 2



    def draw_options(self):
        """Function for drawing options menu"""
        settings = self.settings

        # Creating menu's logo
        for i, line in enumerate(settings.menu_logo):
            settings.screen.addstr(self.logo_pos_y + i, self.logo_pos_x, line, curses.color_pair(settings.main_color))

        #Options positions
        options_pos_y = self.logo_pos_y + len(self.settings.menu_logo)
        options_pos_x = self.logo_pos_x

        #Option's variant x pos
        variants_x = max(len(self.options[i]['name']) for i in range(len(self.options))) + options_pos_x + 2


        # Creating menu's options
        for option in self.options:
            #Creating options buttons
            options_pos_y += 2
            settings.screen.addstr(options_pos_y, options_pos_x, option['name'], curses.color_pair(settings.main_color))
            option['position'] = (options_pos_y, options_pos_x)

            #Creating options variants
            if option['name'] != 'Back':
                settings.screen.addstr(options_pos_y, variants_x, f'{option['action']}', curses.color_pair(settings.main_color))


    def draw_crosshair(self, key):
        """Func for drawing crosshair"""
        settings = self.settings

        #Checking crosshair's directions
        if key == ord('w'):
            self.crosshair_indx -= 1
        elif key == ord('s'):
            self.crosshair_indx += 1

        #Drawing cursor
        indx = self.crosshair_indx % len(self.options)
        self.crosshair_indx = indx
        settings.screen.addstr(self.options[indx]['position'][0], self.options[indx]['position'][1] + 20, '<<<', curses.color_pair(settings.main_color))

        #For debugging
        settings.screen.addstr(0, 0, f'{key}')

    def draw_variants(self, key):
        """Func for drawing option's variants"""
        settings = self.settings
        crosshair_indx = self.crosshair_indx
        action = self.options[crosshair_indx]['action']  # Current option's value

        if action != 'back':
            color_indx = settings.colors.index(action) #Index of current option's value
            variable_in_settings = self.options[crosshair_indx]['settings_name'] #Name of variable in settings to change

            if key in (ord('a'), ord('d')):
                if key == ord('a'):
                    color_indx = (color_indx - 1) % len(settings.colors)
                elif key == ord('d'):
                    color_indx = (color_indx + 1) % len(settings.colors)

                self.options[crosshair_indx]['action'] = settings.colors[color_indx]
                setattr(settings, variable_in_settings, settings.colors[color_indx])

    def reset_options_values(self):
        """When screen opens resets necessary values for options"""
        self.crosshair_indx = 0
        self.options = ({'name': 'Menu color:', 'action': self.settings.main_color, 'position': None,
                         'settings_name': 'main_color'},
                        {'name': 'Snake color:', 'action': self.settings.snake_color, 'position': None,
                         'settings_name': 'snake_color'},
                        {'name': 'Apples color:', 'action': self.settings.apple_color, 'position': None,
                         'settings_name': 'apple_color'},
                        {'name': 'Back', 'action': 'back', 'position': None, 'settings_name': None})


    def run(self):
        settings = self.settings
        self.reset_options_values()

        while True:
            key = settings.screen.getch()
            settings.screen.erase()

            self.draw_options()
            self.draw_crosshair(key)
            self.draw_variants(key)
            action = self.options[self.crosshair_indx]['action']

            if key == ord('q'):
                return 'back'

            if action == 'back' and key == 10:
                return action



class Menu:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.options = [{'name': 'Play', 'action': GameScreen(settings), 'position': None},
                        {'name': 'Options', 'action': Options(settings), 'position': None},
                        {'name': 'Exit', 'action': 'exit', 'position': None}]

        if self.options:
            self.crosshair_indx = 0 # current option
        else:
            self.crosshair_indx = None

        self.logo_pos_y = settings.max_y // 4
        self.logo_pos_x = settings.max_x//2 - len(settings.menu_logo[0])//2


    def draw_menu(self):
        """Func for drawing menu and it's options"""
        settings = self.settings

        # Creating menu's logo
        for i, line in enumerate(settings.menu_logo):
            settings.screen.addstr(self.logo_pos_y+i, self.logo_pos_x, line, curses.color_pair(settings.main_color))

        # Positions for options buttons
        options_pos_y = self.logo_pos_y+len(settings.menu_logo)
        options_pos_x = self.logo_pos_x

        # Creating menu's options
        for option in self.options:
            options_pos_y += 2
            settings.screen.addstr(options_pos_y, options_pos_x, option['name'], curses.color_pair(settings.main_color))
            option['position'] = (options_pos_y, options_pos_x)


    def draw_crosshair(self, key):
        """Func for drawing crosshair"""
        settings = self.settings

        # Part for crosshair
        if key == ord('w'):
            self.crosshair_indx -= 1
        elif key == ord('s'):
            self.crosshair_indx += 1

        # Drawing cursor
        indx = self.crosshair_indx % len(self.options)
        self.crosshair_indx = indx
        settings.screen.addstr(self.options[indx]['position'][0], self.options[indx]['position'][1] + 15, '<<<', curses.color_pair(settings.main_color))

        #For debugging
        settings.screen.addstr(0, 0, f'{key}')


    def reset_menu_values(self):
        self.crosshair_indx = 0

    def run(self):
        """Func for running the menu"""
        settings = self.settings
        self.reset_menu_values()

        while True:
            key = settings.screen.getch()
            settings.screen.erase()

            self.draw_menu()
            self.draw_crosshair(key)

            # Output to main
            if key == 10:
                action = self.options[self.crosshair_indx]['action']
                return action

            elif key == ord('q'):
                return exit




