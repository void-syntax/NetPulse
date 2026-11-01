import argparse
import csv
import json
import pathlib
import platform
import socket
import statistics
import subprocess
import time

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

console = Console()

console.print("[blue]NetPulse: Simple network diagnostic tool[/blue]")
console.print("[bold red]Version: 1.0[/bold red]")
console.print("Author: Asim")
console.print()

parser = argparse.ArgumentParser()

#subparsers for commands

subparsers = parser.add_subparsers(dest="command",required=True, help="Available commands")


# ping command

ping_parser = subparsers.add_parser("ping", help="Ping a host") #ping
ping_parser.add_argument("host", type=str, help="Host to ping")
ping_parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests to send (default: 4)")
ping_parser.add_argument("-i", "--interval", type=float, default=1.0, help="Interval between ping requests in seconds (default: 1.0)")
ping_parser.add_argument("-t", "--timeout", type=int, default=1.0, help="Timeout for each ping request in seconds (default: 1.0)")
ping_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
ping_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")
#command for monitoring

monitor_parser = subparsers.add_parser("monitor", help="Continuously monitor a host") #to monitor
monitor_parser.add_argument("host", type=str, help="Target host")
monitor_parser.add_argument("-i", "--interval", type=float, default=5.0, help="Interval between checks")
monitor_parser.add_argument("-t", "--timeout", type=int, default=1.0, help="Timeout for each check")
monitor_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
monitor_parser.add_argument("-c", "--count", type=int, default=0, help="Number of checks to perform")
monitor_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")
#dns command

dns_parser = subparsers.add_parser("dns", help="Resolve a domain name") #dns
dns_parser.add_argument("domain", type=str, help="Domain name to resolve")
dns_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)") #python netpulse.py dns example.com -o results.json
dns_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")

# self ping check command

check_parser = subparsers.add_parser("check", help="Check internet latency to default DNS servers")
check_parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests (default: 4)")
check_parser.add_argument("-i", "--interval", type=float, default=1.0, help="Interval between requests (default: 1.0)")
check_parser.add_argument("-t", "--timeout", type=int, default=1.0, help="Timeout for each request (default: 1.0)")
check_parser.add_argument("-o", "--output", type=str, help="Output file to save results (JSON or CSV)")
check_parser.add_argument("-p", "--path", type=str, help="Path to save the output file")

#parse the arguments
args = parser.parse_args()

#ping function ----------------------------------------------------------

def get_ping_command(host, timeout=2):
    # Windows -w and macOS -W take MILLISECONDS, Linux -W takes SECONDS
    if platform.system() == "Windows":
        return ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    elif platform.system() == "Linux":
        return ["ping", "-c", "1", "-W", str(timeout), host]
    elif platform.system() == "Darwin":
        return ["ping", "-c", "1", "-W", str(timeout * 1000), host]
    else:
        raise SystemExit(f"Unsupported operating system: {platform.system()}")


def resolve_output_path(output, path=None):
    if not output:
        return None

    if path:
        return pathlib.Path(path) / output

    return pathlib.Path(__file__).resolve().parent.parent / "data" / output

#---------------------------------------------------------------------------------------------------

#ping

def ping_host(host, count, interval, timeout=2, path=None, output=None):
    if count <= 0:
        parser.error("Count must be greater than 0")

    if interval < 0:
        parser.error("Interval cannot be negative")

    if timeout <= 0:
        parser.error("Timeout must be greater than 0")

    output_path = resolve_output_path(output, path)
    ping_command = get_ping_command(host, timeout)
    latencies = []
    sent = 0
    received = 0

    console.print(
        Panel(
            f"[bold green]Target Host:[/bold green] [cyan]{host}[/cyan]\n"
            f"[bold yellow]Requests:[/bold yellow] {count}\n"
            f"[bold yellow]Interval:[/bold yellow] {interval}s\n"
            f"[bold yellow]Timeout:[/bold yellow] {timeout}s",
            title="[bold]Ping Check[/bold]",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 3),
    )
)   
    for i in range(count):

        console.print(f"[{i + 1}/{count}] Checking...")
        start = time.perf_counter()
        result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        end = time.perf_counter()
        sent += 1

        if result.returncode == 0:
            received += 1

            latency = (end - start) * 1000

            latencies.append(latency)

            console.print(f"Host responded: {latency:.2f} ms")

        else:
            console.print("Ping failed.")

        if i < count - 1:
            time.sleep(interval)

