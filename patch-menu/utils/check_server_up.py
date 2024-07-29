from utils.ssh_utils import ssh_login


def check_server_up(hostname):
    try:
        client = ssh_login(hostname)
        client.close()
        return True
    except Exception:
        return False
