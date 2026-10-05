import socket
import subprocess
import argparse
import time
import statistics
import json
import csv
import pathlib
import platform

print("NetPulse: Simple network diagnostic tool")
print("Version: 1.0")
print("Author: Asim")
print()

parser = argparse.ArgumentParser(description="NetPulse: Simple network diagnostic tool")

subparsers = parser.add_subparsers(dest="command",required=True, help="Available commands")

ping_parser = subparsers.add_parser("ping", help="Ping a host") #ping
ping_parser.add_argument("host", type=str, help="Host to ping")
ping_parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests to send (default: 4)")
ping_parser.add_argument("-i", "--interval", type=int, default=1, help="Interval between ping requests in seconds (default: 1.0)")
ping_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")

monitor_parser = subparsers.add_parser("monitor", help="Continuously monitor a host") #to monitor
monitor_parser.add_argument("host", type=str, help="Target host")
monitor_parser.add_argument("-i", "--interval", type=int, default=5, help="Interval between checks")
monitor_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
monitor_parser.add_argument("-c", "--count", type=int, default=0, help="Number of checks to perform")

dns_parser = subparsers.add_parser("dns", help="Resolve a domain name") #dns
dns_parser.add_argument("host", type=str, help="Domain name to resolve")


args = parser.parse_args()

def is_host_alive(host:str) -> bool:
    cmd = ["ping", "-n", "1", host] if platform.system() == "Windows" else ["ping", "-c", "1", host]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return result.returncode == 0

def print_results():
    print(f"Starting NetPulse for {args.host}")
    print(f"Requests: {args.count}")
    print(f"Interval: {args.interval}s")
    print("-" * 35)

if platform.system() == "Windows":
    ping_command = ["ping", "-n", "1", args.host]
else:
    ping_command = ["ping", "-c", "1", args.host]

if args.command == "ping":
    if args.count <= 0:
        parser.error("count must be greater than 0")

    if args.interval < 0:
        parser.error("interval cannot be negative")

    for i in range(args.count):
        print(f"[{i + 1}/{args.count}] Checking...")    
        result = subprocess.run(ping_command, capture_output=True, text=True)

    result  = subprocess.run(["ping", "-n", "4", args.host], capture_output=True, text=True)

    print_results()

if args.command == "monitor":
    if args.interval <= 0:
        parser.error("interval must be greater than 0")
    
    one_time = True

    for i in range(args.count):
        if one_time:
            print(f"Monitoring {args.host} every {args.interval} seconds. Press Ctrl+C to stop.")
        one_time = False
        result = subprocess.run(ping_command, capture_output=True, text=True)
    print_results()

if args.command == "dns":
    try:
        ip_address = socket.gethostbyname(args.domain)
        print(f"{args.domain} resolved to {ip_address}")
    except socket.gaierror:
        print(f"Failed to resolve {args.domain}")

if is_host_alive(args.host):
    print("Host responded.")
else:
    print("Ping failed.")