import json
import requests

MAGE_HEADERS = {'Content-Type': 'application/json'}


def call_api(mage_info, last_minute):
    response = requests.post(
        url='https://api.mage.ai/v1/predict',
        headers=MAGE_HEADERS,
        data=json.dumps({
            'api_key': mage_info['apiKey'],
            'model': mage_info['model'],
            'version': mage_info['version'],
            'features': [mage_info],  # lastMinute is of type Dict
        }),
    )

    predictions = response.json()
    return predictions['prediction']
