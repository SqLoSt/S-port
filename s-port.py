import os
import socket
import concurrent.futures
import sys
from pyfiglet import Figlet

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_port(target, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(0.1)
        try:
            result = client_socket.connect_ex((target, port))
            if result == 0:
                service = socket.getservbyport(port)
                try:
                    banner = client_socket.recv(1024).decode().strip()
                    print(f"\033[32m[SUCCESS]\033[0m Port {port}/{service} is open")
                    print(f"\tBanner: {banner}")
                except:
                    print(f"\033[32m[SUCCESS]\033[0m Port {port}/{service} is open")
                return port
            else:
                print(f"\033[31m[404]\033[0m Port {port} unsuccessful")
        except:
            pass
    return None

def scan_ports():
    target = input("\nEnter the IP address or domain name to scan: ")
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"\033[31m[EROR]\033[0m The given IP address or domain isn't available")
        scan_another()
        return

    open_ports = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=200)
    try:
        results = [executor.submit(scan_port, ip_address, port) for port in range(1, 65536)]
        for result in concurrent.futures.as_completed(results):
            if result.result():
                open_ports.append(result.result())
    except KeyboardInterrupt:
        print(f"\033[31m[EROR]\033[0m Keyboard interrupt detected, aborting")
        sys.exit(0)

    print(f"\n\033[33m[INFO]\033[0m Open ports for {target}:")
    for port in open_ports:
        service = socket.getservbyport(port)
        print(f"\tPort {port}/{service}")
    print()

    scan_another()

def scan_another():
    print("\033[33mDo you want to scan another IP address or domain? (y/n)\033[0m")
    answer = input()
    if answer.lower() == "y":
        clear_terminal()
        f = Figlet(font='univers')
        print("\033[32m" + f.renderText('S-PORT') + "\033[0m")
        scan_ports()
    else:
        clear_terminal()
        f = Figlet(font='univers')
        print("\033[32m" + f.renderText('S-PORT') + "\033[0m")
        print("\033[36mCoded By Github.com/SqLoSt | Discord: SqLoSt#6660\033[0m")
        print("\033[31mThanks for using S-PORT, coded by SqLoSt\033[0m")
        sys.exit(0)

# Example usage
clear_terminal()
f = Figlet(font='univers')
print("\033[32m" + f.renderText('S-PORT') + "\033[0m")
print("\033[36mCoded By Github.com/SqLoSt | Discord: SqLoSt#6660\033[0m")
scan_ports()
