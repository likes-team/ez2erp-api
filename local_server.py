import json
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from lambda_function import lambda_handler


class LambdaLocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'EZ2ERP request = GET > {self.path}')
        self._init_event('GET')

        context = {}
        response = lambda_handler(self.event, context)

        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode('utf-8'))
        # self.wfile.write("It works!".encode("utf-8"))

    def do_POST(self):
        print(f'EZ2ERP request = POST > {self.path}')

        self._init_event('POST')
        print(self.event)

        context = {}
        response = lambda_handler(self.event, context)
        print(response)
        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PUT(self):
        print(f'EZ2ERP request = PUT > {self.path}')

        self._init_event('PUT')
        print(self.event)

        context = {}
        response = lambda_handler(self.event, context)
        print(response)
        self._set_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_DELETE(self):
        print(f'EZ2ERP request = PUT > {self.path}')

        self._init_event('DELETE')
        print(self.event)

        context = {}
        response = lambda_handler(self.event, context)
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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST, PUT, DELETE')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        # self.end_headers()

    def _init_event(self, http_method):
        path = self.path.split('/')

        if len(path) == 3:
            endpoint = path[-2]
            oid = path[-1]
        elif len(path) == 2:
            endpoint = path[-1]
            oid = None
        else:
            raise Exception("Endpoint cannot be determined")

        if http_method in ['POST', 'PUT']:
            post_data = json.loads(
                self.rfile.read(
                    int(self.headers.get('Content-Length'))
                ).decode("UTF-8"))
        else:
            post_data = None

        initial_event = {
            'endpoint': endpoint,
            'httpMethod': http_method,
            'body': {}
        }

        if oid:
            initial_event['body'] = initial_event['body'] | {'oid': oid}

        if post_data:
            initial_event['body'] = initial_event['body'] | post_data

        self.event = initial_event