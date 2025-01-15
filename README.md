# CloudFront Cache Invalidation Lambda Function

This AWS Lambda function integrates with AWS CodePipeline to invalidate the cache of a specified CloudFront distribution. It is designed to automate the invalidation process as part of your CI/CD pipeline, ensuring that updates are propagated immediately.

## Features

- Invalidates CloudFront cache using the AWS SDK.
- Reads `distribution_id` dynamically from CodePipeline user parameters.
- Supports invalidating specific paths or the entire cache (`/*`).
- Reports success or failure back to CodePipeline.

## Requirements

- AWS Lambda with Python 3.9 or later.
- IAM Role with the following permissions:
  - `cloudfront:CreateInvalidation`
  - `codepipeline:PutJobSuccessResult`
  - `codepipeline:PutJobFailureResult`

## Usage

### 1. Set Up the Lambda Function
1. Deploy the code to an AWS Lambda function.
2. Assign the necessary IAM permissions to the Lambda execution role.

### 2. Integrate with AWS CodePipeline
1. Add a custom action to your CodePipeline configuration.
2. Pass the required `UserParameters` in the action configuration as a JSON string:
   ```json
   {
       "distribution_id": "YOUR_DISTRIBUTION_ID"
   }
