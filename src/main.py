import curses
from curses import wrapper


class Settings:
    """Class for storaging parameters"""
    __slots__ = ('screen', 'max_y', 'max_x', 'snake_color', 'snake_logo', 'snake_size', 'colors')

    def __init__(self, screen, snake_color, colors, snake_logo, snake_size=5):
        self.screen = screen
        self.max_y, self.max_x = screen.getmaxyx()
        
        self.snake_color = snake_color
        self.snake_size = snake_size
        self.colors = colors
        self.snake_logo = snake_logo
        
class MainMenu:
    """Class for creating the main menu"""
    def __init__(self, settings: Settings):
        self.settings = settings
        
    def draw_menu(self):
        screen = self.settings.screen
        max_y, max_x = self.settings.max_y, self.settings.max_x
        color_dict = self.settings.colors
        snake_logo = self.settings.snake_logo
        curses.init_pair(1, color_dict['green'], color_dict['black'])

        #Buttons
        start_y = max_y//2 - len(snake_logo)
        buttons = {2: 'Play', 4: 'Settings', 6: 'Exit'}

        # Drawing Snake logo
        for i, j in enumerate(snake_logo):
            screen.addstr(start_y + i, max_x//2 - len(j)//2, j, curses.color_pair(1))

        # Drawing buttons
        for i in range(2, 7, 2):
            screen.addstr(start_y + len(snake_logo) + i, max_x//2 - len(snake_logo[0])//2, buttons[i], curses.color_pair(1))




def main(screen):
    """Main function"""

    screen.timeout(150)
    curses.curs_set(0)

    color_dict = {
        'black': curses.COLOR_BLACK,
        'red': curses.COLOR_RED,
        'green': curses.COLOR_GREEN,
        'yellow': curses.COLOR_YELLOW,
        'blue': curses.COLOR_BLUE,
        'magenta': curses.COLOR_MAGENTA,
        'cyan': curses.COLOR_CYAN,
        'white': curses.COLOR_WHITE,
    }

    snake = [
        " ██████╗ ███╗   ██╗ █████╗ ██╗  ██╗███████╗",  # 1
        " ██╔════╝ ████╗  ██║██╔══██╗██║ ██╔╝██╔════╝",  # 2
        " ╚█████╗  ██╔██╗ ██║███████║█████╔╝ █████╗  ",  # 3
        "  ╚═══██╗ ██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ",  # 4
        " ██████╔╝ ██║ ╚████║██║  ██║██║  ██╗███████╗",  # 5
        " ╚═════╝  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝",  # 6
    ]

    #Stack of screens
    screen_stack =[]

    settings = Settings(screen, curses.color_pair(1), color_dict, snake)
    menu = MainMenu(settings)

    menu.draw_menu()
    screen_stack.append(menu.draw_menu)

    while True:
        key = screen.getch()
        if key == ord('q'):
            break

if __name__ == '__main__':
    wrapper(main)

