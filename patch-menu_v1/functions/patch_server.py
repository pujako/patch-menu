import threading
import os
import datetime
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

    # Function to patch server remotely
    def run_command_and_patch(cmd, hostname):
        nonlocal results
        try:
            client = ssh_login(hostname)  # Use the ssh_login function
            stdin, stdout, stderr = client.exec_command(cmd)
            Patching = stdout.read().decode().strip()
            results.append(f"{hostname}: Patching stat: {Patching}")
        except Exception as e:
            results.append(f"{hostname}: Error fetching patch stat - {str(e)}")
        finally:
            if client:
                client.close()
    
    # Start threads for each server
    for hostname in server_list:
        cmd = "yum update -y"
        thread = threading.Thread(target=run_command_and_patch, args=(cmd, hostname))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
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
