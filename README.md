# aws-lambda-proxies
Creating proxies in AWS EC2 using AWS Lambda functions

# Purpose
I wanted a way of initializing proxies using [goproxy](https://github.com/elazarl/goproxy) in EC2,
but without relying on Terraform like the inspiration for this project, [EC2 Proxies](https://github.com/vifreefly/ec2_proxies) utilized. I also wanted to learn how to create and use AWS Lambda functions, and how they interact with the rest of the AWS ecosystem like EC2.

# Usage
The core of this project is found in the `lambdaFunctions` directory, which contains the Python 2.7 scripts for Lambda. These scripts do rely on a specific HTTP request format though, which is why I've included some example Go code for calling these lambda functions from a different machine.

# Installation
`TODO Fill this in when Go sample code is provided`
