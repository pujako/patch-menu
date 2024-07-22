# utils/ssh_utils.py
import paramiko


def ssh_login(hostname, username='root', key_filename='/home/pujako/.ssh/id_rsa'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname, username=username, key_filename=key_filename)
        return client
    except Exception as e:
        raise e
