import curses
from datetime import datetime

def print_menu(stdscr, selected_row_idx):
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

    # Adding live system date and time under the title
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_x = w // 2 - len(now) // 2
    stdscr.addstr(title_y + 2, date_time_x, now)

    # Define the insight and action columns
    insight_menu = [
        'Enter server list', 
        'List servers', 
        'Check server uptime', 
        'Check Oracle DB Status', 
        'Gather server info', 
        'List repo files'
    ]
    
    action_menu = [
        'Disable external repos', 
        'Enable external repos', 
        'Patch servers', 
        'Reboot servers'
    ]

    # Define the headers for insight and action columns
    insight_header = "|INSIGHT|"
    action_header = "|ACTION|"

    # Calculate positions for the headers and menus
    insight_x = w // 4 - len(insight_header) // 2
    action_x = 3 * w // 4 - len(action_header) // 2
    header_y = h // 4

    # Print headers
    stdscr.addstr(header_y, insight_x, insight_header, curses.A_BOLD)
    stdscr.addstr(header_y, action_x, action_header, curses.A_BOLD)

    # Print insight menu
    for idx, row in enumerate(insight_menu):
        x = w // 4 - len(row) // 2
        y = header_y + 2 + idx
        if selected_row_idx == idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Print action menu
    for idx, row in enumerate(action_menu):
        x = 3 * w // 4 - len(row) // 2
        y = header_y + 2 + idx
        if selected_row_idx == len(insight_menu) + idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Adding Exit at the bottom
    exit_option = "Exit"
    exit_x = w // 2 - len(exit_option) // 2
    exit_y = header_y + max(len(insight_menu), len(action_menu)) + 4
    if selected_row_idx == len(insight_menu) + len(action_menu):
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(exit_y, exit_x, exit_option)
        stdscr.attroff(curses.color_pair(1))
    else:
        stdscr.addstr(exit_y, exit_x, exit_option)

    # Adding initials at the bottom centered
    initials = "pujako"
    initials_x = w // 2 - len(initials) // 2
    initials_y = h - 2  # Positioning the initials at the bottom
    stdscr.addstr(initials_y, initials_x, initials)

    stdscr.refresh()
    return insight_menu + action_menu + [exit_option]

