import json
import cgi
from http.server import HTTPServer, BaseHTTPRequestHandler
from lambda_function import lambda_handler


class LambdaLocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f'EZ2ERP request = GET > {self.path}')
        
        event = {
            'endpoint': self.path.replace('/', ''),
            'httpMethod': {'http': {'method': 'GET'}},
        }
        print(event)
        context = {}
        response = lambda_handler(event, context)

        self.send_response(200)
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

        # length = int(self.headers.get('content-length'))
        # data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        # print(data)
        # recordID = self.path.split('/')[-1]

        # print("length :", length)
        # print("content : %s" % self.rfile.read(length))
        # post_body = self.rfile.read(content_length)
        # test_data = simplejson.loads(post_body)
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
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        self.wfile.write(json.dumps(response).encode('utf-8'))