#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3, warnings
warnings.simplefilter('ignore', urllib3.exceptions.SecurityWarning)

import requests
import json
import re
import queue
import urllib.parse
from ast import literal_eval
from colored import fg, bg, attr
from Modules.Pmass import payloads_mass_bool, payloads_mass_int, payloads_mass_str, payloads_mass_float

def fuzzer(method, url, str_parameters, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy, payloads_file, parameters_in_json_with_start):
	while True:
		if payloads_queue.empty() == True:
			exit()
		else:
			parameter = payloads_queue.get()

			if json_flag == True:			
				
				if parameter.find("None") != -1:
					parameter = parameter.replace("None", "null")

				data_type = check_type(parameter)
				if data_type == "bool":
					parameter = parameter.replace("False", "false").replace("True", "true")

				param_key_value = parameter.split('=', 1)
				mass_with_templates = 'payloads_mass_{}'.format(data_type)

				for template in globals()[mass_with_templates]:
					
					template = template.replace("\\", "\\\\").replace('"', '\\"')

					if template.find('EMPTYvalue') != -1:
						template_with_payload = template.replace('key', param_key_value[0]).replace('EMPTYvalue', '')
						mass_template_with_payload = template_with_payload.split('=', 1)
						params_with_payload = str_parameters.replace(param_key_value[0], mass_template_with_payload[0]).replace(param_key_value[1], mass_template_with_payload[1])
						val = 'EMPTYvalue'
					else:
						template_with_payload = template.replace('key', param_key_value[0]).replace('value', param_key_value[1])
						mass_template_with_payload = template_with_payload.split('=', 1)
						params_with_payload = str_parameters.replace(param_key_value[0], mass_template_with_payload[0]).replace(param_key_value[1], mass_template_with_payload[1])
						val = 'value'

					vihlop = search_payload(template, str_parameters, val, json_flag, param_key_value)

					try:
						req = requests.request(method = method, url = url, cookies = cookies, headers = headers, data = params_with_payload, proxies = proxy, verify = False, allow_redirects = False)
					except Exception as error:
						pass
						print("{}Problem with request during fuzzing:{}".format(fg(1), attr(0)), error)
						continue
				
					if length != len(req.content):
						print_result(req.status_code, len(req.content), vihlop)
					else:
						continue

			else:

				param_key_value = parameter.split('=')	
				data_type = check_type(parameter)			

				mass_with_templates = 'payloads_mass_{}'.format(data_type)
				
				for template in globals()[mass_with_templates]:
					if template.find('EMPTYvalue') != -1:
						params_with_payload = str_parameters.replace(str(parameter), template.replace('key', param_key_value[0]).replace('EMPTYvalue', ''))
						val = 'EMPTYvalue'
					else:
						params_with_payload = str_parameters.replace(str(parameter), template.replace('key', param_key_value[0]).replace('value', param_key_value[1]))
						val = 'value'
					
					vihlop = search_payload(template, params_with_payload, val, json_flag, '')

					if method == 'GET':
						get_params_with_payload = params_with_payload
						params_with_payload = ''
					elif method == 'POST':
						get_params_with_payload = ''

					try:
						req = requests.request(method = method, url = url, params = get_params_with_payload, cookies = cookies, headers = headers, data = params_with_payload, proxies = proxy, verify = False, allow_redirects = False)
					except Exception as error:
						pass
						print("{}Problem with request during fuzzing:{}".format(fg(1), attr(0)), error)
						continue

					if length != len(req.content):
						print_result(req.status_code, len(req.content), vihlop)
					else:
						continue

def check_type(parameter):
	value_type = parameter.split('=')[1].strip()
	try:
		form = type(literal_eval(value_type))
	except Exception as error:
		pass
		form = 'str'
		return form

	return re.search("\<class \'([a-z]+)\'\>", str(form)).group(1)



def search_payload(template, params_with_payload, val, json_flag, param_key_value):
	if json_flag == True:
		payload = template.replace('key', '').replace('EMPTYvalue', '').replace('value', '').replace('=', '').strip()
		red_template = template.replace(payload, fg(1) + '{}'.format(payload) + attr(0))

		if val == 'EMPTYvalue':
			template_with_payload = red_template.replace('key', param_key_value[0]).replace('EMPTYvalue', '')
			mass_template_with_payload = template_with_payload.split('=')
			params_with_payload = params_with_payload.replace(param_key_value[0], mass_template_with_payload[0]).replace(param_key_value[1], mass_template_with_payload[1])
		elif val == 'value':
			template_with_payload = red_template.replace('key', param_key_value[0]).replace('value', param_key_value[1])
			mass_template_with_payload = template_with_payload.split('=')
			params_with_payload = params_with_payload.replace(param_key_value[0], mass_template_with_payload[0]).replace(param_key_value[1], mass_template_with_payload[1])

		return params_with_payload
	else:
		payload = template.replace('key', '').replace(val, '').replace('=', '')
		parameters_with_payload = params_with_payload.split(payload, 1)
		return parameters_with_payload[0] + fg(1) + payload + attr(0) + parameters_with_payload[1]

