from boto3.dynamodb.conditions import Key
from ez2erp_engine.models import User


def login(event):
    email = event.get('email')
    password = event.get('password')
    print("email", email)

    # Sample ORM usage
    key_condition = Key('email').eq(email)
    user: User = User.ez2.select_by_index(
        index_name='email-index',
        key_condition=key_condition
    )

    # # Sample direct usage  
    # dynamodb_client = Ez2DBManager.dynamo_client
    # user = dynamodb_client.table.query(
    #     IndexName='email-index',
    #     KeyConditionExpression=Key(key).eq(val)
    # )

    print(user.__dict__)
    is_password_matched = user.decrypt_password(password)

    if user is None or not is_password_matched:
        return None, "error", "Wrong Credentials!"

    return user.to_dict(), "success", "Logged in Successfully!"

