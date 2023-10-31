###########################################
# IDC API Configs
###########################################

# Create an HTTP API Gateway
resource "aws_apigatewayv2_api" "idc_api" {
  name          = "IDC-Api"
  description   = "This is for workforce management in IAM Identity Center"
  protocol_type = "HTTP"
 
}

# ApiStage - API Gateway Stage
resource "aws_apigatewayv2_stage" "idc_api" {
  api_id = aws_apigatewayv2_api.idc_api.id
  name        = "idc_lambda_dev"
  auto_deploy = true
  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}


# # ApiStage Method settings - settings common for all API stage requests
# resource "aws_api_gateway_method_settings" "all" {
#   rest_api_id          = aws_apigatewayv2_api.idc_api.id
#   stage_name           = aws_apigatewayv2_stage.idc_api.stage_name
#   method_path     = "*/*"

#   settings {
#     metrics_enabled         = true
#     data_trace_enabled      = false
#     logging_level           = "INFO"
#     throttling_burst_limit  = 5000
#     throttling_rate_limit   = 10000
#     cache_data_encrypted    = true
#   }
# }

# Define an HTTP integration for the Lambda function
resource "aws_apigatewayv2_integration" "idc_api" {
  api_id               = aws_apigatewayv2_api.idc_api.id
  integration_type     = "AWS_PROXY"
  integration_uri      = aws_lambda_function.idc_admin.invoke_arn
  integration_method   = "POST"
  connection_type      = "INTERNET"
  timeout_milliseconds = 29000
}

resource "aws_apigatewayv2_route" "add-permission-to-users_route" {
  api_id     = aws_apigatewayv2_api.idc_api.id
  route_key  = "POST /add-permission-to-users" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
  target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
}

resource "aws_apigatewayv2_route" "remove-permission-from-users_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /remove-permission-from-users" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
}

resource "aws_apigatewayv2_route" "create-idc-group_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /create-idc-group" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
  }

  resource "aws_apigatewayv2_route" "remove-idc-group_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /remove-idc-group" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
  }

  resource "aws_apigatewayv2_route" "add-users-to-group_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /add-users-to-group" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
  }

  resource "aws_apigatewayv2_route" "remove-user-from-grp_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /remove-user-from-grp" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
  }

  resource "aws_apigatewayv2_route" "add-permission-to-grp_route" {
    api_id     = aws_apigatewayv2_api.idc_api.id
    route_key  = "POST /add-permission-to-grp" # You can specify the HTTP method you want to use (e.g., GET, POST, ANY)
    target     = "integrations/${aws_apigatewayv2_integration.idc_api.id}"
  }

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.idc_api.name}"

  retention_in_days = 30
}

#Gives API Gateway permission to invoke your Lambda function.
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.idc_admin.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = aws_apigatewayv2_api.idc_api.execution_arn
}

# resource "aws_api_gateway_deployment" "idc_api" {
#  depends_on = [aws_apigatewayv2_integration.idc_api]
#  api_id = aws_apigatewayv2_api.idc_api.id
#  stage_name = "test"
# }