#statistics

    lost = sent - received

    packet_loss = (lost / sent) * 100

    console.print()
    console.print("Statistics")
    console.print("-" * 35)

    console.print(f"Packets: sent:    {sent}")
    console.print(f"Packets received: {received}")
    console.print(f"Packets loss:     {packet_loss:.2f}%")

    if latencies:

        average = statistics.mean(latencies)
        minimum = min(latencies)
        maximum = max(latencies)

        console.print(f"\nAverage latency: {average:.2f}")
        console.print(f"Highest latency: {maximum:.2f}")
        console.print(f"Lowest latency: {minimum:.2f}")


    else:
        console.print("No successful responses.")

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
            console.print("\nNo output file specified.")
#----------------------------------------------------------------------------------------
#monitor function
def monitor_host(host, interval, count, timeout=2.0, path=None, output=None):

    if interval <= 0:
        parser.error("Interval must be greater than 0")
    
    if count < 0:
        parser.error("Count cannot be negative")
    
    if timeout <= 0:
        parser.error("Timeout must be greater than 0")

    output_path = resolve_output_path(output, path)
    ping_command = get_ping_command(host)
    results = []

    console.print(
            Panel(
                f"[bold green]Monitoring:[/bold green] [cyan]{host}[/cyan] every {interval} seconds.\n"
                f"[bold yellow]Press Ctrl+C to stop.[/bold yellow]",
                title="[bold]Monitoring[/bold]",
                box=box.ROUNDED,
                border_style="cyan",
                padding=(1, 3),
        )
    )
    checks = 0

    try:
        while count == 0 or checks < count:
            checks += 1
            start = time.perf_counter()
            result = subprocess.run(ping_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            end = time.perf_counter()

            if result.returncode == 0:
                latency = (end - start) * 1000
                console.print(f"[{checks}] ONLINE - "f"{latency:.2f} ms")
                results.append({"check": checks, "status": "online", "latency_ms": latency})
            else:
                console.print(f"[{checks}] OFFLINE")
                results.append({"check": checks, "status": "offline"})
            
            if count == 0 or checks < count:
                time.sleep(interval)
    except KeyboardInterrupt:
        console.print()
        console.print("Monitoring stopped.")
    finally:
        if output_path:
            save_results_to_file({"host": host, "interval": interval, "checks": len(results), "results": results}, output_path)

#--------------------------------------------------------------------------------------

#dns
def dns_lookup(domain, path=None, output=None):
    output_path = resolve_output_path(output, path)
    try:
        ip_address = socket.gethostbyname(domain)

        console.print(
    Panel(
        Group(
            Text("Here is your IP", style="bold"),
            Panel(f"Domain: {domain}\nIP Address: {ip_address}", border_style="red"),
            Text("DNS Lookup completed successfully", style="italic dim"),
        ),
        title="DNS Lookup",
    )
)
        if output_path:
            save_results_to_file({"domain": domain, "ip_address": ip_address}, output_path)
    except socket.gaierror:
        console.print(f"Failed to resolve domain: {domain}")
        if output_path:
            save_results_to_file({"domain": domain, "status": "failed"}, output_path)

#---------------------------------------------------------------------------------------------

#check my ping
def check_my_ping(count=4, interval=1.0, timeout=2.0, path=None, output=None):
    target_server = "1.1.1.1"
    console.print("[dim]Testing connection latency via Cloudflare DNS (1.1.1.1)...[/dim]")
    ping_host(target_server, count=count, interval=interval, timeout=timeout, path=path, output=output)
#------------------------------------------------------------------------------------------

#save files to json
def save_results_to_file(results, output_file):
    output_path = pathlib.Path(output_file) 
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".json":
        with open(output_path, "w") as f:
            json.dump(results, f, indent=4)
        console.print(f"\nResults saved to {output_path}")
    elif output_path.suffix.lower() == ".csv":
        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            if isinstance(results, dict):
                writer.writerow(results.keys())
                writer.writerow(results.values())
            else:
                for row in results:
                    writer.writerow(row)
        console.print(f"Results saved to {output_path}")
    else:
        console.print(f"Unsupported output format for {output_path}. Use .json or .csv.")

#commands
if args.command == "ping":
    ping_host(args.host, args.count, args.interval, timeout=args.timeout, path=args.path, output=args.output)
elif args.command == "monitor":
    monitor_host(args.host, args.interval, args.count, timeout=args.timeout, path=args.path, output=args.output)
elif args.command == "dns":
    dns_lookup(args.domain, path=args.path, output=args.output)
elif args.command == "check":
    check_my_ping(count=args.count, interval=args.interval, timeout=args.timeout, path=args.path, output=args.output)