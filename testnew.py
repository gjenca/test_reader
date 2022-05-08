#!/usr/bin/env python3
import yaml
import sys
import signal
import socket
import glob
import time

TIMEOUT=1

class TimeOutException(Exception):
   pass
 
def alarm_handler(signum, frame):
    raise TimeOutException()


signal.signal(signal.SIGALRM, alarm_handler)

def print_and_flush(*arg,**narg):

    print(*arg,**narg)
    f=narg.get('file',sys.stdout)
    f.flush()

def handle_timeout(when,comment=None):
    
    print_and_flush(f'>>> TIMEOUT after {TIMEOUT} seconds')
    print_and_flush(f'>>> Timed out while {when}')
    if comment:
        print_and_flush(f'>>> {comment}')
    print_and_flush('>>> Exitting test')
    sys.exit(1)

def readline_tee(f):

    line=f.readline().decode('utf-8')
    ## repr tam je kvoli tomu, aby bolo vidiet aj '\n'
    print_and_flush(f'S->C: {repr(line)}')
    return line

def write_tee(f,s):
    if s:
        print_and_flush(f'C->S: {repr(s)}')
        f.write(s.encode('utf-8'))
        f.flush() 

class Request:

    def __init__(self,d):

        for name in ('method','headers','content'):
            if not name in d:
                raise ValueError(f'{name} missing in request')
        self.method=d['method']
        self.headers=d['headers']
        self.content=d['content']

    def send(self,f):
        write_tee(f,f'{self.method}\n')
        for name,value in self.headers.items():
            write_tee(f,f'{name}:{value}\n')
        # po hlavickach prazdny riadok
        write_tee(f,'\n')
        write_tee(f,self.content)

class Response:

    def __eq__(self,other):
        return self.status==other.status and \
            self.headers==other.headers and \
            self.content==other.content

    def __repr__(self):

        return f'Response: status={self.status} headers={self.headers} content={repr(self.content)}'

    def sort_content(self):
        
        content_lines=self.content.splitlines(keepends=True)
        content_lines.sort()
        self.content=''.join(content_lines)

class ResponseFromDict(Response):

    def __init__(self,d,request):

        self.request=request
        for name in ('status','headers','content'):
            if not name in d:
                raise ValueError(f'{name} missing in response')
        if type(d['status'])!=int:
            raise ValueError('non-numeric status in response')
        self.status=d['status']
        self.headers=d['headers']
        self.content=d['content']
        if self.request.method in ('LS','SEARCH'):
            self.sort_content()

class ResponseFromSocket(Response):
    
    def __init__(self,f,request):
        # citanie statusu

        self.request=request
        try:
            status_in=readline_tee(f)
        except TimeOutException:
            handle_timeout('reading status')
        try:
            status,status_desc=status_in.split(' ',1)
        except ValueError:
            print_and_flush('>>> Expected status line, got something else instead')
            print_and_flush('>>> Exitting test')
            sys.exit(1)
        try:
            self.status=int(status)
        except ValueError:
            print_and_flush('>>> Non-numerical status')
            print_and_flush('>>> Exitting test')
            sys.exit(1)
        # citanie hlaviciek
        self.headers={}
        while True:
            try:
                line_out=readline_tee(f)
            except TimeOutException:
                handle_timeout('reading headers',comment='Probably the server did not write empty line after headers')
            if line_out=='':
                print_and_flush('>>> Server closed connection')
                break
            # prazdny riadok sa skonvertuje na '', newline z konca riadku prec
            line_out=line_out.rstrip()
            # hlavicka
            if ':' in line_out:
                name,value=line_out.split(':',1)
                # medzery zlava budem tolerovat
                value=value.lstrip()
                self.headers[name]=value
            # prazdny riadok -> koniec hlaviciek
            elif not line_out:
                break
            # ani hlavicka, ani prazdny riadok
            else:
                print_and_flush('>>> Expected a header, got something else instead')
                print_and_flush('>>> Exitting test')
                sys.exit(1)
        # citanie obsahu -- berie do uvahy hodnotu hlaviciek
        if 'Lines' in self.headers:
            content_lines=[]
            n=int(self.headers['Lines'])
            for i in range(n):
                try:
                    line=readline_tee(f)
                    content_lines.append(line)
                except TimeOutException:
                    handle_timeout('reading content')
            self.content="".join(content_lines)
        else:
            self.content=""
        if self.request.method in ('LS','SEARCH'):
            self.sort_content()

signal.alarm(TIMEOUT)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',9999))
f=s.makefile(mode='rwb')
for req_resp_fnm in sorted(glob.glob('req_resp*.yaml')):
    with open(req_resp_fnm) as req_resp_file:
        # citanie testu z YAML suboru
        request_d,response_d=yaml.load_all(req_resp_file,Loader=yaml.Loader)
        print_and_flush('==================')
        print_and_flush(f'>>> Filename:{req_resp_fnm}')
        print_and_flush('---')
        # request, ktory posielam
        request=Request(request_d)
        # response, ktoru ocakavam
        try:
            response_expect=ResponseFromDict(response_d,request)
        except ValueError:
            print_and_flush(f'>>> File {req_resp_fnm} is not correct',file=sys.stderr)
            raise
        # vykonanie testu
        # posleme request
        request.send(f)
        print_and_flush('---')
        print_and_flush('>>> End request, awaiting response')
        # precitame response
        signal.alarm(TIMEOUT)
        try:
            response_real=ResponseFromSocket(f,request)
        except TimeOutException:
            print_and_flush(f'>>> Timeout after {TIMEOUT} seconds! (probably a deadlock)')
            print_and_flush('>>> Exitting test')
            sys.exit(1)
        print_and_flush('---')
        if response_real!=response_expect:
            print_and_flush('>>> Unexpected response:')
            print_and_flush('>>> Got response:',response_real)
            print_and_flush('>>> Expected:',response_expect)
            print_and_flush('>>> Exitting test')
            s.close()
            sys.exit(1)
        else:
            print_and_flush('>>> Got expected response, OK')
s.close()
sys.exit(0)
    
