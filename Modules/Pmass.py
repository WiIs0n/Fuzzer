#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colored import fg, bg, attr

payloads_mass_str = []
payloads_mass_int = []
payloads_mass_bool = []
payloads_mass_float = []

def create_mass_with_payloads():
    try:
        file = open("./Payloads/payloads_str.txt", 'r')
    except Exception as error:
	    pass
	    print("{}Problem with payload file:{}".format(fg(1), attr(0)), error)
	    exit()

    for line in file:
        payloads_mass_str.append(line.rstrip().lstrip())

    file.close()


    try:
        file = open("./Payloads/payloads_int.txt", 'r')
    except Exception as error:
	    pass
	    print("{}Problem with payload file:{}".format(fg(1), attr(0)), error)
	    exit()

    for line in file:
        payloads_mass_int.append(line.rstrip().lstrip())

    file.close()


    try:
        file = open("./Payloads/payloads_bool.txt", 'r')
    except Exception as error:
	    pass
	    print("{}Problem with payload file:{}".format(fg(1), attr(0)), error)
	    exit()

    for line in file:
        payloads_mass_bool.append(line.rstrip().lstrip())

    file.close()


    try:
        file = open("./Payloads/payloads_float.txt", 'r')
    except Exception as error:
	    pass
	    print("{}Problem with payload file:{}".format(fg(1), attr(0)), error)
	    exit()

    for line in file:
        payloads_mass_float.append(line.rstrip().lstrip())

    file.close()

    return