def prompt_reboot_mode(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Do you want to reboot servers sequentially or parallelly?\n")
    stdscr.addstr(1, 0, "Press 's' for sequential or 'p' for parallel, 'e' to exit: ")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('s'):
            return 'sequential'
        elif key == ord('p'):
            return 'parallel'
        elif key == ord('e'):
            return 'exit'        
        else:
            stdscr.addstr(2, 0, "Invalid input. Press 's' for sequential or 'p' for parallel: ")
            stdscr.refresh()
