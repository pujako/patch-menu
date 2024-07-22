import curses


def prompt_confirmation(stdscr, server_list, action_name):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, f"Preparing to {action_name} the servers...\n")
    stdscr.addstr(2, 0, "Server list:\n")
    for idx, server in enumerate(server_list):
        stdscr.addstr(idx + 3, 0, f"{server}\n")
    stdscr.addstr(len(server_list) + 4, 0, f"Do you want to proceed with the {action_name}? (yes/no): ")
    stdscr.refresh()
    confirmation = stdscr.getstr().decode('utf-8').lower()
    curses.noecho()
    return confirmation
