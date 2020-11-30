import requests
import json
import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "CONSULADO ESPANOL AUTOMATICO <hectorg87@gmail.com>"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the
# ConfigurationSetName=CONFIGURATION_SET argument below.
CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "eu-west-1"

# The subject line for the email.
SUBJECT = "HAY CITAS PARA EL CONSULADO! "

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("HAY CITAS EN EL CONSULADO\r\n"
             "ENTRA YA!!!!"
            )

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>HAY CITAS EN EL CONSULADO</h1>
  <p>ENTRA YA!!!!</p>
</body>
</html>
            """

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)

def lambda_handler(event = {}, context = {}):
    headers = {'Connection': 'keep-alive',
               'Pragma': 'no-cache',
               'Cache-Control': 'no-cache',
               'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4213.0 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Dest': 'empty',
               'Referer': 'https://app.bookitit.com/es/hosteds/widgetdefault/2e683196f06adbdb38495c2b60c3db653',
               'Accept-Language': 'en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7',
               'Cookie': '_ga=GA1.2.1538114842.1595872736; _gid=GA1.2.1587085622.1595872736; _gat=1',
               }

    r = requests.get(
        'https://app.bookitit.com/onlinebookings/datetime/?callback=jQuery21105800999181571529_1595872860531'
        '&type=default&publickey=2e683196f06adbdb38495c2b60c3db653&lang=es&services%5B%5D=bkt517902&agendas'
        '%5B%5D=bkt209517&version=1234&src=https%3A%2F%2Fapp.bookitit.com%2Fes%2Fhosteds%2Fwidgetdefault'
        '%2F2e683196f06adbdb38495c2b60c3db653&srvsrc=https%3A%2F%2Fapp.bookitit.com&start=2020-07-28&end'
        '=2020-12-31&selectedPeople=1&_=1595872860537', headers=headers)

    response = r.text

    response = response.replace('callback=jQuery21105800999181571529_1595872860531(', '', 1)
    response = response.replace(');', '', 1)

    response_json = json.loads(response)
    print(response_json)
    found_slot = False
    date = ''
    reversed_list = reversed(response_json['Slots'])
    for slot in reversed_list:
        if len(slot['times']) > 0:
            print('TIMES AVAILABLE on' + slot['date'])
            print(slot['times'])
            date = slot['date']
            found_slot = True
            break

    if found_slot:
        print(response)
        # send_email(date)
    else:
        print('NO TIMES AVAILABLE FOUND')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def send_email(date):
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    'dfca87@gmail.com',
                    'hectorg87@gmail.com'
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT + date,
                },
            },
            Source=SENDER
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print('ERROR SENDING EMAIL')
        print(e.response['Error']['Message'])

lambda_handler()
