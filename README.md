
# Fuzzer
Current Release: v0.1 (06.05.2020)

# Foreword!
This is my first program, if you have ideas how to improve it, write to me!  
https://t.me/WiIIson

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
The program sends requests with different payloads and displays a message if the length of the response with the sent payload has changed. You must pay attention to the length of the response and the status of the response.

  --url&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag to send the url of the address  
  --data&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send the POST parameters  
  --threads&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for multithreading  
  --headers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send headers ("Header_1: value_1, Header_2: value_2")  
  --cookies&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send cookies ("PHPSESSID_1=value_1; PHPSESSID_2=value_2")  
  --burp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for get result in Burp. Input ip:port your Burp Suite proxy  
  --proxy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for requests through proxy server. Input ip:port your proxy server  
  --file&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send path to your file with  full request from Burp Suite   
  --json&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag if your POST parameters in JSON format  

__For fuzzing GET parameters use the following commands:__  

`python3 Fuzzer.py --url "https://example.com?param1=1234&param2=ololo"`  

`python3 Fuzzer.py --url "https://example.com?param1=1234&param2=ololo" --headers "Referer: value" --cookies "PHPSESSID=value" --threads 5`

__For fuzzing POST parameters use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --data "param1=1234&param2=ololo"`

`python3 Fuzzer.py --url "https://example.com" --data "param1=1234&param2=ololo" --headers "Referer: value" --proxy 127.0.0.1:9050`

__For fuzzing POST parameters in JSON format use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --data '{"param1":1234, "param2":"ololo"}' --json`

`python3 Fuzzer.py --url "https://example.com" --data '{"param1":1234, "param2":"ololo"}' --json --burp 127.0.0.1:8080`

__For fuzzing POST and GET parameters from file with request use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt"`  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt" --threads 4 --proxy 127.0.0.1:9050`  

__For fuzzing POST parameters in JSON format from file with request use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt" --json`  

![Альтернативный текст](https://github.com/WiIs0n/Fuzzer/blob/master/README_img/img1.jpg)

# How to add your payloads?
In the Payloads folder you can find files with templates for different types of data. Choose which data type your payload belongs to and add it to the file using the template.

__Example:__

Payload: <b>[]</b>  
Template: key<b>[]</b>=value  
Result: param1=1234  ->  param1<b>[]</b>=1234  

__Example:__

Payload: <b>%00</b>  
Template: key=value<b>%00</b>  
Result: param1=1234  ->  param1=1234<b>%00</b>  

__Example:__

Payload: <b>%0A%0D</b>  
Template: key=EMPTYvalue<b>%0A%0D</b>  
Result: param1=1234  ->  param1=<b>%0A%0D</b>  

