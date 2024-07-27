import curses
from datetime import datetime

def print_menu(stdscr, selected_row_idx, selected_col_idx):
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
        if selected_row_idx == idx and selected_col_idx == 0:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Print action menu
    for idx, row in enumerate(action_menu):
        x = 3 * w // 4 - len(row) // 2
        y = header_y + 2 + idx
        if selected_row_idx == idx and selected_col_idx == 1:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    # Adding Exit at the bottom
    exit_option = "Exit"
    exit_x = w // 2 - len(exit_option) // 2
    exit_y = header_y + max(len(insight_menu), len(action_menu)) + 4
    if selected_row_idx == len(insight_menu) + len(action_menu) and selected_col_idx == 0:
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
    return insight_menu, action_menu, exit_option

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)

    selected_row_idx = 0
    selected_col_idx = 0  # 0 for left column, 1 for right column

    insight_menu, action_menu, exit_option = print_menu(stdscr, selected_row_idx, selected_col_idx)

    while True:
        key = stdscr.getch()

        if key == curses.KEY_UP:
            if selected_col_idx == 0:
                selected_row_idx = (selected_row_idx - 1) % (len(insight_menu) + len(action_menu) + 1)
            else:
                selected_row_idx = (selected_row_idx - 1) % len(action_menu)
        elif key == curses.KEY_DOWN:
            if selected_col_idx == 0:
                selected_row_idx = (selected_row_idx + 1) % (len(insight_menu) + len(action_menu) + 1)
            else:
                selected_row_idx = (selected_row_idx + 1) % len(action_menu)
        elif key == curses.KEY_LEFT:
            selected_col_idx = 0
            if selected_row_idx >= len(insight_menu):
                selected_row_idx = 0
        elif key == curses.KEY_RIGHT:
            selected_col_idx = 1
            if selected_row_idx >= len(action_menu):
                selected_row_idx = 0
        elif key == ord('\n'):
            if selected_col_idx == 0:
                if selected_row_idx < len(insight_menu):
                    stdscr.addstr(0, 0, f"Selected {insight_menu[selected_row_idx]}")
                    stdscr.refresh()
                else:
                    break
            else:
                if selected_row_idx < len(action_menu):
                    stdscr.addstr(0, 0, f"Selected {action_menu[selected_row_idx]}")
                    stdscr.refresh()
                else:
                    break

        insight_menu, action_menu, exit_option = print_menu(stdscr, selected_row_idx, selected_col_idx)

curses.wrapper(main)
