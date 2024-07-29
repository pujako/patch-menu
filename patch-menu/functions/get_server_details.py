import curses


def get_server_details(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter the target server IPs or hostnames (one per line, leave empty line to finish):\n")
    server_list = []
    while True:
        hostname = stdscr.getstr().decode('utf-8').strip()
        if not hostname:
            break
        server_list.append(hostname)
    curses.noecho()
    return server_list
