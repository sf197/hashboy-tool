#!/usr/bin/env python3

import re
import os
import sys
import requests
import argparse
import concurrent.futures

print ('''\033[1;97m    __               __    __               
   / /_  ____ ______/ /_  / /_  ____  __  __
  / __ \/ __ `/ ___/ __ \/ __ \/ __ \/ / / /
 / / / / /_/ (__  ) / / / /_/ / /_/ / /_/ / 
/_/ /_/\__,_/____/_/ /_/_.___/\____/\__, /  
                                   /____/
\033[92mAuthor:Leiothrix  Github:https://github.com/sf197\033[0m\n''')

parser = argparse.ArgumentParser()
parser.add_argument('-s','--hash', help='hash', dest='hash')
parser.add_argument('-f','--file', help='file containing hashes', dest='file')
parser.add_argument('-t','--threads', help='number of threads', dest='threads', type=int)
args = parser.parse_args()

#Colors and shit like that
end = '\033[0m'
red = '\033[91m'
green = '\033[92m'
white = '\033[97m'
dgreen = '\033[32m'
yellow = '\033[93m'
back = '\033[7;91m'
run = '\033[97m[~]\033[0m'
que = '\033[94m[?]\033[0m'
bad = '\033[91m[-]\033[0m'
info = '\033[93m[!]\033[0m'
good = '\033[92m[+]\033[0m'

if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

cwd = os.getcwd()
file = args.file
thread_count = args.threads or 4

dist = args.hash
if dist.isdigit()==True and dist.isalpha()==True and dist.isalnum()==False:
    print ('%s This hash type is not supported.' % bad)
    sys.exit(1)

def cmd5(hashvalue, hashtype):
    response = requests.get('http://www.cmd5.com').text
    match = re.search(r'id="__EVENTTARGET" value="(.*?)"', response)
    list = [match.group(1)]
    match = re.search(r'id="__VIEWSTATE" value="(.*?)"', response)
    list += [match.group(1)]
    match = re.search(r'id="__VIEWSTATEGENERATOR" value="(.*?)"', response)
    list += [match.group(1)]
    match = re.search(r'id="ctl00_ContentPlaceHolder1_HiddenField2" value="(.*?)"', response)
    list += [match.group(1)]
    data = {"__EVENTTARGET": list[0],"__VIEWSTATE": list[1],"__VIEWSTATEGENERATOR": list[2],"ctl00$ContentPlaceHolder1$TextBoxInput": hashvalue,"ctl00$ContentPlaceHolder1$InputHashType": hashtype,"ctl00$ContentPlaceHolder1$Button1": "\u67e5\u8be2","ctl00$ContentPlaceHolder1$HiddenField1": "","ctl00$ContentPlaceHolder1$HiddenField2": list[3]}
    rtext = requests.post('http://www.cmd5.com', data=data, headers={'referer':'http://www.cmd5.com'}).text
    hashtype = re.search(r'selected="selected" value="(.+?)"', rtext)
    match = re.search(r'LabelAnswer" onmouseover="toggle\(\);">(.+?)<\/span>', rtext)
    if match:
        return match.group(1)+"(hash-type:"+hashtype.group(1)+")"
    else:
    	return False

def hashtoolkit(hashvalue, hashtype):
    response = requests.get('http://hashtoolkit.com/reverse-hash/?hash=', hashvalue).text
    match = re.search(r'/generate-hash/?text=.*?"', response)
    if match:
        return match.group(1)
    else:
        return False

def gamma(hashvalue, hashtype):
    response = requests.get('http://www.nitrxgen.net/md5db/' + hashvalue).text
    if response:
        return response
    else:
        return False


def theta(hashvalue, hashtype):
    response = requests.get('http://md5decrypt.net/Api/api.php?hash=%s&hash_type=%s&email=deanna_abshire@proxymail.eu&code=1152464b80a61728' % (hashvalue, hashtype)).text
    if len(response) != 0:
        return response
    else:
        return False

