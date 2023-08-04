#can you please check this for assigning permission. If it works then we can make api with lambda:

import boto3

# Create a Boto3 IAM client
iam_client = boto3.client('iam')

# Example: Attach an IAM policy to a user
user_name = 'your username'
policy_arn = 'arn:aws:iam::aws:policy/AmazonS3FullAccess'

response = iam_client.attach_user_policy(
    UserName=user_name,
    PolicyArn=policy_arn
)

print(response)
Ehtisham A.
Aug 03, 2023, 8:45 AM

Change permission set for user:

import boto3

def change_permission_set(user_id, permission_set_arn):
    sso_admin_client = boto3.client('sso-admin')
    instance_arn = 'arn:aws:sso:::instance/sso-instance-id'
    
    response = sso_admin_client.create_account_assignment(
        InstanceArn=instance_arn,
        TargetId=user_id,
        TargetType='USER',
        PermissionSetArn=permission_set_arn
    )
    
    return response

# Lambda handler
def lambda_handler(event, context):
    user_id = event['user_id']
    permission_set_arn = 'arn:aws:sso:::permissionSet/permission-set-id'
    
    response = change_permission_set(user_id, permission_set_arn)
    return response
Ehtisham A.
Aug 03, 2023, 8:45 AM

Removing Access for a User:

import boto3

def remove_access(user_id):
    sso_admin_client = boto3.client('sso-admin')
    instance_arn = 'arn:aws:sso:::instance/sso-instance-id'
    
    response = sso_admin_client.delete_account_assignment(
        InstanceArn=instance_arn,
        TargetId=user_id,
        TargetType='USER'
    )
    
    return response

# Lambda handler
def lambda_handler(event, context):
    user_id = event['user_id']
    
    response = remove_access(user_id)
    return response
Ehtisham A.
Aug 03, 2023, 8:46 AM

Assigning Users or Groups to an AWS Account:

import boto3

def assign_user_to_account(user_id, account_id):
    sso_admin_client = boto3.client('sso-admin')
    instance_arn = 'arn:aws:sso:::instance/sso-instance-id'
    
    response = sso_admin_client.create_account_assignment(
        InstanceArn=instance_arn,
        TargetId=user_id,
        TargetType='USER',
        AccountId=account_id
    )
    
    return response

# Lambda handler
def lambda_handler(event, context):
    user_id = event['user_id']
    account_id = 'aws-account-id'
    
    response = assign_user_to_account(user_id, account_id)
    return response
Ehtisham A.
Aug 03, 2023, 8:46 AM

Add user to IAM group:

import boto3

# Create a Boto3 IAM client
iam_client = boto3.client('iam')

# Example: Add a user to an IAM group
user_name = 'example_user'
group_name = 'example_group'

response = iam_client.add_user_to_group(
    GroupName=group_name,
    UserName=user_name
)

print(response)
Ehtisham A.
Aug 03, 2023, 8:47 AM

remove user from IAM group:

import boto3

# Create a Boto3 IAM client
iam_client = boto3.client('iam')

# Example: Remove a user from an IAM group
user_name = 'example_user'
group_name = 'example_group'

response = iam_client.remove_user_from_group(
    GroupName=group_name,
    UserName=user_name
)

print(response)
Ehtisham A.
Aug 03, 2023, 8:47 AM

--------------------------------
Ehtisham A.
Aug 03, 2023, 8:47 AM

please test these scripts if its working then we can create APIs.
 
import boto3

def remove_access(user_id):
    sso_admin_client = boto3.client('sso-admin')
    instance_arn = 'arn:aws:sso:::instance/sso-instance-id'
    permission_set_arn = 'arn:aws:sso:::permissionSet/permission-set-id'
    
    response = sso_admin_client.delete_account_assignment(
        InstanceArn=instance_arn,
        TargetId=user_id,
        TargetType='USER',
        PermissionSetArn=permission_set_arn,
        PrincipalType='USER',
        PrincipalId=user_id
    )
    
    return response

# Lambda handler
if __name__ == "__main__":
   
    user_id = ""    
    response = remove_access(user_id)
    print(response)
