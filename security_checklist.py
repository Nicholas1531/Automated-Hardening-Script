import os
import subprocess

def check_firewall():
    result = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
    return "Firewall is ACTIVE" if "active" in result.stdout.lower() else "Firewall is DISABLED"

def check_sudo_users():
    result = subprocess.run(['getent', 'group', 'sudo'], capture_output=True, text=True)
    return f"Sudo Users: {result.stdout.strip()}"

def check_world_writable():
    result = subprocess.run(['find', '/', '-type', 'f', '-perm', '0002', '-not', '-path', '*/proc/*'], capture_output=True, text=True)
    return "World Writable Files Found:\n" + result.stdout if result.stdout else "No world writable files found."

def check_failed_ssh_logins():
    result = subprocess.run(['sudo', 'journalctl', '-u', 'ssh', '--no-pager', '-n', '50', '|', 'grep', 'Failed'], capture_output=True, text=True, shell=True)
    return "Recent Failed SSH Logins:\n" + result.stdout if result.stdout else "No failed SSH login attempts detected."

def check_open_ports():
    result = subprocess.run(['sudo', 'netstat', '-tulnp'], capture_output=True, text=True)
    return "Open Ports:\n" + result.stdout

def check_password_policy():
    result = subprocess.run(['cat', '/etc/login.defs'], capture_output=True, text=True)
    return "Password Policy Settings:\n" + '\n'.join([line for line in result.stdout.split('\n') if "PASS" in line])

def main():
    print("Running Automated Security Checklist...\n")
    checks = {
        "Firewall Status": check_firewall(),
        "Sudo Users": check_sudo_users(),
        "World Writable Files": check_world_writable(),
        "Failed SSH Logins": check_failed_ssh_logins(),
        "Open Ports": check_open_ports(),
        "Password Policy": check_password_policy()
    }
    
    report = "\n".join([f"{key}:\n{value}\n{'-'*40}" for key, value in checks.items()])
    
    with open("security_report.txt", "w") as f:
        f.write(report)
    
    print("Security Checklist Completed. Report saved as 'security_report.txt'.")

if __name__ == "__main__":
    main()