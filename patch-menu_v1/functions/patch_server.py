import threading
import os
import datetime
from utils.prompt_confirmation import prompt_confirmation
from utils.run_command_on_remote import run_command_on_remote

def patch_server(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Preparing to patch the servers...\n")
    stdscr.refresh()
    confirmation = prompt_confirmation(stdscr, server_list, "patch")
    if confirmation == 'yes':
       stdscr.clear()
       stdscr.addstr(0, 0, "Patching the servers...\n")
       stdscr.refresh()
       results = []
       threads = []
       for idx, hostname in enumerate(server_list):
           y = idx + 1
           x = 0
           cmd = "yum update -y"
           thread = threading.Thread(target=run_command_on_remote, args=(stdscr, cmd, y, x, hostname, results))
           threads.append(thread)
           thread.start()

           for thread in threads:
               thread.join()

            # Write results to file with timestamp
           log_directory = 'log'
           if not os.path.exists(log_directory):
            os.makedirs(log_directory)
           timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
           filename = f'patch_results_{timestamp}.txt'
           filepath = os.path.join(log_directory, filename)
           with open(filepath, 'w') as f:
                for result in results:
                    f.write(result + '\n')

           stdscr.addstr(len(server_list) + 1, 0, f"Patching complete. Results saved to {filepath}. Press any key to return to the menu.")
           stdscr.refresh()
           stdscr.getch()

           stdscr.clear()
#           menu = print_menu(stdscr, current_row)