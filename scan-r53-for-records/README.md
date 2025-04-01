# Route 53 Record Checker

[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/downloads/)
[![AWS Route 53](https://img.shields.io/badge/AWS-Route53-orange.svg)](https://aws.amazon.com/route53/)

This Python script searches through all AWS Route 53 hosted zones (public and private) for records matching a specific target string. It runs locally and outputs results to both the console and a text file (`route53_records.txt`).

> **Important Note:**  
> This script is designed to be executed locally on your machine—not as part of a CloudFormation stack or Lambda function. It requires AWS credentials to be configured locally (via AWS CLI or a credentials file) or through an assumed role.

## 🚀 Why

Manually checking DNS records across multiple Route 53 hosted zones in the AWS Console can be tedious, especially in large AWS accounts. This tool automates the process by:
- Quickly scanning all hosted zones for a target string.
- Saving time and reducing manual errors.
- Documenting matching records automatically for further analysis.

## 📋 Overview

The script features:
- **Comprehensive Scanning:**  
  Searches all Route 53 hosted zones (public and private) in your AWS account.
- **Record Support:**  
  Supports both standard resource records (A, CNAME, etc.) and alias records.
- **Pagination Handling:**  
  Automatically handles pagination for large datasets.
- **Output:**  
  Displays results on the console and writes them to `route53_records.txt`.
- **Local Execution:**  
  Runs on your local machine using Python 3.x and the boto3 AWS SDK.

*Note: since this is just a helper script, no logging or exceptions handling procedures are implemented*

## Prerequisites

- **Python 3.x** installed on your machine
- **AWS Credentials:**
  - Configured via AWS CLI (`aws configure`) in `~/.aws/credentials` and `~/.aws/config`
  - Or an assumed role with appropriate permissions or exported keys
- **Required Permissions:**
  - `route53:ListHostedZones`
  - `route53:ListResourceRecordSets`

## 🔧 Setup

1. **Clone or Download the Script:**
   - Download `scan_route53_for_records.py` & `requirements.txt` to your local machine.

2. **Set Up a Virtual Environment (Recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run:**
   ```bash
    python3 scan_route53_for_records.py --target "example.com"
    ```

### 📄 Example Output

```bash
Found matching records:
Zone: example.com (Public)
Type: A
Name: test.example.com
Value: 192.0.2.1
---
```