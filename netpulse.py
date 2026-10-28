import socket
import subprocess
import argparse
import time
import statistics
import json
import csv
import pathlib
import platform

from rich import print

print("[bold blue]NetPulse: Simple network diagnostic tool[/bold blue]")
print("[bold red]Version: 1.0[/bold red]")
print("Author: Asim")
print()

parser = argparse.ArgumentParser(description="NetPulse: Simple network diagnostic tool")

subparsers = parser.add_subparsers(dest="command",required=True, help="Available commands")

ping_parser = subparsers.add_parser("ping", help="Ping a host") #ping
ping_parser.add_argument("host", type=str, help="Host to ping")
ping_parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests to send (default: 4)")
ping_parser.add_argument("-i", "--interval", type=float, default=1.0, help="Interval between ping requests in seconds (default: 1.0)")
ping_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
ping_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")

monitor_parser = subparsers.add_parser("monitor", help="Continuously monitor a host") #to monitor
monitor_parser.add_argument("host", type=str, help="Target host")
monitor_parser.add_argument("-i", "--interval", type=float, default=5.0, help="Interval between checks")
monitor_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
monitor_parser.add_argument("-c", "--count", type=int, default=0, help="Number of checks to perform")
monitor_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")

dns_parser = subparsers.add_parser("dns", help="Resolve a domain name") #dns
dns_parser.add_argument("domain", type=str, help="Domain name to resolve")
dns_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)") #python netpulse.py dns example.com -o results.json
dns_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")

args = parser.parse_args()

#ping function

def get_ping_command(host):
   if platform.system() == "Windows":
        return ["ping", "-n", "1", host]
   else:
        return ["ping", "-c", "1", host]


def resolve_output_path(output, path=None):
    if not output:
        return None

    if path:
        return pathlib.Path(path) / output

    return pathlib.Path(output)


def ping_host(host, count, interval, path=None, output=None):
    if count <= 0:
        parser.error("Count must be greater than 0")

    if interval < 0:
        parser.error("Interval cannot be negative")

    output_path = resolve_output_path(output, path)
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

    print(f"Packets: sent:    {sent}")
    print(f"Packets received: {received}")
    print(f"Packets loss:     {packet_loss:.2f}%")

    if output_path:
        results = {
            "host": host,
            "count": count,
            "interval": interval,
            "sent": sent,
            "received": received,
            "lost": lost,
            "packet_loss_percent": packet_loss,
            "latencies_ms": latencies,
        }
        save_results_to_file(results, output_path)
    else:
        print("No output file specified.")

    if latencies:

        average = statistics.mean(latencies)
        minimum = min(latencies)
        maximum = max(latencies)

    else:
        print("No successful responses.")

#monitor function
def monitor_host(host, interval, count, path=None, output=None):

    if interval <= 0:
        parser.error("Interval must be greater than 0")
    
    if count < 0:
        parser.error("Count cannot be negative")
    
    output_path = resolve_output_path(output, path)
    ping_command = get_ping_command(host)
    results = []

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
                results.append({"check": checks, "status": "online", "latency_ms": latency})
            else:
                print(f"[{checks}] OFFLINE")
                results.append({"check": checks, "status": "offline"})
            
            if count == 0 or checks < count:
                time.sleep(interval)
    except KeyboardInterrupt:
        print()
        print("Monitoring stopped.")
    finally:
        if output_path:
            save_results_to_file({"host": host, "interval": interval, "checks": len(results), "results": results}, output_path)

#dns
def dns_lookup(domain, path=None, output=None):
    output_path = resolve_output_path(output, path)
    try:
        ip_address = socket.gethostbyname(domain)
        print(f"Domain: {domain}")
        print(f"IP Address: {ip_address}")
        if output_path:
            save_results_to_file({"domain": domain, "ip_address": ip_address}, output_path)
    except socket.gaierror:
        print(f"Failed to resolve domain: {domain}")
        if output_path:
            save_results_to_file({"domain": domain, "status": "failed"}, output_path)

#save files to json
def save_results_to_file(results, output_file):
    output_path = pathlib.Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".json":
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {output_path}")
    elif output_path.suffix.lower() == ".csv":
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            if isinstance(results, dict):
                writer.writerow(results.keys())
                writer.writerow(results.values())
            else:
                for row in results:
                    writer.writerow(row)
        print(f"Results saved to {output_path}")
    else:
        print(f"Unsupported output format for {output_path}. Use .json or .csv.")

#commands
if args.command == "ping":
    ping_host(args.host, args.count, args.interval, path=args.path, output=args.output)
elif args.command == "monitor":
    monitor_host(args.host, args.interval, args.count, path=args.path, output=args.output)
elif args.command == "dns":
    dns_lookup(args.domain, path=args.path, output=args.output)