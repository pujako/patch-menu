# Patch Menu

![image](https://github.com/user-attachments/assets/fdd79c56-e307-4e29-af37-fc05792d0f5f)




`patch-menu` is a Python-based command-line tool designed for managing Linux patches and system maintenance. It provides a text-based user interface (TUI) for various administrative tasks, including checking server uptime, listing repository files, and applying patches.

## Features

- **Server Management**: Enter and manage server lists.
- **System Checks**: View server uptime, list repository files, and check system resources.
- **Patch Management**: Perform system updates on multiple servers.
- **Reboot Management**: Reboot selected servers and manage reboot status.
- **Logging**: Save command outputs and results to log files.

## Installation

To install `patch-menu`, follow these steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/pujako/patch-menu.git
    cd patch-menu
    ```

2. **Install Dependencies**:

    It’s recommended to use a virtual environment. First, create and activate a virtual environment:

    ```bash
    python -m venv myenv
    source myenv/bin/activate
    ```

    Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Installation
I am working to package it - maybe I lied ;0

## Usage
Update your ssh private key path in the utils/ssh_utils.py

```bash
key_filename = '<rsa path goes here>' 
```

Start the application:

```bash
cd patch-menu/patch-menu_v1
pyhton main.py
```

## Menu Options

- **Enter Server List**: Add servers to the list for management.
- **List Servers**: Display the current list of servers.
- **Check Server Uptime**: View the uptime of the listed servers.
- **Check Oracle DB Status**: View the Oracle DB status of the listed servers.
- **Gather server info**: Record and save info for each server as such system selease, DB instances, disk usage, uptime, IP addresses and process list.
- **List Repo Files**: List repository files on the servers.
- **Disable External Repos**: Temporarily disable external repositories.
- **Enable External Repos**: Re-enable external repositories.
- **Patch Servers**: Apply system updates to the listed servers.
- **Reboot Servers**: Reboot selected servers.
- **Exit**: Exit the application.

## Logs

Logs are saved in the `log` directory within the current working directory. Each log file is timestamped and named according to the action performed (e.g., `patch_results_<timestamp>.txt`).

## Development

To contribute to the development of `patch-menu`, you can:

1. **Fork the Repository** on GitHub.
2. **Make Changes** to the codebase.
3. **Submit a Pull Request** for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [arrazzaq.zahari@gmail.com](mailto:arrazzaq.zahari@gmail.com).
