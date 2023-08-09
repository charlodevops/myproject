# myproject


Can you try to create a python script through boto3 where we can

 

add users to account

remove user to account

update user permissions

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html

IdentityStore - Boto3 1.28.18 documentation



if there was a way to assign users and groups to an account in IAM Identity Center through boto3 SDK as you weren't able to find it in the Identity Store documentation. I was able to locate the SDK documentation for SSOAdmin which had the documentation [1] for the APIs you were looking for, specifically create_account_assignment(). The same for delete_account_assignment().



Delete User from Group:

https://vyjow5c5mk.execute-api.eu-central-1.amazonaws.com/delete-user-group?user=averymanyi@idc.com&&group=Database

Add User in Group:

https://vyjow5c5mk.execute-api.eu-central-1.amazonaws.com/add-user-group?user=averymanyi@idc.com&&group=Database

Add Permission to the PermissionSet:

https://vyjow5c5mk.execute-api.eu-central-1.amazonaws.com/attach-policy-permission-set?permisionArn=arn:aws:sso:::permissionSet/ssoins-698759770ce5a35e/ps-e7c813ef49a4b795&&PolicyArn=arn:aws:iam::aws:policy/CloudSearchFullAccess








https://zbcrbm2j6c.execute-api.eu-central-1.amazonaws.com/add-permission?user=agborntuibate@idc.com&&permissionSetArn=arn:aws:sso:::permissionSet/ssoins-79071ef5f2a874d9/ps-c44ec5bf2930a163
Ehtisham A.
Aug 09, 2023, 9:47 AM

https://zbcrbm2j6c.execute-api.eu-central-1.amazonaws.com/remove-permission?user=agborntuibate@idc.com&&permissionSetArn=arn:aws:sso:::permissionSet/ssoins-79071ef5f2a874d9/ps-c44ec5bf2930a163
