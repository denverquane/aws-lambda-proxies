# aws-lambda-proxies
Creating proxies in AWS EC2 using AWS Lambda functions

# Purpose
I wanted a way of initializing proxies using [goproxy](https://github.com/elazarl/goproxy) in EC2,
but without relying on Terraform, like the inspiration for this project ([EC2 Proxies](https://github.com/vifreefly/ec2_proxies)) utilized. I also wanted to learn how to create and use AWS Lambda functions, and how they interact with the rest of the AWS ecosystem like EC2.

# Usage
The core of this project is found in the `lambdaFunctions` directory, which contains the Python 2.7 scripts for Lambda. These scripts do rely on a specific, opinionated HTTP request format body like the following:
```
{
  "PROXY_PORT": "56675",
  "PROXY_USER": "",
  "PROXY_PASSWORD": "",
  "PROXY_TYPE": "http",
  "INSTANCE_TYPE": "t2.micro",
  "UNIQUE_ID": "SampleUniqueId1234"
}
```

