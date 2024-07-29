import curses


def select_servers_to_reboot(stdscr, server_list):
    selected_servers = []
    selected_indices = []
    current_row = 0

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        stdscr.addstr(0, 0, "Select servers to reboot (press Enter to confirm):\n")

        for idx, server in enumerate(server_list):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                if server in selected_servers:
                    stdscr.addstr(idx + 2, 0, "[X] " + server)
                else:
                    stdscr.addstr(idx + 2, 0, "[ ] " + server)
                stdscr.attroff(curses.color_pair(1))
            else:
                if server in selected_servers:
                    stdscr.addstr(idx + 2, 0, "[X] " + server)
                else:
                    stdscr.addstr(idx + 2, 0, "[ ] " + server)

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(server_list) - 1:
            current_row += 1
        elif key == ord(' ') and server_list[current_row] not in selected_servers:
            selected_servers.append(server_list[current_row])
            selected_indices.append(current_row)
        elif key == ord(' ') and server_list[current_row] in selected_servers:
            selected_servers.remove(server_list[current_row])
            selected_indices.remove(current_row)
        elif key == curses.KEY_ENTER or key == 10:
            break

    return selected_servers, selected_indices
