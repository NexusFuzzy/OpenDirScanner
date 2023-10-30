import argparse
import ipaddress
import os
import random
from concurrent.futures import ThreadPoolExecutor

import requests
from pyfiglet import Figlet

pool = ThreadPoolExecutor(max_workers=10)


def save_output(protocol, ip_address, content):
    try:
        print("Storing output to " + os.path.join(os.getcwd(), 'output', protocol + "_" + ip_address + ".txt"))
        if not os.path.isdir(os.path.join(os.getcwd(), 'output')):
            print("Creating output directory")
            os.mkdir(os.path.join(os.getcwd(), 'output'))

        with open(os.path.join(os.getcwd(), 'output', protocol + "_" + ip_address + ".txt"), 'w') as filehandle:
            filehandle.write(content)
    except Exception as ex_write_output:
        print("Error while writing output to file: " + str(ex_write_output))


def scan(ip_address):
    protocols = ["http", "https"]
    for protocol in protocols:
        try:
            print("Now trying " + ip_address + " via " + protocol.upper())
            result = requests.get(protocol + "://" + ip_address, timeout=5)
            if result.status_code == 200:
                if "Index of".upper() in result.text.upper() or "Last modified".upper() in result.text.upper():
                    save_output(protocol, ip_address, result.text)
                else:
                    print("Server returned content but does not seem to be directory listing!")
        except Exception as ex_connect:
            print("Couldn't scan server " + protocol + "://" + ip_address + ": " + str(ex_connect))


def print_header():
    possible_fonts = ['banner', 'big', 'digital', 'shadow']
    f = Figlet(font=possible_fonts[random.randint(0, len(possible_fonts) - 1)])
    print(f.renderText("OpenDirScanner"))


print_header()
parser = argparse.ArgumentParser(
                    prog='OpenDirScanner',
                    description='Script to scan a range of IP addresses in CIDR format for Open Directories',
                    epilog='Do not pwn what you do not own')

parser.add_argument('-r', '--range', help='IP range in CIDR format (example: 192.168.0.1/24)')
parser.add_argument('-i', '--ip_address', help='Scan single IP address')
parser.add_argument('-t', '--threads', help='Number of concurrent threads when scanning a range (default: 10)', type=int)

args = parser.parse_args()

if args.threads:
    pool = ThreadPoolExecutor(max_workers=args.threads)

if args.range:
    try:
        for ip in ipaddress.IPv4Network(args.range):
            pool.submit(scan, str(ip))

        pool.shutdown(wait=True)

    except Exception as ex:
        print("Error while trying to scan range: " + str(ex))

elif args.ip_address:
    try:
        scan(args.ip_address)
    except Exception as ex:
        print("Error while scanning single IP address: " + str(ex))

else:
    parser.print_help()
