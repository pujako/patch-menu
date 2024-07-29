import threading
from utils.ssh_utils import ssh_login  # Import the ssh_login function

def check_oracle_db_status(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Checking Oracle DB status on servers:\n")
    stdscr.refresh()

    results = []
    threads = []

    # Function to check Oracle DB status on remote server and collect results
    def run_command_and_collect_results(hostname):
        nonlocal results
        try:
            client = ssh_login(hostname)  # Use the ssh_login function
            command = "ps -ef | egrep 'pmon|LISTENER' | egrep -v grep"
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            client.close()
            
            if error:
                result = f"{hostname}: Error checking Oracle DB status - {error}"
            elif output:
                result = f"{hostname}: Oracle DB status:\n{output}"
            else:
                result = f"{hostname}: Oracle DB and Listener not found."
                
            results.append(result)
        except Exception as e:
            results.append(f"{hostname}: Exception occurred - {str(e)}")

    # Start threads for each server
    for hostname in server_list:
        thread = threading.Thread(target=run_command_and_collect_results, args=(hostname,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Display results
    y = 1
    for result in results:
        stdscr.addstr(y, 0, f"{result}\n")
        y += result.count('\n') + 1  # Adjust y for the number of lines in the result

    stdscr.addstr(y, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()
