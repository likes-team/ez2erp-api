import json
import boto3
from ez2erp_engine.db import Ez2DBManager
from endpoints import (
    auth, user, inventory
)
from ez2erp_engine.models import Organization


def lambda_handler(event, context):
    # TODO: Move keys to enviroment variable
    session = boto3.Session(
        aws_access_key_id="AKIA47CRWL5IINEGSZNO",
        aws_secret_access_key="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",
        region_name='ap-southeast-1'
    )
    print("Received event:", json.dumps(event))
    Ez2DBManager.connect_db(session)

    # Request parameters
    endpoint = event.get('endpoint')
    http_method = event.get('httpMethod')
    body = event.get('body')
    print ("This is the endpoint",endpoint)
    print ("this is the http method",http_method)

    status = "success"
    data = None
    message = None

    match endpoint:
        case "login":
            data, status, message = auth.login(event)
        case "users":
            if http_method == 'GET':
                data = {'fname': 'test', 'lname': 'data'}
                message = "Success!"
            elif http_method == 'POST':
                data, status, message = user.create_user(body)
        case "products":
            if http_method == 'GET':
                data, status, message = inventory.get_products(body)
            elif http_method == 'POST':
                data, status, message = inventory.create_product(body)
            elif http_method == 'PUT':
                data, status, message = inventory.edit_product(body)
            elif http_method == 'DELETE':
                data, status, message = inventory.delete_product(body)
        case "organizations":
            print("TEST")
            org = Organization(name="test2")
            org.name = "test"
            org.description = "descriptions"
            print(org.__dict__)

        case "orders":
            pass
        case "payments":
            pass
        case default:
            status = "error"
            message = "Endpoint is not available"

    response = {
        'status': status,
        'message': message
    }
    response = response | data
    return response


def _start_server():
    from http.server import HTTPServer
    from local_server import LambdaLocalServer

    host = "localhost"
    port = 8000
    httpd = HTTPServer(('', port), LambdaLocalServer)
    print(f'Lambda Local Server is running on http://{host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    # python lambda_function.py starting point"
    _start_server()
