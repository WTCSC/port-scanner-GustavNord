import subprocess
import ipaddress
import sys
import platform
import socket

def ping_host(ip):
    try:
        # Check the operating system and use the appropriate ping command.
        if platform.system().lower()== "windows":
            response = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # For Windows, use '-n' for count and '-w' for timeout in milliseconds.
        else:
            response = subprocess.run(['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # For Linux/macOS, use '-c' for count and '-W' for timeout in seconds.

        if response.returncode == 0:
            # If ping succeeded.
            if "time=" in response.stdout.decode():
                # Extract the response time from the ping output and round it to 2 decimal places.
                time_ms = round(float(response.stdout.decode().split("time=")[1].split()[0]), 2)
                return "Up", time_ms
                # Return status "Up" and the time in ms.
        
        if response.returncode != 0:
        # If ping failed or no time in the response.
            return "Down", "No response"
            # Return "Down" if no response is received.
    except Exception as e:
        # Catch any unexpected errors and return an error message.
        return "Error", str(e)

def scan_network(cidr):

    up_count = 0
    down_count = 0
    error_count = 0
    # Count of hosts that responded successfully (Up), hosts that did not respond (Down), and count of hosts where there was an error during ping.

    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        # Convert CIDR notation into an IPv4 network object.
    except ValueError:
        print("Error: Invalid CIDR notation.")
        sys.exit(1)
        # Error handling for invalid CIDR input.

    print(f"Scanning network {cidr}")
    # Print that the scanning has started.

    for ip in network.hosts():
        status, message = ping_host(ip)
        # Iterate over all host IP addresses in the network range and ping the current host and get the status and message.

        if status == "Up":
            # Check the ping result and update the corresponding counts.
            up_count += 1
            print(f"{ip} - Up ({message}ms)")
            # Print the IP and its response time if it's "Up."
        elif status == "Down":
            down_count += 1
            print(f"{ip} - Down ({message})")
            # Print "Down" if no response.
        else:
            error_count += 1
            print(f"{ip} - Error ({message})")
            # Print any error message if something went wrong.

    return up_count, down_count, error_count
    # Return counts of "Up", "Down", and "Error" hosts.

def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(0.5)
        output = test_socket.connect((ip, port))
        
        try:
            test_socket.connect((ip, port))
            open_ports.append(port)
            test_socket.close()
        except socket.timeout and socket.error:
            test_socket.close() 
            pass

    return open_ports

def main():
    # Check if exactly one argument (the CIDR) is passed when running the script.
    if len(sys.argv) != 2:
        print("Usage: python scan.py <CIDR>")
        sys.exit(1)
        # Provide usage instructions if argument is missing.

    cidr = sys.argv[1]
    # Get the CIDR notation from the command-line arguments.
    try:
        # Call the scan_network function to scan the network and store the counts.
        up_count, down_count, error_count = scan_network(cidr)
        print("Scan complete.")
        print(f"Found {up_count} active hosts, {down_count} down, and {error_count} errors")
        # Output the results of the scan.
    except ValueError:
        print("Error: Invalid CIDR notation.")
        # Error handling for invalid CIDR input.

if __name__ == "__main__":
        main()
        # If this script is being run directly (not imported as a module), run the main function.