from classes import Snake, Apple
import curses
from curses import wrapper
from time import sleep


def main(screen, color='green'):
    """Main function for game"""

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

    screen.timeout(150)
    curses.curs_set(0)

    curses.init_pair(1, color_dict[color], curses.COLOR_BLACK)
    curses.init_pair(2, color_dict['red'], curses.COLOR_BLACK)
    curses.init_pair(3, color_dict['yellow'], curses.COLOR_BLACK)

    # Snake
    snake = Snake(curses.color_pair(1))

    max_y, max_x = screen.getmaxyx()

    # Apple
    apple = Apple(curses.color_pair(2))
    apple.generate_apple(max_y, max_x, snake.cords, screen)

    #Game play
    while True:
        # Getting pressed key
        key = screen.getch()
        if key == ord('q'):
            break

        # Checking if apple is eaten
        if apple.is_eaten:
            if not apple.generate_apple(max_y, max_x, snake.cords, screen):
                # You won screen
                screen.erase()
                screen.addstr(max_y, max_x, 'YOU WON', curses.color_pair(3))
                screen.refresh()
                sleep(1.5)
                break

        # Getting new snake cords
        snake.change_path(key)
        if not snake.change_cords(max_y, max_x, apple.cords):
            # Game Over screen

            screen.erase()
            screen.addstr(max_y // 2, max_x // 2, 'GAMEOVER', curses.color_pair(2))
            screen.refresh()
            sleep(1.5)
            break

        if snake.cords[0] == apple.cords:
            apple.is_eaten = True

        snake.draw(screen)
        screen.refresh()




if __name__ == '__main__':
    wrapper(main)