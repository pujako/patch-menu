import time
import datetime
import threading
import os
from utils.prompt_confirmation import prompt_confirmation
from utils.ssh_utils import ssh_login  # Import the ssh_login function
from utils.select_servers_to_reboot import select_servers_to_reboot
from utils.check_server_up import check_server_up


def bounce_server(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Preparing to reboot the servers...\n")
    stdscr.refresh()

    selected_servers, selected_indices = select_servers_to_reboot(stdscr, server_list)
    if not selected_servers:
        stdscr.clear()
        stdscr.addstr(0, 0, "No servers selected for reboot. Press any key to return to the menu.")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.clear()
        stdscr.addstr(0, 0, "Selected servers for reboot:\n")
        for server in selected_servers:
            stdscr.addstr(1, 0, f"{server}\n")
            stdscr.refresh()

        confirmation = prompt_confirmation(stdscr, selected_servers, "reboot")
        if confirmation == 'yes':
            stdscr.clear()
            stdscr.addstr(0, 0, "Rebooting the selected servers...\n")
            stdscr.refresh()

            results = []
            threads = []

        def run_command_on_remote_bounce(stdscr, cmd, y, x, hostname, results, client=None, is_reboot=False):
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            log_directory = 'logs'
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            log_filename = f"{hostname}.bounce.{timestamp}.log"
            log_filepath = os.path.join(log_directory, log_filename)

            with open(log_filepath, 'w') as log_file:
                log_file.write(f"Command: {cmd}\n")
                log_file.write(f"Hostname: {hostname}\n\n")

                if is_reboot:
                    results.append(f"{hostname}: Rebooting...")
                    stdscr.addstr(y, x, f"{hostname}: Rebooting...\n")
                    stdscr.refresh()
                    time.sleep(20)  # Wait 20 seconds after issuing reboot command
                    while not check_server_up(hostname):
                        time.sleep(5)  # Check every 5 seconds if the server is back online

                    try:
                        client.close()
                        client = ssh_login(hostname)  # Use the ssh_login function

                        stdin, stdout, stderr = client.exec_command("uptime")
                        uptime = stdout.read().decode().strip()
                        results.append(f"{hostname}: Rebooted and back online. Uptime: {uptime}")
                        stdscr.addstr(y, x, f"{hostname}: Rebooted and back online. Uptime: {uptime}\n")
                        stdscr.refresh()

                        # Wait for 20 seconds before proceeding to the next server
                        time.sleep(20)

                        log_file.write(f"Rebooted and back online. Uptime: {uptime}\n")

                    except Exception as e:
                        results.append(f"{hostname}: Error fetching uptime - {str(e)}")
                        stdscr.addstr(y, x, f"{hostname}: Error fetching uptime - {str(e)}\n")
                        stdscr.refresh()
                        log_file.write(f"Error fetching uptime - {str(e)}\n")

                else:
                    for line in iter(stdout.readline, ""):
                        stdscr.addstr(y, x, f"{hostname}: {line.strip()}\n")
                        stdscr.refresh()
                        log_file.write(f"{line.strip()}\n")
                    results.append(f"{hostname}: Complete!")
                    log_file.write("Complete!\n")

            if client is not None:
                client.close()

        
        for idx, hostname in zip(selected_indices, selected_servers):
            y = idx + 1
            x = 0
            cmd = "shutdown -r now"
            thread = threading.Thread(target=run_command_on_remote_bounce, args=(stdscr, cmd, y, x, hostname, results, None, True))
            threads.append(thread)
            thread.start()
            time.sleep(20)  # Wait 20 seconds before proceeding to next server

        for thread in threads:
            thread.join()

        # Write results to file with timestamp
        log_directory = 'logs'
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'reboot_results_{timestamp}.txt'
        filepath = os.path.join(log_directory, filename)
        with open(filepath, 'w') as f:
            for result in results:
                f.write(result + '\n')

        stdscr.addstr(len(selected_servers) + 1, 0, f"Reboot complete on all selected servers. Results saved to {filepath}. Press any key to return to the menu.")
        stdscr.refresh()
        stdscr.getch()
