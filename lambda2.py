import boto3
import json
from aws_lambda_powertools.event_handler.api_gateway import (
    ApiGatewayResolver,
    ProxyEventType,
    Response,
)

client = boto3.client('identitystore')
sso_client = boto3.client('sso-admin')
instance_arn = 'arn:aws:sso:::instance/ssoins-79071ef5f2a874d9'
app = ApiGatewayResolver(proxy_type=ProxyEventType.APIGatewayProxyEventV2)
        


@app.get('/add-permission') 
def addPermToUser():
    username = app.current_event.get_query_string_value(name="user", default_value=None)
    permission_set_arn = app.current_event.get_query_string_value(name="permissionSetArn", default_value=None)
    acc= app.current_event.get_query_string_value(name="account_id", default_value=None)
    
    idc = boto3.client('identitystore')

    response_user=idc.get_user_id(
        IdentityStoreId='d-9267420026',
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'emails.value',
                'AttributeValue': f"{username}"
            }    
    })

    sso_client = boto3.client('sso-admin')
    
    response_account = sso_client.create_account_assignment(
        InstanceArn='arn:aws:sso:::instance/ssoins-79071ef5f2a874d9',
        TargetId=acc,
        TargetType='AWS_ACCOUNT',
        PermissionSetArn=permission_set_arn,
        PrincipalType='USER',
        PrincipalId=response_user['UserId']
    )
    if(response_account['ResponseMetadata']['HTTPStatusCode']):
        print(f"Permission added to {username} to {acc}")
    return Response(status_code=200,content_type="application/json",body=json.dumps(response_account, default=str))

@app.get('/remove-permission') 
def removePermFromUser():
    username = app.current_event.get_query_string_value(name="user", default_value=None)
    permission_set_arn = app.current_event.get_query_string_value(name="permissionSetArn", default_value=None)
    acc= app.current_event.get_query_string_value(name="account_id", default_value=None)
    idc = boto3.client('identitystore')

    response_user=idc.get_user_id(
        IdentityStoreId='d-9267420026',
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'emails.value',
                'AttributeValue': f"{username}"
            }
    })

    sso_client = boto3.client('sso-admin')
    
    response_account = sso_client.delete_account_assignment(
        InstanceArn='arn:aws:sso:::instance/ssoins-79071ef5f2a874d9',
        TargetId=acc,
        TargetType='AWS_ACCOUNT',
        PermissionSetArn=permission_set_arn,
        PrincipalType='USER',
        PrincipalId=response_user['UserId']
    )
    if(response_account['ResponseMetadata']['HTTPStatusCode']):
        print(f"Permission removed from {username} to {acc}")
            
    return Response(status_code=200,content_type="application/json",body=json.dumps(response_account, default=str))

def lambda_handler(event, context):
    return app.resolve(event, context)
