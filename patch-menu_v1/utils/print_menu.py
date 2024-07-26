import curses
import time
from datetime import datetime

def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # Adding the title
    title = "NES Linux Patch Menu v1.1"
    title_x = w // 2 - len(title) // 2
    title_y = 1  # Positioning the title at the top
    stdscr.attron(curses.color_pair(2))  # Assuming color_pair(2) is for the title
    stdscr.addstr(title_y, title_x, title)
    stdscr.attroff(curses.color_pair(2))

    # Create a border around the title
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(title_y - 1, title_x - 2, "+", curses.A_BOLD)
    stdscr.addstr(title_y - 1, title_x - 1, "-" * len(title), curses.A_BOLD)
    stdscr.addstr(title_y - 1, title_x + len(title), "+", curses.A_BOLD)
    stdscr.addstr(title_y + 1, title_x - 2, "+", curses.A_BOLD)
    stdscr.addstr(title_y + 1, title_x + len(title), "+", curses.A_BOLD)
    stdscr.addstr(title_y, title_x - 2, "|", curses.A_BOLD)
    stdscr.addstr(title_y, title_x + len(title), "|", curses.A_BOLD)
    stdscr.addstr(title_y + 1, title_x - 1, "-" * len(title), curses.A_BOLD)
    stdscr.attroff(curses.color_pair(2))

    # Defining the menu items
    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx + 4  # +4 to account for the title and date/time
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Adding initials at the bottom centered
    initials = "pujako"
    initials_x = w // 2 - len(initials) // 2
    initials_y = h - 2  # Positioning the initials at the bottom
    stdscr.addstr(initials_y, initials_x, initials)

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    selected_row_idx = 0

    menu = ['Enter server list', 'List servers', 'Check server uptime', 'Gather server info', 'List repo files', 'Disable external repos', 'Enable external repos', 'Patch servers', 'Reboot servers', 'Exit']

    while True:
        stdscr.clear()
        print_menu(stdscr, selected_row_idx, menu)

        # Adding live system date and time under the title
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        h, w = stdscr.getmaxyx()
        date_time_x = w // 2 - len(now) // 2
        stdscr.addstr(3, date_time_x, now)

        stdscr.refresh()
        time.sleep(1)  # Refresh every second

        key = stdscr.getch()

        if key == curses.KEY_UP and selected_row_idx > 0:
            selected_row_idx -= 1
        elif key == curses.KEY_DOWN and selected_row_idx < len(menu) - 1:
            selected_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # Handle the selected menu option here
            if menu[selected_row_idx] == 'Exit':
                break

if __name__ == "__main__":
    curses.wrapper(main)
