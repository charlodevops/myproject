@app.post('/add-permission') 
def addPermToUser():
    post_data = app.current_event.json_body
    print(post_data)
    username = post_data.get("user", None)
    permission_set_arn = post_data.get("permissionSetArn", None)
    acc= post_data.get("account_id", None)




@app.post('/remove-permission') 
def removePermFromUser():
    try:
        post_data = app.current_event.json_body
        username = post_data.get("user", None)
        permission_set_arn = post_data.get("permissionSetArn", None)
        acc= post_data.get("account_id", None)
