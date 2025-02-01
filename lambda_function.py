import json
import boto3
from ez2erp_engine.db import Ez2DBManager
from endpoints import auth, user


def lambda_handler(event, context):
    # TODO: Move keys to enviroment variable
    session = boto3.Session(
        aws_access_key_id="AKIA47CRWL5IINEGSZNO",
        aws_secret_access_key="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",
        region_name='ap-southeast-1'
    )
    Ez2DBManager.connect_db(session)

    # Request parameters
    endpoint = event.get('endpoint')
    
    try:
        http_method = event['requestContext']['http']['method']
    except KeyError:
        endpoint = None

    status = "success"

    match endpoint:
        case "login":
            data, status, message = auth.login(event)
        case "users":
            if http_method == 'GET':
                data = {'fname': 'test', 'lname': 'data'}
                message = "Success!"
            elif http_method == 'POST':
                data = user.create_user(event)
                message = "User created successfully!"

        case "orders":
            pass
        case "payments":
            pass
        case default:
            status = "error"
            message = "Endpoint is not available"

    return {
        'status': status,
        'data': data,
        'message': message
    }


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
