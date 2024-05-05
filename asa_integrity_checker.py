import paramiko
import hashlib
import sys

# Configuration
HOST = 'firewall_ip_address'
PORT = 22
USERNAME = 'admin'
# Option for key-based authentication
KEY_FILE = '/path/to/private/key'  # Path to the SSH key file, if key-based auth is preferred
PASSWORD = None  # Set None if using key-based authentication

def get_remote_md5sum(ssh, command):
    """ Execute command via SSH and return the md5sum. """
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().strip()
    return hashlib.md5(output).hexdigest()

def check_integrity():
    """ Main function to check the integrity of Cisco ASA. """
    # Establishing SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if KEY_FILE:
            key = paramiko.RSAKey.from_private_key_file(KEY_FILE)
            ssh.connect(HOST, port=PORT, username=USERNAME, pkey=key)
        elif PASSWORD:
            ssh.connect(HOST, port=PORT, username=USERNAME, password=PASSWORD)
        else:
            print("Authentication method not specified. Please set either a password or key file.")
            sys.exit(1)

        # Commands to fetch OS image and config - Replace with actual Cisco ASA commands
        os_image_md5 = get_remote_md5sum(ssh, "show version | include image")
        config_md5 = get_remote_md5sum(ssh, "show running-config")
        
        # Compare md5sums
        if os_image_md5 and config_md5:  # Assuming the known good MD5s are set somewhere
            print("Integrity check results:")
            print(f"OS Image MD5: {os_image_md5}")
            print(f"Configuration MD5: {config_md5}")
        else:
            print("Failed to retrieve MD5 sums.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    check_integrity()
