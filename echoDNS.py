#!/usr/bin/python3
import certifi
import dns.resolver
import requests
import argparse
from colorama import Fore, Style, init
import pyfiglet


# ANSI color codes
BLUE = "\033[94m"
RESET = "\033[0m"

#make ASCII art banner
def printBanner():
    init(autoreset=True)
    banner = pyfiglet.figlet_format("EchoDNS", font="slant")
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}A Comprehensive DNS Query Tool{Style.RESET_ALL}\n")
    print(f"{Fore.MAGENTA}Developed by Mostafa Shaaban{Style.RESET_ALL}\n")
    print(f"{Fore.MAGENTA}V1.0{Style.RESET_ALL}\n")



dnsRecords = ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT"]


# Standard DNS query method
def queryDNS(domain, recordType=None, dnsServer=None, useDoH=False, baseurl=None):
    
    resolver = dns.resolver.Resolver()
    if dnsServer:
        resolver.nameservers = [dnsServer]
    results = []
    recordList = [recordType] if recordType else dnsRecords
    for record in recordList:
        try:
            if useDoH:
                result = queryDNSOverHTTPS(domain, record, baseurl)
                if result:
                    for line in result:
                        results.append(line)
            else:
                answers = resolver.resolve(domain, record)
                for rdata in answers:
                    results.append((record, rdata.to_text()))
        except dns.resolver.NoAnswer:
            print(f"\033[93mNo {record} record found for {domain}\033[0m")
        except dns.resolver.NXDOMAIN:
            print(f"\033[91mNo such domain: {domain}\033[0m")
            return
        except Exception as e:
            print(f"\033[91mError querying {record} : {e}\033[0m")


    print(f"\n{'Record':<8} | Value")
    print('-' * 40)
    for rec, val in results:
        print(f"\033[92m{rec:<8}\033[0m | {val}")
    return results


# DNS over HTTPS method
def queryDNSOverHTTPS(domain, recordType=None, baseurl=None):
    results = []
    recordList = [recordType] if recordType else dnsRecords
    headers = {'Accept': 'application/dns-json'}


    # Default baseurl if not provided
    if not baseurl:
        baseurl = "https://dns.google/resolve"


    for record in recordList:
        url = f"{baseurl}?name={domain}&type={record}"
        try:
            response = requests.get(url, headers=headers, verify=certifi.where())
            response.raise_for_status()
            data = response.json()
            if "Answer" not in data:
                print(f"\033[93mNo {record} record found for {domain}\033[0m")
                continue
            for answer in data["Answer"]:
                results.append((record, answer["data"]))
        except requests.exceptions.RequestException as e:
            print(f"\033[91mError querying {record} : {e}\033[0m")
    if results:
        print(f"\n{BLUE}Results for {record} records via DoH:{RESET}")
        print(f"\n{'Record':<8} | Value")
        print('-' * 40)
        for rec, val in results:
            print(f"\033[92m{rec:<8}\033[0m | {val}")
    else:
        print(f"\033[93mNo records found for {domain}\033[0m")
    return results


# AXFR method (with resolver for nameserver)
def performAXFR(domain, nameserver):
    
    import traceback
    init(autoreset=True)

    try:
        print(f"{Fore.MAGENTA}[Output Colors ]{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW} Info:{Style.RESET_ALL}     General progress & actions")
        print(f"  {Fore.GREEN} Success:{Style.RESET_ALL}  Successful operations or retrieved records")
        print(f"  {Fore.RED} Error:{Style.RESET_ALL}     Failures, refused transfers, or timeouts")
        print(f"  {Fore.CYAN} Type:{Style.RESET_ALL}      DNS record type (A, MX, TXT, etc.)")
        print("-" * 80 + "\n")

        print(f"{Fore.YELLOW}[*] Resolving nameserver {nameserver} ...{Style.RESET_ALL}")
        ns_ip = dns.resolver.resolve(nameserver, "A")[0].to_text()
        print(f"{Fore.CYAN}[*] Using IP {ns_ip} for AXFR\n{Style.RESET_ALL}")

        print(f"{Fore.YELLOW}[*] Attempting AXFR for {domain} from {ns_ip} ...{Style.RESET_ALL}\n")
        xfr = dns.query.xfr(ns_ip, domain, lifetime=15)
        zone = dns.zone.from_xfr(xfr)

        print(f"{Fore.GREEN}AXFR results for {domain} from {nameserver} ({ns_ip}):{Style.RESET_ALL}\n")
        print(f"{'Name':<30} {'TTL':<8} {'Class':<6} {'Type':<8} Value")
        print(f"{'-'*100}")

        record_count = 0
        for name, node in zone.nodes.items():
            for rdataset in node.rdatasets:
                ttl = rdataset.ttl
                rdtype = dns.rdatatype.to_text(rdataset.rdtype)
                for rdata in rdataset:
                    record_count += 1
                    print(f"{Fore.GREEN}{str(name):<30}{Style.RESET_ALL} "
                          f"{ttl:<8} IN     {Fore.CYAN}{rdtype:<8}{Style.RESET_ALL} "
                          f"{rdata.to_text()}")

        print(f"\n{Fore.YELLOW}[+] Total records retrieved: {record_count}{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}[✓] AXFR completed successfully!{Style.RESET_ALL}")

    except dns.exception.FormError:
        print(f"{Fore.RED}[!] AXFR refused or not supported by {nameserver}{Style.RESET_ALL}")
    except dns.exception.Timeout:
        print(f"{Fore.RED}[!] AXFR request to {nameserver} timed out{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error performing AXFR for {domain} from {nameserver}{Style.RESET_ALL}")
        print(f"    → Exception Type: {type(e).__name__}")
        print(f"    → Exception Message: {repr(e)}")
        print("    → Traceback (most recent call last):")
        traceback.print_exc()

# Main entry point
if __name__ == "__main__":
    printBanner()
    parser = argparse.ArgumentParser(description="EchoDNS Tool")
    parser.add_argument("-d", "--domain", nargs='+', help="Domain(s) to query", required=True)
    parser.add_argument("-t", "--type", help="Type of DNS record to query (e.g., A, MX, CNAME), default is all types")
    parser.add_argument("--doh", action="store_true", help="Use DNS over HTTPS (DoH)")
    parser.add_argument("-s", "--server", help="Specify DNS server to use", default=None)
    parser.add_argument("--axfr", action="store_true", help="Perform AXFR from specified nameserver")
    parser.add_argument("--baseurl", help="Base URL for DoH server - e.g. https://dns.google/resolve", default=None)

    args = parser.parse_args()

    for domain in args.domain:
        if args.axfr:
            if not args.server:
                print("\033[91mNameserver must be specified for AXFR using -s option\033[0m")
            else:
                performAXFR(domain, args.server)
        elif args.doh:
            queryDNSOverHTTPS(domain, args.type, args.baseurl)
        else:
            queryDNS(domain, args.type, args.server, args.doh, args.baseurl)
