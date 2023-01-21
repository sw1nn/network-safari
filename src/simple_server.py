from http.server import HTTPServer, BaseHTTPRequestHandler
from http.client import HTTPConnection
from socketserver import ThreadingMixIn
from threading import Thread, Timer
import socket
import os,sys
import ssl

def build_ssl_context(protocol):
    context = ssl.SSLContext(protocol)

    # turn off some checking in TLS - this is generally a bad idea,
    # but we're just testing. In a production environment you would
    # ensure that certificates and hostnames validate
    context.check_hostname = False
    context.verify_mode = False

    context.load_cert_chain(certfile='./safari.cert', keyfile='./safari.key')

    return context

def delayed_GET(host, path):
   print(f"GET-ing http://{host}{path}")
   c = HTTPConnection(host)
   try:
        c.request("GET", path)
        r = c.getresponse()
        print(r.status, r.reason)
   except socket.gaierror:
       print(f"Error resolving {host}", file=sys.stderr)
   finally:
       c.close()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(socket.gethostname())
        idx=int(socket.gethostname()[4]) + 1
        if idx > 3:
            idx = 1
        args = (f"host{idx}.safari.", self.path)
        Timer(5.0, delayed_GET, args).start();

        self.protocol_version = "HTTP/1.1"
        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status": "All Good"}')

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
        
def build_http_server(hostname, port, https=False, server_class=ThreadingHTTPServer, handler_class=RequestHandler, ):
    server_address = (socket.gethostbyname(hostname), port)
    server = server_class(server_address, handler_class)
    if https:
        server.socket = build_ssl_context(ssl.PROTOCOL_TLS_SERVER).wrap_socket(server.socket, server_side=True)

    print(f'{"HTTPS" if https else "HTTP"} Server listening on {server.server_address} ...')
    server. serve_forever()
 
def run():
    """Entrypoint for python server"""
    hostname = socket.gethostname()
    http_port = int(os.getenv('SAFARI_PORT_BASE', 0 )) + 80;
    https_port = int(os.getenv('SAFARI_PORT_BASE', 0 )) + 443;

    http = Thread(target=build_http_server, args=[hostname, http_port])
    https = Thread(target=build_http_server, args=[hostname, https_port],kwargs={'https': True})

    http.start()
    https.start()

    http.join()
    https.join()

if __name__ == "__main__":
    run()
