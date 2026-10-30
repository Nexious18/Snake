import curses
from curses import wrapper
from game_classes import Snake, Apple
from screen_classes import *
from time import sleep

snake = [
        " ██████╗ ███╗   ██╗ █████╗ ██╗  ██╗███████╗",  # 1
        " ██╔════╝ ████╗  ██║██╔══██╗██║ ██╔╝██╔════╝",  # 2
        " ╚█████╗  ██╔██╗ ██║███████║█████╔╝ █████╗  ",  # 3
        "  ╚═══██╗ ██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝  ",  # 4
        " ██████╔╝ ██║ ╚████║██║  ██║██║  ██╗███████╗",  # 5
        " ╚═════╝  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝",  # 6
    ]

def main(screen):
    """Main function"""
    screen.timeout(150)
    curses.curs_set(0)

    init_colors()

    settings = Settings(screen, snake, 3)
    settings.stack.append(Menu(settings))

    while True:
        try:
            action = settings.stack[-1].run()
        except (IndexError, KeyError, AttributeError):
            break

        if action == 'exit':
            break
        elif action == 'back':
            settings.stack.pop()
        else:
            settings.stack.append(action)

if __name__ == '__main__':
    wrapper(main)

