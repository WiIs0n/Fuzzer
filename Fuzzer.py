#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  Author: Danil
#  Nickname: Wils0n
#  Telegram: https://t.me/WiIIson
#  Contact with me if you have idea how make this programm better or you find bug in program.

import argparse
import threading
from colored import fg, bg, attr

from Modules.Pmass import *
from Modules.Parser import *

print("\n{}%{}{}00000000{}                                   ".format(fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}000000{}                                   {}%{}{}0d%00{}    ".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}00{}                               {}%{}{}000d0A{} {}%{}{}0d  %0{}    ".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}00000{} {}%{}{}0d{}   {}%{}{}0D{} {}[union] [select]{} {}%{}{}00{}     {}%{}{}0a--%0{}   ".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}000{}   {}%{}{}0d{}   {}%{}{}0D{}    {}%{}{}0A{}      {}%{}{}0D{}  {}%{}{}0000{}   {}%{}{}0a\"\"{}   ".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}00{}     {}%{}{}0d{}  {}%{}{}0D{}  {}%{}{}0A{}     {}%{}{}0D{}     {}%{}{}00{}     {}%{}{}0a %00{}   ".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("{}%{}{}00{}       {}%{}{}OdOD{}  {}[union] [select]{} {}%{}{}000d0D{} {}%{}{}0D  %00{}  \n".format(fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0), fg(1), attr(0), fg(220), attr(0)))
print("Enter --help if you want to know about the features of the program.\n")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help = True, formatter_class = argparse.RawDescriptionHelpFormatter, epilog = """examples:
    If your request in file:
        python3 Fuzzer.py --file ~/Desktop/request.txt --thread 3 --url "https://example.com"
        python3 Fuzzer.py --file ~/Desktop/request.txt --thread 3 --url "https://example.com" --json

    Without file:
        python3 Fuzzer.py --url "https://example.com?param1=123&param2=True"
        python3 Fuzzer.py --url "https://example.com?param1=123&param2=True" --proxy 111.222.333.444:8787
        python3 Fuzzer.py --url "https://example.com?param1=123&param2=True" --data "param1=True&param2=1234" --burp 127.0.0.1:8080
        python3 Fuzzer.py --url "https://example.com?param1=123&param2=True" --data '{"param1":1234, "param2":True, "param3":"ololo"}' --json
        python3 Fuzzer.py --url "https://example.com?param1=123&param2=True" --headers "Header_1: value_1, Header_2: value_2" --cookies "PHPSESSID_1=value_1"
    """)
    parser.add_argument('--url', type = str, help = 'Input URL address in quotes', required=True)
    parser.add_argument('--data', type = str, help = 'Input POST parameters in quotes')
    parser.add_argument('--file', type = str, help = 'Input path to your file with request from Burp Suite')
    parser.add_argument('--threads', type = int, help = 'Input number of threads')
    parser.add_argument('--json', action = 'store_true', help = 'Use this flag if your POST parameters in JSON format')
    parser.add_argument('--proxy', type = str, help = "Input ip:port your proxy server")
    parser.add_argument('--burp', type = str, help = "Input ip:port your Burp Suite proxy")
    parser.add_argument('--headers', type = str, help = "Input your headers in quotes (\"Header_1: value_1, Header_2: value_2\")")
    parser.add_argument('--cookies', type = str, help = "Input your cookies in quotes (\"PHPSESSID_1=value_1; PHPSESSID_2=value_2\")")
    args = parser.parse_args()


    create_mass_with_payloads()

    if args.proxy == None and args.burp == None:
        proxy = {}
    elif args.proxy != None:
        proxy = {"http":"socks4://{}".format(args.proxy),
                 "https":"socks4://{}".format(args.proxy)}
    elif args.burp != None:
        proxy = {"http":"http://{}".format(args.burp),
                 "https":"https://{}".format(args.burp)}

    if args.threads == None:
        threads = 1
    elif args.threads != None:
        threads = args.threads

    if args.file != None:
        if args.url == None:
            print("{}Input URL address in format https://example.com{}".format(fg(1), attr(0))) 
            exit()
        else:
            data_parser(args.file, args.url, threads, args.json, proxy)
    else:
        data_parser_without_file(args.url, args.data, threads, proxy, args.json, args.headers, args.cookies)
