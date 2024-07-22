import paramiko
import time
import os
import datetime
from utils.check_server_up import check_server_up
from utils.ssh_utils import ssh_login  # Import the ssh_login function


def run_command_on_remote(stdscr, cmd, y, x, hostname, results, client=None, is_reboot=False):
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_directory = 'log'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_filename = f"{hostname}.yumupdate.{timestamp}.log"
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

    stdin, stdout, stderr = client.exec_command(cmd)

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
