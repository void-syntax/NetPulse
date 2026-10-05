# ⚡ NetPulse

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Version](https://img.shields.io/badge/version-1.0-orange)
![Status](https://img.shields.io/badge/status-in%20development-yellow)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

**NetPulse** is a lightweight command-line network diagnostic tool written in Python.

It allows you to check host availability, measure approximate response latency, continuously monitor a host, and resolve domain names to IP addresses.

> 🚧 **NetPulse is currently under active development.**
>
> The current version is functional and can be used, but new features, improvements, and refinements are still being added.

---

## ✨ Features

- 📡 Ping a host and check its availability
- ⏱️ Measure approximate response latency
- 📊 Calculate packet loss
- 🔄 Continuously monitor a host
- 🌐 Resolve domain names to IP addresses
- 🖥️ Windows and Linux support
- ⚙️ Configurable request count and intervals
- 💻 Simple command-line interface

---

## 🧠 How It Works

NetPulse uses Python's standard library together with the operating system's `ping` command.

### Ping

When you run:

```bash
python netpulse.py ping google.com
```

NetPulse:

1. Detects the operating system.
2. Builds the appropriate `ping` command.
3. Sends one ping request per check.
4. Measures the execution time using `time.perf_counter()`.
5. Determines whether the request succeeded.
6. Calculates packet loss.
7. Displays the results in the terminal.

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
Display results
```

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

Example:

```text
Domain: google.com
IP Address: 142.250.x.x
```

---

## 🚀 Installation

### Requirements

- Python 3.x
- Windows or Linux
- Network connection

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/NetPulse.git
cd NetPulse
```

No external Python packages are required.

NetPulse currently uses Python's standard library.

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

Press `Ctrl+C` to stop monitoring.

### DNS Lookup

```bash
python netpulse.py dns google.com
```

---

## 📊 Example

```text
Starting NetPulse for google.com
Requests: 4
Interval: 1.0s
-----------------------------------

[1/4] Checking...
Host responded: 24.31 ms

[2/4] Checking...
Host responded: 21.87 ms

[3/4] Checking...
Host responded: 23.14 ms

[4/4] Checking...
Host responded: 22.91 ms

Statistics
-----------------------------------
Packets: sent:     4
Packets received:  4
Packets loss:     0.00%
```

---

## 🧰 Built With

| Module | Purpose |
|---|---|
| `argparse` | Command-line interface |
| `subprocess` | Execute system ping commands |
| `socket` | DNS resolution |
| `time` | Latency measurement and intervals |
| `statistics` | Statistical calculations |
| `platform` | Operating system detection |

---

## 🗺️ Roadmap

NetPulse is still under active development.

### Current

- [x] CLI interface
- [x] Host pinging
- [x] Minimum latency output
- [x] Average latency output
- [x] Maximum latency output
- [x] Latency measurement
- [x] Packet loss calculation
- [x] Host monitoring
- [x] DNS lookup
- [x] Windows/Linux support

### Planned

- [ ] JSON export
- [ ] CSV export
- [ ] Improved latency accuracy
- [ ] Real-time statistics
- [ ] Multiple host monitoring
- [ ] Improved error handling
- [ ] Automated tests
- [ ] Configuration file

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
