# ⚡ NetPulse

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/version-1.2-orange)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**NetPulse** is a lightweight command-line network diagnostic tool written in Python.

It allows you to check host availability, measure approximate response latency, continuously monitor a host, and resolve domain names to IP addresses.

> 📢 **Update (v1.2):**
> Full **macOS support** and CLI flag adjustments! NetPulse now builds the correct `ping` command for Windows, Linux, and macOS, and a new `-t/--timeout` flag lets you control how long to wait for each reply.

> 🚧 **NetPulse is currently under active development.**
>
> The current version is functional and can be used, but new features, improvements, and refinements are still being added.

---

## ✨ Features

- 📡 Ping a host and check its availability
- 🎨 Modern and clean terminal UI powered by **Rich** (styled panels, tables, and colors)
- ⏱️ Measure approximate response latency
- 📊 Calculate packet loss
- 🔄 Continuously monitor a host
- 🌐 Resolve domain names to IP addresses
- 📁 Auto-export reports directly to a dedicated `data/` directory (JSON / CSV)
- 🖥️ Windows, Linux, and macOS support
- ⚙️ Configurable request count, intervals, and timeout
- 💻 Simple command-line interface

---

## 🧠 How It Works

NetPulse uses Python's standard library together with the operating system's `ping` command, beautifully rendered with `rich`.

### Ping

When you run:

```bash
python netpulse.py ping google.com
```

NetPulse:

1. Detects the operating system (Windows, Linux, or macOS).
2. Builds the appropriate `ping` command with the correct flags and timeout units for that OS.
3. Sends one ping request per check.
4. Measures the execution time using `time.perf_counter()`.
5. Determines whether the request succeeded.
6. Calculates packet loss.
7. Displays styled summary panels in the terminal.

The basic process looks like this:

```text
Host
  │
  ▼
Send ping request
  │
  ├── Success ──► Measure latency
  │
  └── Failure ──► Count as lost packet
  │
  ▼
Calculate statistics
  │
  ▼
Display styled results
```

### Cross-platform flags

The `ping` utility differs between operating systems, so NetPulse adapts automatically:

| OS | Count flag | Timeout flag | Timeout unit |
|---|---|---|---|
| Windows | `-n` | `-w` | milliseconds |
| Linux | `-c` | `-W` | seconds |
| macOS | `-c` | `-W` | milliseconds |

You always pass the timeout in **seconds** with `-t`, and NetPulse converts it for your system.

### Monitor

The `monitor` command repeatedly checks a host at a specified interval.

```bash
python netpulse.py monitor google.com -i 5
```

The host is checked every 5 seconds until the requested number of checks is completed or `Ctrl+C` is pressed.

### DNS

The `dns` command uses Python's `socket` module to resolve a domain name to an IP address.

```bash
python netpulse.py dns google.com
```

### Check

The `check` command measures your own connection latency by pinging Cloudflare DNS (`1.1.1.1`).

```bash
python netpulse.py check
```

---

## 🚀 Installation

### Requirements

- Python 3.x
- Windows, Linux, or macOS
- Network connection

Clone the repository:

```bash
git clone https://github.com/void-syntax/NetPulse.git
cd NetPulse
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Usage

### Ping a Host

```bash
python netpulse.py ping google.com
```

### Specify Request Count

```bash
python netpulse.py ping google.com -c 10
```

### Specify Interval

```bash
python netpulse.py ping google.com -i 2
```

### Specify Timeout

Set how many seconds to wait for each reply (default: 2):

```bash
python netpulse.py ping google.com -t 5
```

### Monitor a Host

```bash
python netpulse.py monitor google.com
```

Monitor with a custom interval:

```bash
python netpulse.py monitor google.com -i 5
```

Monitor with a specific number of checks:

```bash
python netpulse.py monitor google.com -c 20
```

Monitor with a custom timeout:

```bash
python netpulse.py monitor google.com -t 3
```

Press `Ctrl+C` to stop monitoring.

### DNS Lookup

```bash
python netpulse.py dns google.com
```

### Check Your Connection

```bash
python netpulse.py check -c 6 -t 3
```

### Command Reference

| Command | Required | Optional flags |
|---|---|---|
| `ping` | `host` | `-c`, `-i`, `-t`, `-o`, `-p` |
| `monitor` | `host` | `-i`, `-t`, `-c`, `-o`, `-p` |
| `dns` | `domain` | `-o`, `-p` |
| `check` | none | `-c`, `-i`, `-t`, `-o`, `-p` |

| Flag | Description | Default |
|---|---|---|
| `-c`, `--count` | Number of requests / checks | `4` (`0` = endless for `monitor`) |
| `-i`, `--interval` | Seconds between requests | `1.0` (`5.0` for `monitor`) |
| `-t`, `--timeout` | Seconds to wait for each reply | `2` |
| `-o`, `--output` | Output file (`.json` or `.csv`) | none |
| `-p`, `--path` | Custom folder for the output file | `data/` |

Run `python netpulse.py <command> -h` to see the options for any command.

### Save Results to JSON or CSV

You can export results using `-o/--output`. By default, files are saved directly into the project's `data/` directory:

#### JSON export

```bash
python netpulse.py ping google.com -c 4 -o results.json
python netpulse.py dns google.com -o dns-results.json
```

#### CSV export

```bash
python netpulse.py ping google.com -c 4 -o results.csv
python netpulse.py monitor google.com -c 5 -i 2 -o monitor.csv
```

You can also specify a custom path using `-p/--path`:

```bash
python netpulse.py ping google.com -c 4 -o results.json -p ./reports
```

---

## 🧰 Built With

| Module / Package | Purpose |
|---|---|
| `rich` | Terminal styling, styled panels, and formatted output |
| `argparse` | Command-line interface |
| `subprocess` | Execute system ping commands |
| `socket` | DNS resolution |
| `time` | Latency measurement and intervals |
| `statistics` | Statistical calculations |
| `platform` | Operating system detection |
| `pathlib` | Cross-platform file path resolution |

---

## 🗺️ Roadmap

NetPulse is still under active development.

### Current

- [x] CLI interface
- [x] Rich terminal UI (panels and colored output)
- [x] Host pinging
- [x] Minimum, average, and maximum latency statistics
- [x] Packet loss calculation
- [x] Host monitoring
- [x] DNS lookup
- [x] Windows/Linux/macOS support
- [x] JSON export
- [x] CSV export
- [x] Automatic saving to `data/` folder
- [x] macOS full support and flag adjustments (`-t/--timeout`)

### Planned

- [ ] Improved latency accuracy (ICMP socket / output parsing)
- [ ] Real-time live dashboards via Rich Live
- [ ] Multiple host monitoring
- [ ] Configuration file support

---

## 🔐 Responsible Use

NetPulse is intended for network diagnostics and monitoring of systems you own or have permission to test.

Do not use it to interfere with, overload, or disrupt systems without authorization.

---

## 👨‍💻 Author

**Asim Mammadrzayev**

Computer Engineering Student interested in programming, networking, and cybersecurity.

---

## 📄 License

This project is licensed under the MIT License.
