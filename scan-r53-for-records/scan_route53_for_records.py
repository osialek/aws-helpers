import boto3
import argparse


def check_all_hosted_zones(target_string):
    """Check all Route 53 hosted zones for records matching the target string.

    Args:
        target_string: The string to search for in the record values.
        output_file: Path to the output file for writing matching records.

    Returns:
        A list of dictionaries containing the matching record details.
    """
    # Initialize AWS Route 53 client
    route53 = boto3.client('route53')

    print(f"Searching for records with target: {target_string}")

    # List to store results
    matching_records = []

    # Paginate through all hosted zones
    paginator = route53.get_paginator('list_hosted_zones')

    try:
        for page in paginator.paginate():
            for zone in page['HostedZones']:
                zone_id = zone['Id']
                zone_name = zone['Name'].rstrip('.')  # Remove trailing dot
                is_private = zone['Config']['PrivateZone']

                zone_type = 'Private' if is_private else 'Public'
                print(f"Checking zone: {zone_name} ({zone_type})")

                # Get all resource record sets in the zone
                record_paginator = route53.get_paginator(
                    'list_resource_record_sets'
                    )
                for record_page in record_paginator.paginate(HostedZoneId=zone_id):
                    for record in record_page['ResourceRecordSets']:
                        record_name = record['Name'].rstrip('.')
                        # Check different record types
                        if 'ResourceRecords' in record:
                            for rr in record['ResourceRecords']:
                                if target_string in rr['Value']:
                                    matching_records.append({
                                        'Zone': zone_name,
                                        'Type': record['Type'],
                                        'Name': record_name,
                                        'Value': rr['Value'],
                                        'Private': is_private
                                    })
                        elif 'AliasTarget' in record:
                            if target_string in record['AliasTarget']['DNSName']:
                                matching_records.append({
                                    'Zone': zone_name,
                                    'Type': record['Type'],
                                    'Name': record_name,
                                    'Value': record['AliasTarget']['DNSName'],
                                    'Private': is_private
                                })

        # Print results
        if matching_records:
            print("\nFound matching records:")
            for record in matching_records:
                print(f"Zone: {record['Zone']} ({'Private' if record['Private'] else 'Public'})")
                print(f"Type: {record['Type']}")
                print(f"Name: {record['Name']}")
                print(f"Value: {record['Value']}")
                print("---")

            # Replace the results printing section with:
            with open('route53_records.txt', 'w') as f:
                f.write("Found matching records:\n")
                for record in matching_records:
                    f.write(f"Zone: {record['Zone']} ({'Private' if record['Private'] else 'Public'})\n")
                    f.write(f"Type: {record['Type']}\n")
                    f.write(f"Name: {record['Name']}\n")
                    f.write(f"Value: {record['Value']}\n")
                    f.write("---\n")
        else:
            print("\nNo matching records found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Check all Route 53 records for a specific target string')
    parser.add_argument('--target', required=True, help='Target string to search for in records')

    # Parse arguments
    args = parser.parse_args()

    # Run the check
    check_all_hosted_zones(args.target)


if __name__ == "__main__":
    main()
