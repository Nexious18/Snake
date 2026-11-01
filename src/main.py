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
    curses.curs_set(0)
    screen.timeout(125)

    init_colors()

    settings = Settings(screen, snake, 3)
    settings.stack.append(Menu(settings))

    while True:
        try:
            screen.erase()
            action = settings.stack[-1].run()
        except (IndexError, KeyError):
            break

        if action == 'exit':
            break
        elif action == 'back':
            settings.stack.pop()
        else:
            settings.stack.append(action)

if __name__ == '__main__':
    wrapper(main)

