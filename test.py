#!/usr/bin/env python3

import sys
import re
import os
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
parser.add_argument('-d','--dir', help='directory containing hashes', dest='dir')
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
directory = args.dir
file = args.file
thread_count = args.threads or 4

if directory:
    if directory[-1] == '/':
        directory = directory[:-1]

def delta(hashvalue, hashtype):
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
    match = re.search(r'LabelAnswer" onmouseover="toggle\(\);">(.+?)<\/span>', rtext)
    if match:
        return match.group(1)
    else:
    	return False



md5 = [delta]
#sha1 = [alpha, beta, theta, delta]
#sha256 = [alpha, beta, theta]
#sha384 = [alpha, beta, theta]
#sha512 = [alpha, beta, theta]

def crack(hashvalue):
    result = False
    if len(hashvalue) == 32:
        if not file:
            print ('%s Hash function : MD5' % info)
        for api in md5:
            r = api(hashvalue, 'md5')
            if r:
                return good + hashvalue + "->" + r
    elif len(hashvalue) == 40:
        if not file:
            print ('%s Hash function : SHA1' % info)
        for api in sha1:
            r = api(hashvalue, 'sha1')
            if r:
                return r
    elif len(hashvalue) == 64:
        if not file:
            print ('%s Hash function : SHA-256' % info)
        for api in sha256:
            r = api(hashvalue, 'sha256')
            if r:
                return r
    elif len(hashvalue) == 96:
        if not file:
            print ('%s Hash function : SHA-384' % info)
        for api in sha384:
            r = api(hashvalue, 'sha384')
            if r:
                return r
    elif len(hashvalue) == 128:
        if not file:
            print ('%s Hash function : SHA-512' % info)
        for api in sha512:
            r = api(hashvalue, 'sha512')
            if r:
                return r
    else:
        if not file:
            print ('%s This hash type is not supported.' % bad)
            quit()
        else:
            return False

result = {}

def threaded(hashvalue):
    resp = crack(hashvalue)
    if resp:
        print (hashvalue + ' : ' + resp)
        result[hashvalue] = resp

def grepper(directory):
    os.system('''grep -Pr "[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}" %s --exclude=\*.{png,jpg,jpeg,mp3,mp4,zip,gz} |
        grep -Po "[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}" >> %s/%s.txt''' % (directory, cwd, directory.split('/')[-1]))
    print ('%s Results saved in %s.txt' % (info, directory.split('/')[-1]))

def miner(file):
    lines = []
    found = set()
    with open(file, 'r') as f:
        for line in f:
            lines.append(line.strip('\n'))
    for line in lines:
        matches = re.findall(r'[a-f0-9]{128}|[a-f0-9]{96}|[a-f0-9]{64}|[a-f0-9]{40}|[a-f0-9]{32}', line)
        if matches:
            for match in matches:
                found.add(match)
    print ('%s Hashes found: %i' % (info, len(found)))
    threadpool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
    for hashvalue in found:
        print (hashvalue)
        threaded(hashvalue)



    #futures = (threadpool.submit(threaded, hashvalue) for hashvalue in found)
    #for i, _ in enumerate(concurrent.futures.as_completed(futures)):
        #if i + 1 == len(found) or (i + 1) % thread_count == 0:
            #print('%s Progress: %i/%i' % (info, i + 1, len(found)), end='\r')

def single(args):
    result = crack(args.hash)
    if result:
        print (result)
    else:
        print ('%s Hash was not found in any database.' % bad)

if directory:
    try:
        grepper(directory)
    except KeyboardInterrupt:
        pass

elif file:
    try:
        miner(file)
    except KeyboardInterrupt:
        pass
    with open('cracked-%s' % file.split('/')[-1], 'w+') as f:
        for hashvalue, cracked in result.items():
            f.write(hashvalue + ':' + cracked + '\n')
    print ('%s Results saved in cracked-%s' % (info, file.split('/')[-1]))

elif args.hash:
    single(args)
