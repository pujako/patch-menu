import curses

from utils.print_menu import print_menu
from functions.get_server_details import get_server_details
from functions.list_servers import list_servers
from functions.list_repo_files import list_repo_files
from functions.disable_external_repos import disable_external_repos
from functions.enable_external_repos import enable_external_repos
from functions.check_server_uptime import check_server_uptime
from functions.gather_server_info import gather_server_info
from functions.patch_server import patch_server
from functions.bounce_server import bounce_server
from functions.check_oracle_db_status import check_oracle_db_status


def main(stdscr):
    # Color setup
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE) # Highlight color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK) # Title color
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Clock color
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Menu color
    current_row = 0
    server_list = []

    while True:
        menu = print_menu(stdscr, current_row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key == 10:
            if current_row == 0:  # Enter server list
                server_list = get_server_details(stdscr)
            elif current_row == 1:  # List servers
                list_servers(stdscr, server_list)
            elif current_row == 2:  # Check server uptime
                check_server_uptime(stdscr, server_list)
            elif current_row == 3:  # Check Oracle DB Status
                check_oracle_db_status(stdscr, server_list)
            elif current_row == 4:  # Gather server info
                gather_server_info (stdscr, server_list)
            elif current_row == 5:  # List repo files
                list_repo_files(stdscr, server_list)
            elif current_row == 6:  # Disable external repos
                disable_external_repos(stdscr, server_list)
            elif current_row == 7:  # Enable external repos
                enable_external_repos(stdscr, server_list)
            elif current_row == 8:  # Patch servers
                patch_server(stdscr, server_list)
            elif current_row == 9:  # Reboot servers
                bounce_server(stdscr, server_list)
            elif current_row == 10:  # Exit
                break

        menu = print_menu(stdscr, current_row)

    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
