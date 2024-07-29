def list_servers(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Entered servers:\n")
    for idx, server in enumerate(server_list):
        stdscr.addstr(idx + 1, 0, server)
    stdscr.addstr(len(server_list) + 1, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()
