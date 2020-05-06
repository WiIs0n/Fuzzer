
# Fuzzer
Current Release: v0.1 (06.05.2020)

# Overview
This program made for automatical process fuzzing of parameters in big requests. The program finds changes in the length of the response when fuzzing and reports about it. For explotation this programm you need Python 3.

# Operating Systems supported
- Windows XP/7/8/10
- GNU/Linux
- MacOSX

# What can tool?
- Fuzzing POST parameters
- Fuzzing POST parameters in JSON format
- Fuzzing GET parameters

# Features
- Multithreaded
- HTTP proxy support
- Burp proxy support (you can immediately see all the requests with payloads in Burp Suite)
- It is easy to use
- You can add your own payloads for fuzzing
- You no longer need to think about headers and cookies, just send full request from Burp Suite to the Fuzzer and the program will parse the request itself
- The program determines the data type of each parameter (String, Integer, Float, Boolean) from the request (the type of payload depends on this)

# How it use?
  --url&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input URL address in quotes  
  --data&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input POST parameters in quotes  
  --threads&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input number of threads  
  --headers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input your headers in quotes ("Header_1: value_1, Header_2: value_2")  
  --cookies&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input your cookies in quotes ("PHPSESSID_1=value_1; PHPSESSID_2=value_2")  
  --burp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input ip:port your Burp Suite proxy  
  --proxy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input ip:port your proxy server  
  --file&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Input path to your file with request from Burp Suite  
  --json&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag if your POST parameters in JSON format  

__For fuzzing GET parameters without headers and cookies use the following command:__  
`python3 Fuzzer.py --url "https://example.com?param1=123&param2=True"`



