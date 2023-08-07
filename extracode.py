import json
import boto3

def delete_user_from_group():
    client = boto3.client('identitystore')
    sso_client = boto3.client('sso-admin')
    
    #getting identityStoreId 
    
    instance_arn = 'arn:aws:sso:::instance/ssoins-698759770ce5a35e'
    
    response = sso_client.list_instances()
    instance_id = None
    for instance in response['Instances']:
        if instance['InstanceArn'] == instance_arn:
            print(instance)

    #delete user from group
    
    # Prepare the member_id parameter as a dictionary with the UserId field
    member_id = {
        'UserId': "9384c842-3071-70cf-67d6-f6ae0d6bc248"
    }
    
    # Call the get_group_membership_id API
    response = client.get_group_membership_id(
        IdentityStoreId=identitystore_id,
        GroupId="d324a832-d0d1-70d1-58af-5a59c3ce9675",
        MemberId=member_id
    )
    
    # MembershipId = "63f4f822-4031-704e-a00b-c1abbfb4fe1c" 
    IdentityStoreId = "d-996707e2f3"
    
    response = client.delete_group_membership(
    IdentityStoreId='d-996707e2f3',
    MembershipId='63f4f822-4031-704e-a00b-c1abbfb4fe1c'
    )
    
    # return response
    
    # added user in the group
    
    response = client.create_group_membership(
    IdentityStoreId='d-996707e2f3',
    GroupId='d324a832-d0d1-70d1-58af-5a59c3ce9675',
    MemberId={
        'UserId': '9384c842-3071-70cf-67d6-f6ae0d6bc248'
    }
        )
    # return response
    
    # attch managed policy to permission set
    response = sso_client.attach_managed_policy_to_permission_set(
        InstanceArn=f'arn:aws:sso:::instance/ssoins-698759770ce5a35e',
        PermissionSetArn="arn:aws:sso:::permissionSet/ssoins-698759770ce5a35e/ps-e7c813ef49a4b795",
        ManagedPolicyArn="arn:aws:iam::aws:policy/CloudSearchFullAccess"
    )
    # return response
    
    # Use the get_user_id API with the alternate identifier (userName)
    response = client.get_user_id(
        IdentityStoreId=IdentityStoreId,
        AlternateIdentifier={
            'UniqueAttribute': {
                'AttributePath': 'userName',
                'AttributeValue': "averymanyi@idc.com"
            }
        }
    )
    
    # return response
    
    # # Use the get_group_id API with the alternate identifier (userName)
    # response = client.get_group_id(
    #     IdentityStoreId=IdentityStoreId,
    #     AlternateIdentifier={
    #         'UniqueAttribute': {
    #             'AttributePath': 'displayName',
    #             'AttributeValue': "Database"
    #         }
    #     }
    # )
    
    # return response
    
    # List all the permission sets
    response = sso_client.list_permission_sets(
        InstanceArn= 'arn:aws:sso:::instance/ssoins-698759770ce5a35e'
        )
    # return response["PermissionSets"]
    permission_sets = response['PermissionSets']

    # Find the permission set with the matching name
    for permission_set in permission_sets:
        if permission_set['Name'] == "AdministratorAccess":
            return permission_set['Arn']
    

def lambda_handler(event, context):
    response = delete_user_from_group()
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
