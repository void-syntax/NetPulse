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
ping_parser.add_argument("-i", "--interval", type=float, default=1.0, help="Interval between ping requests in seconds (default: 1.0)")
ping_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")

monitor_parser = subparsers.add_parser("monitor", help="Continuously monitor a host") #to monitor
monitor_parser.add_argument("host", type=str, help="Target host")
monitor_parser.add_argument("-i", "--interval", type=float, default=5.0, help="Interval between checks")
monitor_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
monitor_parser.add_argument("-c", "--count", type=int, default=0, help="Number of checks to perform")

dns_parser = subparsers.add_parser("dns", help="Resolve a domain name") #dns
dns_parser.add_argument("domain", type=str, help="Domain name to resolve")


args = parser.parse_args()

#ping function

def get_ping_command(host):
   if platform.system() == "Windows":
        return ["ping", "-n", "1", host]
   else:
        return ["ping", "-c", "1", host]

def ping_host(host, count, interval):
    if count <= 0:
        parser.error("Count must be greater than 0")

    if interval < 0:
        parser.error("Interval cannot be negative")
    
    ping_command = get_ping_command(host)
    latencies = []
    sent = 0
    received = 0

    print(f"Starting NetPulse for {host}")
    print(f"Requests: {count}")
    print(f"Interval: {interval}s")
    print("-" * 35)

    for i in range(count):

        print(f"[{i + 1}/{count}] Checking...")
        start = time.perf_counter()
        result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        sent += 1

        if result.returncode == 0:
            received += 1

            latency = (end - start) * 1000

            latencies.append(latency)

            print(f"Host responded: {latency:.2f} ms")

        else:
            print("Ping failed.")

        if i < count - 1:
            time.sleep(interval)

#statistics

    lost = sent - received

    packet_loss = (lost / sent) * 100

    print()
    print("Statistics")
    print("-" * 35)

    print(f"Packets: sent:     {sent}")
    print(f"Packets received: {received}")
    print(f"Packets loss:     {packet_loss:.2f}%")

    if latencies:

        average = statistics.mean(latencies)
        minimum = min(latencies)
        maximum = max(latencies)

    else:
        print("No successful responses.")

#monitor function
def monitor_host(host, interval, count):

    if interval <= 0:
        parser.error("Interval must be greater than 0")
    
    if count < 0:
        parser.error("Count cannot be negative")
    
    ping_command = get_ping_command(host)

    print(f"Monitoring {host} every {interval} seconds.")

    print("Press Ctrl+C to stop.")
    print("-" * 35)

    checks = 0

    try:
        while count == 0 or checks < count:
            checks += 1
            start = time.perf_counter()
            result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            end = time.perf_counter()

            if result.returncode == 0:
                latency = (end - start) * 1000
                print(f"[{checks}] ONLINE - "f"{latency:.2f} ms")
            else:
                print(f"[{checks}] OFFLINE")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print()
        print("Monitoring stopped.")

#dns
def dns_lookup(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"Domain: {domain}")
        print(f"IP Address: {ip_address}")
    except socket.gaierror:
        print(f"Failed to resolve domain: {domain}")

#commands
if args.command == "ping":
    ping_host(args.host, args.count, args.interval)
elif args.command == "monitor":
    monitor_host(args.host, args.interval, args.count)
elif args.command == "dns":
    dns_lookup(args.domain)