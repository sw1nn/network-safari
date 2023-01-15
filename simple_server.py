from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
import socket
import threading


def delayed_GET(host, path):
   print(f"GET-ing http://{host}{path}")
   c = HTTPConnection(host)
   try:
        c.request("GET", path)
        r = c.getresponse()
        print(r.status, r.reason)
   finally:
       c.close()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        idx=int(socket.gethostname()[-1]) + 1
        if idx > 3:
            idx = 1
        args = (f"host{idx}", self.path)
        threading.Timer(5.0, delayed_GET, args).start();

        self.protocol_version = "HTTP/1.1"
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")

        
       

def run(server_class=HTTPServer, handler_class=RequestHandler):
    """Entrypoint for python server"""
    server_address = (socket.gethostbyname(socket.gethostname()), 80)
    httpd = server_class(server_address, handler_class)
    print(f"Server listening on {server_address} ...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
