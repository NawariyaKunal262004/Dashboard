import streamlit as st
import time

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    st.warning("⚠️ Paramiko not installed. SSH functionality will be limited. Install with: `pip install paramiko`")

def run_remote_command(hostname, username, password, command, port=22):
    """
    Run a command on a remote server via SSH
    
    Args:
        hostname (str): Server IP or hostname
        username (str): SSH username
        password (str): SSH password
        command (str): Command to execute
        port (int): SSH port (default: 22)
    
    Returns:
        tuple: (success: bool, output: str)
    """
    if not PARAMIKO_AVAILABLE:
        return False, "Paramiko not installed. Please install it with: pip install paramiko"
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to server
        ssh.connect(hostname, port=port, username=username, password=password, timeout=10)
        
        # Execute command
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Get output
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        # Close connection
        ssh.close()
        
        if error:
            return False, f"Error: {error}"
        else:
            return True, output
            
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

def start_apache_server(hostname, username, password, port=22):
    """
    Start Apache server on remote machine
    
    Args:
        hostname (str): Server IP or hostname
        username (str): SSH username
        password (str): SSH password
        port (int): SSH port (default: 22)
    
    Returns:
        tuple: (success: bool, message: str)
    """
    if not PARAMIKO_AVAILABLE:
        return False, "Paramiko not installed. Please install it with: pip install paramiko"
    
    try:
        # Create SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to server
        ssh.connect(hostname, port=port, username=username, password=password, timeout=10)
        
        # Start Apache
        stdin, stdout, stderr = ssh.exec_command("sudo systemctl start apache2")
        error = stderr.read().decode('utf-8')
        
        if error:
            # Try alternative command
            stdin, stdout, stderr = ssh.exec_command("sudo service apache2 start")
            error = stderr.read().decode('utf-8')
        
        # Check if Apache is running
        stdin, stdout, stderr = ssh.exec_command("systemctl is-active apache2")
        status = stdout.read().decode('utf-8').strip()
        
        # Close connection
        ssh.close()
        
        if status == "active":
            return True, "Apache server is now running and accessible"
        else:
            return False, f"Failed to start Apache: {error}"
            
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
