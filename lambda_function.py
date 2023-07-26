
import ssl
import socket
import datetime
import boto3

def check_ssl_certificate_expiry(domain):
    try:
        port = 443  # Assume default port 443 for SSL connections
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                certificate = ssock.getpeercert()
            certExpires = datetime.datetime.strptime(certificate["notAfter"], "%b %d %H:%M:%S %Y %Z")
            daysToExpiration = (certExpires - datetime.datetime.now()).days
            return daysToExpiration, domain
    except Exception as e:
        return None, domain

def lambda_handler(event, context):
    sns_topic_arn = "arn:aws:sns:us-east-1:450706366824:test"  # Replace with your SNS topic ARN
    domain_file = "server_ip.txt" # Replace your domain list in the server_ip.txt file

    with open(domain_file) as ip_file:
        for ip in ip_file:
            ip = ip.strip()  # Remove leading/trailing whitespaces and newline characters
            days_to_expiry, domain = check_ssl_certificate_expiry(ip)

            if days_to_expiry is not None:
                print(f"Checking certificate for server {domain}")
                print(f"Expires on: {days_to_expiry} days")
                
                if days_to_expiry < 30:
                    message = f"ALERT: The SSL certificate for {domain} expires in {days_to_expiry} days. Please renew it!"
                else:
                    message = f"The SSL certificate for {domain} expires in {days_to_expiry} days."
            else:
                print(f"Error on connection to server: {domain}")
                message = f"Error on connection to server: {domain}"

            # Publish the message to the SNS topic if expiry date is below 30 days
            if days_to_expiry is not None and days_to_expiry < 30:
                sns_client = boto3.client("sns")
                sns_client.publish(TopicArn=sns_topic_arn, Message=message)

    return {
        "statusCode": 200,
        "body": "SSL certificate check completed."
    }

