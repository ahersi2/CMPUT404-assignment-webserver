#  coding: utf-8 
import socketserver
import os
import sys

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        #print("cameinto handle function")
        current_dir= os.getcwd()
        updated_dir=current_dir+"/www"
        dirs=os.listdir(updated_dir)
        updated_dir1=updated_dir+'/index.html'
        updated_dir1_css=updated_dir+'/base.css'
        #updated_dir2=os.path.join(updated_dir,'deep/index.html')
        updated_dir2=updated_dir+'/index.html'
        updated_dir2_css=updated_dir+'/deep/deep.css'

        self.data = self.request.recv(1024).strip()
        self.data=self.data.decode("utf-8")
        #print(self.data)
        a = self.data.splitlines()
        directory=a[0].split()
        #print(updated_dir+directory[1])

        #print("Here is wasdfasdfsadhether it is a directoy")
        #print(os.path.exists(updated_dir+directory[1]))

        #print(directory[0])
        #print("about to check")
        if("/.." in directory[1]):
            #print("here is the ...............")
            self.request.send(b'HTTP/1.1 404 not found\r\n')
        if(directory[0]!="POST" or directory[0]!="PUT" or directory[0]!="DELETE"):
            #print(directory[1])
            if(os.path.exists(updated_dir+directory[1])):
                #print("path does exists")
                if(".css" in directory[1]):
                    #print("CAME INTO CSS CONDITION")
                    with open(updated_dir+directory[1],"r") as f:
                        read_html=f.read()
                        self.request.send(b'HTTP/1.1 200 OK\n')
                        self.request.send(b'Content-Type: text/css \n')
                        self.request.send(b'\n')
                        self.request.send(bytearray(read_html,'utf-8'))
                else:
                    #print("CAME INTO INDEX CONDTION")
                    self.indexPage((updated_dir+directory[1]))
            else:
                #print("CAME INTO SENDING 404 ERROR")
                self.request.send(b'HTTP/1.1 404 not found\r\n')


            if(".css" in a[0]):
                #print("asdfasfasfsfdsafdsafdsf")
                if(os.path.isdir(updated_dir+directory[1])==True):

                    with open(updated_dir+directory[1],"r") as f:
                        read_html=f.read()
                        self.request.send(b'HTTP/1.1 200 OK\n')
                        self.request.send(b'Content-Type: text/css \n')
                        self.request.send(b'\n')
                        self.request.send(bytearray(read_html,'utf-8'))
            elif("deep/base.css" in a[0]):
                #print("shouldnt come in here")
                with open(updated_dir2_css,"r") as f:
                    read_html=f.read()
                    self.request.send(b'HTTP/1.1 200 OK\n')
                    self.request.send(b'Content-Type: text/css \n')
                    self.request.send(b'\n')
                    self.request.send(bytearray(read_html,'utf-8'))
        else:
            #print("22222222222222222222")
            if("/.." in directory[1]):
                #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                self.request.send(b'HTTP/1.1 404 not found\r\n')
            else:
                self.request.send(b'HTTP/1.1 405 Method Not Allowed\r\n')


        
        #print(a)
        url=""
        for i in a:
            #print("*&*&*&&&*&*&***&*&*&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            if("Referer" in i):
                url=i.split("/")
        #print("the length of the url is :"+str(len(url)))
        #print(url)

        #if len(url)<5:
        #    print("came in first part")
        #    self.firstPage(updated_dir1,updated_dir1_css)
       # else:
        #    print("came in second part")
        #    self.secondPage(updated_dir2)
       


        #print ("Got a request of: %s\n" % self.data)

        #with open(updated_dir1,"r") as f:
            #print("------------------")
         #   read_html=f.read()
            #print("------------------")


        #response = "\HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n"+read_html


        
        #self.request.sendall(bytearray(response,'utf-8'))

    def indexPage(self,updated_dir1):
        #print("CAME INTO FIRSTPAGE FUNCTION")
        #print(updated_dir1)
        if(".html" in updated_dir1):

            with open(updated_dir1,"r") as f:
                #print("------------------")
                read_html=f.read()
                #print("------------------")
            self.request.send(b'HTTP/1.0 200 OK\n')
            self.request.send(b'Content-Type: text/html \n')
            self.request.send(b'\n')
            self.request.send(bytearray(read_html,'utf-8'))
        else:
            #print(updated_dir1)
            if(updated_dir1.endswith('/')==False):
                #print("cameinto the right place")
                self.request.send(b'HTTP/1.1 301 MOVED PERMANENTLY\r\n')
                self.request.send(b'Location: http://127.0.0.1:8080/deep/index.html\r\n')
                #self.end_headers()

            else:

                updated_dir1=updated_dir1+'index.html'
                #print("CAADFASDFSADFME IN HERE")
                #print(updated_dir1)
                with open(updated_dir1,"r") as f:
                    #print("------------------")
                    read_html=f.read()
                    #print("------------------")
                self.request.send(b'HTTP/1.0 200 OK\n')
                self.request.send(b'Content-Type: text/html \n')
                self.request.send(b'\n')
                self.request.send(bytearray(read_html,'utf-8'))

            #response = "\HTTP/1.1 200 OK\r\n Content-Type: text/html\r\n"+read_html

            #self.request.sendall(bytearray(response,'utf-8'))
            #print("should be another css")

            #with open(updated_dir1_css,"r") as f:
                #print("------------------")
             #   read_html=f.read()
                #print("------------------")
            #response = "\HTTP/1.1 200 OK\r\n Content-Type: text/css\r\n"+read_html
            #self.request.sendall(bytearray(response,'utf-8'))
            #print()
        
    def secondPage(self,updated_dir2):
        print("CAME INTO SECONDPAGE FUNCTION")
        with open(updated_dir2,"r") as f:
            print(updated_dir2)
            print(type(updated_dir2))
            #print("------------------")
            read_html=f.read()
            #print("------------------")
            print(read_html)
        self.request.send(b'HTTP/1.0 200 OK\n')
        self.request.send(b'Content-Type: text/html \n')
        self.request.send(b'\n')
        self.request.send(bytearray(read_html,'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    
