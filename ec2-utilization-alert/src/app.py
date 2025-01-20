import os
import json
import requests

def lambda_handler(event, context):
    # Log the entire event for detailed inspection
    print("Received event:", json.dumps(event, indent=2))
    
    slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL', '')
    
    if not slack_webhook_url:
        raise ValueError("SLACK_WEBHOOK_URL environment variable is not set")

    try:
        # Attempt to extract keys from a potential nested structure
        alarm_name = event.get('alarmData', {}).get('alarmName', 'Unknown Alarm')
        state = event.get('alarmData', {}).get('state', {}).get('value', 'Unknown State')
        reason = event.get('alarmData', {}).get('state', {}).get('reason', 'No reason provided')

        print(f"Extracted values: AlarmName={alarm_name}, NewStateValue={state}, NewStateReason={reason}")

        # Construct the Slack message payload with improved structure
        slack_message = {
            "text": "🚨 EC2 High Utilization Alert 🚨",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*EC2 High Utilization Alert*"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Alarm Name:*\n{alarm_name}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*State:*\n{state}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Reason:*\n{reason}"
                        }
                    ]
                }
            ]
        }

        # Send the message to Slack
        response = requests.post(
            slack_webhook_url,
            data=json.dumps(slack_message),
            headers={"Content-Type": "application/json"}
        )

        print(f"Slack Response Status: {response.status_code}")
        print(f"Slack Response Body: {response.text}")

        if response.status_code != 200:
            raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Alert sent successfully"})
        }

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        raise e
