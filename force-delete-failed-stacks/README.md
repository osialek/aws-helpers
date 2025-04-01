# Lambda Force Delete Stacks

This CloudFormation stack template deploys a Lambda function written in python designed to force delete CloudFormation stacks based on a matching name pattern. The Lambda function uses environment variables to determine which stacks to delete and in which regions to operate.

**Important Note:**\
This solution is intended to be used only on stacks in the DELETE_FAILED state.\
Attempting to force delete stacks that are not in the DELETE_FAILED state will result in errors such as:

```ruby
Error deleting stack STACKNAME: An error occurred (ValidationError) when calling the DeleteStack operation: Invalid operation on stack [arn:aws:cloudformation:us-east-1:ACCOUNT_ID:stack/STACKNAME/cfae05a0-f301-11ef-97fc-0e0c5416d0eb]. You can activate DeletionMode FORCE_DELETE_STACK in a delete stack operation only when the stack is in the DELETE_FAILED state.
```

## Why

I unfortunately ran into a situation where I had deployed a large number of stacks in my AWS organization that, for some reason, got stuck in the DELETE_FAILED state. Even AWS Support was unable to help me, so I had to use a script to remove them. Removing them manually in the console with the force delete flag selected wouldn't have been an issue, but doing that in the AWS Console for tens of different accounts across multiple regions would have been extremely tedious. Thus, here is a solution for such situations.

# Overview

The solution includes:
- Python-based Lambda Function that:
  - Retrieves a target region/s or if not provided executes in all enabled regions in that account
  - Scans each region for CloudFormation stacks
  - Matches stack names against a user-defined regular expression or keyword
  - Initiates a force deletion for matching stacks that are in the DELETE_FAILED state
- IAM Role and Policy:\
  The template creates an IAM Role and attaches a policy that grants the Lambda function necessary permissions for:
  - Managing CloudWatch Logs
  - Describing, listing, and deleting CloudFormation stacks
  - Describing AWS regions via EC2
- Custom Resource Trigger:
  - A custom resource is used to trigger the Lambda function. This allows the Lambda to be invoked as part of the stack lifecycle.
  - If Lambda fails for some reason, stack should also fail and delete all resources

## Template Parameters

- **StackNamePattern (String):**
  - The regular expression pattern used to identify CloudFormation stacks for deletion.
  - Example: *test-stack* deletes stacks whose names contains *test-stack*.

- **Regions (String):**
  - A single region or a comma-separated list of AWS regions where the deletion should execute.
  - If a value is provided (e.g., "us-east-1, us-west-2"), the Lambda operates only in these regions.
  - If left empty, the function fetches all enabled regions automatically.

## How to deploy/run

1. Download the Cloudformation template 'force_delete_failed_stacks.yaml'
2. Create Cloudformation stack using this template

Simple as that!

## Reusability and Deployment Considerations

- **Lambda Reusability:**
  - The Lambda function is designed to be deployed as part of a CloudFormation stack. It uses cfnresponse to send responses back to CloudFormation as part of a custom resource lifecycle. This means it is not intended to be invoked directly outside of this context—attempting to do so will result in errors.
- **Stack Lifecycle:**
  - Once the Lambda function has executed its task, the CloudFormation stack (including all resources) should be deleted. This allows you to redeploy the solution with different keywords or regions if needed and cleans up the environment.
- **Alternative Deployment Options:**
  - If you require running the Lambda function outside of the CloudFormation context (for example, manually triggering it), you must modify the deployment:
    - Deploy the Lambda function without the custom resource trigger in the CloudFormation template.
    - Remove or modify the cfnresponse calls in the Lambda code. Without doing that, it will cause the Lambda to run into errors, as it expects to be triggered and managed by CloudFormation.

# Important information

Since this solution only removes stacks that are in the DELETE_FAILED state, there is minimal risk in deploying it. However, be careful when setting the keyword/stack name pattern to ensure it does not affect other stacks. Be as precise as possible with the StackNamePattern value.