def search_payload_start(str_parameters, payload):
	return str_parameters.replace("*", "{}{}{}".format(fg(1), payload, attr(0)))

def print_result(status_code, length, vihlop):
	if (status_code == 200 or status_code == 302 or status_code == 301):
		print("{}[+]{} Status code: {}{}{} Content length: {}{}{} \n {} \n".format(fg(2), attr(0), fg(2), status_code, attr(0), fg(2), length, attr(0), vihlop))
	elif status_code != 200 and status_code != 302 and status_code != 301:
		print("{}[+]{} Status code: {}{}{} Content length: {}{}{} \n {} \n".format(fg(2), attr(0), fg(1), status_code, attr(0), fg(2), length, attr(0), vihlop))

def fuzzer_user_payloads(method, url, str_parameters, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy, payloads_file, parameters_in_json_with_start):
	if url.find("*") != -1 or str_parameters.find("*") != -1 or parameters_in_json_with_start.find("*") != -1:
		users_payload_queue = queue.Queue()

		file = open(payloads_file, 'r')
		for line in file:
			users_payload_queue.put(line.strip())
			#print(urllib.parse.quote(payload)) //////////////////////////////////// ПОСМОТРЕТЬ НАДО ЛИ ЭТО

		if json_flag == True:
			str_parameters = parameters_in_json_with_start
			str_parameters = str_parameters.replace("False", "false").replace("True", "true")

			mass_params = str_parameters.split(",")

			str_parameters = ""

			for line in mass_params:
				if line.find("**") != -1:
					mass_line = line.split(":")
					
					if mass_line[1].find('"') != -1:
						line = mass_line[0] + ':"*"'
					elif mass_line[1].find('"') == -1:
						line = mass_line[0] + ':*'

					if mass_line[1].find("}") != -1:
						line = line + "}"

				str_parameters = str_parameters + line + ","

			str_parameters = str_parameters.rstrip(",")
			
			while True:
				if users_payload_queue.empty() == True:
					exit()
				else:
					payload = users_payload_queue.get()
					payload = payload.replace("\\", "\\\\").replace('"', '\\"')
					vihlop = search_payload_start(str_parameters, payload)

					params_with_payload = str_parameters.replace("*", payload)

					try:
						req = requests.request(method = method, url = url, cookies = cookies, headers = headers, data = params_with_payload, proxies = proxy, verify = False, allow_redirects = False)
					except Exception as error:
						pass
						print("{}Problem with request during fuzzing:{}".format(fg(1), attr(0)), error)
						continue
				
					if length != len(req.content):
						print_result(req.status_code, len(req.content), vihlop)
					else:
						continue


		if json_flag == False:
			if str_parameters.find("**") != -1:
				mass_params = str_parameters.strip().split("&")

				str_parameters = ""

				for line in mass_params:
					if line.find("**") != -1:
						line = line.split("=")[0] + "=*"
					str_parameters = str_parameters + line + "&"

				str_parameters = str_parameters.rstrip("&")

			while True:
				if users_payload_queue.empty() == True:
					exit()
				else:
					payload = users_payload_queue.get()
					vihlop = search_payload_start(str_parameters, payload) 

					if method == 'GET':
						get_params_with_payload = str_parameters.replace("*", payload)
						params_with_payload = ''
					elif method == 'POST':
						get_params_with_payload = ''
						params_with_payload = str_parameters.replace("*", payload)

					try:
						req = requests.request(method = method, url = url, params = get_params_with_payload, cookies = cookies, headers = headers, data = params_with_payload, proxies = proxy, verify = False, allow_redirects = False)
					except Exception as error:
						pass
						print("{}Problem with request during fuzzing:{}".format(fg(1), attr(0)), error)
						continue

					if length != len(req.content):
						print_result(req.status_code, len(req.content), vihlop)
					else:
						continue

	else:
		print("{}[!]{} Add * or ** to specify a parameter for fuzzing.".format(fg(1), attr(0)))