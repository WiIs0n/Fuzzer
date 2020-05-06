#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import queue
from colored import fg, bg, attr
from Modules.Checker import *
from Modules.Fuzz import *

cookies = {}
headers = {}
payloads_queue = queue.Queue()

def h_and_c(headers_and_cookies):
    for line in headers_and_cookies:
        if line.find('Cookie') != -1:
            line = line.split(':', 1)
            line = line[1].split(';')
            line = [i for i in line if i != '']
            for drop_line in line:
                drop_line = drop_line.split('=', 1)
                cookies[drop_line[0].lstrip().rstrip()] = drop_line[1].lstrip().rstrip()
        else:
            line = line.split(':', 1)
            headers[line[0].lstrip().rstrip()] = line[1].lstrip().rstrip()


def data_parser(path_to_file, url_form_user, threads, json_flag, proxy):
    try:
        with open(path_to_file, 'r') as f:
            file_lines = f.read().strip().splitlines()
    except Exception as error:
        print("{}Problem with request file:{}".format(fg(1), attr(0)), error)
        exit()

    f.close()

    headers_and_cookies = [i for i in file_lines if i != '' and i.find('Connection') == -1 and i.find('Host') == -1]

    hat_of_request = headers_and_cookies[0].split(' ')
    del(headers_and_cookies[0])

    method = hat_of_request[0].strip()
    full_url = url_form_user + hat_of_request[1].strip()

    if json_flag == True:
        parameters_in_json = headers_and_cookies[len(headers_and_cookies) - 1].lstrip().rstrip()
        del(headers_and_cookies[len(headers_and_cookies) - 1])
                                            
        h_and_c(headers_and_cookies)
        length = check_request(headers, cookies, method, full_url, parameters_in_json, json_flag, proxy)
        
        jsonn = json.loads(parameters_in_json)
        mass_parameters = []
        for line in jsonn:
            mass_parameters.append(str(line) + "=" + jsonn['{}'.format(line)])

        for param in mass_parameters:
            payloads_queue.put(param.strip())

        for line in range(threads):
            th = threading.Thread(target = fuzzer, args = (method, full_url, parameters_in_json, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy))
            th.start()
            
    elif json_flag == False:
        if method == 'POST':
            str_parameters = headers_and_cookies[len(headers_and_cookies) - 1].strip()
            mass_parameters = str_parameters.split('&')
            del(headers_and_cookies[len(headers_and_cookies) - 1])
            url = full_url
        elif method == 'GET':
            str_parameters = hat_of_request[1].split('?', 1)[1].strip()
            mass_parameters = str_parameters.split('&')
            url = url_form_user + hat_of_request[1].split('?', 1)[0].strip()

        h_and_c(headers_and_cookies)
        length = check_request(headers, cookies, method, full_url, str_parameters, json_flag, proxy)

        for line in mass_parameters:
            payloads_queue.put(line.strip())

        for line in range(threads):
            th = threading.Thread(target = fuzzer, args = (method, url, str_parameters, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy))
            th.start()

def data_parser_without_file(url, data, threads, proxy, json_flag, h, c):
    if h != None:
        h_mass = h.split(',')

        for line in h_mass:
            line_mass = line.strip().split(':')
            try:
                headers[line_mass[0].lstrip().rstrip()] = line_mass[1].lstrip().rstrip()
            except Exception as error:
                pass
                continue

    if c != None:
        c_mass = c.split(';')

        for line in c_mass:
            line_mass = line.strip().split('=')
            try:
                cookies[line_mass[0].lstrip().rstrip()] = line_mass[1].lstrip().rstrip()
            except Exception as error:
                pass
                continue

    if json_flag == True:
        method = 'POST'
        full_url = url
        parameters_in_json = data

        length = check_request(headers, cookies, method, full_url, parameters_in_json, json_flag, proxy)
        
        jsonn = json.loads(parameters_in_json)
        mass_parameters = []
        for line in jsonn:
            mass_parameters.append(str(line) + "=" + jsonn['{}'.format(line)])

        for param in mass_parameters:
            payloads_queue.put(param.strip())
        
        for line in range(threads):
            th = threading.Thread(target = fuzzer, args = (method, full_url, parameters_in_json, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy))
            th.start()

    elif json_flag == False:
        if data == None:
            method = 'GET'
            full_url = url
            str_parameters = url.split('?', 1)[1].strip()
            mass_parameters = str_parameters.split('&')
            url = url.split('?', 1)[0].strip()
        elif data != None:
            method = 'POST'
            full_url = url
            str_parameters = data
            mass_parameters = str_parameters.split('&')

        length = check_request(headers, cookies, method, full_url, str_parameters, json_flag, proxy)

        for line in mass_parameters:
            payloads_queue.put(line.strip())

        for line in range(threads):
            th = threading.Thread(target = fuzzer, args = (method, url, str_parameters, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy))
            th.start()
