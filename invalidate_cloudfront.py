import boto3
import time
import json

def invalidate_cloudfront_cache(distribution_id, paths):
    # Initialize the CloudFront client
    cloudfront = boto3.client('cloudfront')
    caller_reference = f"my-invalidation-{int(time.time())}"

    try:
        # Create a cache invalidation request
        response = cloudfront.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': caller_reference  # You can use any unique string here
            }
        )

        # Print the CloudFront cache invalidation response
        print("Cache invalidation request created successfully:")
        print(response)

    except Exception as e:
        print("Error creating cache invalidation request:", str(e))

def lambda_handler(event, context):
    codepipeline = boto3.client('codepipeline')
    job_id = event['CodePipeline.job']['id']
    try:
        #distribution_id = "E2ZHLKEJUYB333"
        user_parameters = event.get('CodePipeline.job', {}).get('data', {}).get('actionConfiguration', {}).get('configuration', {}).get('UserParameters', {})
        #params_object = json.loads(user_parameters)
        distribution_id = json.loads(user_parameters).get('distribution_id',{})
        paths_to_invalidate = ["/*"]  # Use ["/*"] to invalidate the entire cache
        invalidate_cloudfront_cache(distribution_id, paths_to_invalidate)
        
        codepipeline.put_job_success_result(jobId=job_id)
    except Exception as e:
        # If there is an error, call putJobFailureResult instead
        codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                'type': 'JobFailed',
                'message': f"Lambda function failed with error: {str(e)}"
            }
        )
        print(f"Job {job_id} failed: {str(e)}")
    return {
        'statusCode': 200,
        'body': 'Lambda function executed successfully'
    }
