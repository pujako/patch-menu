import threading
from utils.ssh_utils import ssh_login  # Import the ssh_login function

def check_oracle_db_status(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Checking Oracle DB status on servers:\n")
    stdscr.refresh()

    results = []
    threads = []

    # Function to check Oracle DB status on remote server and collect results
    def run_command_and_collect_results(cmd, hostname):
        nonlocal results
        try:
            client = ssh_login(hostname)  # Use the ssh_login function
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if error:
                results.append(f"{hostname}: Error checking Oracle DB status - {error}")
            elif output:
                results.append(f"{hostname}: Oracle DB status:\n{output}")
            else:
                results.append(f"{hostname}: Oracle DB and Listener not found.")
        except Exception as e:
            results.append(f"{hostname}: Exception occurred - {str(e)}")
        finally:
            if client:
                client.close()

    # Start threads for each server
    for hostname in server_list:
        cmd = "ps -ef | egrep 'pmon|LISTENER' | egrep -v grep"
        thread = threading.Thread(target=run_command_and_collect_results, args=(cmd, hostname))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Display results
    y = len(server_list) + 2
    for result in results:
        stdscr.addstr(y, 0, f"{result}\n")
        y += 1

    stdscr.addstr(y, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()
