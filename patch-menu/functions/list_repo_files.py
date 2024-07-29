import threading
from utils.ssh_utils import ssh_login  # Import the ssh_login function


def list_repo_files(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Listing repository files in /etc/yum.repos.d/:\n")
    stdscr.refresh()

    results = {}
    threads = []

    # Function to run the command on remote server and collect results
    def run_command_on_remote_and_collect(cmd, hostname):
        try:
            client = ssh_login(hostname)  # Use the ssh_login function
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            results[hostname] = output.splitlines()
        except Exception as e:
            results[hostname] = [f"Error: {str(e)}"]
        finally:
            if client:
                client.close()

    # Start threads for each server
    for hostname in server_list:
        cmd = "ls -l /etc/yum.repos.d/ | egrep '.repo$'"
        thread = threading.Thread(target=run_command_on_remote_and_collect, args=(cmd, hostname))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Display results
    y = len(server_list) + 2
    for hostname in server_list:
        stdscr.addstr(y, 0, f"{hostname}:\n")
        y += 1
        if hostname in results:
            for line in results[hostname]:
                stdscr.addstr(y, 0, f"{line}\n")
                y += 1
        stdscr.addstr(y, 0, f"{hostname}: Complete!\n")
        y += 1

    stdscr.addstr(y, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()
