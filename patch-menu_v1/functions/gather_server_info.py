import os
from datetime import datetime
from utils.ssh_utils import ssh_login  # Import the ssh_login function


def gather_server_info(stdscr, server_list):
    # Define the log directory
    log_directory = 'log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    results = []

    for hostname in server_list:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Gathering information from {hostname}...\n")
        stdscr.refresh()

        # Setup SSH connection
        try:
            ssh = ssh_login(hostname)  # Use the ssh_login function

            # Define commands to execute
            commands = [
                ("uname -r", "Kernel"),
                ("cat /etc/system-release", "System Release"),
                ("date", "Date"),
                ("ls -l /etc/yum.repos.d/", "Repos"),
                ("ps -ef | grep -e pmon -e LISTENER", "DB Instances"),
                ("df -h", "Disk Usage"),
                ("uptime", "Uptime"),
                ("ip a", "IP Addresses"),
                ("ps -ef", "Process List")
            ]

            # Execute each command and collect the output
            all_output = ""
            for cmd, header in commands:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                output = stdout.read().decode().strip()
                all_output += f"\n{header}:\n{'-'*len(header)}\n{output}\n"

            # Write results to file
            filename = f'{hostname}.gather_info.{timestamp}.log'
            filepath = os.path.join(log_directory, filename)
            with open(filepath, 'w') as f:
                f.write(all_output)

            results.append(f"Information for {hostname} saved to {filepath}")

        except Exception as e:
            results.append(f"Failed to gather information from {hostname}: {str(e)}")
        finally:
            ssh.close()

    return results
