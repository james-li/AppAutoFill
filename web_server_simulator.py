#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import traceback
from http.server import  HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

class MyHttpServer(HTTPServer):
    def __init__(self, base_path, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)
        self.RequestHandlerClass.base_path = base_path

class MyHttpHandler(SimpleHTTPRequestHandler):
    # RESPONSE = {
    #     "path": "C:\\Program Files (x86)\\PremiumSoft\\Navicat for MySQL\\navicat.exe",
    #     "param": "",
    #     "appAutoFill":{
    #
    #     },
    #     "callback": "http://localhost:8080/callback"
    # }

    RESPONSE = {
        "path": "D:\\work\\AppAutoFill\\AppDemo1.exe",
        "param": "",
        "callback": "http://localhost:8080/callback"
    }

    def do_Header(self, responseCode):
        self.send_response(responseCode)
        self.send_header("Content-Type", "Application/json")
        self.end_headers()

    def do_GET(self):
        querypath = urlparse(self.path)
        _host, _ip = self.request.getsockname()
        print(querypath)
        code = 200
        response = dict()
        if querypath.path == '/req' :
            if querypath.query:
                params = dict(pair.split('=') for pair in querypath.query.split('&'))
                app = params.get("app")
                try:
                    appfile = os.path.join(self.base_path, "test", app+".json")
                    response = json.loads(open(appfile, "rb").read().decode("utf-8"))
                except:
                    traceback.print_exc()
                    code = 404
            else:
                response = self.RESPONSE
        self.do_Header(code)
        if response:
            response["callback"] = "http://%s:%d/callback"%(_host, _ip)
        self.wfile.write(json.dumps(response).encode("utf8"))


if __name__ == "__main__":
    host = ('', 8080)
    server = MyHttpServer(os.path.dirname(os.path.abspath(sys.argv[0])), host, MyHttpHandler)
    print("Start http server at %d"%(host[1]))
    server.serve_forever()
