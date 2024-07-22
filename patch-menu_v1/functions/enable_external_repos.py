import threading
from utils.ssh_utils import ssh_login  # Import the ssh_login function


def enable_external_repos(stdscr, server_list):
    stdscr.clear()
    stdscr.addstr(0, 0, "Enabling external repository files in /etc/yum.repos.d/:\n")
    stdscr.refresh()

    results = []
    threads = []

    # Function to execute the command and collect results
    def run_command_and_collect_results(cmd, hostname):
        nonlocal results
        try:
            client = ssh_login(hostname)  # Use the ssh_login function
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8')
            results.append(f"{hostname}: {output.strip()}")
        except Exception as e:
            results.append(f"{hostname}: Error: {str(e)}")
        finally:
            if client:
                client.close()

    # Start threads for each server
    for idx, hostname in enumerate(server_list):
        cmd = '''
            repo_dir="/etc/yum.repos.d"
            for repo_file in "$repo_dir"/*; do
                if [ "$repo_file" != "$repo_dir/redhat.repo" ] && [[ "$repo_file" == *"-disabled" ]]; then
                    repo_filename=$(basename "$repo_file")
                    new_filename="${repo_filename%-disabled}"
                    mv "$repo_file" "$repo_dir/$new_filename"
                    echo "Restored $repo_filename to $new_filename"
                fi
            done
        '''
        thread = threading.Thread(target=run_command_and_collect_results, args=(cmd, hostname))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Display results
    y = 2
    for result in results:
        stdscr.addstr(y, 0, f"{result}\n")
        y += 1

    stdscr.addstr(y, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()
