# functions/patch_server.py

import threading
import datetime
import os
import curses
from utils.prompt_confirmation import prompt_confirmation
from utils.ssh_utils import ssh_login  # Import the ssh_login function

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

        def run_command_on_remote_patch(stdscr, cmd, y, x, hostname, results):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            # Get the directory of the main.py script
            main_py_path = os.path.abspath(__file__)  # Path to this script
            main_dir = os.path.dirname(main_py_path)  # Directory of this script
            log_directory = os.path.join(main_dir, 'logs')
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            log_filename = f"{hostname}.patch.{timestamp}.log"
            log_filepath = os.path.join(log_directory, log_filename)

            client = None
            try:
                client = ssh_login(hostname)  # Use the ssh_login function
                stdin, stdout, stderr = client.exec_command(cmd)

                with open(log_filepath, 'w') as log_file:
                    log_file.write(f"Command: {cmd}\n")
                    log_file.write(f"Hostname: {hostname}\n\n")
                    log_file.write("Standard Output:\n")
                    
                    # Reading stdout line by line
                    while True:
                        line = stdout.readline()
                        if not line:
                            break
                        stdscr.addstr(y, x, f"{hostname}: {line}")
                        stdscr.refresh()
                        log_file.write(f"{line}")

                    log_file.write("\nStandard Error:\n")
                    stderr_lines = stderr.read().decode().splitlines()
                    for line in stderr_lines:
                        stdscr.addstr(y, x, f"{hostname}: {line}\n")
                        stdscr.refresh()
                        log_file.write(f"{line}\n")
                    
                results.append(f"{hostname}: Patch completed successfully.")
            except Exception as e:
                results.append(f"{hostname}: Error during patch - {str(e)}")
            finally:
                if client:
                    client.close()
                results.append(f"{hostname}: Complete!")

        for idx, hostname in enumerate(server_list):
            y = idx + 1
            x = 0
            cmd = "yum update -y"
            thread = threading.Thread(target=run_command_on_remote_patch, args=(stdscr, cmd, y, x, hostname, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Write results to file with timestamp
        log_directory = 'logs'
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
