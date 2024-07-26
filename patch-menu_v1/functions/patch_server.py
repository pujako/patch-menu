import threading
import datetime
import paramiko
import os
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

    def run_command_on_remote(stdscr, cmd, y, x, hostname, results, client=None, is_reboot=False):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        log_directory = 'log'
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        log_filename = f"{hostname}.patch.{timestamp}.log"
        log_filepath = os.path.join(log_directory, log_filename)

        if client is None:
            try:
                client = ssh_login(hostname)  # Use the ssh_login function
            except paramiko.ssh_exception.AuthenticationException as e:
                results.append(f"{hostname}: Authentication failed - {str(e)}")
                client.close()
                return
            except paramiko.ssh_exception.SSHException as e:
                results.append(f"{hostname}: SSH session failed to establish - {str(e)}")
                client.close()
                return
            except Exception as e:
                results.append(f"{hostname}: Connection failed - {str(e)}")
            client.close()
            return

        stdscr.addstr(y, x, f"{hostname}: {cmd}\n")
        stdscr.refresh()

        with open(log_filepath, 'w') as log_file:
            log_file.write(f"Command: {cmd}\n")
            log_file.write(f"Hostname: {hostname}\n\n")

        for idx, hostname in enumerate(server_list):
            y = idx + 1
            x = 0
            cmd = "yum update -y"
            thread = threading.Thread(target=run_command_on_remote, args=(stdscr, cmd, y, x, hostname, results))
            threads.append(thread)
            thread.start()

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
