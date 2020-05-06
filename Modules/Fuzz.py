#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib3, warnings
warnings.simplefilter('ignore', urllib3.exceptions.SecurityWarning)

import requests
import json
import re
from ast import literal_eval
from colored import fg, bg, attr
from Modules.Pmass import payloads_mass_bool, payloads_mass_int, payloads_mass_str, payloads_mass_float

def fuzzer(method, url, str_parameters, mass_parameters, length, json_flag, cookies, headers, payloads_queue, proxy):
	while True:
		if payloads_queue.empty() == True:
			exit()
		else:
			parameter = payloads_queue.get()

			if json_flag == True:
				param_key_value = parameter.split('=', 1)
				data_type = check_type(parameter)
				mass_with_templates = 'payloads_mass_{}'.format(data_type)

				for template in globals()[mass_with_templates]:
					if data_type == 'str' and template.find('"') != -1:
						template = template.replace('"', '\\"')

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

def print_result(status_code, length, vihlop):
	if (status_code == 200 or status_code == 302 or status_code == 301):
		print("{}[+]{} Status code: {}{}{} Content length: {}{}{} \n {} \n".format(fg(2), attr(0), fg(2), status_code, attr(0), fg(2), length, attr(0), vihlop))
	elif status_code != 200 and status_code != 302 and status_code != 301:
		print("{}[+]{} Status code: {}{}{} Content length: {}{}{} \n {} \n".format(fg(2), attr(0), fg(1), status_code, attr(0), fg(2), length, attr(0), vihlop))
