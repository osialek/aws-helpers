# AWS-HELPERS

Self-developed helper scripts and solutions for managing AWS infrastructure. Each directory in this repository contains a separate, self-contained solution designed to simplify common AWS tasks.

## 📂 Repository Structure

- **[force-delete-failed-stacks](./force-delete-failed-stacks/)**\
  Contains the CloudFormation template and Python-based Lambda function that force deletes CloudFormation stacks stuck in the DELETE_FAILED state.
  - **Overview:**
    - This solution deploys a Lambda function that uses environment variables to determine which stacks to delete based on a matching name pattern and region(s). It is specifically designed to work on stacks in the DELETE_FAILED state.
- **[scan-r53-for-records](./scan-r53-for-records/)**\
  Contains a Python script that scans all AWS Route 53 hosted zones for records containing a specified target string.
  - **Overview:**
    - Searches both public and private hosted zones for standard and alias records. Outputs matching records to the console and `route53_records.txt`.


## 🔧 Getting Started

To get started with any solution:

1. Navigate to the specific solution directory (e.g., force-delete-failed-stacks).
2. Read the README file provided within that directory for detailed deployment and usage instructions.
3. Follow instruction how to use it
