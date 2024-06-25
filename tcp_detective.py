import socket
import threading
import os
from colorama import init, Fore, Style

# Initialize colorama for colored output
init()

# Dictionary mapping ports to descriptions
port_descriptions = {
    20: {
        'name': 'FTP (File Transfer Protocol)',
        'functionality': 'Allows file transfer between a client and server over a network.',
        'uses': 'Commonly used to upload/download files. Can be used for automated backups and data distribution.',
        'risks': 'Open FTP ports may expose sensitive data or allow unauthorized file transfers.'
    },
    21: {
        'name': 'FTP (File Transfer Protocol)',
        'functionality': 'Allows file transfer between a client and server over a network.',
        'uses': 'Commonly used to upload/download files. Can be used for automated backups and data distribution.',
        'risks': 'Open FTP ports may expose sensitive data or allow unauthorized file transfers.'
    },
    22: {
        'name': 'SSH (Secure Shell)',
        'functionality': 'Provides secure access to a remote computer.',
        'uses': 'Used for remote administration, file transfer, and tunneling.',
        'risks': 'Open SSH ports may be targeted for brute-force attacks to gain unauthorized access.'
    },
    80: {
        'name': 'HTTP (Hypertext Transfer Protocol)',
        'functionality': 'Used for transmitting hypermedia documents (web pages).',
        'uses': 'Enables web browsing and accessing websites.',
        'risks': 'Open HTTP ports may expose websites to attacks such as SQL injection or cross-site scripting.'
    },
    443: {
        'name': 'HTTPS (Hypertext Transfer Protocol Secure)',
        'functionality': 'Secured version of HTTP with encryption.',
        'uses': 'Securely transmits sensitive information such as login credentials or payment details over the internet.',
        'risks': 'Open HTTPS ports may still be vulnerable to attacks targeting SSL/TLS protocols or certificate vulnerabilities.'
    },
    # Add more ports and descriptions as needed or use hackertarget api for automation
}

# Function to print the banner
def print_banner():
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear the console
    banner = f"""
    {Fore.GREEN}{Style.BRIGHT}
    ======================================
                  TCP_Finder
           Developed By: Anshika Awasthi
    ======================================
    {Style.RESET_ALL}
    """
    print(banner)

# Function to perform the port scan
def scan(host, port, results):
    s = socket.socket()
    s.settimeout(1)  # Set socket timeout to 1 second
    result = s.connect_ex((host, port))  # Attempt to connect to the port
    if result == 0:
        results.append(port)  # Append the open port to results list
        if port in port_descriptions:
            # Print detailed information if port is in port_descriptions
            print(f"{Fore.GREEN}Port {port} is open: {port_descriptions[port]['name']}")
            print(f"Functionality: {port_descriptions[port]['functionality']}")
            print(f"Uses: {port_descriptions[port]['uses']}")
            print(f"Risks: {port_descriptions[port]['risks']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Port {port} is open{Style.RESET_ALL}")
        print()  # Print an additional newline for separation
    s.close()  # Close the socket

# Function to start the scanning process
def start_scan(host, start, end):
    results = []
    threads = []

    # Create threads for each port in the specified range
    for port in range(start, end + 1):
        t = threading.Thread(target=scan, args=(host, port, results))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    return results  # Return list of open ports

# Main function
def main():
    print_banner()  # Print TCP_Finder banner
    host = input(f"{Fore.GREEN}Enter host to scan: {Style.RESET_ALL}")  # Get target host from user
    print(f"""
    {Fore.GREEN}Select scan type:
    1. Scan All Ports
    2. Scan Top 1000 Ports
    3. Custom Scan
    {Style.RESET_ALL}
    """)
    option = input(f"{Fore.GREEN}Enter your choice (1/2/3): {Style.RESET_ALL}")  # Get scan type choice

    if option == '1':
        start = 1
        end = 65535
    elif option == '2':
        start = 1
        end = 1000
    elif option == '3':
        start = int(input(f"{Fore.GREEN}Enter start port: {Style.RESET_ALL}"))  # Get start port for custom scan
        end = int(input(f"{Fore.GREEN}Enter end port: {Style.RESET_ALL}"))  # Get end port for custom scan
    else:
        print(f"{Fore.RED}Invalid option. Exiting.{Style.RESET_ALL}")  # Handle invalid input
        return

    print(f"{Fore.GREEN}Scanning {host} from port {start} to {end}...{Style.RESET_ALL}")  # Print scanning message
    results = start_scan(host, start, end)  # Perform port scan

    if results:
        print(f"{Fore.GREEN}Open ports:{Style.RESET_ALL}")  # Print open ports header
        for port in results:
            if port not in port_descriptions:
                print(f"{Fore.GREEN}Port {port} is open{Style.RESET_ALL}")  # Print open ports without description
    else:
        print(f"{Fore.RED}No open ports found.{Style.RESET_ALL}")  # Print message if no open ports found

if __name__ == "__main__":
    main()  # Run the main function if script is executed directly
