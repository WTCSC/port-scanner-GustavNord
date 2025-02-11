# IP Address Scanner Script
This script scans a network range specified in CIDR notation (192.168.1.0/24) and reports the status of each IP address in the range. The script pings each host and returns the host's status and notes if it's "Up", "Down", or if an error occured during the scan. It also includes response times for each successful ping. This script accepts one command-line argument. The network range to scan in CIDR format `192.168.1.0/24`. 

## Introduction
This script allows user to scan a network range given in CIDR notation. It checks the status of each IP address in the range by using `ping` and checks if the IP is reachable and provides detailed information about the status of each IP address

- **Up**: The IP responded to the ping request and shows the response time.
- **Down**: The IP did not respond to the ping.
- **Error**: An error occurred during the ping attempt.

---

## Installation

1. Clone or download the repository
2. Make sure Python is installed on your system and in your PATH
4. Install required dependencies if needed

--- 

## Usage

### Run the Script

Run the script from the command line to scan a network range provided in CIDR notation.

```python
python3 port_scanner.py 192.168.1.0/24
```

Output Example:
```python
Scanning network 192.168.1.0/24...

192.168.1.1 - Up (2ms)
192.168.1.2 - Down (No response)
192.168.1.3 - Up (5ms)
192.168.1.4 - Up (3ms)
192.168.1.5 - Error (Connection timeout)

Scanning ports on active hosts

192.168.1.1 (Up) Response Time: 2ms
- Port 22 (Open)
- Port 80 (Open)
- Port 443 (Open)

192.168.1.3 (Up) Response Time: 5ms
 - Port 22 (Open)

192.168.1.4 (Up) Response Time: 3ms
 - Port 443 (Open)

Scan complete.
Found 3 active hosts, 1 down, and 1 error
```

## Error Handling
The script has error handling for these situations:

1. Invalid CIDR Notation
**Error message:**  
`"Error: Invalid CIDR notation."`

2. Ping Error
If there is a connection issue or timeout during the ping attempt, the script will log it as an error.  
**Error message:**  
`"Error: Connection timeout"`

## Troubleshooting

1. Invalid CIDR Notation
**Solution:** Ensure that the CIDR is correctly formatted: `192.168.1.0/24`.

2. Ping Command Fails
**Solution:** Check that the target IP address is active and connected to the network.

3. Python Not Found
**Solution:** Make sure that Python is installed to your PATH and can be accessed from the command-line. 

# Scan Specific Ports
You can also scan specific ports on active hosts by using the `-p` option and the list of ports or a range of ports. 

```python
python3 port_scanner.py 192.168.1.0/24 -p 22, 80, 443
```

This will scan ports 22 (SSH), 80 (HTTP), and 443 (HTTPS) on each active host that responds to the ping.


You can also specify a range of ports:
```python
python3 port_scanner.py 192.168.1.0/24 -p 1000-1020

This will scan ports from 1000 to 1020 on each active host.
```


## Extras
**Notes:**
- The script pings each IP address in the given range and reports the status.
- The script supports both Windows and Linux/macOS systems.
- The response times for active IPs are measured in milliseconds.
