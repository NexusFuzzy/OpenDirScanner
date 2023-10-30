# OpenDirScanner
Python tool to scan a single IP or CIDR range of IP addresses for open directories


  ____                   _____  _      _____                                 
 / __ \                 |  __ \(_)    / ____|                                
| |  | |_ __   ___ _ __ | |  | |_ _ _| (___   ___ __ _ _ __  _ __   ___ _ __ 
| |  | | '_ \ / _ \ '_ \| |  | | | '__\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
| |__| | |_) |  __/ | | | |__| | | |  ____) | (_| (_| | | | | | | |  __/ |   
 \____/| .__/ \___|_| |_|_____/|_|_| |_____/ \___\__,_|_| |_|_| |_|\___|_|   
       | |                                                                   
       |_|                                                                   

usage: OpenDirScanner [-h] [-r RANGE] [-i IP_ADDRESS] [-t THREADS] [-e] [-d]

Script to scan a range of IP addresses in CIDR format for Open Directories

options:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE
                        IP range in CIDR format (example: 192.168.0.1/24)
  -i IP_ADDRESS, --ip_address IP_ADDRESS
                        Scan single IP address
  -t THREADS, --threads THREADS
                        Number of concurrent threads when scanning a range
                        (default: 10)
  -e, --extract_links   Automatically extract found links
  -d, --download_files  Automatically download found links

Do not pwn what you do not own