def haq4u(hashvalue, hashtype):
    response = requests.get('http://' + hashvalue + '.haq4u.com').text
    match = re.search(r'.haq4u.com">(.+?)</a></br>', response)
    if match:
        return match.group(1)
    else:
    	return False

def bugbank(hashvalue, hashtype):
    data = {'md5text': hashvalue}
    response = requests.post('https://www.bugbank.cn/api/md5', data).text
    match = re.search(r'"answer":"(.+?)"', response)
    if match:
        return match.group(1)
    else:
    	return False

def gongjuji(hashvalue, hashtype):
    response = requests.get('http://md5.gongjuji.net/common/md5dencrypt/?UpperCase=' + hashvalue).text
    match = re.search(r'"PlainText":"(.+?)"', response)
    if match:
        return match.group(1)
    else:
    	return False

def mysql(hashvalue, hashtype):
    data = {'hash': hashvalue}
    response = requests.post('https://www.mysql-password.com/api/get-password', data=data).text
    match = re.search(r'"password":"(.+?)"', response)
    if match:
        return match.group(1)+"(hash-type:mysql)"
    else:
    	return False



md5 = [cmd5, gamma, hashtoolkit, theta, haq4u, bugbank, gongjuji]
sha1 = [cmd5, mysql, hashtoolkit, theta, bugbank]
sha256 = [cmd5, hashtoolkit, theta]
sha384 = [cmd5, hashtoolkit, theta]
sha512 = [cmd5, hashtoolkit, theta]

def crack(hashvalue):
    result = False
    if len(hashvalue) == 16:
        if not file:
            print ('%s Hash function : MD5-16' % info)
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return good + "->" + r
    elif len(hashvalue) == 32:
        if not file:
            print ('%s Hash function : MD5' % info)
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return good + "->" + r
    elif len(hashvalue) == 40:
        if not file:
            print ('%s Hash function : SHA1' % info)
        for api in sha1:
            r = api(hashvalue, 'sha1')
            if r:
                return good + "->" + r
    elif len(hashvalue) == 64:
        if not file:
            print ('%s Hash function : SHA-256' % info)
        for api in sha256:
            r = api(hashvalue, 'sha256')
            if r:
                return good + "->" + r
    elif len(hashvalue) == 96:
        if not file:
            print ('%s Hash function : SHA-384' % info)
        for api in sha384:
            r = api(hashvalue, 'sha384')
            if r:
                return good + "->" + r
    elif len(hashvalue) == 128:
        if not file:
            print ('%s Hash function : SHA-512' % info)
        for api in sha512:
            r = api(hashvalue, 'sha512')
            if r:
                return good + "->" + r
    else:
        if not file:
            print ('%s This hash type is not supported.Only [MD5,sha1,sha256,sha384,sha512,mysql5] is allowed' % bad)
            quit()
        else:
            return False

result = {}

def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        print (hashvalue + ' : ' + resp)
        result[hashvalue] = resp

def miner(file):
    lines = []
    found = set()
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.strip('\n'))
    for line in lines:
        matches = re.findall(r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}|[a-f0-9]{16}', line)
        if matches:
            for match in matches:
                found.add(match)
    print ('%s Hashes found: %i' % (info, len(found)))
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
    futures = (threadpool.submit(threaded, hashvalue) for hashvalue in found)
    for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        if i + 1 == len(found) or (i + 1) % thread_count == 0:
            print('%s Progress: %i/%i' % (info, i + 1, len(found)), end='\r')

def single(args):
    result = crack(args.hash)
    if result:
        print (result)
    else:
        print ('%s Hash was not found in any database.' % bad)

if file:
    try:
        miner(file)
    except KeyboardInterrupt:
        pass
    with open('hash-%s' % file.split('/')[-1], 'w+') as f:
        for hashvalue, cracked in result.items():
            f.write(hashvalue + ':' + cracked + '\n')
    print ('%s Results saved in cracked-%s' % (info, file.split('/')[-1]))

elif args.hash:
    single(args)
