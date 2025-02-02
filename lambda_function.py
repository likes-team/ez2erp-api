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
    print("Received event:", json.dumps(event))
    Ez2DBManager.connect_db(session)

    # Request parameters
    
    try:
        endpoint = event.get('endpoint')
        http_method = event.get('httpMethod')
        body = event.get('body')
        print ("This is the endpoint",endpoint)
        print ("this is the http method",http_method)
    except KeyError:
      #  endpoint = None
        http_method = None  # Ensure http_method is always defined
        print("Error: requestContext.http.method not found in event")
        data = None 

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
                if http_method:
                    print("This is the http method True")
                data = user.create_user(body)
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
