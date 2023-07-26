# Step 1 (Create the SNS topic)

Create SNS topic and add email subscriptions whichever you want to notified. 

# Step 2 (Create the Lambda Function)

Create IAM ROLE with SNS full access to send the email notification.

Create the Lambdafunction with python 3.7 runtime, and give the iam role before created one.


# Step 3 (Prepare the lambda function code)

Add the lambda function code in lambda_function.py file. 

Note:- In the provided code, we need to change the SNS topic ARN and remind notification days like 30 days, 20 days.

Add the domain list in the server_ip.txt file.

Now, after adding the contents to the file, deploy and test the function.

