import boto3
import json


user="agborntuibate@fico.com"
def sts(account_id):
    try:
        sts_client = boto3.client('sts')
        role_arn = "arn:aws:iam::"+account_id+":role/GTS-AWSEngineering"
        role_session_name = 'monitor'
        credentials = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=role_session_name)
        return credentials['Credentials']
    except Exception as e:
        # print(e)
        return ''

def addPermToUser():
    acc='289670889007'
    creds=sts(acc)
    if(creds!=''):
        idc = boto3.client('identitystore',region_name='us-west-2',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'])

        response=idc.get_user_id(
            IdentityStoreId='d-9267420026',
            AlternateIdentifier={
                'UniqueAttribute': {
                    'AttributePath': 'emails.value',
                    'AttributeValue': "agborntuibate@fico.com"
                }
        })

        sso_client = boto3.client('sso-admin',region_name='us-west-2',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'])
        
        response = sso_client.create_account_assignment(
            InstanceArn='arn:aws:sso:::instance/ssoins-79071ef5f2a874d9',
            TargetId='027907692231',
            TargetType='AWS_ACCOUNT',
            PermissionSetArn='arn:aws:sso:::permissionSet/ssoins-79071ef5f2a874d9/ps-c44ec5bf2930a163',
            PrincipalType='USER',
            PrincipalId=response['UserId']
        )
        if(response['ResponseMetadata']['HTTPStatusCode']):
            print(f"Permission added to {user}")

def removePermFromUser():
    acc='289670889007'
    creds=sts(acc)
    if(creds!=''):
        idc = boto3.client('identitystore',region_name='us-west-2',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'])

        response=idc.get_user_id(
            IdentityStoreId='d-9267420026',
            AlternateIdentifier={
                'UniqueAttribute': {
                    'AttributePath': 'emails.value',
                    'AttributeValue': "agborntuibate@fico.com"
                }
        })

        sso_client = boto3.client('sso-admin',region_name='us-west-2',
            aws_access_key_id=creds['AccessKeyId'],
            aws_secret_access_key=creds['SecretAccessKey'],
            aws_session_token=creds['SessionToken'])
        
        response = sso_client.delete_account_assignment(
            InstanceArn='arn:aws:sso:::instance/ssoins-79071ef5f2a874d9',
            TargetId='027907692231',
            TargetType='AWS_ACCOUNT',
            PermissionSetArn='arn:aws:sso:::permissionSet/ssoins-79071ef5f2a874d9/ps-c44ec5bf2930a163',
            PrincipalType='USER',
            PrincipalId=response['UserId']
        )
        if(response['ResponseMetadata']['HTTPStatusCode']):
            print(f"Permission removed from {user}")


def main():
    print(f"Changes will be made in account 289670889007 to user {user}")
    print("Press 1 to add permission\nPress 2 to remove permission\n")
    choice=input("Choice - ")
    if(choice=="1"):
        addPermToUser()
    else:
        removePermFromUser()


main()
