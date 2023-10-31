###########################################
# IDC Lambda Configs
###########################################

data "archive_file" "lambda_idc_function" {
  type        = "zip"
  source_dir  = "${path.module}/lib/idc_function"
  output_path = "${path.module}/lib/idc_code.zip"
}

resource "aws_cloudwatch_log_group" "idc_admin" {
  name = "/aws/lambda/${aws_lambda_function.idc_admin.function_name}"

  retention_in_days = 30
}

resource "aws_lambda_function" "idc_admin" {
  filename      = "${path.module}/lib/idc_code.zip"
  function_name = "idc_admin"
  role          = aws_iam_role.lambda_role.arn
  handler       = "idc_code.lambda_handler"
  runtime       = "python3.10"
# Enable CloudWatch logging
    tracing_config {
    mode = "Active"
  }
  # Enable the Lambda Insights Extension Layer
  # Using latest version from AWS list here: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-extension-versions.html  
  layers     = ["arn:aws:lambda:us-west-2:580247275435:layer:LambdaInsightsExtension:14"]

}





###########################################
# IDC IAM Configs
###########################################

# IAM Role to Allow Lambda execution 
resource "aws_iam_role" "lambda_role" {
  name = "idc_aws_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "iam_policy" {
  name   = "LambdaFunctionPolicy"
  path   = "/"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

# Attach AWSLambdaBasicExecutionRole managed policy
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy to allow Lambda Insights Extension
resource "aws_iam_role_policy_attachment" "cloudwatch_lambda_insights" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLambdaInsightsExecutionRolePolicy"
}

# IAM Role for API Gateway to log API requests to CloudWatch
# TODO - Role name must match “GTS-*-Service-Role” name format in order to be allowed to create log groups per current SCP
resource "aws_iam_role" "api_cloudwatch_role" {
  name = "idc_aws_iam_role_for_api"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      },
    ]
  })
}

# IAM Policy for API Gateway to get and create log events in CloudWatch
# Ignore TFSEC findings about wildcarded policy permissions
#tfsec:ignore:aws-iam-no-policy-wildcards
resource "aws_iam_role_policy" "api_cloudwatch_policy" {
  name = "idc_aws_policy_for_api_log"
  role = aws_iam_role.api_cloudwatch_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogStreams",
          "logs:DescribeLogGroups",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
          "logs:StartQuery",
          "logs:StopQuery",
          "logs:DescribeQueries",
          "logs:GetLogGroupFields",
          "logs:GetLogRecord",
          "logs:GetQueryResults"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

