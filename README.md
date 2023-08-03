# myproject


Can you try to create a python script through boto3 where we can

 

add users to account

remove user to account

update user permissions

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sso-admin.html

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html

IdentityStore - Boto3 1.28.18 documentation



if there was a way to assign users and groups to an account in IAM Identity Center through boto3 SDK as you weren't able to find it in the Identity Store documentation. I was able to locate the SDK documentation for SSOAdmin which had the documentation [1] for the APIs you were looking for, specifically create_account_assignment(). The same for delete_account_assignment().
