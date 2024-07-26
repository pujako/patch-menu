import curses
import time
import datetime
import threading
import os

from utils.run_command_on_remote import run_command_on_remote
from utils.prompt_confirmation import prompt_confirmation
from utils.print_menu import print_menu
from utils.select_servers_to_reboot import select_servers_to_reboot
from functions.get_server_details import get_server_details
from functions.list_servers import list_servers
from functions.list_repo_files import list_repo_files
from functions.disable_external_repos import disable_external_repos
from functions.enable_external_repos import enable_external_repos
from functions.check_server_uptime import check_server_uptime
from functions.gather_server_info import gather_server_info
from functions.patch_server import patch_server


def main(stdscr):
    # Color setup
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
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
            elif current_row == 3:  # Gather server info
                stdscr.clear()
                stdscr.addstr(0, 0, "Gathering information from the servers...\n")
                stdscr.refresh()

                results = gather_server_info(stdscr, server_list)

                stdscr.clear()
                stdscr.addstr(0, 0, "Information gathered. Results:\n")
                stdscr.refresh()

                for result in results:
                    stdscr.addstr(result + '\n')

                stdscr.addstr(len(server_list) + 1, 0, "Press any key to return to the menu.")
                stdscr.refresh()
                stdscr.getch()

                stdscr.clear()
                menu = print_menu(stdscr, current_row)
            elif current_row == 4:  # List repo files
                list_repo_files(stdscr, server_list)
            elif current_row == 5:  # Disable external repos
                disable_external_repos(stdscr, server_list)
            elif current_row == 6:  # Enable external repos
                enable_external_repos(stdscr, server_list)
            elif current_row == 7:  # Patch servers
                patch_server(stdscr, server_list)
            elif current_row == 8:  # Reboot servers
                stdscr.clear()
                stdscr.addstr(0, 0, "Preparing to reboot the servers...\n")
                stdscr.refresh()

                selected_servers, selected_indices = select_servers_to_reboot(stdscr, server_list)
                if not selected_servers:
                    stdscr.clear()
                    stdscr.addstr(0, 0, "No servers selected for reboot. Press any key to return to the menu.")
                    stdscr.refresh()
                    stdscr.getch()
                else:
                    stdscr.clear()
                    stdscr.addstr(0, 0, "Selected servers for reboot:\n")
                    for server in selected_servers:
                        stdscr.addstr(1, 0, f"{server}\n")
                    stdscr.refresh()

                    confirmation = prompt_confirmation(stdscr, selected_servers, "reboot")
                    if confirmation == 'yes':
                        stdscr.clear()
                        stdscr.addstr(0, 0, "Rebooting the selected servers...\n")
                        stdscr.refresh()

                        results = []
                        threads = []
                        for idx, hostname in zip(selected_indices, selected_servers):
                            y = idx + 1
                            x = 0
                            cmd = "reboot"
                            thread = threading.Thread(target=run_command_on_remote, args=(stdscr, cmd, y, x, hostname, results, None, True))
                            threads.append(thread)
                            thread.start()
                            time.sleep(20)  # Wait 20 seconds before proceeding to next server

                        for thread in threads:
                            thread.join()

                        # Write results to file with timestamp
                        log_directory = 'log'
                        if not os.path.exists(log_directory):
                            os.makedirs(log_directory)
                        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f'reboot_results_{timestamp}.txt'
                        filepath = os.path.join(log_directory, filename)
                        with open(filepath, 'w') as f:
                            for result in results:
                                f.write(result + '\n')

                        stdscr.addstr(len(selected_servers) + 1, 0, f"Reboot complete on all selected servers. Results saved to {filepath}. Press any key to return to the menu.")
                        stdscr.refresh()
                        stdscr.getch()

                    stdscr.clear()
                    menu = print_menu(stdscr, current_row)

            elif current_row == 9:  # Exit
                break

        menu = print_menu(stdscr, current_row)

    curses.endwin()


if __name__ == "__main__":
    curses.wrapper(main)
