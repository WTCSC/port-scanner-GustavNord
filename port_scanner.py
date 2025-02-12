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

def scan_ports(ip, ports):
    # Scans given IP for open ports and will return a list of the open ports.
    open_ports = []
    for port in ports:
        # Creates a new socket to test each port.
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.settimeout(0.5)
        # Adds a timeout for each port connection establishment attempt. 
        
        try:
            # Try to connect to the port and if successful the port is open.
            if test_socket.connect_ex((ip, port)) == 0:
                open_ports.append(port)
        except (socket.timeout, socket.error):
            # If there is a timeout or error, continue scanning other ports
            pass

        test_socket.close()
        # Close the socket after checking the port. 

    return open_ports

def scan_network(cidr, ports=None):
    # Scans the network that is defined by the CIDR range for Up hosts. 

    up_hosts = []
    down_count = 0
    error_count = 0
    # List of hosts that responded successfully (Up), counts hosts that did not respond (Down), and count of hosts where there was an error during ping.

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
            up_hosts.append((ip, message))
            print(f"{ip} - Up ({message}ms)")
            # Print the IP and its response time if it's "Up."
        elif status == "Down":
            down_count += 1
            print(f"{ip} - Down")
            # Print "Down" if no response.
        else:
            error_count += 1
            print(f"{ip} - Error ({message})")
            # Print any error message if something went wrong.

    if ports:
        print("\nScanning ports on active hosts\n")
        # If ports were specified it will start scanning open ports on Up hosts. 
        for ip, message in up_hosts:
            if isinstance(message, float):
                # If the response time is a number, use it.
                response_time = message
            else:
                response_time = "No response"

            open_ports = scan_ports(str(ip), ports)
            # Scans the specified ports for open ports.
            if open_ports:
                print(f"{ip} (Up) Response Time: {response_time}ms")
                # If open ports are found it will print the IP and response time. 
                for port in open_ports:
                    print(f" - Port {port} (Open)")
                    # Print each open port.

    return len(up_hosts), down_count, error_count
    # Returns the count of up hosts, down hosts, and errors.

def parse_ports(port_arg):
    # Parses a string of ports or port ranges into a sorted list of individual ports.
    ports = set()
    for part in port_arg.split(','):
        if '-' in part:
            # If a range is specified, parse the start and end of the range. 
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
            # Add all ports in the range.
        else:
            # If a single port is specified it will add it directly. 
            ports.add(int(part))
    return sorted(ports)
    # Return the list of sorted ports. 

def main():
    # Check if exactly one argument (the CIDR) is passed when running the script.
    if len(sys.argv) < 2:
        print("Usage: python scan.py <CIDR> [-p <ports>]")
        sys.exit(1)
        # Provide usage instructions if argument is missing.

    cidr = sys.argv[1]
    ports = None

    if len(sys.argv) > 2 and sys.argv[2] == "-p":
        # Check if the '-p' option is provided to specify ports for scanning.
        if len(sys.argv) < 4:
            print("Error: No ports specified for scanning.")
            sys.exit(1)
            # If no ports are specified after '-p' print an error and exit.
        ports = parse_ports(sys.argv[3])
        # Parse the port list.

    # Get the CIDR notation from the command-line arguments.
    try:
        # Call the scan_network function to scan the network and store the counts.
        up_hosts, down_count, error_count = scan_network(cidr, ports)
        up_count = len(up_hosts)
        print("Scan complete.")
        print(f"Found {up_count} active hosts, {down_count} down, and {error_count} errors")
        # Output the results of the scan.
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
if __name__ == "__main__":
        main()
        # If this script is being run directly (not imported as a module), run the main function.