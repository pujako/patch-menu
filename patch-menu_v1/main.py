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
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    selected_row_idx = 0
    selected_col_idx = 0  # 0 for the left column, 1 for the right column
    server_list = []

    while True:
        insight_menu, action_menu, exit_option = print_menu(stdscr, selected_row_idx, selected_col_idx)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            if selected_col_idx == 0:
                selected_row_idx = (selected_row_idx - 1) % (len(insight_menu) + 1)
            else:
                selected_row_idx = (selected_row_idx - 1) % (len(action_menu))
        elif key == curses.KEY_DOWN:
            if selected_col_idx == 0:
                selected_row_idx = (selected_row_idx + 1) % (len(insight_menu) + 1)
            else:
                selected_row_idx = (selected_row_idx + 1) % (len(action_menu))
        elif key == curses.KEY_LEFT:
            selected_col_idx = 0
            if selected_row_idx >= len(insight_menu):
                selected_row_idx = 0
        elif key == curses.KEY_RIGHT:
            selected_col_idx = 1
            if selected_row_idx >= len(action_menu):
                selected_row_idx = 0
        elif key == curses.KEY_ENTER or key == 10:
            if selected_col_idx == 0:
                if selected_row_idx == 0:  # Enter server list
                    server_list = get_server_details(stdscr)
                elif selected_row_idx == 1:  # List servers
                    list_servers(stdscr, server_list)
                elif selected_row_idx == 2:  # Check server uptime
                    check_server_uptime(stdscr, server_list)
                elif selected_row_idx == 3:  # Check Oracle DB Status
                    check_oracle_db_status(stdscr, server_list)
                elif selected_row_idx == 4:  # Gather server info
                    gather_server_info(stdscr, server_list)
                elif selected_row_idx == 5:  # List repo files
                    list_repo_files(stdscr, server_list)
                elif selected_row_idx == len(insight_menu):  # Exit
                    break
            else:
                if selected_row_idx == 0:  # Disable external repos
                    disable_external_repos(stdscr, server_list)
                elif selected_row_idx == 1:  # Enable external repos
                    enable_external_repos(stdscr, server_list)
                elif selected_row_idx == 2:  # Patch servers
                    patch_server(stdscr, server_list)
                elif selected_row_idx == 3:  # Reboot servers
                    bounce_server(stdscr, server_list)

        insight_menu, action_menu, exit_option = print_menu(stdscr, selected_row_idx, selected_col_idx)

    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
