#!/usr/bin/env python3

import boto3
import datetime
import smtplib
import os
from email.message import EmailMessage
server = 'mail.example.com'
user = 'noreply@example.com'
password = ''
sender = 'noreply@example.com'
recepients = ['test@example.com']
os.environ['AWS_DEFAULT_REGION'] = 'eu-central-1'
#def lambda_handler(event, context):
session = boto3.Session()
# Create a Cost Explorer client
client_ce = session.client('ce')
# Create EC2 resource session
client_instance = session.resource('ec2')
# Set time range to cover the last full calendar month
# Note that the end date is EXCLUSIVE (e.g., not counted)
now = datetime.datetime.utcnow()
last_month = now.month-1 if now.month > 1 else 12
#report_date = now()
# Set the end of the range to start of the current month
end = datetime.datetime(year=now.year, month=now.month, day=1)
# Subtract a day and then "truncate" to the start of previous month
start = end - datetime.timedelta(days=1)
start = datetime.datetime(year=start.year, month=start.month, day=1)
# Get the month as string for email purposes
month = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()[last_month-1]
# Convert them to strings
start = start.strftime('%Y-%m-%d')
end = end.strftime('%Y-%m-%d')
html = '<html><body>Dear Team,<br><br>AWS Bill for the instances configured for memebres in Tools Account:<br><br><table border="1"><tr><th>' + '</th><th nowrap>'.join(["Owner", "Instance Type", "Billed Amount",  "Month", "Launch_Time"]) + '</th></tr>'
#Cost Explorer API with Cost explorer tag Name
for tag_values in ("tools-gpu","tools-arm-csdk"):
    response = client_ce.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End':  end
        },
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        Filter={
            "Tags": {
                "Key": "Name",
                "Values": [tag_values]
            }
        }
    )
    amount = response['ResultsByTime'][0]['Total']['BlendedCost']['Amount']
#EC2 instances API
    instances = client_instance.instances.filter(Filters=[{
        'Name':'tag:Name',
        'Values':[tag_values]}])

    for instance in instances:
#        print(instance)
        for tag in instance.tags:
            if 'Owner'in tag['Key']:
                owner = tag['Value']
        instance_type = instance.instance_type
        launch_time   = instance.launch_time.strftime("%d/%m/%Y, %H:%M:%S")
#        print(launch_time)
    if tag_values == "tools-gpu":
        html += '<tr><td nowrap>' + owner  + '</td><td>' + '</td><td>'.join([instance_type,amount,month,launch_time]) + '</td></tr>'
    elif tag_values == "tools-arm-csdk":
        html += '<tr><td nowrap>' + owner  + '</td><td>' + '</td><td>'.join([instance_type,amount,month,launch_time]) + '</td></tr>'

html += '</table><br>Best Regards,<br>DevOps Team</body></html>'

msg = EmailMessage()
msg['Subject'] = 'AWS Billing for Instance in Tools Account for Month: ' + month
msg['From'] = sender
msg['To'] = recepients
msg.set_content(html, subtype = 'html')

print('Sending Email....')
mail = smtplib.SMTP('smtp.office365.com',587)
mail.ehlo()
mail.starttls()
mail.login(user, password)
mail.sendmail(sender, recepients, msg.as_string())
mail.close()
