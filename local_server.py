import json
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from lambda_function import lambda_handler


class LambdaLocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'EZ2ERP request = GET > {self.path}')

        path = self.path.split('/')
        if len(path) == 3:
            endpoint = path[-2]
            oid = path[-1]
        elif len(path) == 2:
            endpoint = path[-1]
            oid = None
    
        event = {
            'endpoint': endpoint,
            'httpMethod': 'GET',
        }

        if oid:
            event['body'] = {'oid': oid} 

        print(event)
        context = {}
        response = lambda_handler(event, context)

        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode('utf-8'))
        # self.wfile.write("It works!".encode("utf-8"))

    def do_POST(self):
        print(f'EZ2ERP request = POST > {self.path}')
        # content_length = self.headers.getheaders('content-length')

        post_data = json.loads(
            self.rfile.read(
                int(self.headers.get('Content-Length'))
            ).decode("UTF-8"))
        event = {
            'endpoint': self.path.replace('/', ''),
            'httpMethod': 'POST',
            'body': post_data
        }
        event = event | post_data

        print(event)
        context = {}
        response = lambda_handler(event, context)
        print(response)
        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PUT(self):
        print(f'EZ2ERP request = PUT > {self.path}')
        post_data = json.loads(
            self.rfile.read(
                int(self.headers.get('Content-Length'))
            ).decode("UTF-8"))
        event = {
            'endpoint': self.path.replace('/', ''),
            'httpMethod': 'POST',
            'body': post_data
        }
        event = event | post_data

        print(event)
        context = {}
        response = lambda_handler(event, context)
        print(response)
        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_OPTIONS(self):
        self._set_headers()
        self.end_headers()

    def _set_headers(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # self.end_headers()