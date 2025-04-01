import boto3
import logging
import re
import cfnresponse
import os
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def delete_stacks(cf_client, stack_name):
    """Force deletes the stack with specified keyword in its name"""
    try:
        logger.info(f'Deletion initiated for stack: {stack_name}')
        response = cf_client.delete_stack(
            StackName=stack_name,
            DeletionMode='FORCE_DELETE_STACK'
        )
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == 'ValidationError' and "DELETE_FAILED" in error_message:
            logger.warning(f'Expected error for stack {stack_name}: {error_message}')
            # Do not re-raise; this is a known issue.
            # If this is the known error regarding DELETE_FAILED state, log a warning
            # FORCE_DELETE_STACK cannot be executed on the stack which is not in DELETE_FAILED state
            # READ README.MD
        else:
            logger.error(f'Unexpected error deleting stack {stack_name}: {error_message}')
            # Re-raise the exception for unknown errors to fail the Lambda.
            raise

def lambda_handler(event,context):
    try:
        # Check if a list of regions is provided in the environment variables
        regions_list = os.environ.get('REGIONS')
        if regions_list:
            regions = [r.strip() for r in regions_list.split(',') if r.strip()]
            logger.info(f'Using provided regions: {regions}')
        else:
            # Fetch all enabled AWS Regions
            ec2_client = boto3.client('ec2')
            regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
            logger.info(f'No regions provided; using all enabled regions: {regions}')


        # Get the stack name pattern from environment variables
        pattern = os.environ.get('STACK_NAME_PATTERN')

        # Loop through all regions
        for region in regions:
            logger.info(f'Checking region {region}')

            # Initialize CloudFormation client for the region
            cf_client = boto3.client('cloudformation', region_name=region)

            # Get the list of all stacks in the region
            stacks = cf_client.describe_stacks()

            # Iterate over stacks and delete the ones that match the pattern
            for stack in stacks['Stacks']:
                stack_name = stack['StackName']
                if re.match(pattern, stack_name):
                    logger.info(f'Found matching stack: {stack_name} in region {region}. Deleting...')
                    try:
                        delete_stacks(cf_client,stack_name)
                    except Exception as e:
                        logger.error(f"Error deleting stack {stack_name}: {repr(e)}")

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {'status': 'success'})
        return {
            'statusCode': 200,
            'body': 'Stack deletion process completed'
        }
    except Exception as e:
        print("error:", repr(e))
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, {'reason': repr(e)})
