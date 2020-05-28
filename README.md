
# Fuzzer
Current Release: v0.1 (06.05.2020)

# Foreword!
This is my first program, if you have any idea about how to improve it or you find bug, please contact me!  
https://t.me/WiIIson

# Overview
This program is made for parameters fuzzing automation in big requests. The program finds changes in the response's length during fuzzing and informs the user about it. The script runs Python 3.

# Operating Systems supported
- Windows XP/7/8/10
- GNU/Linux
- MacOSX

# What does the tool can?
- Fuzzing POST parameters
- Fuzzing POST parameters in JSON format
- Fuzzing GET parameters

# Features
- Multithreaded
- HTTP proxy support
- Burp proxy support (you can immediately see all the requests with payloads in Burp Suite)
- It is easy to use
- You can send file with user payloads to programm for fuzzing parameters
- You can add your own payloads for fuzzing
- You no longer need to think about headers and cookies, just send full request from Burp Suite to the Fuzzer and the program will parse the request itself
- The program determines the data type of each parameter (String, Integer, Float, Boolean) from the request (the type of payload depends on this)

# How to use it?
The program sends requests with different payloads and displays a message if the length of the response with the sent payload has changed. You must pay attention to the length of the response and the status of the response.

  --url&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag to send the url of the address  
  --data&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send the POST parameters  
  --threads&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for multithreading  
  --headers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send headers ("Header_1: value_1, Header_2: value_2")  
  --cookies&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send cookies ("PHPSESSID_1=value_1; PHPSESSID_2=value_2")  
  --burp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for get result in Burp. Input ip:port your Burp Suite proxy  
  --proxy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for requests through proxy server. Input ip:port your proxy server  
  --file&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send path to your file with  full request from Burp Suite   
  --payloads&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use this flag for send path to your file with user payloads

__For fuzzing GET parameters use the following commands:__  

`python3 Fuzzer.py --url "https://example.com?param1=1234&param2=ololo"`  

`python3 Fuzzer.py --url "https://example.com?param1=1234&param2=ololo" --headers "Referer: value" --cookies "PHPSESSID=value" --threads 5`

__For fuzzing POST parameters use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --data "param1=1234&param2=ololo"`

`python3 Fuzzer.py --url "https://example.com" --data "param1=1234&param2=ololo" --headers "Referer: value" --proxy 127.0.0.1:9050`

__For fuzzing POST parameters in JSON format use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --data '{"param1":1234, "param2":"ololo"}'`

`python3 Fuzzer.py --url "https://example.com" --data '{"param1":1234, "param2":"ololo"}' --burp 127.0.0.1:8080`

__For fuzzing POST and GET parameters from file with request use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt"`  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt" --threads 4 --proxy 127.0.0.1:9050`  

__For fuzzing parameters from file with user payloads:__ 

`python3 Fuzzer.py --url "https://example.com" --data 'param1=1234&param2=ololo*' --payloads "/home/payloads.txt"`
 
If you use the --payloads flag, you must specify the option whitch you fuzzing:
\* - add payload where there is an asterisk. (par=123* -> par=123PAYLOAD)
\*\* - using a double asterisk you can replace the parameter value with payload. (par=123** -> par=PAYLOAD)

__For fuzzing POST parameters in JSON format from file with request use the following commands:__  

`python3 Fuzzer.py --url "https://example.com" --file "~/Desktop/request.txt"`  

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

# In the future
- Add fuzzing for headers  
- Add fuzzing for cookies  
- Add random user agent  
- The analyzer of the response, which will search anomalies while fuzzing, for example sql errors and so on  
