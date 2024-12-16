import json
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ASANA_ACCESS_TOKEN = '2/1208949436499772/1208966929891876:a349b7e5da40143bb212757b2da52124'
BASE_URL = 'https://app.asana.com/api/1.0'

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.json
    if 'events' in payload:
        for event in payload['events']:
            if event['type'] == 'task':
                handle_task_update(event)
    return jsonify({'status': 'received'}), 200

def handle_task_update(event):
    task_id = event['resource']
    task_url = f"{BASE_URL}/tasks/{task_id}"

    headers = {
        'Authorization': f'Bearer {ASANA_ACCESS_TOKEN}',
        'Content-Type': 'application/json',
    }

    # Fetch current task data
    response = requests.get(task_url, headers=headers)
    task_data = response.json().get('data')

    # Check for the status field being 'Bust'
    if task_data.get('custom_fields') and any(
        field['enum_value']['name'] == 'Bust'
        for field in task_data['custom_fields'] if field['enum_value']
    ):
        # Prepare data to update the Balance field
        update_data = {
            "data": {
                "custom_fields": {
                    "Balance": -500  # Replace 'balance_field_gid' with actual GID
                }
            }
        }
        
        # Send update request to Asana
        requests.put(task_url, headers=headers, json=update_data)

if __name__ == '__main__':
    app.run(port=5000)
