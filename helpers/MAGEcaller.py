import json
import requests

MAGE_HEADERS = { 'Content-Type': 'application/json' }


def call_api(mageInfo, lastMinute):
    response = requests.post(
        url='https://api.mage.ai/v1/predict',
        headers=MAGE_HEADERS,
        data=json.dumps({
            'api_key': mageInfo['apiKey'],
            'model': mageInfo['model'],
            'version': mageInfo['version'],
            'features': [lastMinute], # lastMinute is of type Dict
        }),
    )

    predictions = response.json()
    return predictions['prediction']
