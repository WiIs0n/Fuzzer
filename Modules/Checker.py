#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from colored import fg, bg, attr

def check_request(headers, cookies, method, url, str_parameters, json_flag, proxy):
	if json_flag == True:
		json_params = json.dumps(str_parameters)
		try:
			req = requests.request(method = method, url = url, cookies = cookies, headers = headers, data = json.loads(json_params), proxies = proxy, verify = False)
		except Exception as error:
			pass
			print("{}Error in current request to {}:{} {}".format(fg(1), url, attr(0), error))
			exit()
		

	if method == 'GET':
		str_post_params = ''
	elif method == 'POST':
		str_post_params = str_parameters

	try:
		req = requests.request(method = method, url = url, cookies = cookies, headers = headers, data = str_post_params, proxies = proxy, verify = False)
	except Exception as error:
		pass
		print("{}Error in current request to {}:{} {}".format(fg(1), url, attr(0), error))
		exit()

	if req.status_code == 200 or req.status_code == 302 or req.status_code == 302 or req.status_code == 201:
		print("~~~~~~~~~~ {}Current state{} ~~~~~~~~~~".format(fg(220), attr(0)))
		print("{}[+]{} Page is found. Status code: {}{}{}".format(fg(2), attr(0), fg(2), req.status_code, attr(0)))
		print("{}[+]{} Responce content length: {}{}{}".format(fg(2), attr(0), fg(2), len(req.content), attr(0)))
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

		return len(req.content)
	else:
		print("~~~~~~~~~~ {}Current state{} ~~~~~~~~~~".format(fg(220), attr(0)))
		print("{}[-]{} Problem with request. Status code: {}{}{}".format(fg(1), attr(0), fg(1), req.status_code, attr(0)))
		print("{}[+]{} Responce content length: {}{}{}".format(fg(2), attr(0), fg(2), len(req.content), attr(0)))
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		exit()