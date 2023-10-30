import argparse
import ipaddress
import os
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from pyfiglet import Figlet
from bs4 import BeautifulSoup
import urllib.request

pool = ThreadPoolExecutor(max_workers=10)
extract_links = False
download_files = False


def save_output(protocol, ip_address, content):
    try:
        print("Storing output to " + os.path.join(os.getcwd(), 'output', protocol + "_" + ip_address + ".txt"))
        if not os.path.isdir(os.path.join(os.getcwd(), 'output')):
            print("Creating output directory")
            os.mkdir(os.path.join(os.getcwd(), 'output'))

        with open(os.path.join(os.getcwd(), 'output', protocol + "_" + ip_address + ".txt"), 'w') as filehandle:
            filehandle.write(content)

        if extract_links:
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all("a")
            with open(os.path.join(os.getcwd(), 'output', protocol + "_" + ip_address + "_links.txt"), 'w') as filehandle:
                for l in links:
                    try:
                        filehandle.write(protocol + "://" + ip_address + l.get("href") + "\n")
                        if download_files:
                            if l.get("href") != "/":
                                if not os.path.isdir(os.path.join(os.getcwd(), 'output', ip_address)):
                                    print("Creating download directory")
                                    os.mkdir(os.path.join(os.getcwd(), 'output', ip_address))
                                file_path = os.path.join(os.getcwd(), 'output', ip_address, l.get("href").replace("\\", "").replace("/", ""))
                                print("Storing downloaded file to: " + file_path)
                                urllib.request.urlretrieve(protocol + "://" + ip_address + l.get("href"), file_path)
                    except Exception as ex:
                        print("Couldn't store downloaded file :" + str(ex))
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
parser.add_argument('-e', '--extract_links', help="Automatically extract found links", action="store_true")
parser.add_argument('-d', '--download_files', help="Automatically download found links", action="store_true")

args = parser.parse_args()

if args.threads:
    pool = ThreadPoolExecutor(max_workers=args.threads)

if args.extract_links:
    extract_links = True

if args.download_files:
    extract_links = True
    download_files = True

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
